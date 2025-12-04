# control_escolar_back
control_escolar_back

Backend Django (API REST)

Proyecto: backend de un sistema de control escolar hecho con Django + Django REST Framework. Este repo contiene únicamente la parte del servidor (API). El frontend (Angular) se conecta a estas rutas para gestionar usuarios y datos: maestros, alumnos, gráficas (endpoints para estadísticas) y admins; cada entidad tiene su CRUD y control de permisos.

Características

API REST para gestión de:

Maestros (CRUD)

Alumnos (CRUD)

Administradores (CRUD / permisos elevados)

Gráficas 

Autenticación y autorización (token / JWT) para proteger rutas.

Paginación, filtros y búsqueda en listados.

CORS configurado para permitir peticiones desde el frontend Angular.

Serializers y validaciones en el backend.

Clona el repo:

git clone <url-del-repo>
cd control_escolar_back

Crea y activa entorno virtual:

python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

Instala dependencias:

pip install -r requirements.txt

Configura variables de entorno (ejemplo .env):

DJANGO_SECRET_KEY="tu_secret_key"
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=postgres://user:pass@localhost:5432/control_escolar_db
CORS_ALLOWED_ORIGINS=http://localhost:4200


Ejecuta migraciones:

python manage.py migrate

Crea superusuario (admin):

python manage.py createsuperuser

Levanta el servidor:

python manage.py runserver

El backend quedará disponible en http://127.0.0.1:8000/.

