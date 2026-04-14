import asyncio
import json
import os
import csv
import time
import random
from dotenv import load_dotenv

from src.clients.groq_client import GroqClient
from src.defenses import SpotlightingDefense, DataSentinelDefense
from src.attacks.injector import inject_payload, inject_combined
from src.evaluator import score_response
from src.metrics import calc_asv

load_dotenv()


async def run_phase3_trial(
    model_client,
    sentinel: DataSentinelDefense,
    spotlight: SpotlightingDefense,
    tier: str,
    payload_id: str,
    benign_prompt: str,
    payload_text: str,
    use_combine: bool,
):
    """
    Single Phase 3 trial testing two defenses against one payload.

    Spotlighting: wraps the prompt before sending to the model, then scores
    whether the injection bypassed the defense.

    DataSentinel: probes the raw payload text only (no injection context needed)
    and detects whether the canary is suppressed.
    """
    attack_label = "combine" if use_combine else "direct"

    # --- Spotlighting: wrap prompt, send to model, score result ---
    start_t = time.time()
    spotlight_bypassed = 0
    spotlight_response = ""
    try:
        hardened = spotlight.wrap(
            task_instruction=benign_prompt,
            untrusted_data=payload_text,
        )
        spotlight_response = await model_client.generate(hardened)
        spotlight_bypassed = score_response(tier, spotlight_response)
    except Exception as e:
        print(f"[Spotlight Error] {payload_id}: {e}")
    spotlight_latency = int((time.time() - start_t) * 1000)

    # --- DataSentinel: probe raw payload text ---
    start_t = time.time()
    sentinel_detected = 0
    try:
        detected = await sentinel.is_malicious(payload_text)
        sentinel_detected = 1 if detected else 0
    except Exception as e:
        print(f"[Sentinel Error] {payload_id}: {e}")
    sentinel_latency = int((time.time() - start_t) * 1000)

    print(
        f"[{tier}] {payload_id} ({attack_label}) -> "
        f"Spotlight bypassed: {bool(spotlight_bypassed)} ({spotlight_latency}ms), "
        f"Sentinel detected: {bool(sentinel_detected)} ({sentinel_latency}ms)"
    )

    return {
        "payload_id": payload_id,
        "tier": tier,
        "attack_type": attack_label,
        "spotlight_bypassed": spotlight_bypassed,
        "spotlight_response": spotlight_response[:300],
        "sentinel_detected": sentinel_detected,
        "spotlight_latency_ms": spotlight_latency,
        "sentinel_latency_ms": sentinel_latency,
    }


async def run_phase3(limit: int = 5):
    print("Initializing Phase 3 components...")
    model_client = GroqClient()
    sentinel = DataSentinelDefense(client=model_client)
    spotlight = SpotlightingDefense()

    print("Loading datasets...")
    with open("dataset/benign_samples.json", encoding="utf-8") as f:
        benign_samples = json.load(f)

    with open("dataset/payloads.json", encoding="utf-8") as f:
        payloads_data = json.load(f)

    tiers = {
        "L1": payloads_data.get("L1_naive_override", []),
        "L2": payloads_data.get("L2_context_shift", []),
        "L3": payloads_data.get("L3_markdown_exfiltration", []),
    }

    sem = asyncio.Semaphore(2)
    tasks = []

    async def bound_trial(*args, **kwargs):
        async with sem:
            result = await run_phase3_trial(*args, **kwargs)
            await asyncio.sleep(2)
            return result

    for tier, payloads in tiers.items():
        selected = payloads if limit <= 0 else payloads[:limit]
        for p in selected:
            benign = (
                random.choice(benign_samples).get("text", "Summarize this.")
                if benign_samples else "Summarize this."
            )
            payload_text = p.get("text", "")
            payload_id = p.get("id", "unknown")

            for use_combine in (False, True):
                tasks.append(bound_trial(
                    model_client, sentinel, spotlight,
                    tier, payload_id, benign, payload_text, use_combine,
                ))

    print(f"Running {len(tasks)} Phase 3 trials (direct + combine per payload)...")
    completed = await asyncio.gather(*tasks)

    os.makedirs("results", exist_ok=True)
    csv_file = "results/phase3_defense_benchmark.csv"
    fields = [
        "payload_id", "tier", "attack_type",
        "spotlight_bypassed", "spotlight_response",
        "sentinel_detected",
        "spotlight_latency_ms", "sentinel_latency_ms",
    ]
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in completed:
            writer.writerow(row)

    print(f"\nResults written to {csv_file}")
    _print_summary(completed)
    print("\nPhase 3 complete!")


def _print_summary(completed: list[dict]):
    print("\n--- Phase 3 Summary ---")
    print(f"{'Tier':<6} {'Attack':<8} {'ASV':>6} {'Spotlight bypass':>17} {'Sentinel detect':>16} {'N':>5}")
    print("-" * 60)
    for tier in ("L1", "L2", "L3"):
        for attack_type in ("direct", "combine"):
            subset = [r for r in completed if r["tier"] == tier and r["attack_type"] == attack_type]
            if not subset:
                continue
            asv = calc_asv(tier, [r["spotlight_response"] for r in subset])
            bypass_rate = sum(r["spotlight_bypassed"] for r in subset) / len(subset)
            detect_rate = sum(r["sentinel_detected"] for r in subset) / len(subset)
            print(
                f"{tier:<6} {attack_type:<8} {asv:>6.2f} {bypass_rate:>17.2f} {detect_rate:>16.2f} {len(subset):>5}"
            )
