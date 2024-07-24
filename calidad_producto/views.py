import pytz
import pandas as pd
from django.contrib import messages
from .models import Archivo, ArchivoInfo
from babel.dates import format_datetime
from django.shortcuts import render, redirect, get_object_or_404
from .lectura_armonico import leer_archivo, seleccionar_filas_columnas, ajustar_encabezado, contar_valores_mayores, calcular_porcentaje_valores_mayores

from django.db import DatabaseError
from pandas.errors import EmptyDataError


def index(request):
    return render(request, 'calidad_producto/index.html')


def vista_armonicos(request):

    # Obtener todos los archivos desde la base de datos mediante la fecha ascendentemente
    archivos_armonicos = Archivo.objects.all().order_by('subido_el')

    # Configurar la zona horaria
    tz = pytz.timezone('America/Guayaquil')

    # Todos los archivos inician con un "/archivo " y la fecha esta en ingles, se crea una lista de diccionarios con toda la información de cada archivo
    archivos_con_nombres_modificados = [
        {
            'id': archivo.id,
            'archivo': archivo.archivo.name.split('/')[-1],
            # 'subido_el': archivo.subido_el
            'subido_el': format_datetime(archivo.subido_el.astimezone(tz), format='dd MMMM yyyy, hh:mm a', locale='es_ES')
        }
        for archivo in archivos_armonicos
    ]

    # Renderizamos los nombres formateados en la vista de "armonicos.html" pasándolos por parámetro
    return render(request, 'armonicos/armonicos.html', {'archivos': archivos_con_nombres_modificados})


def vista_armonico_detalle(request, archivo_id):
    # Obtener el archivo evitando que el servidor colapse
    archivo = get_object_or_404(Archivo, id=archivo_id)

    # Mostrar solamente el nombre del archivo, sin el "archivo/" al inicio
    nombre_archivo = archivo.archivo.url.split('/')[-1]
    print("Nombre del Archivo Seleccionado: ", nombre_archivo)

    # Obtener la información del archivo
    archivo_info_obj = archivo.info.first()
    print("Archivo Info Objeto: ", archivo_info_obj)
    archivo_info = archivo_info_obj.data if archivo_info_obj else {}

    print("Información del archivo seleccionado: ", archivo_info)

    return render(request, 'armonicos/armonico_detalle.html', {'nombre_archivo': nombre_archivo, 'archivo_info': archivo_info})


def vista_tendencia(request):
    # Renderizar a tendencias.html
    return render(request, 'tendencias/tendencias.html')


def vista_crear_armonico(request):
    return render(request, 'armonicos/crear_armonico.html')


def crear_armonico_unico(request):
    # Si la solicitud es POST, procesar el formulario
    if request.method == 'POST':

        # Obtener el archivo de la solicitud
        if 'archivo_unico' in request.FILES:

            # Obtener el archivo de la solicitud
            archivo_unico = request.FILES['archivo_unico']

            # Crear un nuevo objeto de archivo y guardarlo en la base de datos
            nuevo_archivo = Archivo(archivo=archivo_unico)

            # Guardar el archivo en la base de datos
            nuevo_archivo.save()

            try:
                # Guardar el archivo en la base de datos, procesa el archivo y muestra un mensaje de éxito
                procesar_archivo_armonico(nuevo_archivo)
                messages.success(request, 'Archivo procesado correctamente.')
                return redirect('vista_armonicos')

            except (ValueError, EmptyDataError) as e:
                # Mostrar un mensaje de error si ocurre un error al procesar el archivo eliminando el archivo de la base de datos
                messages.error(
                    request, f'Ocurrió un error al procesar el archivo: {e}')
                nuevo_archivo.delete()

            except DatabaseError as e:
                # Mostrar un mensaje de error si ocurre un error en la base de datos eliminando el archivo de la base de datos
                messages.error(request, f'Error de base de datos: {e}')
                nuevo_archivo.delete()

            except Exception as e:
                # Mostrar un mensaje de error si ocurre un error inesperado eliminando el archivo de la base de datos
                messages.error(request, f'Error inesperado: {e}')
                nuevo_archivo.delete()

        else:
            # Mostrar un mensaje de error si no se encuentra el archivo en la solicitud
            messages.error(request, 'Por favor, seleccione un archivo .xlsx.')

    # Renderizar la vista de crear armonico
    return render(request, 'armonicos/crear_armonico.html')


