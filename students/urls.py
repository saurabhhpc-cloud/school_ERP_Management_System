from django.urls import path
from .views import import_students_excel
from . import views

app_name = "students"
urlpatterns = [
    path("", views.student_list, name="list"),
    path("import/", views.import_students_excel, name="import_students"),
   
  
]
