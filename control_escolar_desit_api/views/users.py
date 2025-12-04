from django.db.models import *
from django.db import transaction
from control_escolar_desit_api.serializers import UserSerializer
from control_escolar_desit_api.serializers import *
from control_escolar_desit_api.models import *
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny

class AdminAll(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        admin = Administradores.objects.filter(user__is_active = 1).order_by("id")
        lista = AdminSerializer(admin, many=True).data
        return Response(lista, 200)


class AdminView(generics.CreateAPIView): 
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        admin = get_object_or_404(Administradores, id = request.GET.get("id"))
        admin = AdminSerializer(admin, many=False).data
        return Response(admin, 200)
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        user = UserSerializer(data=request.data)
        
        if user.is_valid():
            role = request.data['rol']
            first_name = request.data['first_name']
            last_name = request.data['last_name']
            email = request.data['email']
            password = request.data['password']
            
            existing_user = User.objects.filter(email=email).first()
            if existing_user:
                return Response({"message":"Username "+email+", is already taken"},400)

            user = User.objects.create(
                username=email,
                email=email,
                first_name=first_name,
                last_name=last_name,
                is_active=1
            )
            user.save()
            user.set_password(password)
            user.save()

            group, created = Group.objects.get_or_create(name=role)
            group.user_set.add(user)
            group.save()

            admin = Administradores.objects.create(
                user=user,
                clave_admin=request.data["clave_admin"],
                telefono=request.data["telefono"],
                rfc=request.data["rfc"].upper(),
                edad=request.data["edad"],
                ocupacion=request.data["ocupacion"]
            )
            admin.save()

            return Response({"Admin creado con el ID: ": admin.id }, 201)

        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @transaction.atomic
    def put(self, request, *args, **kwargs):
        permission_classes = (permissions.IsAuthenticated,)
        admin = get_object_or_404(Administradores, id=request.data["id"])
        admin.clave_admin = request.data["clave_admin"]
        admin.telefono = request.data["telefono"]
        admin.rfc = request.data["rfc"]
        admin.edad = request.data["edad"]
        admin.ocupacion = request.data["ocupacion"]
        admin.save()
        
        user = admin.user
        user.first_name = request.data["first_name"]
        user.last_name = request.data["last_name"]
        user.save()
        
        return Response({
            "message": "Administrador actualizado correctamente", 
            "admin": AdminSerializer(admin).data
        }, 200)
        
    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        admin = get_object_or_404(Administradores, id=request.GET.get("id"))
        try:
            admin.user.delete()
            return Response({"details":"Administrador eliminado"},200)
        except Exception as e:
            return Response({"details":"Algo pasó al eliminar"},400)



class TotalUsuariosView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request, *args, **kwargs):
        try:
            # Contar administradores activos
            total_admins = Administradores.objects.filter(user__is_active=1).count()
            
            # Contar maestros activos
            total_maestros = Maestros.objects.filter(user__is_active=1).count()
            
            # Contar alumnos activos
            total_alumnos = Alumnos.objects.filter(user__is_active=1).count()
            
            return Response({
                "admins": total_admins,
                "maestros": total_maestros,
                "alumnos": total_alumnos,
                "total": total_admins + total_maestros + total_alumnos
            }, 200)
        except Exception as e:
            return Response({
                "error": str(e),
                "admins": 0,
                "maestros": 0,
                "alumnos": 0,
                "total": 0
            }, 500)