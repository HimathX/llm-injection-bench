import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

# ── Phase 1 Chart ────────────────────────────────────────────
p1 = pd.read_csv("results/phase1_raw.csv")

models = ["claude", "gemini", "groq"]
tiers  = ["L1", "L2", "L3"]
colors = {"claude": "#4fc3f7", "gemini": "#ef5350", "groq": "#66bb6a"}

fig, ax = plt.subplots(figsize=(10, 5), facecolor="#0f0f1a")
ax.set_facecolor("#12121f")

x     = np.arange(len(tiers))
width = 0.25

for i, model in enumerate(models):
    rates = []
    for tier in tiers:
        subset = p1[(p1["model"] == model) & (p1["tier"] == tier)]
        rate   = subset["score"].astype(int).mean() * 100 if len(subset) else 0
        rates.append(rate)
    offset = (i - 1) * width
    bars = ax.bar(x + offset, rates, width * 0.9,
                  label=model.capitalize(), color=colors[model], alpha=0.85)
    for bar, rate in zip(bars, rates):
        if rate > 0:
            ax.text(bar.get_x() + bar.get_width()/2,
                    bar.get_height() + 1.5,
                    f"{rate:.0f}%",
                    ha="center", color="white", fontsize=9, fontweight="bold")

ax.set_xticks(x)
ax.set_xticklabels(["L1: Naive Override", "L2: Context Shift", "L3: Markdown Exfil"],
                   color="#ccc", fontsize=11)
ax.set_yticks(range(0, 101, 20))
ax.set_yticklabels([f"{v}%" for v in range(0, 101, 20)], color="#aaa")
ax.set_ylabel("Attack Success Rate (%)", color="#aaa")
ax.set_title("Phase 1 — Prompt Injection Attack Success Rates\n1,029 trials across 3 models",
             color="white", fontsize=12, fontweight="bold", pad=12)
ax.set_ylim(0, 110)
ax.legend(facecolor="#1e1e2e", labelcolor="white", fontsize=9)
ax.grid(axis="y", color="#333", linestyle="--", alpha=0.5)
for spine in ax.spines.values():
    spine.set_edgecolor("#333")

plt.tight_layout()
plt.savefig("results/phase1_chart.png", dpi=150,
            bbox_inches="tight", facecolor=fig.get_facecolor())
print("✅ Saved results/phase1_chart.png")
plt.close()

# ── Phase 2 Chart ────────────────────────────────────────────
p2 = pd.read_csv("results/phase2_defense_benchmark.csv")

fig, axes = plt.subplots(1, 2, figsize=(14, 5), facecolor="#0f0f1a")
fig.suptitle("Phase 2 — Defense Benchmark", color="white",
             fontsize=13, fontweight="bold", y=1.02)

tiers_p2  = ["BENIGN", "L1", "L2", "L3"]
tier_colors = ["#4fc3f7", "#ef5350", "#ffa726", "#ce93d8"]

# Panel 1 — Detection recall
ax = axes[0]
ax.set_facecolor("#12121f")

emb_recall, judge_recall = [], []
for tier in tiers_p2:
    subset = p2[p2["tier"] == tier]
    mal    = subset[subset["is_malicious_true"] == 1] if tier != "BENIGN" else subset
    if tier == "BENIGN":
        emb_recall.append(subset["embedding_flagged"].astype(int).mean() * 100)
        judge_recall.append(subset["judge_flagged"].astype(int).mean() * 100)
    else:
        mal = subset[subset["is_malicious_true"].astype(int) == 1]
        emb_recall.append(mal["embedding_flagged"].astype(int).mean() * 100 if len(mal) else 0)
        judge_recall.append(mal["judge_flagged"].astype(int).mean() * 100 if len(mal) else 0)

x2    = np.arange(len(tiers_p2))
width = 0.35
ax.bar(x2 - width/2, emb_recall,   width * 0.9, label="Embedding Filter",
       color="#4fc3f7", alpha=0.85)
ax.bar(x2 + width/2, judge_recall, width * 0.9, label="LLM Judge",
       color="#ef5350", alpha=0.85)
ax.set_xticks(x2)
ax.set_xticklabels(tiers_p2, color="#ccc")
ax.set_ylabel("Detection Rate (%)", color="#aaa")
ax.set_title("Detection Rate by Tier\n(BENIGN = False Positive Rate)",
             color="white", fontsize=10)
ax.set_ylim(0, 110)
ax.legend(facecolor="#1e1e2e", labelcolor="white", fontsize=9)
ax.grid(axis="y", color="#333", linestyle="--", alpha=0.5)
ax.tick_params(colors="#aaa")
for spine in ax.spines.values():
    spine.set_edgecolor("#333")

# Panel 2 — Latency
ax2 = axes[1]
ax2.set_facecolor("#12121f")
defenses = ["Embedding Filter", "LLM Judge"]
avg_lats = [
    p2["embedding_latency_ms"].astype(float).mean(),
    p2["judge_latency_ms"].astype(float).mean()
]
bars = ax2.bar(defenses, avg_lats, color=["#4fc3f7", "#ef5350"],
               alpha=0.85, width=0.4)
for bar, lat in zip(bars, avg_lats):
    ax2.text(bar.get_x() + bar.get_width()/2,
             bar.get_height() + 30,
             f"{lat:.0f}ms", ha="center",
             color="white", fontsize=11, fontweight="bold")
ax2.set_ylabel("Average Latency (ms)", color="#aaa")
ax2.set_title("Latency Overhead Per Call",
              color="white", fontsize=10)
ax2.tick_params(colors="#aaa")
ax2.grid(axis="y", color="#333", linestyle="--", alpha=0.5)
for spine in ax2.spines.values():
    spine.set_edgecolor("#333")

plt.tight_layout()
plt.savefig("results/phase2_chart.png", dpi=150,
            bbox_inches="tight", facecolor=fig.get_facecolor())
print("✅ Saved results/phase2_chart.png")
plt.close()