import requests
import requests

def subir_a_netlify():
    url = "https://api.netlify.com/api/v1/sites/<SITE_ID>/deploys"
    headers = {
        "Authorization": "Bearer <TOKEN>"
    }

    files = {
        'file': ('index.html', open('public/index.html', 'rb')),
    }

    response = requests.post(url, headers=headers, files=files)
    print(f"✅ Subida a Netlify: {response.status_code}", response.text)

