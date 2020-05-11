from flask import Flask, render_template, request
import pickle
app = Flask(__name__)

file = open('Models\\model.pkl','rb')
clf = pickle.load(file)
file.close()

@app.route('/', methods=['GET','POST'])
def hello_world():
    
    if request.method=='POST':
        myDict = request.form
        fever = float(myDict['fever'])
        age = int(myDict['age'])
        pain = int(myDict['pain'])
        runnyNose = int(myDict['runnyNose'])
        diffBreath = int(myDict['diffBreath'])
        
        inputfeatures = [fever, pain, age, runnyNose, diffBreath]
        infProba = clf.predict_proba([inputfeatures])[0][1]
        infProba = infProba*100
        print(infProba)
        return render_template('show.html', inf=infProba)
    return render_template('index.html')
    # return 'Hello World' +str(infProba)


if __name__ == "__main__":
    app.run(debug=True)