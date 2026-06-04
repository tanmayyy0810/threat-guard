import pandas as pd

# Load dataset
df = pd.read_csv("dataset/malicious_phish.csv")

# Convert labels
df['label'] = df['type'].apply(
    lambda x: 0 if x == 'benign' else 1
)

# Keep only required columns
df = df[['url', 'label']]

# Save cleaned dataset
df.to_csv("dataset/malicious_phish.csv", index=False)

print("✅ Dataset cleaned & ready")
