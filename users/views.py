from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth import get_user_model

Users = get_user_model()

def login_view(request, user_id):
    
    authenticated_user = authenticate(request, user_id_tg=user_id)
    
    if authenticated_user is not None:
        login(request, authenticated_user)
        return redirect('main:main')
    
    return render(request, 'users/load.html', {'error_message': 'Пользователь не найден или аутентификация не удалась.'})