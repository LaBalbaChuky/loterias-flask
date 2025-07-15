import requests

def subir_a_netlify():
    TOKEN = "nfp_UErELT16pDTr8x4z9aLR96GtcpHiEZ6M16dc"
    SITE_ID = "837f7e6f-1855-4f9a-ad30-4a0bc29bdd72"

    try:
        with open("public/index.html", "rb") as f:
            files = {
                'file': ('index.html', f)
            }
            headers = {
                "Authorization": f"Bearer {TOKEN}"
            }

            response = requests.post(
                f"https://api.netlify.com/api/v1/sites/{SITE_ID}/deploys",
                files=files,
                headers=headers
            )

            if response.status_code == 200:
                url = response.json().get("deploy_ssl_url", "")
                print("✅ Subido correctamente a Netlify:")
                print("🔗 URL del sitio:", url)
            else:
                print("❌ Error al subir:", response.status_code, response.text)
    except Exception as e:
        print("❌ Error general:", e)
