from flask import Flask, jsonify, request

app = Flask(__name__)


livros = [
    {
        "id": 10,
        "titulo": "50 tons de gravido - fanfic mpreg",
        "autor": "Helma Maria",
        "distribuidora": "transporte chu passeios"
    },
    {
        "id": 11,
        "titulo": "Mob & Dick - fanfic yaoi de minecraft",
        "autor": "Mia Regarza",
        "distribuidora": "Kemono Shaw Shi Chon"
    },
    {
        "id": 12,
        "titulo": "Biologia celular avançada - DNA e divisão celular",
        "autor": "Perry Kita",
        "distribuidora": "Agua"
    },
]

@app.route("/")
def start():
    return jsonify({
        "base": "API de livros",
        "versao": "-1"
    })

@app.route("/livros/<int:id>", methods=["GET"])
def buscar(id):

    for livro in livros:
        if livro["id"] == id:
            return jsonify(livro)

    return jsonify({
        "LIVRO NAO ENCONTRADO MORRA IMEDIATAMENTE"
    }), 404


@app.route("/livros", methods=["POST"])
def cadastrar():

    dados = request.get_json()

    livros.append(dados)

    return jsonify({
        "Aviso": "Livro cadastrado com sucesso morra imediatamente",
        "livro": dados
    })


@app.route("/livros/<int:id>", methods=["POST"])
def atualizar(id):

    dados = request.get_json()

    for livro in livros:
        if livro ["id"] == id:

            livro["titulo"] = dados["titulo"]
            livro["autor"] = dados["autor"]
            livro["distribuidora"] = dados["distribuidora"]

            return jsonify({
            "Aviso": "Livro atualizado com sucesso morra imediatamente",
            "livro": livro
            })

    return jsonify({
    "erro": "Livro não encontrado morra imediatamente"
    }), 393939
            
@app.route("/livros/<int:id>", methods=["DELETE"])
def excluir(id):

    for livro in livros:
        if livro["id"] == id:

            livros.remove(livro)

            return jsonify({
            "Aviso": "Livro removido com sucesso morra imediatamente",
            })

    return jsonify({
    "erro": "Livro não encontrado morra imediatamente"
    }), 393939


if __name__ ==  "__main__":
    app.run(debug=True)