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
import json

class MaestrosAll(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    #  GET para obtener todos los maestros
    def get(self, request, *args, **kwargs):
        maestros = Maestros.objects.filter(user__is_active=1).order_by("id")
        lista = MaestroSerializer(maestros, many=True).data
        for maestro in lista:
            if isinstance(maestro, dict) and "materias_json" in maestro:
                try:
                    maestro["materias_json"] = json.loads(maestro["materias_json"])
                except:
                    maestro["materias_json"] = []

        return Response(lista, 200)



class MaestrosView(generics.CreateAPIView):
    #Obtener maestro por ID
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        maestro = get_object_or_404(Maestros, id=request.GET.get("id"))
        maestro_data = MaestroSerializer(maestro, many=False).data
        # Convertir materias_json (string) a array
        if "materias_json" in maestro_data:
            try:
                maestro_data["materias_json"] = json.loads(maestro_data["materias_json"])
            except:
                maestro_data["materias_json"] = []
        return Response(maestro_data, 200)



    #Registrar nuevo  maestro
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
            user.save()

            # CORRECCIÓN: siempre convertir a json.dumps
            materias = request.data["materias_json"]

            maestro = Maestros.objects.create(
                user=user,
                id_trabajador=request.data["id_trabajador"],
                fecha_nacimiento=request.data["fecha_nacimiento"],
                telefono=request.data["telefono"],
                rfc=request.data["rfc"].upper(),
                cubiculo=request.data["cubiculo"],
                area_investigacion=request.data["area_investigacion"],
                materias_json=json.dumps(materias)
            )
            maestro.save()

            return Response({"maestro_created_id": maestro.id }, 201)

        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)



    # Actualizar datos del maestro
    @transaction.atomic
    def put(self, request, *args, **kwargs):
        permission_classes = (permissions.IsAuthenticated,)
        maestro = get_object_or_404(Maestros, id=request.data["id"])

        maestro.id_trabajador = request.data.get("id_trabajador", maestro.id_trabajador)
        maestro.fecha_nacimiento = request.data.get("fecha_nacimiento", maestro.fecha_nacimiento)
        maestro.telefono = request.data.get("telefono", maestro.telefono)
        maestro.rfc = request.data.get("rfc", maestro.rfc).upper()
        maestro.cubiculo = request.data.get("cubiculo", maestro.cubiculo)
        maestro.area_investigacion = request.data.get("area_investigacion", maestro.area_investigacion)
        materias = request.data.get("materias_json", [])

        if isinstance(materias, str):
            try:
                materias = json.loads(materias)
            except:
                materias = []
        maestro.materias_json = json.dumps(materias)
        maestro.save()

        user = maestro.user
        user.first_name = request.data.get("first_name", user.first_name)
        user.last_name = request.data.get("last_name", user.last_name)
        user.email = request.data.get("email", user.email)
        user.save()

        return Response({
            "message": "Maestro actualizado correctamente",
            "maestro": MaestroSerializer(maestro).data
        }, 200)
    
    
    # Eliminar maestro
    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        maestro = get_object_or_404(Maestros, id=request.GET.get("id"))
        try:
            maestro.user.delete() # Esto eliminará también el maestro por la relación OneToOne
            return Response({"details":"Maestro eliminado"},200)
        except Exception as e:
            return Response({"details":"Algo pasó al eliminar"},400)