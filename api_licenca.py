from flask import Flask, request, jsonify

app = Flask(__name__)

# Banco simulado com controle por chave e ID de máquina autorizado
LICENCAS_VALIDAS = {
    "minha-chave-123": {
        "status": "valido",
        "maquinas_autorizadas": ["5f39a1c2b4e709dd", "abc123def4567890", "492f730ab1f23e20"]
    },
    "cliente-beto-2025": {
        "status": "valido",
        "maquinas_autorizadas": ["beto-pc-01"]
    },
    "cliente-expirado": {
        "status": "expirado",
        "maquinas_autorizadas": []
    },
    "cliente-camilla-esposa": {
        "status": "valido",
        "maquinas_autorizadas": ["e8c0fed28fc99772"]
    },
}

@app.route('/api/validar', methods=['POST'])
def validar():
    dados = request.get_json()
    chave = dados.get("chave", "")
    id_maquina = dados.get("id_maquina", "")

    if chave in LICENCAS_VALIDAS:
        licenca = LICENCAS_VALIDAS[chave]
        if licenca["status"] != "valido":
            return jsonify({"status": "expirado"})
        if id_maquina not in licenca["maquinas_autorizadas"]:
            return jsonify({"status": "bloqueado"})
        return jsonify({"status": "valido"})
    else:
        return jsonify({"status": "invalido"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
