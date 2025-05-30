from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Simulando banco de dados de licenças
LICENCAS_VALIDAS = {
    "minha-chave-123": {
        "status": "valido",
        "expira_em": "2025-12-31",
        "maquinas_autorizadas": ["5f39a1c2b4e709dd", "492f730ab1f23e20"]
    },
    "cliente-beto-2025": {
        "status": "valido",
        "expira_em": "2025-07-15",
        "maquinas_autorizadas": ["beto-pc-01"]
    },
    "cliente-expirado": {
        "status": "expirado",
        "expira_em": "2024-12-31",
        "maquinas_autorizadas": []
    },
    "cliente-camilla-esposa": {
        "status": "valido",
        "expira_em": "2025-06-30",
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

        # Verifica se a licença foi desativada
        if licenca["status"] != "valido":
            return jsonify({"status": "expirado"})

        # Verifica se o ID da máquina está autorizado
        if id_maquina not in licenca["maquinas_autorizadas"]:
            return jsonify({"status": "bloqueado"})

        # Verifica validade por data
        hoje = datetime.now().date()
        validade = datetime.strptime(licenca["expira_em"], "%Y-%m-%d").date()
        if hoje > validade:
            return jsonify({"status": "expirado"})

        return jsonify({"status": "valido"})

    return jsonify({"status": "invalido"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
