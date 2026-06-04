import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Feature extraction function
def extract_features(url):
    return [
        len(url),
        url.count('.'),
        url.count('@'),
        url.count('-'),
        1 if url.startswith("https") else 0
    ]

# Load cleaned dataset
data = pd.read_csv("dataset/malicious_phish.csv")

# Convert URLs into numbers
X = data['url'].apply(lambda x: extract_features(str(x))).tolist()
y = data['label']

# Split data (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train ML model
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Test model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("✅ URL Model Accuracy:", accuracy)

# Save model
joblib.dump(model, "models/url_model.pkl")
print("✅ Model saved in models/url_model.pkl")
test_url = "http://paypal-login-secure.com"
prediction = model.predict([extract_features(test_url)])

print("🔍 Test URL:", test_url)
print("🛑 Prediction:", "Phishing" if prediction[0] == 1 else "Legitimate")