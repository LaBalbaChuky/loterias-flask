import requests
import requests

def subir_a_netlify():
    url = "https://api.netlify.com/api/v1/sites/<837f7e6f-1855-4f9a-ad30-4a0bc29bdd72>/deploys"
    headers = {
        "Authorization": "Bearer <nfp_UErELT16pDTr8x4z9aLR96GtcpHiEZ6M16dc>"
    }

    files = {
        'file': ('index.html', open('public/index.html', 'rb')),
    }

    response = requests.post(url, headers=headers, files=files)
    print(f"✅ Subida a Netlify: {response.status_code}", response.text)
