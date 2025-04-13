
from flask import Flask, render_template_string
import os
from attached_assets.scraper import html

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string(html)

if __name__ == '__main__':
    os.makedirs('templates', exist_ok=True)
    app.run(host='0.0.0.0', port=5000)
