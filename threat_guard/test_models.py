import joblib

# Load models
url_model = joblib.load("models/url_model.pkl")
email_model = joblib.load("models/email_model.pkl")
vectorizer = joblib.load("models/email_vectorizer.pkl")

def extract_features(url):
    return [[
        len(url),
        url.count('.'),
        url.count('@'),
        url.count('-'),
        1 if "https" in url else 0
    ]]

# Test URL
test_url = "http://paypal-login-secure.com"
print("URL Prediction:", url_model.predict(extract_features(test_url)))

# Test Email
test_email = "Your account is blocked. Click here to verify"
email_vec = vectorizer.transform([test_email])
print("Email Prediction:", email_model.predict(email_vec))
