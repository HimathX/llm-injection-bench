from datasets import load_dataset
import pandas as pd
import json

def main():
    print("Loading deepset/prompt-injections dataset...")
    ds = load_dataset("deepset/prompt-injections")
    df = pd.DataFrame(ds["train"])
    
    # 1. Export Adversarial (label=1) for Claude
    adversarial_df = df[df["label"] == 1][["text"]]
    adversarial_csv_path = "dataset/audit_queue.csv"
    adversarial_df.to_csv(adversarial_csv_path, index=False)
    print(f"Exported {len(adversarial_df)} adversarial samples to {adversarial_csv_path}")

    # 2. Extract 50 Benign (label=0) samples
    benign_df = df[df["label"] == 0][["text"]].sample(n=50, random_state=42)
    benign_samples = benign_df.to_dict(orient="records")
    
    benign_json_path = "dataset/benign_samples.json"
    with open(benign_json_path, "w", encoding="utf-8") as f:
        json.dump(benign_samples, f, indent=2, ensure_ascii=False)
    print(f"Exported {len(benign_samples)} benign samples to {benign_json_path}")

if __name__ == "__main__":
    main()
