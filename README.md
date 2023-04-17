# Comandos necesarios para el desarrollo

## Instalacion de librerias

``` bash
pip install -r requirements.txt
```

## Migraciones de la BBDD -> Crear archivo de la base de datos o cuando se hagan modificaciones en los modelos

``` bash
python manage.py makemigrations
```

``` bash
python manage.py migrate
```

## Cargar datos en la base de datos

``` bash
python import_db.py
```

## Crear usuario admin para el panel de administrador

``` bash
python manage.py createsuperuser
```
