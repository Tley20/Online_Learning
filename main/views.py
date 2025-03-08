from django.shortcuts import render,get_object_or_404,redirect
from .models import Course
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import Profile

def index(request):
    courses = Course.objects.all()
    return render(request, 'main/index.html', {'courses': courses})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'main/course_detail.html',{'course': course})

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("index")
    return render(request, "main/login.html")

def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 != password2:
            messages.error(request, "Пароли не совпадают!")
            return render(request, "main/register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Такой пользователь уже существует!")
            return render(request, "main/register.html")

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        login(request, user)  # Автоматический вход после регистрации
        return redirect("index")  # Перенаправляем на главную страницу

    return render(request, "main/register.html")


def logout_view(request):
    logout(request)
    return redirect("index")

@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, "main/profile.html", {"profile": profile})

@login_required
def edit_profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "main/edit_profile.html", {"form": form})


def homepage(request):
    courses = Course.objects.all()[:3]
    return render(request, "main/home.html", {"courses": courses})

from django.http import JsonResponse

def course_list_api(request):
    courses = Course.objects.all().values('id', 'title', 'description')
    return JsonResponse(list(courses), safe=False)
