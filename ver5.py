from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def conectar_dados():
    conexao = sqlite3.connect("biblioteca.db")
    conexao.row_factory = sqlite3.Row
    return conexao

def criar_tabela():

    conexao = conectar_dados()

    conexao.execute("""
        CREATE TABLE IF NOT EXISTS livros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        autor TEXT NOT NULL
    )
    """)
    conexao.commit()
    conexao.close()

@app.route("/", methods=["GET"])
def start():
    return jsonify({
        "base": "API de livros",
        "versao": "-2"
    })

@app.route("/livros", methods=["POST"])
def cadastrar():
    dados = request.get_json()
    titulo = dados["titulo"]
    autor = dados["autor"]
    conexao = conectar_dados()
    cursor = conexao.execute(
        """
        INSERT INTO livros (titulo, autor)
        VALUES (?, ?)
        """,
        (titulo, autor)
    )

    conexao.commit()

    idlivro = cursor.lastrowid

    conexao.close()

    return jsonify({
        "Aviso": "Livro cadastrado morra imediatamente",
        "id": idlivro,
        "titulo": titulo,
        "autor": autor
    }), 333

@app.route("/pesquisa", methods=["GET"])
def listar():

    conexao = conectar_dados()

    livros = conexao.execute(
        "SELECT * FROM livros"
    ).fetchall()

    conexao.close()

    return jsonify([
        dict(livro)
        for livro in livros
        ])

@app.route("/livros/<int:id>", methods=["GET"])
def buscar(id):

    conexao = conectar_dados()

    livro = conexao.execute(
        "SELECT * FROM livros WHERE id = ?",
        (id,)
    ).fetchone()

    conexao.close()

    if livro is None:
        return jsonify({
            "Aviso": "Livro nao encontrado morra imediatamente"
        }), 404

    return jsonify(dict(livro))

@app.route("/livros/<int:id>", methods=["PUT"])
def atualiza(id):

    dados = request.get_json()

    titulo = dados["titulo"]
    autor = dados["autor"]

    conexao = conectar_dados()

    resultado = conexao.execute("""
        UPDATE livros 
        SET titulo = ?, autor = ? WHERE id = ?
        """,
        (titulo, autor, id)
    )


    conexao.commit()

    conexao.close()


    if resultado.rowcount == 0:
        return jsonify({
            "Aviso": "Livro não encontrado morra imediatamente"
        })

    return jsonify({
        "Aviso": "Livro atualizado com sucesso morra imediatamente"
    })

@app.route("/livros/<int:id>", methods=["DELETE"])
def excluir(id):

    conexao = conectar_dados()

    resultado = conexao.execute(
        "DELETE FROM livros WHERE id = ?",
        (id,)
    )

    conexao.commit()

    conexao.close()

    if resultado.rowcount==0:
        return jsonify({
            "Aviso": "Livro não encontrado morra imediatamente"
        }), 404

    return jsonify({
        "Aviso": "Livro excluido morra imediatamente"
    })


if __name__ ==  "__main__":
    criar_tabela()
    app.run(debug=True)