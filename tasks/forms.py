from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        # Modelo en el cual estará basado el formulario
        model = Task
        # Campos que se mostrarán en el formulario
        fields = ["title", "description", "important"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Título de la tarea"}),
            "description": forms.Textarea(attrs={"class": "form-control", "placeholder": "Descripción de la tarea"}),
            "important": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }