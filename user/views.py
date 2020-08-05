from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from requests import get
from bs4 import BeautifulSoup
from .models import schedule1


def index(request):
    #upcoming rounds
    url1="https://codeforces.com/contests"
    response1=get(url1)
    upcoming_rounds=BeautifulSoup(response1.text,'html.parser')
    rounds=upcoming_rounds.find("div",class_="datatable")
    r=rounds.find_all("tr")
    r=r[1:]
    #print(r)
    ls1=[]
    for i in r:
        cnt={}
        cnt["name"]=i.find("td").string[2:-6]
        cnt["time"]=i.find("span").string
        cnt["duration"]=i.find_all("td")[3].string[10:-6]
        ls1.append(cnt)
    for i in ls1:
        schedule1.objects.create(name=i['name'], time=i['time'], duration=i['duration'])

    return render(request, 'user/index.html', {'title': 'index'})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            htmly = get_template('user/email.html')
            d = {'username': username}
            subject, from_email, to = 'welcome', 'nishtha.idr@gmail.com', email
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            ##################################################################
            messages.success(request, f'Your account has been created ! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form': form, 'title': 'register here'})


def login1(request):
    if request.method == 'POST':

        # AuthenticationForm_can_also_be_used__

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            form = login(request, user)
            messages.success(request, f' welcome {username} !!')
            return redirect('index')
        else:
            messages.info(request, f'account done not exit plz sign in')
    form = AuthenticationForm()
    return render(request, 'user/login.html', {'form': form, 'title': 'log in'})
