Quick start

1. Create a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. (Optional) Train models if you need to rebuild them:

```powershell
cd threat_guard
python train_url_model.py
python train_email_model.py
```

4. Run the app:

```powershell
cd threat_guard
python app.py
```

Open http://127.0.0.1:5000 in your browser.
