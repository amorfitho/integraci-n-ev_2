# integraci-n-ev_2
repositorio para lo de integracion

## ENTORNO VIRTUAL Y LEVANTAR PÁGINA

0. Borrar entorno virtual si es que da problemas:

Abre la terminal y ejecuta (desde la carpeta de tu proyecto):

    rmdir /s /q venv

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