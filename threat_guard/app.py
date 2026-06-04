# from flask import Flask, render_template

# app = Flask(__name__)

# @app.route("/")
# def home():
#     return render_template("index.html")

# @app.route("/url")
# def url_page():
#     return render_template("url.html")

# @app.route("/email")
# def email_page():
#     return render_template("email.html")

# @app.route("/about")
# def about_page():
#     return render_template("about.html")

# if __name__ == "__main__":
#     app.run(debug=True)
print("🔥 app.py loaded")

from flask import Flask, render_template, request
import joblib
from pathlib import Path

# Base directory of this file — makes paths work regardless of CWD
BASE_DIR = Path(__file__).resolve().parent

# Create Flask app with explicit template/static folders (robust to run modes)
app = Flask(__name__, static_folder=str(BASE_DIR / "static"), template_folder=str(BASE_DIR / "templates"))

# ================= LOAD MODELS (safe)
def safe_load(path):
    try:
        p = BASE_DIR / path
        return joblib.load(str(p))
    except Exception as e:
        print(f"⚠️ Failed to load model {path}: {e}")
        return None

url_model = safe_load("models/url_model.pkl")
email_model = safe_load("models/email_model.pkl")
email_vectorizer = safe_load("models/email_vectorizer.pkl")


TRUSTED_DOMAINS = [
    "chatgpt.com",
    "google.com",
    "openai.com",
    "github.com",
    "microsoft.com"
]


# ================= HELPER FUNCTION =================
# def extract_url_features(url):
#     suspicious_words = ["login", "verify", "secure", "account", "bank"]

#     return [[
#         len(url),
#         url.count('.'),
#         url.count('@'),
#         url.count('-'),
#         1 if url.startswith("https") else 0,
#         sum(word in url.lower() for word in suspicious_words)
#     ]]
# def extract_url_features(url):
#     return [[
#         len(url),
#         url.count('.'),
#         url.count('@'),
#         url.count('-'),
#         1 if url.startswith("https") else 0
#     ]]
def extract_url_features(url):
    features = [
        len(url),
        url.count('.'),
        url.count('@'),
        url.count('-'),
        1 if url.startswith("https") else 0
    ]
    print("DEBUG URL FEATURES:", features, "COUNT:", len(features))
    return [features]


# def extract_url_features(url):
#     return [[
#         len(url),
#         url.count('.'),
#         url.count('@'),
#         url.count('-'),
#         1 if url.startswith("https") else 0
#     ]]

# ================= ROUTES =================

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about_page():
    return render_template("about.html")

# @app.route("/url", methods=["GET", "POST"])
# def url_page():
#     result = None

#     if request.method == "POST":
#         user_url = request.form["url"]
#         prediction = url_model.predict(extract_url_features(user_url))[0]

#         if prediction == 1:
#             result = "🚨 Phishing URL Detected"
#         else:
#             result = "✅ Legitimate URL"

#     return render_template("url.html", result=result)





# @app.route("/url", methods=["GET", "POST"])
# def url_page():
#     result = None

#     if request.method == "POST":
#         user_url = request.form["url"]

#         prob = url_model.predict_proba(
#             extract_url_features(user_url)
#         )[0][1]

#         # 🔐 Rule-based checks (OVERRIDE)
#         if "-" in user_url and "login" in user_url.lower():
#             result = "🚨 Phishing URL Detected (Rule-based)"

#         elif not user_url.startswith("https"):
#             result = "⚠️ Suspicious URL (No HTTPS)"

#         else:
#             prediction = url_model.predict(extract_url_features(user_url))[0]
#             if prediction == 1:
#                 result = f"🚨 Phishing URL Detected (Confidence: {prob*100:.2f}%)"
#             else:
#                 result = f"✅ Legitimate URL (Confidence: {(1-prob)*100:.2f}%)"
                

#     return render_template("url.html", result=result)



# @app.route("/url", methods=["GET", "POST"])
# def url_page():
#     result = None

#     if request.method == "POST":
#         user_url = request.form["url"]

#         # RULE-BASED OVERRIDE (no ML yet)
#         if "-" in user_url and "login" in user_url.lower():
#             result = "🚨 Phishing URL Detected (Rule-based)"

#         else:
#             features = extract_url_features(user_url)

#             prediction = url_model.predict(features)[0]
#             prob = url_model.predict_proba(features)[0][1]

#             if prediction == 1:
#                 result = f"🚨 Phishing URL (Confidence: {prob*100:.2f}%)"
#             else:
#                 result = f"✅ Legitimate URL (Confidence: {(1-prob)*100:.2f}%)"

#     return render_template("url.html", result=result)

from urllib.parse import urlparse

@app.route("/url", methods=["GET", "POST"])
def url_page():
    result = None

    if request.method == "POST":
        user_url = request.form["url"].strip()

        domain = urlparse(user_url).netloc.lower()

        # ✅ Whitelist override
        if any(trusted in domain for trusted in TRUSTED_DOMAINS):
            result = "✅ Legitimate URL (Trusted Domain)"

        # 🚨 Rule-based phishing patterns
        elif "-" in domain and "login" in domain:
            result = "🚨 Phishing URL Detected (Rule-based)"

        else:
                features = extract_url_features(user_url)
                if url_model is None:
                    result = "⚠️ URL model not available. Run training or check models folder."
                else:
                    prediction = url_model.predict(features)[0]
                    prob = url_model.predict_proba(features)[0][1]

                    if prediction == 1:
                        result = f"🚨 Phishing URL (ML Confidence: {prob*100:.2f}%)"
                    else:
                        result = f"✅ Legitimate URL (ML Confidence: {(1-prob)*100:.2f}%)"

    return render_template("url.html", result=result)



@app.route("/email", methods=["GET", "POST"])
def email_page():
    result = None

    if request.method == "POST":
        email_text = request.form["email"]
        if email_vectorizer is None or email_model is None:
            result = "⚠️ Email model or vectorizer not available. Run training or check models folder."
        else:
            email_vector = email_vectorizer.transform([email_text])
            prediction = email_model.predict(email_vector)[0]

            if prediction == 1:
                result = "🚨 Malicious / Spam Email Detected"
            else:
                result = "✅ Safe Email"

    return render_template("email.html", result=result)

# ================= RUN APP =================
if __name__ == "__main__":
    app.run(debug=True)
