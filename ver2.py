from flask import Flask

app = Flask(__name__)


@app.route("/")
def start():
    return "<h1>Inicio do projeto</h1>"



@app.route("/aluno/<nome>")
def aluno(nome):
    return f"Aluno: {nome}"

if __name__ == "__main__":
    app.run(debug=True)
