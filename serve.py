# serve.py
from waitress import serve
from app import create_app

app = create_app()
print("Starting local server on http://localhost:5000")

serve(app, host="0.0.0.0", port=5000)
