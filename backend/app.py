import os
import subprocess
from flask import Flask, request, jsonify, send_file, render_template

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_DIR = os.path.join(BASE_DIR, "../users")
CA_CERT = os.path.join(BASE_DIR, "../ca/root/certs/root.crt")

# =========================
# PAGE WEB
# =========================
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


# =========================
# 1️⃣ GENERER CERTIFICAT
# =========================
@app.route("/generate", methods=["POST"])
def generate():
    name = request.form.get("name")

    subprocess.run(
        ["bash", "../scripts/generate_cert.sh", name],
        cwd=BASE_DIR
    )

    return "Certificat généré pour " + name


# =========================
# 2️⃣ VERIFIER CERTIFICAT
# =========================
@app.route("/verify", methods=["POST"])
def verify():
    name = request.form.get("name")
    cert_path = os.path.join(USERS_DIR, name, f"{name}.crt")
    crl_path = os.path.join(BASE_DIR, "../ca/root/crl.pem")

    if not os.path.exists(cert_path):
        return "Certificat introuvable"

    if not os.path.exists(crl_path):
        return "CRL introuvable (aucun certificat révoqué)"

    result = subprocess.run(
        [
            "openssl", "verify",
            "-CAfile", CA_CERT,
            "-CRLfile", crl_path,
            "-crl_check",
            cert_path
        ],
        capture_output=True,
        text=True
    )

    return result.stdout


# =========================
# 3️⃣ TELECHARGER CERTIFICAT
# =========================
@app.route("/download", methods=["POST"])
def download():
    name = request.form.get("name")
    cert_path = os.path.join(USERS_DIR, name, f"{name}.crt")

    if not os.path.exists(cert_path):
        return "Certificat introuvable"

    return send_file(cert_path, as_attachment=True)


# =========================
# 4️⃣ REVOQUER CERTIFICAT
# =========================
@app.route("/revoke", methods=["POST"])
def revoke():
    name = request.form.get("name")

    subprocess.run(
        ["bash", "../scripts/revoke_cert.sh", name],
        cwd=BASE_DIR
    )

    return "Certificat révoqué pour " + name


# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

