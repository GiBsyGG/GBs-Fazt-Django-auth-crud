from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import Task


from .forms import TaskForm

# Create your views here.
def home(request):
    # pasamos el contexto lo que devuelve el UserCreationForm, sin parentesis xd
    return render(request, "tasks/home.html")


def signup(request):
    
    # Si el request es GET, renderizamos el formulario de registro
    if request.method == "GET":
        return render(request, "tasks/signup.html", {
        "form": UserCreationForm,
            })
    
    # Si el request es POST, creamos el usuario, pero antes verificamos las contraseñas
    else:
        if request.POST["password1"] == request.POST["password2"]:
            #probamos que no falle en peticioes
            try:
                # Si el formulario es valido, creamos el usuario, espera usuario y contraseña
                user = User.objects.create_user(username=request.POST["username"], password=request.POST["password1"]);
                # Lo guardamos en la DB 
                user.save()

                # Logueamos al usuario, creando la cookie de session
                login(request, user)

                #si todo sale bien despues de guardar el usuario, redirigimos a la pagina de tasks
                return redirect("tasks")
            except IntegrityError:
                return render(request, "tasks/signup.html", {
                    "form": UserCreationForm,
                    "error": "El nombre de usuario ya existe"})
        else:
            return render(request, "tasks/signup.html", {
                    "form": UserCreationForm,
                    "error": "No coinciden las contraseñas"})


@login_required
def tasks(request):
    # Consultaremos las tareas en la DB, pero solo las del usuario que está logueado  y las no completadas
    Tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, "tasks/tasks.html", {
        "tasks": Tasks
    })


@login_required
def create_task(request):

    if request.method == "GET":
        return render(request, "tasks/create_task.html", {
            "form": TaskForm,
            })
    else:
        try:
            # Esto generará un formulario con los datos que nos llegan del POST, para guardarlo en la DB, es otra forma de hacerlo a parte de con el modelo
            form = TaskForm(request.POST)
            # Guardarmeos los datos como una tarea nueva, el commit=False es para que no se guarde esto como instancia en la DB, esto se hará luego
            new_task = form.save(commit=False)

            # Asignamos el usuario que ha creado la tarea
            new_task.user = request.user

            # Ahora si guardamos la tarea en la DB
            new_task.save()

            # Redirigimos a la pagina de tasks
            return redirect("tasks")
        except ValueError:
            return render(request, "tasks/create_task.html", {
                "form": TaskForm,
                "error": "provee datos validos"
                })


@login_required
def task_detail(request, task_id):
    if request.method == "GET":
        # Traemos la tarea de la DB con su id y con el usuario logueado
        task = get_object_or_404(Task, pk=task_id, user=request.user)

        #Crearemos un form para editar la tarea, pero usaremos el ya creado por nosotros antes
        form = TaskForm(instance=task)

        return render(request, "tasks/task_detail.html", {
            "task": task,
            "form": form
        })
    else:
        try:
            # Si el request es POST, actualizaremos la tarea con los datos que nos mandaron
            task = get_object_or_404(Task, pk=task_id, user=request.user)

            # Creamos un form con los datos que nos llegan del POST para guardar un dato nuevo
            form = TaskForm(request.POST, instance=task)

            # Actualizamos la tarea
            form.save()
            return redirect("tasks")
        except ValueError:
            return render(request, "tasks/task_detail.html", {
                "task": task,
                "form": form,
                "error": "Datos invalidos"
            })


@login_required
def tasks_completed(request):
    # Consultaremos las tareas en la DB, pero solo las del usuario que está logueado  y las completadas, ordenadas de la mas ultima a la menor
    Tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, "tasks/tasks.html", {
        "tasks": Tasks
    })


@login_required
def complete_task(request, task_id):
    # Traemos la tarea de la DB con su id y con el usuario logueado
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        # Actualizamos la tarea con la fecha actual en el datecompleted
        task.datecompleted = timezone.now()
        # Guardamos la tarea en la DB
        task.save()
        return redirect("tasks")


@login_required
def delete_task(request, task_id):
    # Traemos la tarea de la DB con su id y con el usuario logueado
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        # Eliminamos la tarea de la DB
        task.delete()
        return redirect("tasks")
    

@login_required
def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == "GET":
        return render(request, "tasks/signin.html", {
        "form": AuthenticationForm
            })
    else:
        # Si me llega un POST, verificamos el login con el metodo authenticate, si es valido devuelve el usuario, si no el usuario es None
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])

        # Comprobamos si el usuario está vacio
        if user is None:
            return render(request, "tasks/signin.html", {
                "form": AuthenticationForm,
                "error": "El usuario o la contraseña no son correctos"
                })
        else:
            # Si el usuario no es None, lo logueamos y le redirigimos a la pagina de tasks
            login(request, user)
            return redirect("tasks")