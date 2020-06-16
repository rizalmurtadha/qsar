from flask import Flask, redirect, url_for, render_template, request, send_from_directory
import qsar_mlr
import os

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/build",methods=["GET", "POST"])
def build():
    target = os.path.join(APP_ROOT, 'uploads/')
    if request.method=="POST":
        if request.files['file'].filename == '':
            return render_template("build.html",message="Please choose CSV file")
        else:
            file = request.files["file"]
            destination = "/".join([target,file.filename])
            file.save(destination)
            csv_destination = destination.replace(".csv","")
            # return csv_destination
            qsar_mlr.qsar_web(csv_destination,1,1)
            output = open("output.txt", "r")
            return render_template("build.html",message="Success", output=output.read())
            # return output.read().replace("\n", "<br>")
    return render_template("build.html",message="",output="-")

@app.route('/build/<string:filename>')
def download_filse(filename):
    # return folder
    return send_from_directory(os.path.join(APP_ROOT),
                               filename=filename, as_attachment=True)
if __name__ == "__main__":
    app.run(debug=True)