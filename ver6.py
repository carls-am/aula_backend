from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

#■█■█■█■█■█■█■█■█■█■█■█■█■█■
# CONFIGURAR BANCO DE DADOS
#■█■█■█■█■█■█■█■█■█■█■█■█■█■

def conectar_dados():
    conexao = sqlite3.connect("biblioteca3.db")
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao

def criar_tabelas():

    conexao = conectar_dados()

    conexao.execute("""
    CREATE TABLE IF NOT EXISTS autores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        nacionalidade TEXT NOT NULL
        )
    """)

    conexao.execute("""
    CREATE TABLE IF NOT EXISTS livros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        ano TEXT NOT NULL,
        autorid INTEGER NOT NULL,
        
        FOREIGN KEY (autorid)
            REFERENCES autores(id)

        )
    """)


    conexao.commit()
    conexao.close()

@app.route("/")
def start():
    return jsonify({
        "base": "API de livros",
        "versao": "pje"
    })

#■█■█■█■█■█■█■█■█■█■█■█■█■█■
#    CONFIGURAR AUTORES
#■█■█■█■█■█■█■█■█■█■█■█■█■█■

#◆ ▬▬▬▬▬▬ ❴✪❵ ▬▬▬▬▬▬ ◆
#     CRUD - CREATE
#◆ ▬▬▬▬▬▬ ❴✪❵ ▬▬▬▬▬▬ ◆

@app.route("/autores", methods=["POST"])
def cadastrar_autor():

    dados = request.get_json()

    nome = dados["nome"]
    nacionalidade = dados["nacionalidade"]

    conexao = conectar_dados()
    cursor = conexao.execute(
        """
        INSERT INTO autores
        (nome, nacionalidade)
        VALUES (?, ?)
        """, (nome, nacionalidade)
    )

    conexao.commit()
    idautor = cursor.lastrowid
    conexao.close()
    return jsonify({
        "Aviso": "Autor cadastrado com sucesso morra imediatamente",
        "autor": {
            "id": idautor,
            "nome": nome,
            "nacionalidade": nacionalidade
        }
    }), 201

#◆ ▬▬▬▬▬▬ ❴✪❵ ▬▬▬▬▬▬ ◆
#   CRUD - READ ALL
#◆ ▬▬▬▬▬▬ ❴✪❵ ▬▬▬▬▬▬ ◆

@app.route("/autores", methods=["GET"])
def listar_autores():
    conexao = conectar_dados()
    autores = conexao.execute(
        """
        SELECT * FROM autores
        ORDER BY id
        """
    ).fetchall()

    conexao.close()

    return jsonify([
        dict(autor)
        for autor in autores
    ])

#◆ ▬▬▬▬▬▬ ❴✪❵ ▬▬▬▬▬▬ ◆
#     CRUD - READ
#◆ ▬▬▬▬▬▬ ❴✪❵ ▬▬▬▬▬▬ ◆

@app.route("/autores/<int:id>", methods=["GET"])
def buscar_autor(id):

    conexao = conectar_dados()
    autor = conexao.execute(
        """
        SELECT * FROM autores
        WHERE id = ?
        """, (id,)
    ).fetchone()
    
    conexao.close()

    if autor is None:
        return jsonify({
            "Aviso": "Autor não encontrado morra novamente mais tarde"
        }), 404

    return jsonify(dict(autor))

#◆ ▬▬▬▬▬▬ ❴✪❵ ▬▬▬▬▬▬ ◆
#     CRUD - UPDATE
#◆ ▬▬▬▬▬▬ ❴✪❵ ▬▬▬▬▬▬ ◆

@app.route("/autores/<int:id>", methods=["PUT"])
def atualizar_ator(id):
    dados = request.get_json()

    nome = dados["nome"]
    nacionalidade = dados["nacionalidade"]

    conexao = conectar_dados()
    resultado = conexao.execute(
        """
        UPDATE autores
        SET
            nome = ?,
            nacionalidade = ?
        WHERE id = ?
        """,(nome, nacionalidade, id)
    )

    conexao.commit()
    conexao.close()

    if resultado.rowcount == 0:
        return jsonify({
            "Aviso": "Autor nao encontrado com sucesso"
        }), 404
    return jsonify({
        "Aviso": "to sem ideia morra imediatamente"
    })

#◆ ▬▬▬▬▬▬ ❴✪❵ ▬▬▬▬▬▬ ◆
#     CRUD - DELETE
#◆ ▬▬▬▬▬▬ ❴✪❵ ▬▬▬▬▬▬ ◆

@app.route("/autores/<int:id>", methods=["DELETE"])
def excluir_autor(id):

    conexao = conectar_dados()

    resultado = conexao.execute(
        "DELETE FROM autores WHERE id = ?",
        (id,)
    )

    conexao.commit()

    conexao.close()

    if resultado.rowcount == 0:
        return jsonify({
            "Aviso": "Autor não encontrado morra imediatamente"
        }), 404

    return jsonify({
        "Aviso": "Autor foi mandado para uma ilha remota no leste da africa sem nenhum contato humano"
    })

#■█■█■█■█■█■█■█■█■█■█■█■█■█■
#    CONFIGURAR LIVROS
#■█■█■█■█■█■█■█■█■█■█■█■█■█■

#◆ ▬▬▬▬▬▬ ❴✪❵ ▬▬▬▬▬▬ ◆
#     CRUD - CREATE
#◆ ▬▬▬▬▬▬ ❴✪❵ ▬▬▬▬▬▬ ◆


@app.route("/livros", methods=["POST"])
def cadastrar_livro():
    dados = request.get_json()
    titulo = dados["titulo"]
    ano = dados["ano"]
    #puxar chave primaria no autor
    autorid = dados["autorid"]

    conexao = conectar_dados()

    #conectar a chave do autor
    autor = conexao.execute("""
        SELECT id
        FROM autores
        WHERE id = ?
        """, (autorid,)).fetchone()

    if autor is None:
        conexao.close()

        return jsonify({
           "Aviso": "Autor nao encontrado, certifique-se de que o autor está numa ilha remota no leste da africa",
        }), 404
    #conectou ou nao a chave do autor

    cursor = conexao.execute("""
        INSERT INTO livros
        (titulo, ano, autorid)
        VALUES (?, ?, ?)
    """, (titulo, ano, autorid))

    conexao.commit()

    idlivro=cursor.lastrowid

    conexao.close()

    return jsonify({
        "Aviso": "Um macaco, após infinitas tentativas, conseguiu escrever o seu livro com sucesso após apertar as teclas aleatoriamente",
        "Livro": {
            "id": idlivro,
            "titulo": titulo,
            "ano": ano,
            "autorid": autorid,
        }
    }), 201


@app.route("/pesquisa", methods=["GET"])
def listar_livros():

    conexao = conectar_dados()

    livros = conexao.execute("""
        SELECT
            livros.id,
            livros.titulo,
            livros.ano,
            autores.nome AS autor,
            autores.nacionalidade
        FROM livros
        JOIN autores
        ON livros.autorid = autores.id
        ORDER BY livro.id
    """
    ).fetchall()

    conexao.close()

    return jsonify([
        dict(livro)
        for livro in livros
        ])

if __name__ ==  "__main__":
    criar_tabelas()
    app.run(debug=True)