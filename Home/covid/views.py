from django.shortcuts import render
from django.urls import include
from django.http import HttpResponse
import pickle, requests, json

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
        
        model_file = {'random':'RF48.pkl', 'decision':'decision48.pkl', 'lr':'LR48.pkl', 'knn':'knn48.pkl'}
        file = open(f'D:\\Internship\\Models\\{model_file[model]}','rb')
        clf = pickle.load(file)
        file.close()

        inputfeatures = [cough, fever, throat, diffBreath]
        infProba = clf.predict([inputfeatures])[0]
        infProba = infProba*100
        print(infProba)
        inf = {"infProba": infProba}
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
    
        