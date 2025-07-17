import requests
import os

def subir_a_netlify():
    site_id = "837f7e6f-1855-4f9a-ad30-4a0bc29bdd72"
    token = "nfp_UErELT16pDTr8x4z9aLR96GtcpHiEZ6M16dc"
    file_path = "public/index.html"

    if not os.path.exists(file_path):
        print("❌ El archivo index.html no existe.")
        return

    with open(file_path, "rb") as f:
        files = {
            'file': ('index.html', f, 'text/html')
        }
        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = requests.post(
            f"https://api.netlify.com/api/v1/sites/{site_id}/deploys",
            headers=headers,
            files=files
        )

        if response.status_code == 200 or response.status_code == 201:
            deploy_url = response.json().get("deploy_ssl_url") or response.json().get("deploy_url")
            print("✅ Subido a Netlify:", deploy_url)
        else:
            print("❌ Error al subir:", response.status_code, response.text)
