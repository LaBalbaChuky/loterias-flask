import requests

def subir_a_netlify():
    TOKEN = "TU_TOKEN_NETLIFY"
    SITE_ID = "TU_SITE_ID"

    with open("public/index.html", "rb") as f:
        files = {'file': ('index.html', f)}
        headers = {"Authorization": f"Bearer {TOKEN}"}

        response = requests.post(
            f"https://api.netlify.com/api/v1/sites/{SITE_ID}/deploys",
            files=files,
            headers=headers
        )

        if response.status_code == 200:
            print("✅ Subido a Netlify:", response.json()["deploy_ssl_url"])
        else:
            print("❌ Error al subir:", response.status_code, response.text)
