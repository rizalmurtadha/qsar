from flask import Flask, redirect, url_for, render_template, request, send_from_directory
import qsar_mlr
import createPlot
import os
import pandas
import csv

app = Flask(__name__) 
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

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
                maxModel = count_clmn(destination)
                return render_template("build.html",selected="1", pass_name=destination, maxmodel=maxModel, file_name=file.filename)
        elif gen=="1":
            # Generate model
            destination = request.form['destination']
            csv_destination = destination.replace(".csv","")
            bestModel = request.form['bestModel']
            qsar_mlr.qsar_web(csv_destination,1,bestModel)
            output = readoverview()
            for i in range(int(bestModel)):

                qsar_mlr.qsar_web(csv_destination,2,'model_'+str(i+1))
                csv_pred = "/".join([APP_ROOT,'model_'+str(i+1)+'_pred'])
                createPlot.create(csv_pred,i)
            plotsrc = "/".join([APP_ROOT,'plot_'])
            # return plotsrc
            return render_template("build.html",message="Success",selected="0", output=output, n_model=int(bestModel))
    return render_template("build.html",selected="0", message="",output="-")

@app.route("/predict",methods=["GET", "POST"])
def prediction():
    target = os.path.join(APP_ROOT, 'uploads/')
    
    if request.method=="POST":
        if request.files['fileCsv'].filename == '' :
                return render_template("predict.html",message="Please choose CSV file")
        else:
            fileCsv = request.files["fileCsv"]
            fileModel = request.files["fileModel"]
            csv_destination = "/".join([target,fileCsv.filename])
            modelDestination = "/".join([target,fileModel.filename])
            fileCsv.save(csv_destination)
            fileModel.save(modelDestination)
            csv_destination = csv_destination.replace(".csv","")
            model_Destination = str(fileModel.filename).replace(".p","")
            qsar_mlr.qsar_web(csv_destination,2,model_Destination)
            resultname = (fileModel.filename).replace(".p","_pred.csv")
            return render_template("predict.html",message="Success",name=resultname)
    return render_template("predict.html",messaeg="-")


@app.route('/build/<string:filename>')
def download_filse(filename):
    # return folder
    # try:
    #     response = send_from_directory(os.path.join(APP_ROOT),
    #                                    filename=filename,as_attachment=True)
    #     response.cache_control.max_age = 60  # e.g. 1 minute
    #     return response

    # except:
    #     return str("asd")
    return send_from_directory(os.path.join(APP_ROOT),
                               filename=filename, as_attachment=True)

def readoverview():
    with open("output.txt", "r") as input:
        overview = input.read().split("\n\n\n")
    return overview

def count_clmn(filename):
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            return(len(row))

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

if __name__ == "__main__":
    app.run(debug=True)