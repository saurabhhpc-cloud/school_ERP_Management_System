from django import forms

class StudentImportForm(forms.Form):
    file = forms.FileField()
