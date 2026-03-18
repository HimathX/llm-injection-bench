# llm-injection-bench — Publishing Roadmap

## Phase: Before Writing Anything

### 1. Fix the L3 Webhook
Replace `localhost:5000` with a real public URL using [webhook.site](https://webhook.site) — free, no setup required.
Re-run L3 trials and verify actual HTTP requests fire on the server.
**This is non-negotiable before publishing.**

### 2. Pull the 21 False Positive Rows
Open `phase2_defense_benchmark.csv`, filter `is_malicious_true=0` AND `judge_flagged=1`.
Read every single one. Find out why the judge blocked legitimate emails.
This analysis goes directly into Part 2.

### 3. Increase L3 Trials to 30 Per Payload
Currently 3 trials per payload is too thin to be defensible.
Re-run the harness with L3 only, 30 trials per payload.
Takes ~20 minutes and costs almost nothing.

### 4. Write the Gemini vs Claude Gap Paragraph
Don't just report 36.5% vs 20% — hypothesize why.
Different RLHF approach, system prompt handling, context window behavior — something.
One paragraph. This is what separates a benchmark from a research article.

### 5. Generate Final Charts
Run the harness visualizer to produce:
- `results/phase1_chart.png`
- `results/phase2_chart.png`

These are your hero images. **Do not write a single word of the article until these exist.**

> Do these in order. Do not skip to writing.

---

## Phase: Writing & Publishing

### 1. Write Part 1 Draft
Lead with L3 hitting every model, that's your opening line.
Show the results table with real numbers. Include `phase1_chart.png`.
Don't over-explain — let the data speak.
**Target: 1,200 words maximum.**

### 2. Write Part 2 Draft
Lead with the 42% false positive rate — that's your hook.
Show the latency numbers:
- Embedding filter avg: **659ms**
- LLM Judge avg: **2,567ms**

Include bypass examples from `L1_020`, `L1_055`, `L1_071`.
**Target: 1,000 words.**

### 3. Publish the GitHub Repo
- Clean up the codebase
- Finalize `README.md` with real numbers in the findings table
- Push to GitHub

Do this **48 hours before Part 1 goes live** so early readers can star it before the article drops.

### 4. Publish Part 1
Post to Towards Data Science or Substack.
Link the GitHub repo in the **first paragraph**.

Suggested title:
> *"I Ran 1,029 Prompt Injection Tests. Here's What Actually Works in 2025."*

### 5. Publish Part 2 + Launch Community Challenge
Post Part 2 **one week after Part 1**.
At the end, open a GitHub Discussion inviting readers to submit bypass payloads that fool the judge.

This turns a static article into a live experiment that compounds over time.