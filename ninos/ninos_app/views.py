from django.shortcuts import render,redirect
from django.core.mail import EmailMultiAlternatives
import requests


siteurl = "http://ninos.pythonanywhere.com/"
title = 'Ninos App'
# Create your views here.
def home(request):
    subtitle = ['home','pagina inicial Ninos App']
    user = request.user
    if str(user)=="AnonymousUser":
        return render(request,'index.html',dict(title=title,subtitle = subtitle,view="home.html"))
    else:
        return render(request,'index.html',dict(title=title,subtitle = ["home","bem vindo de volta {}".format(user)],view="home.html"))

def account(request):
    subtitle = ['conta','pagina inicial Ninos App']
    return render(request,'index.html',dict(title=title,view="account.html"))

def confirm(request):
    subs = [['Login','cadastramento de usuário'],['OK','tudo certo!'],['ERRO','ha algo de arrado']]
    erro = None
    url="https://fsfwefdefeeddfcef.herokuapp.com/register"

    if request.method=="POST":
        #pegou o email do user
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        if email!=None and senha==None:
            data = {'email':email}
            try:
                tk = requests.post(url=url,data=data)
            except:
                erro = 'problemas de conexão ao servidor, recarregue a pagina e tente novamente'
                return render(request,'index.html',dict(view='login.html',title=title,subtitle=subs[0],mode="1",email=email,erro = erro))


            turl = siteurl+"confirm?"+tk.text
            htmlEmail =  """<h3>Termine seu cadastro na NinosApp </h3>
            <p>Para terminar seu cadrastro, <a href="{turl}">click aqui</a><p><br/>
            <p><font color="#f00">obs: </font> você tem apenas 10 minutos para realizar seu cadastro, caso nao seja confirmado, acesse {url} e faça esta etapa novamente
            </p><br/>
            <small>Esta é uma menssagem enviada altomaticamente. Por favor não responsa.</small>""".format(url=siteurl,turl=turl)
            sub = "termine seu cadastro na NinosApp"
            text_content = ''
            f ='suport@ninosapp.com'

            try:
                msg = EmailMultiAlternatives(sub,text_content,f, [email])
                msg.attach_alternative(htmlEmail, 'text/html')
                msg.send()
            except:
                erro = 'email invalido!'
                return render(request,'index.html',dict(view='login.html',title=title,subtitle=subs[0],mode="1",erro = erro))


            return render(request,'index.html',dict(view='next.html',title=title,subtitle=subs[1],form={"token":tk.text}))

        else:
            return redirect('home')
    elif request.method=="GET":
        token = request.GET.get('t')
        if token==None:
            return render(request,'index.html',dict(title=title,view='error.html',e=0,erro='ERRO 404'))
        else:
            try:
                url="https://fsfwefdefeeddfcef.herokuapp.com/register"
                tk = requests.post(url=url)
            except:
                return render(request,'index.html',dict(title=title,view='error.html',subtitle=subs[2],e=1,erro='codigo de confirmação inválido'))
    else:
        return redirect('home')


def login(request):
    mode = request.GET.get('mode')
    if not mode==None:
        return render(request,'index.html',dict(view='login.html',title=title,mode=mode))
    else:
        return render(request,'index.html',dict(view='login.html',title=title,mode='1'))

def logout(request):
    return render(request,'index.html',dict(view='login.html',title=title))




