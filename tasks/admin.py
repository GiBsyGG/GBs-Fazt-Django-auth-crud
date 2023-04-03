from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    # Que campos queremos que se muestren en la tabla que sean solo lectura, se coloca en una tupla, por eso la coma al final
    readonly_fields = ('created',)

# Register your models here.
admin.site.register(Task, TaskAdmin)