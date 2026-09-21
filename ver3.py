from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def start():
    return "inicio do projeto"

@app.route("/cadastro", methods=["POST"])
def cadastro():

    dados = request.get_json()

    return jsonify({
        "Mensagem": "Cadastro realizado",
        "dados": dados
    })

@app.route("/item")
def item():

    id = request.args.get("id", "Não informado")

    #?id= wtf
    return f"item: {id}"

if __name__ ==  "__main__":
    app.run(debug=True)