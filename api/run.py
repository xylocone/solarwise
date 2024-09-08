from app import app

"""
Pages
"""


@app.route("/health")
def home():
    return {"status": "ok"}, 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
