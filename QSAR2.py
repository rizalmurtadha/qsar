from flask import Flask, redirect, url_for, render_template, request
import os

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def home():
    return render_template("index2.html")

@app.route("/build",methods=["GET", "POST"])
def build():
    target = os.path.join(APP_ROOT, 'uploads/')
    if request.method=="POST":
        if request.files['file'].filename == '':
            return render_template("build2.html",message="Please choose CSV file")
        else:
            file = request.files["file"]
            destination = "/".join([target,file.filename])
            file.save(destination)
            return render_template("build2.html",message="Success")
    return render_template("build2.html",message="")

if __name__ == "__main__":
    app.run(debug=True)