from django.db.models import *
from django.db import transaction
from control_escolar_desit_api.serializers import *
from control_escolar_desit_api.models import *
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
import json


class MateriasAll(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    # Obtener todas las materias
    def get(self, request, *args, **kwargs):
        materias = Materias.objects.all().order_by("id")
        lista = MateriasSerializer(materias, many=True).data
        return Response(lista, 200)



class MateriasView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    # Obtener materia por ID
    def get(self, request, *args, **kwargs):
        materia_id = request.GET.get("id")
        if materia_id:
            materia = get_object_or_404(Materias, id=materia_id)
            materia_data = MateriasSerializer(materia, many=False).data
            return Response(materia_data, 200)
        else:
            return Response({"error": "ID requerido"}, 400)

    # Registrar nueva materia
    @transaction.atomic
    def post(self, request, *args, **kwargs):

        materia_data = request.data.copy()

        # Convertir dict a JSON string
        if isinstance(materia_data.get("dias"), dict):
            materia_data["dias"] = json.dumps(materia_data["dias"])

        serializer = MateriasSerializer(data=materia_data)

        if serializer.is_valid():

            materia = Materias.objects.create(
                nrc = materia_data["nrc"],
                nombre = materia_data["nombre"],
                seccion = materia_data["seccion"],
                dias = materia_data["dias"],
                hora_inicio = materia_data["hora_inicio"],
                hora_final = materia_data["hora_final"],
                salon = materia_data["salon"],
                programa = materia_data["programa"],
                profesor_id = materia_data["profesor"],
                creditos = materia_data["creditos"],
            )

            return Response({"Materia creada con el ID: ": materia.id}, 201)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    # Actualizar materia
    @transaction.atomic
    def put(self, request, *args, **kwargs):

        materia = get_object_or_404(Materias, id=request.data["id"])

        dias = request.data["dias"]
        if isinstance(dias, dict):
            dias = json.dumps(dias)

        materia.nrc = request.data["nrc"]
        materia.nombre = request.data["nombre"]
        materia.seccion = request.data["seccion"]
        materia.dias = dias
        materia.hora_inicio = request.data["hora_inicio"]
        materia.hora_final = request.data["hora_final"]
        materia.salon = request.data["salon"]
        materia.programa = request.data["programa"]
        materia.profesor_id = request.data["profesor"]
        materia.creditos = request.data["creditos"]

        materia.save()

        return Response(
            {
                "message": "Materia actualizada correctamente",
                "materia": MateriasSerializer(materia).data
            },
            200
        )



    # Eliminar materia
    @transaction.atomic
    def delete(self, request, *args, **kwargs):

        materia = get_object_or_404(Materias, id=request.GET.get("id"))
        try:
            materia.delete()
            return Response({"details": "Materia eliminada"}, 200)

        except Exception:
            return Response({"details": "Algo pasó al eliminar"}, 400)