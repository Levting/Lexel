import pytz
import locale
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ArchivoForm
from .models import Archivo, ArchivoInfo
import pandas as pd
from .lectura_armonico import leer_archivo, seleccionar_filas_columnas, ajustar_encabezado, contar_valores_mayores, calcular_porcentaje_valores_mayores
from django.contrib import messages

from django.db import DatabaseError
from pandas.errors import EmptyDataError

from babel.dates import format_datetime


def inicio(request):  # /calidad_producto
    return render(request, 'calidad_producto.html')


def vista_armonicos(request):

    # Obtener todos los archivos desde la base de datos mediante la fecha ascendetemente
    archivos_armonicos = Archivo.objects.all().order_by('subido_el')

    # Configurar la zona horaria
    tz = pytz.timezone('America/Guayaquil')

    # Todos los archivos inician con un "/archivo " y la fecha esta en ingles, se crea una lista de diccionarios con toda la información de cada archivo
    archivos_con_nombres_modificados = [
        {
            'id': archivo.id,
            'archivo': archivo.archivo.name.split('/')[-1],
            'subido_el': format_datetime(archivo.subido_el.astimezone(tz), format='dd MMMM yyyy, hh:mm a', locale='es_ES')
        }
        for archivo in archivos_armonicos
    ]

    # Renderizamos los nombres formateados en la vista de "armonicos.html" pasándolos por parámetro
    return render(request, 'armonicos/armonicos.html', {'archivos': archivos_con_nombres_modificados})


def vista_armonico_detalle(request, archivo_id):
    # archivo = Archivo.objects.get(id=archivo_id)
    archivo = get_object_or_404(Archivo, id=archivo_id)

    # Mostrar solamente el nombre del archivo, sin el "archivo/" al inicio
    nombre_archivo = archivo.archivo.url.split('/')[-1]
    print("Nombre del Archivo Seleccionado: ", nombre_archivo)

    archivo_info = archivo.info.all()
    print(archivo_info.values())

    return render(request, 'armonicos/armonico_detalle.html', {'nombre_archivo': nombre_archivo, 'archivo_info': archivo_info})


def vista_tendencia(request):
    return render(request, 'tendencias/tendencias.html')


def crear_armonico(request):
    if request.method == 'POST':
        # Crear un formulario con los datos del archivo
        formulario = ArchivoForm(request.POST, request.FILES)

        # Verifica si el formulario es válido
        if formulario.is_valid():
            # Guardar el archivo en la base de datos
            nuevo_archivo = formulario.save()

            try:
                procesar_archivo_armonico(nuevo_archivo)
                messages.success(request, 'Archivo procesado correctamente.')
                return redirect('armonicos')

            except (ValueError, EmptyDataError) as e:
                messages.error(
                    request, f'Ocurrió un error al procesar el archivo: {e}')
                # Eliminar el archivo guardado si ocurrió un error  al procesar el archivo
                nuevo_archivo.delete()

            except DatabaseError as e:
                messages.error(request, f'Error de base de datos: {e}')
                # Eliminar el archivo guardado si ocurrió un error en la base de datos
                nuevo_archivo.delete()

            except Exception as e:
                messages.error(request, f'Error inesperado: {e}')
                nuevo_archivo.delete()  # Eliminar el archivo guardado si ocurrió un error inesperado

        else:
            # Mostrar un mensaje de error si el formulario no es válido
            messages.error(request, 'Error al procesar el formulario.')
    else:
        # Crear un formulario vacío
        formulario = ArchivoForm()

    # renderizar el formulario
    return render(request, 'armonicos/crear_armonico.html', {'form': formulario})


def procesar_archivo_armonico(archivo_excel):
    df = leer_archivo(archivo_excel.archivo.path)
    if df is None:
        raise ValueError("No se pudo leer el archivo.")

    print(df.to_string(index=False))

    print("DataFrame Original:")
    print(df)  # Mostrar el DataFrame completo

    # SELECCIONAR LAS FILAS Y COLUMNAS NECESARIAS
    filas = slice(1, None)
    columnas = slice(1, None)
    df_seleccionado = seleccionar_filas_columnas(df, filas, columnas)

    print("\nDataFrame Seleccionado:")
    print(df_seleccionado)

    df_seleccionado = ajustar_encabezado(df_seleccionado)

    # Convertir los datos a tipo numérico y llenar NaN con 0
    df_seleccionado = df_seleccionado.apply(
        pd.to_numeric, errors='coerce').fillna(0)

    print("\nDataFrame Seleccionado con Encabezado Ajustado sin índices:")
    print(df_seleccionado.to_string(index=False))

    valores_mayores = contar_valores_mayores(df_seleccionado, 5)

    print("\nValores mayores a 5 por columna:")
    print(valores_mayores)

    total_filas = df_seleccionado.shape[0]  # Número total de filas
    porcentaje_valores_mayores = calcular_porcentaje_valores_mayores(
        valores_mayores, total_filas)

    print("\nPorcentaje de valores mayores a 5 por columna:")
    print(porcentaje_valores_mayores)

    # Formatear la salida como la deseas
    for columna in df_seleccionado.columns:

        ArchivoInfo.objects.create(
            nombre_columna=columna,
            valor=porcentaje_valores_mayores[columna].round(2),
            archivo=archivo_excel,
        )

    """ # Guardar la información en el modelo ArchivoInfo
    for columna in df_seleccionado.columns:
        for valor in df[columna]:
            print(columna, valor)
            ArchivoInfo.objects.create(
                archivo=archivo_excel,
                nombre_columna=columna,
                valor=valor
            ) """
