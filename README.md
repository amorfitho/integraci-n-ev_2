# integraci-n-ev_2
repositorio para lo de integracion

# DJANGO_WEB

## ENTORNO VIRTUAL Y LEVANTAR PÁGINA

0. Borrar entorno virtual si es que da problemas:

Abre la terminal y ejecuta (desde la carpeta de tu proyecto):

    Remove-Item -Recurse -Force venv

1. Crear un entorno virtual

Abre la terminal y ejecuta (desde la carpeta de tu proyecto):

    python -m venv venv

Esto creará una carpeta llamada "venv" que contiene el entorno virtual.

2. Activar el entorno virtual

    venv\Scripts\activate

3. Instalar paquetes con pip

Con el entorno activado, instala los paquetes necesarios:

    pip install -r requirements.txt

4. Guardar dependencias en requirements.txt (opcional)(obligatorio si es que se instalan nuevas dependencias a lo largo del proyecto)

Para guardar los paquetes instalados:

    pip freeze > requirements.txt

5. Ejecutar el servicio "python manage.py runserver" en la terminal

## CREACIÓN DE BD

python manage.py makemigrations
python manage.py migrate

## POBLADO DE TABLAS

python manage.py loaddata datos.json

# API_WEBSERVICES

1. Correr app.py
2. Correr config.py
3. Levantar main.py en una terminal aparte de la terminal que levantó la web django.

## PARA VERLA DESDE OTRO PC

1. ython manage.py runserver 0.0.0.0:8000 -> levantar así django web
2. python main.py -> levanta así main.py de api_webservices

Consultas ya no serian así: http://localhost:5000/producto/3, si no que consultas serían de esta nueva forma: http://IPv4:5000/producto/3 (ipconfig)

#ADMIN
<!-- admin
usuario: Admin
contraseña: 9j/&2tR3
correo: fab.gonzaleza@duocuc.cl -->