from django.shortcuts import render
from django.urls import include
from django.contrib import messages
from django.http import HttpResponse
import pickle, requests, json
from covid.models import UserData, LargeData

# Create your views here.
def home(request):
    return render(request, 'index.html')

def test(request):
    if request.method=='POST':
        name = request.POST['name']
        fever = int(request.POST['fever'])
        cough = int(request.POST['cough'])
        throat = int(request.POST['throat'])
        diffBreath = int(request.POST['diffBreath'])
        model = request.POST['model']   

        if fever<0 or fever>20 or cough<0 or cough>20 or throat<0 or throat>20 or diffBreath<0 or diffBreath>20:
            messages.error(request, "Please enter the deatils between 1 to 20.")
            return render(request, 'index.html')  
        
        model_file = {'random':'RF48.pkl', 'decision':'decision48.pickle', 'lr':'LR48.pkl', 'knn':'knn48.pkl'}
        file = open(f'static\\Models\\{model_file[model]}','rb')
        clf = pickle.load(file)
        file.close()

        inputfeatures = [cough, fever, throat, diffBreath]
        infProba = clf.predict_proba([inputfeatures])[0][1]
        infProba = infProba*100
        inf = {"infProba": round(infProba, 2)}
        result = clf.predict([inputfeatures])[0]
        obj = UserData(name=name, fever=fever, cough=cough, throat=throat, breathing=diffBreath, result=result)
        obj.save()

        messages.success(request, "Your Result is Generated")
        return render(request, 'show.html', inf)
    return HttpResponse("There is an ERROR!!!!!!!!!!!!!")

def dashboard(request):
    url = "https://covid19.mathdro.id/api/"
    text = getdata(url)

    wConfirmed = text['confirmed']['value']
    wRecovered = text['recovered']['value']
    wDeath = text['deaths']['value']
    wActive = wConfirmed-wRecovered-wDeath
    lastUpdate = text['lastUpdate']
    params = {'confirmed':wConfirmed, 'recovered':wRecovered, 'death':wDeath, 'active':wActive, 'lastUpdate':lastUpdate}
    return render(request, 'dashboard.html', params)

def getdata(url):
    r= requests.get(url)
    return json.loads(r.text)

def search(request):
    if request.method=='POST':
        url = "https://covid19.mathdro.id/api/"
        text = getdata(url)

        wConfirmed = text['confirmed']['value']
        wRecovered = text['recovered']['value']
        wDeath = text['deaths']['value']
        wActive = wConfirmed-wRecovered-wDeath
        lastUpdate = text['lastUpdate']

        state = request.POST['search']
        url1 = f"https://covid19.mathdro.id/api/countries/{state}"
        data = getdata(url1)

        sConfirmed = data['confirmed']['value']
        sRecovered = data['recovered']['value']
        sDeath = data['deaths']['value']
        sActive = sConfirmed-sRecovered-sDeath

        params = {'confirmed':wConfirmed, 'recovered':wRecovered, 'death':wDeath, 'active':wActive, 'sconfirmed': sConfirmed, 'srecovered':sRecovered, 'sdeath':sDeath, 'sactive':sActive, 'state':state.upper(), 'lastUpdate':lastUpdate[:10]}
        return render(request, 'search.html', params)
    return HttpResponse("There is an ERROR!!!!!!!!!!")

def form(request):
    return render(request, 'form.html')

def formTest(request):
    if request.method=='POST':
        box = {'cough':0, 'throat':0, 'weakness':0, 'diffBreath':0, 'drowsiness':0, 'pain':0, 'blood':0, 'appetide':0}
        name = request.POST['name']
        fever = float(request.POST['fever'])
        age = int(request.POST['age'])
        gender = int(request.POST['gender'])
        travel = int(request.POST['travel'])
        symptoms = int(request.POST['symptoms'])
        model = request.POST['model']
       
        checkb = request.POST.getlist('checks[]')
        if not len(checkb)==0:
            for i in checkb:
                box[i]=1
                print(box[i])

        model_file = {'random':'RF148.pkl', 'decision':'des_symptoms.pickle', 'lr':'LR148.pkl', 'knn':'knn148.pkl'}
        file = open(f'static\\Models\\{model_file[model]}','rb')
        clf = pickle.load(file)
        file.close()

        inputfeatures = [age,gender,fever,box['cough'],box['throat'],box['weakness'],box['diffBreath'],box['drowsiness'],box['pain'],travel,symptoms,box['blood'],box['appetide']]
        info = clf.predict_proba([inputfeatures])
        infProba = info[0][1]+info[0][2]
        infProba = infProba*100
        inf = {"infProba": round(infProba,2)}
        result = clf.predict([inputfeatures])[0]

        obj = LargeData(name=name, age=age, fever=fever, gender=gender, cough=box['cough'], throat=box['throat'], weakness=box['weakness'], diffBreath=box['diffBreath'], drowsiness=box['drowsiness'], pain=box['pain'], travel=travel, symptoms=symptoms, blood=box['blood'], appetide=box['appetide'], result=result)
        obj.save()

        if int(infProba)>80:
            messages.error(request, "You are at high risk")
        elif int(infProba)>60 or int(infProba)<81:
            messages.warning(request, "You are at low risk")
        else:
            messages.success(request, "Your Result is Generated")
        return render(request, 'show.html', inf)
    return render(request, 'error.html')
        

