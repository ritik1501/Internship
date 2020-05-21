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
        name = request.POST['name']
        age = int(request.POST['age'])
        fever = float(request.POST['fever'])
        gender = int(request.POST['gender'])
        cough = int(request.POST['cough'])
        throat = int(request.POST['throat'])
        weakness = int(request.POST['weakness'])
        diffBreath = int(request.POST['diffBreath'])
        drowsiness = int(request.POST['drowsiness'])
        pain = int(request.POST['pain'])
        travel = int(request.POST['travel'])
        symptoms = int(request.POST['symptoms'])
        blood = int(request.POST['blood'])
        appetide = int(request.POST['appetide'])
        model = request.POST['model']

        if age>150 or fever<95.0 or fever>105.0:
            messages.error(request, "Please enter valid details.")
            return render(request, 'index.html') 
        
        model_file = {'random':'RF148.pkl', 'decision':'RF148.pickle', 'lr':'LR148.pkl', 'knn':'knn148.pkl'}
        file = open(f'static\\Models\\{model_file[model]}','rb')
        clf = pickle.load(file)
        file.close()

        inputfeatures = [age,gender,fever,cough,throat,weakness,diffBreath,drowsiness,pain,travel,symptoms,blood,appetide]
        info = clf.predict_proba([inputfeatures])
        infProba = info[0][1]+info[0][2]
        infProba = infProba*100
        inf = {"infProba": round(infProba,2)}
        result = clf.predict([inputfeatures])[0]

        obj = LargeData(name=name, age=age, fever=fever, gender=gender, cough=cough, throat=throat, weakness=weakness, diffBreath=diffBreath, drowsiness=drowsiness, pain=pain, travel=travel, symptoms=symptoms, blood=blood, appetide=appetide, result=result)
        obj.save()

        messages.success(request, "Your Result is Generated")
        return render(request, 'show.html', inf)
    return HttpResponse('There is an ERROR!!!!!!!!!!!!!!!!!!!!!!!111')