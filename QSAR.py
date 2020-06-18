from flask import Flask, redirect, url_for, render_template, request, send_from_directory
import qsar_mlr
import os
import pandas
import csv

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/build",methods=["GET", "POST"])
def build():
    target = os.path.join(APP_ROOT, 'uploads/')
    
    if request.method=="POST":
        gen=gen=request.form['generate']
        if gen=="0" :
            try:
                getfile = request.files['file']
            except:
                return render_template("build.html",selected="0", message="",output="-")

            if request.files['file'].filename == '' :
                return render_template("build.html",message="Please choose CSV file")
            else:
                file = request.files["file"]
                destination = "/".join([target,file.filename])
                file.save(destination)
                maxModel = count_clmn(file.filename)
                return render_template("build.html",selected="1", pass_name=destination, maxmodel=maxModel, file_name=file.filename)
        elif gen=="1":
            # Generate model
            destination = request.form['destination']
            csv_destination = destination.replace(".csv","")
            bestModel = request.form['bestModel']
            qsar_mlr.qsar_web(csv_destination,1,bestModel)
            output = open("output.txt", "r")
            return render_template("build.html",message="Success",selected="0", output=output.read())
    return render_template("build.html",selected="0", message="",output="-")

@app.route('/build/<string:filename>')
def download_filse(filename):
    # return folder
    return send_from_directory(os.path.join(APP_ROOT),
                               filename=filename, as_attachment=True)

def count_clmn(filename):
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            return(len(row))



if __name__ == "__main__":
    app.run(debug=True)