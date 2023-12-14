from flask import Flask, render_template, request
from testersearchfunction import InvertedIndex

app = Flask(__name__)
invertedIndex = InvertedIndex()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query_str = request.form["query"]
        results = invertedIndex.searchSingleWord(query_str)
        return render_template("index.html", query=query_str, results=results)
    return render_template("index.html", query="", results=[])

if __name__ == "__main__":
    app.run(debug=True)
