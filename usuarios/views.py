from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib.auth import authenticate, login

def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    else:
        primeiro_nome = request.POST.get('primeiro_nome')
        sobrenome = request.POST.get('sobrenome')
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')
        email = request.POST.get('email')
        
        if senha != confirmar_senha:
            messages.add_message(request, constants.ERROR, 'As senhas não são iguais')
            return redirect('/usuarios/cadastro')
        
        if len(senha) < 6 :
            messages.add_message(request, constants.ERROR, 'A senha deve ter no mínimo 6 caracteres')
            return redirect('/usuarios/cadastro')

        try:
            user = User.objects.create_user(
                first_name=primeiro_nome,
                last_name=sobrenome,
                username=username,
                email=email,
                password=senha,
            )
            messages.add_message(request, constants.SUCCESS, 'Usuário cadastrado com sucesso')
        except:
            messages.add_message(request, constants.ERROR, '500')
            return redirect('/usuarios/cadastro')
        
        return redirect('/usuarios/cadastro')
    
    
def logar(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        
        user = authenticate(username=username, password=senha)
        
        if user:
            login(request, user)
            return redirect('/')
        else:
            messages.add_message(request, constants.ERROR, 'Usuario ou senha invalidos')
            return redirect('/usuarios/login')
            
            
            
            
            
            
            
            
            
            
            
            