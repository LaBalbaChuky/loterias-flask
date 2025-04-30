import paramiko


def main():
    host = "ssh.pythonanywhere.com"
    port = 22
    username = "OmarValdez"
    password = "Loteria2024"  # cámbiala aquí si ya la actualizaste
    local_path = "resultados.html"
    remote_path = "/home/OmarValdez/templates/resultados.html"

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port=port, username=username, password=password)

        sftp = ssh.open_sftp()
        sftp.put(local_path, remote_path)
        print(f"✅ Subido: {local_path} → {remote_path}")
        sftp.close()
        ssh.close()

    except Exception as e:
        print(f"❌ Error al subir archivo: {e}")


if __name__ == "__main__":
    main()