def crear_armonico_lote(request):

    # Si la solicitud es POST, procesar el formulario
    if request.method == 'POST':

        # Obtener los archivos de la solicitud
        if 'archivos_lote' in request.FILES:

            # De la solicitud, obtener los archivos
            archivos = request.FILES.getlist('archivos_lote')

            # Para cada archivo en la lista de archivos
            for archivo in archivos:

                # Crear un nuevo archivo a partir del archivo actual
                nuevo_archivo = Archivo(archivo=archivo)

                # Guardar el archivo en la base de datos
                nuevo_archivo.save()

                try:
                    # Procesar el archivo y mostrar un mensaje de éxito
                    procesar_archivo_armonico(nuevo_archivo)
                    messages.success(
                        request, f'Archivo {archivo.name} procesado correctamente.')

                except (ValueError, EmptyDataError) as e:
                    # Mostrar un mensaje de error si ocurre un error al procesar el archivo eliminando el archivo de la base de datos
                    messages.error(
                        request, f'Ocurrió un error al procesar el archivo {archivo.name}: {e}')
                    nuevo_archivo.delete()

                except DatabaseError as e:
                    # Mostrar un mensaje de error si ocurre un error en la base de datos eliminando el archivo de la base de datos
                    messages.error(request, f'Error de base de datos: {e}')
                    nuevo_archivo.delete()

                except Exception as e:
                    # Mostrar un mensaje de error si ocurre un error inesperado eliminando el archivo de la base de datos
                    messages.error(
                        request, f'Error inesperado al procesar el archivo {archivo.name}: {e}')
                    nuevo_archivo.delete()
            
        # Redirigir a la página de armonicos
        return redirect('vista_armonicos')

    else:
        # Mostrar un mensaje de error si el formulario no es válido
        messages.error(request, 'Error al procesar el formulario.')

    # Renderizar la vista de crear armonico
    return render(request, 'armonicos/crear_armonico.html')


def eliminar_armonico(request, archivo_id):
    # Obtener el archivo evitando que el servidor colapse
    archivo = get_object_or_404(Archivo, id=archivo_id)

    if request.method == 'POST':
        # Eliminar el archivo
        archivo.delete()

        # Mostrar un mensaje de éxito
        messages.success(request, 'Archivo eliminado correctamente.')

        # Redirigir a la página de armonicos
        return redirect('vista_armonicos')


def procesar_archivo_armonico(archivo_excel):
    # Leer el archivo cargado
    df = leer_archivo(archivo_excel.archivo.path)

    # Controlamos la lectura del archivo, para que sea correcta.
    if df is None:
        raise ValueError("No se pudo leer el archivo.")

    # print(df.to_string(index=False))

    # print("DataFrame Original:")
    # print(df)

    # SELECCIONAR LAS FILAS Y COLUMNAS NECESARIAS
    filas = slice(11, -1)
    columnas = slice(10, None)
    df_seleccionado = seleccionar_filas_columnas(df, filas, columnas)

    # print("\nDataFrame Seleccionado:")
    # print(df_seleccionado)

    df_seleccionado = ajustar_encabezado(df_seleccionado)

    # Convertir los datos a tipo numérico y llenar NaN con 0
    df_seleccionado = df_seleccionado.apply(
        pd.to_numeric, errors='coerce').fillna(0)

    # print("\nDataFrame Seleccionado con Encabezado Ajustado sin índices:")
    # print(df_seleccionado)

    valores_mayores = contar_valores_mayores(df_seleccionado, 5)

    print("\nValores mayores a 5 por columna:")
    print(valores_mayores)

    total_filas = df_seleccionado.shape[0]  # Número total de filas
    porcentaje_valores_mayores = calcular_porcentaje_valores_mayores(
        valores_mayores, total_filas)

    print("\nPorcentaje de valores mayores a 5 por columna:")
    print(porcentaje_valores_mayores)

    # Crear un diccionario con los datos de las columnas, asegurándose de convertir a tipos nativos de Python
    data = {
        columna: {
            # Convertir a int
            'conteo': int(valores_mayores[columna]),
            # Convertir a float
            'porcentaje': float(porcentaje_valores_mayores[columna].round(5))
        }
        for columna in df_seleccionado.columns
    }

    # print("\nData: ", data)

    # Crear un objeto ArchivoInfo con la información del archivo
    ArchivoInfo.objects.create(
        archivo=archivo_excel,
        data=data
    )
