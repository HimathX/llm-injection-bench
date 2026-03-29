# llm-injection-bench — Roadmap

## Status Overview

| Phase | Status | Output |
|-------|--------|--------|
| Phase 1: Exploit Mapping | COMPLETE | `results/phase1_raw.csv` (1,029 trials) |
| Phase 2: Defense Benchmark | COMPLETE | `results/phase2_defense_benchmark.csv` |
| Phase 3: Research Paper Extensions | IN PROGRESS | — |

---

## Immediate Fixes (Blocking Publication)

### 1. Fix the L3 Webhook
Replace `localhost:5000` in `src/evaluator_l3_webhook.py` with a real public URL.
Use [webhook.site](https://webhook.site) — free, no setup required.
Re-run L3 trials and verify actual HTTP requests fire.
**Nothing with L3 can be published until this is done.**

### 2. Analyze 21 False Positive Rows
Filter `results/phase2_defense_benchmark.csv`:
`is_malicious_true=0` AND `judge_flagged=1`
Read every row. Understand why the LLM judge flagged legitimate inputs.
This analysis is a key finding — goes directly into the paper's defense evaluation section.

### 3. Increase L3 Trials to 30 Per Payload
Currently 3 trials per payload is statistically indefensible.
Re-run L3 only with 30 trials per payload (~20 min, near-zero cost).

---

## Phase 3: New Experiments (For Research Paper)

### 4. Add CombineAttacker
Port the Combined Attack from `Open-Prompt-Injection/` (Liu et al. 2310.12815):
combines Escape Characters + Context Ignoring + Fake Completion.
- Create `src/attacks/combine_attacker.py`
- Add as **L2-combined** tier
- Run against all 3 models, output `results/phase3_combined_attack.csv`

### 5. Add DataSentinel Defense
Port from `Open-Prompt-Injection/OpenPromptInjection/apps/DataSentinelDetector.py` (Liu et al.):
game-theoretic detection using an adversarial probe.
- Create `src/defenses/data_sentinel.py`
- Add to Phase 2 benchmark loop as Defense 3
- Record TPR, FPR, latency alongside existing two defenses

### 6. Add Spotlighting Defense
Implement from Debenedetti et al. (2503.18813v2 / CaMeL paper):
wraps untrusted data in special markers before passing to LLM.
- Create `src/defenses/spotlighting.py`
- Low implementation effort, meaningful comparison point

### 7. Implement Formal Metrics
Replace raw "success rate" with the 4-metric system from Liu et al.:
`PNA-T`, `PNA-I`, `ASV`, `MR`
- Create `src/metrics.py`
- Apply to Phase 1 results retrospectively
- Makes results comparable to prior published benchmarks

### 8. Re-run Phase 2 with 4 Defenses
Once DataSentinel and Spotlighting are implemented:
- Re-run Phase 2 with all 4 defenses
- Output `results/phase3_defense_comparison.csv`
- Regenerate `results/phase2_chart.png` with updated data

---

## Paper Writing

### 9. Write Gemini vs Claude Gap Analysis
You have 36.5% vs 20% attack success rates — don't just report the numbers.
Hypothesize why: RLHF approach differences, system prompt handling, context window behavior.
One strong paragraph. This separates a benchmark from a research paper.

### 10. Write L3 Exfiltration Section
Frame clearly:
> "The model reproduced the exfiltration payload in its output. In any system that renders
> markdown — a Slack bot, a web dashboard, an agent UI — this is a live data exfiltration.
> We verified this by piping output through mistune and firing a real HTTP request."
Connect to WAInjectBench (2510.01354v1) VPI threat class.

### 11. Populate README Findings Table
Update `README.md` with real Phase 1 and Phase 2 numbers.
Do this before pushing to GitHub.

### 12. Write `CONTRIBUTING.md`
Define payload submission format for the community challenge.
Include bypass criteria, labeling format, credit policy.

---

## Publishing

### 13. Push to GitHub
Clean up repo, finalize README with real numbers.
Push **48 hours before Part 1 article drops** so early readers can star it.

### 14. Publish Part 1 — The Exploit Map
Lead with L3 hitting every model.
Link GitHub repo in the first paragraph.
Include `results/phase1_chart.png` as hero image.
Target: Towards Data Science or Substack.

Suggested title:
> *"I Ran 1,029 Prompt Injection Tests. Here's What Actually Works in 2025."*

### 15. Publish Part 2 — The Defense Problem
Lead with the 42% false positive rate from the LLM judge.
Show latency numbers: embedding 659ms vs judge 2,567ms.
Include bypass examples from `L1_020`, `L1_055`, `L1_071`.

### 16. Launch Community Challenge
Open a GitHub Discussion inviting bypass payload submissions.
Credit verified bypasses in `payloads.json`.

---

## Checklist Before Submitting Paper

- [ ] L3 webhook URL replaced and re-run with 30 trials
- [ ] 21 false positive rows analyzed and documented
- [ ] CombineAttacker implemented and benchmarked
- [ ] DataSentinel defense implemented and benchmarked
- [ ] Spotlighting defense implemented and benchmarked
- [ ] Formal metrics (ASV, MR, PNA-T, PNA-I) applied to all results
- [ ] At least one verified bypass example documented
- [ ] README findings table populated with real numbers
- [ ] `CONTRIBUTING.md` written
- [ ] All external code (StruQ, Open-Prompt-Injection) properly cited
