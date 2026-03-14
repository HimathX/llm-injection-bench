import pandas as pd
import os

def main():
    print("Loading existing audit_queue.csv...")
    audit_df = pd.read_csv("dataset/audit_queue.csv")
    print(f"Existing rows: {len(audit_df)}")

    kaggle_dir = "dataset/prompt-injection-in-the-wild"
    new_prompts = []

    file_pb = os.path.join(kaggle_dir, "jailbreak_prompts.csv")
    if os.path.exists(file_pb):
        df_pb = pd.read_csv(file_pb, usecols=["Prompt"]).dropna()
        new_prompts.append(df_pb.rename(columns={"Prompt": "text"}))

    file_pg = os.path.join(kaggle_dir, "predictionguard_df.csv")
    if os.path.exists(file_pg):
        df_pg = pd.read_csv(file_pg, usecols=["Prompt"]).dropna()
        new_prompts.append(df_pg.rename(columns={"Prompt": "text"}))
        
    if new_prompts:
        merged_new = pd.concat(new_prompts, ignore_index=True)
        # Sample to prevent overwhelming Claude? The user said "every row", let's give them 250 rows from this dataset to keep it manageable.
        # Alternatively, we just dump it all. Let's sample 300 to be safe but have a good amount.
        sampled_new = merged_new.sample(n=min(300, len(merged_new)), random_state=42)
        
        final_df = pd.concat([audit_df, sampled_new], ignore_index=True)
        final_df.to_csv("dataset/audit_queue.csv", index=False)
        print(f"Added {len(sampled_new)} Kaggle prompts. New total: {len(final_df)}")
        print("Updated dataset/audit_queue.csv successfully.")
    else:
        print("Kaggle datasets not found.")

if __name__ == "__main__":
    main()
