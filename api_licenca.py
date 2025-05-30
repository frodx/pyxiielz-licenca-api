from flask import Flask, request, jsonify

app = Flask(__name__)

# Simulando banco de dados de licenças
LICENCAS_VALIDAS = {
    "minha-chave-123": {"status": "expirado"},
    "cliente-beto-2025": {"status": "valido"},
    "cliente-expirado": {"status": "expirado"},
}

@app.route('/api/validar', methods=['POST'])
def validar():
    dados = request.get_json()
    chave = dados.get("chave", "")

    if chave in LICENCAS_VALIDAS:
        return jsonify(LICENCAS_VALIDAS[chave])
    else:
        return jsonify({"status": "invalido"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
