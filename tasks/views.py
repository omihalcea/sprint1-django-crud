from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.db import IntegrityError
from .forms import FilmForm
from .models import Film


# Create your views here.
def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                # Register a new user
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1']
                )
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                # Return error si l'usuari ja existeix
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Username already exists'
                })
        else:
            return render(request, 'signup.html', {
                'form': UserCreationForm,
                'error': 'Passwords do not match'
            })


def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Username or password is incorrect'
            })
        else:

            login(request, user)
            return redirect('home')
            return HttpResponse('Passwords did not match')


def films(request):
    allfilms = Film.objects.all()
    return render(request, 'films.html', {'films': allfilms})


def add_film(request):
    try:
        if request.method == 'GET':
            return render(request, 'add_film.html', {
                'form': FilmForm
            })
        else:
            form = FilmForm(request.POST)
            form.save()
            return render(request, 'add_film.html', {
                'form': FilmForm
            })
    except ValueError:
        return render(request, 'add_film.html', {
            'form': FilmForm,
            'error': 'Bad data passed in. Try again.'
        })

def film_detail(request, film_id):
    film = get_object_or_404(Film, pk=film_id)
    if request.method == 'GET':
        form = FilmForm(instance=film)
        return render(request, 'film_detail.html', {'film': film, 'form': form})
    else:
        form = FilmForm(request.POST, instance=film)
        if form.is_valid():
            form.save()
            return redirect('film_detail', film_id=film.id)
        return render(request, 'film_detail.html', {'film': film, 'form': form})


def delete_film(request, film_id):
    film = get_object_or_404(Film, pk=film_id)
    if request.method == 'POST':
        film.delete()
        return redirect('films')
