from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=200)
    # TextField es un campo de texto largo, y blank=True es para que no sea obligatorio, si no se pasa nada, se guarda como un string vacio
    description = models.TextField(blank=True)
    # auto_now_add=True, cuando se crea el objeto, se guarda la fecha actual si no se pasa ese dato
    created = models.DateTimeField(auto_now_add=True)
    # null=True, es un campo vacio inicialmente
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    # on_delete=models.CASCADE, si se borra el usuario, se borran las tareas asociadas a ese usuario, importante esto
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + " - by " + str(self.user.username)