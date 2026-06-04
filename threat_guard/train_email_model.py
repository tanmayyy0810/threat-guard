import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import joblib

# Load cleaned email dataset
data = pd.read_csv("dataset/emails.csv")

X = data['text_combined']
y = data['label']

# Convert text to numerical features
vectorizer = TfidfVectorizer(
    stop_words='english',
    max_features=5000
)

X_vectorized = vectorizer.fit_transform(X)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X_vectorized, y, test_size=0.2, random_state=42
)

# Train model
model = MultinomialNB()
model.fit(X_train, y_train)

# Evaluate model
accuracy = accuracy_score(y_test, model.predict(X_test))
print("✅ Email Model Accuracy:", accuracy)

# Save model and vectorizer
joblib.dump(model, "models/email_model.pkl")
joblib.dump(vectorizer, "models/email_vectorizer.pkl")

print("✅ Email model & vectorizer saved successfully")
