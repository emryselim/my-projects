from flask import Flask

app = Flask(__name__)

@app.route("/")
def head():
    return "Hello Selimalp"

@app.route("/second")
def second():
    return "This is my second page"

@app.route("/third/subthird")
def third():
    return "<h2>This is the subpath of third page</h2>"

if __name__ == "__main__":
    app.run(debug=True)