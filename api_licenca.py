
# ==========================================
# API de Licenciamento para Pyxiielz Converter
# Suporte a primeira ativação automática e expiração
# ==========================================

from flask import Flask, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

# 🔐 Caminho do arquivo de licenças
LICENCAS_FILE = "licencas.json"

# 📦 Carrega as licenças do arquivo
if os.path.exists(LICENCAS_FILE):
    with open(LICENCAS_FILE, "r") as f:
        LICENCAS = json.load(f)
else:
    LICENCAS = []

# 💾 Salva alterações no arquivo
def salvar_licencas():
    with open(LICENCAS_FILE, "w") as f:
        json.dump(LICENCAS, f, indent=4)

# 📆 Calcula dias restantes até o vencimento
def calcular_dias_restantes(data_expiracao):
    hoje = datetime.now().date()
    try:
        expira = datetime.strptime(data_expiracao, "%Y-%m-%d").date()
        return (expira - hoje).days
    except:
        return -1

# 🚪 Rota principal de validação
@app.route("/api/validar", methods=["POST"])
def validar():
    req = request.get_json()
    chave = req.get("chave")
    id_maquina = req.get("id_maquina")

    if not chave or not id_maquina:
        return jsonify({"status": "invalido"})

    for lic in LICENCAS:
        if lic["chave"] == chave:
            # Primeira ativação
            if lic["id_maquina"] == "":
                lic["id_maquina"] = id_maquina
                salvar_licencas()
            elif lic["id_maquina"] != id_maquina:
                return jsonify({"status": "bloqueado"})

            dias = calcular_dias_restantes(lic["expira_em"])
            if dias >= 0:
                return jsonify({"status": "valido", "dias_restantes": dias})
            else:
                return jsonify({"status": "expirado"})

    return jsonify({"status": "invalido"})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
