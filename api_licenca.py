# ==========================================
# API de Licenciamento para Pyxiielz Converter
# Versão com suporte a expiracao por data ("expira_em")
# ==========================================

from flask import Flask, request, jsonify
from datetime import datetime
import hashlib

app = Flask(__name__)

# Simula banco de dados de licenças
LICENCAS = [
    {
        "chave": "cliente-camilla-esposa",
        "id_maquina": "",  # Deixe vazio para aceitar qualquer uma
        "expira_em": "2025-06-30"  # AAAA-MM-DD
    },
    {
        "chave": "cliente-teste",
        "id_maquina": "1234ABCD5678EFGH",  # Exemplo de ID fixo
        "expira_em": "2025-12-31"
    }
]

def calcular_dias_restantes(data_expiracao):
    hoje = datetime.now().date()
    try:
        expira = datetime.strptime(data_expiracao, "%Y-%m-%d").date()
        delta = (expira - hoje).days
        return delta
    except:
        return -1

@app.route("/api/validar", methods=["POST"])
def validar():
    req = request.get_json()
    chave = req.get("chave")
    id_maquina = req.get("id_maquina")

    for lic in LICENCAS:
        if lic["chave"] == chave:
            # Verifica id_maquina se estiver definido
            if lic["id_maquina"] and lic["id_maquina"] != id_maquina:
                return jsonify({"status": "bloqueado"})

            dias = calcular_dias_restantes(lic["expira_em"])
            if dias >= 0:
                return jsonify({"status": "valido", "dias_restantes": dias})
            else:
                return jsonify({"status": "expirado"})

    return jsonify({"status": "invalido"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
