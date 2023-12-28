from flask import Flask, render_template, request
from testersearchfunction import InvertedIndex
from addnewfile import AddNewFile

app = Flask(__name__)
invertedIndex = InvertedIndex()
add_new_file = AddNewFile()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query_str = request.form["query"]
        query_words = query_str.split()  # Split query into words

        if len(query_words) == 1:
            # Single-word query
            results = invertedIndex.searchSingleWord(query_str)
        else:
            # Multi-word query
            results = invertedIndex.searchMultiWord(query_str)

        return render_template("index.html", query=query_str, results=results)
    
    return render_template("index.html", query="", results=[])
@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        uploaded_file = request.files["file"]
        if uploaded_file.filename != "":
            # Save the uploaded file to a temporary location
            temp_path = f"{uploaded_file.filename}"
            uploaded_file.save(temp_path)

            # Call the addFileToForwardIndex function with the uploaded file
            add_new_file.addFileToForwardIndex(temp_path)

    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True)

