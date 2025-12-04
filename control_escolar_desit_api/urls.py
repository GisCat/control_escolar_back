from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views.bootstrap import VersionView
from control_escolar_desit_api.views import users
from control_escolar_desit_api.views import alumnos
from control_escolar_desit_api.views import maestros
from control_escolar_desit_api.views import materias
from control_escolar_desit_api.views import auth
from control_escolar_desit_api.views import bootstrap

urlpatterns = [
    # ADMIN
    path('admin/', users.AdminView.as_view()),
    path('lista-admins/', users.AdminAll.as_view()),
    path('total-usuarios/', users.TotalUsuariosView.as_view()),

    # ALUMNOS
    path('alumnos/', alumnos.AlumnosView.as_view()),
    path('lista-alumnos/', alumnos.AlumnosAll.as_view()),

    # MAESTROS
    path('maestros/', maestros.MaestrosView.as_view()),
    path('lista-maestros/', maestros.MaestrosAll.as_view()),

    # MATERIAS 
    path('materias/', materias.MateriasView.as_view()),          # POST, PUT, DELETE
    path('lista-materias/', materias.MateriasAll.as_view()),     # GET todas

    # LOGIN / LOGOUT
    path('login/', auth.CustomAuthToken.as_view()),
    path('logout/', auth.Logout.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
