from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route("/generate", methods=["POST"])
def generate():
    name = request.json["name"]
    subprocess.run(["bash", "scripts/generate_cert.sh", name])
    return jsonify({"status": "generated", "user": name})

@app.route("/verify", methods=["POST"])
def verify():
    name = request.json["name"]
    result = subprocess.run(
        ["bash", "scripts/verify_cert.sh", name],
        capture_output=True,
        text=True
    )
    return jsonify({"result": result.stdout})

@app.route("/revoke", methods=["POST"])
def revoke():
    name = request.json["name"]
    subprocess.run(["bash", "scripts/revoke_cert.sh", name])
    return jsonify({"status": "revoked", "user": name})

app.run(host="0.0.0.0", port=5000)

