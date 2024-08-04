# Lexel

Proyecto de evaluación de la calidad del producto y servicio técnico.

## Calidad del producto

Consiste en la depuración para archivos de categoría armónico y de tendencia, cada uno con su propio modo.

## Requisitos previos

Asegúrate de tener instalados los siguientes requisitos:

- Python 3.11
- pip (Gestor de Paquetes de Python)
- virtualenv (Entonrno Virtual) (Opcional, pero recomendado)
- PostgreSQL (Base de Datos) (incluye pgAdmin 4) - [Descargar pgAdmin](https://www.pgadmin.org/download/)

## Instalación

1. **Clona el repositorio en tu máquina local:**

    ```sh
    git clone https://github.com/Levting/Lexel.git
    cd Lexel
    ```

    También puedes usar GitHub Desktop: abre el botón verde de "Código" y selecciona la opción "Abrir con GitHub Desktop" para copiar el enlace.

2. **(Opcional) Crea un entorno virtual para el proyecto:**

    ```sh
    python -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
    ```

3. **Instala las dependencias del proyecto:**

    ```sh
    pip install -r requirements.txt
    ```

## Configuración de PostgreSQL

1. **Crea la base de datos en PostgreSQL:**

    Asegúrate de tener PostgreSQL instalado y funcionando.

    a. Abre pgAdmin 4 y crea una nueva base de datos llamada `lexel`. 

    b. Si es necesario, crea un nuevo usuario y asegúrate de que tenga todos los privilegios sobre la base de datos `lexel`.

2. **Configura la conexión a la base de datos:**

    Dirígete a `lexel/settings.py` y ubica el siguiente bloque de código. Cambia la contraseña de la base de datos por la tuya.

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'lexel',
            'USER': 'postgres',
            'PASSWORD': 'sebas1105',  # Cambia por tu contraseña
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
    ```

3. **Realiza las migraciones:**

    Aplica las migraciones de base de datos para crear las tablas necesarias:

    ```sh
    python manage.py migrate
    ```

## Ejecución

1. **Inicia el servidor de desarrollo:**

    ```sh
    python manage.py runserver
    ```

2. **Accede a la aplicación:**

    Abre tu navegador y visita `http://127.0.0.1:8000/` para ver la aplicación en funcionamiento.

## Archivos Importantes

- **`lexel/settings.py`:** Contiene la configuración del proyecto, incluida la conexión a la base de datos.
- **`requirements.txt`:** Lista de dependencias del proyecto.
- **`Lexcel.excalidraw`:** Es un dibujo del proyecto que contiene el modelo de la base de datos. Para verlo ingresa a `https://excalidraw.com/`.

- **`calidad_producto/models.py`:** Modelos del sistema, se especifica el archivo, categoria, tipo, etc. Relaciones entre si.
- **`calidad_producto/resources/depuracion_armonico.py`:** Contiene los pasos de depuracion, en obtener los valores mayores al 5% para cada modelo de analizador.
- **`calidad_producto/resources/depuracion_tendencia.py`:** Conteiene los pasos de depuración en obtener los porcentajes de desviacion, flicker, desbalance para tipos monofásicos y trifásicos.
