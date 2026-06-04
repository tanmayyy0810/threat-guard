import pandas as pd

# Load dataset
df = pd.read_csv("dataset/phishing_email.csv")

# Select correct columns
df = df[['text_combined', 'label']]

# Make sure label is numeric
df['label'] = df['label'].apply(
    lambda x: 1 if str(x).lower() in ['phishing', 'spam', '1'] else 0
)

# Save cleaned dataset
df.to_csv("dataset/emails.csv", index=False)

print("✅ Email dataset cleaned successfully")
