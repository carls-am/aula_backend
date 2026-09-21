from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/curso")
def curso():
    return jsonify({
        "curso": "Engenharia de Software"
    })

@app.route("/aluno")
def aluno():
    return jsonify({
        "aluno": "John Whatsapp"
    })

if __name__ == "__main__":
    app.run(debug=True)
