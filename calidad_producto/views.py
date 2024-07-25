import pandas as pd
from django.contrib import messages
from .models import Archivo, ArchivoInfo
from django.utils.timezone import localtime
from babel.dates import format_datetime
from django.shortcuts import render, redirect, get_object_or_404
from .lectura_armonico import leer_archivo, seleccionar_filas_columnas, ajustar_encabezado, contar_valores_mayores, calcular_porcentaje_valores_mayores

from django.db import DatabaseError
from pandas.errors import EmptyDataError


def index(request):
    """
    Visita la página "Calidad del Producto"
    """
    return render(request, 'calidad_producto/index.html')

# Armonicos


def vista_armonicos(request):
    """
    Visita la página de armonicos, obtenemos todos los datos de la base de datos con la temática de armonicos y mostramos en la vista armonicos.html
    """
    archivos_formateados = obtener_archivos_por_categoria('armonico')
    return render(request, 'armonicos/armonicos.html', {'archivos': archivos_formateados})


def vista_armonico_detalle(request, archivo_id):
    """
    Visita la página de detalle de armonicos, obtenemos el archivo seleccionado y mostramos en la vista "armonico_detalle.html"
    """

    # Obtener el archivo evitando que el servidor colapse
    archivo = get_object_or_404(Archivo, id=archivo_id)

    # Mostrar solamente el nombre del archivo, sin el "archivo/" al inicio
    nombre_archivo = archivo.archivo.url.split('/')[-1]

    # Obtener la información del archivo
    archivo_info_obj = archivo.info.first()
    archivo_info = archivo_info_obj.data if archivo_info_obj else {}

    # print("\nInformación del archivo seleccionado:\n", archivo_info)

    return render(request, 'armonicos/armonico_detalle.html', {'nombre_archivo': nombre_archivo, 'archivo_info': archivo_info})


def vista_crear_armonico(request):
    """
    Visita la página de crear armonico, mostramos la vista "crear_armonico.html"
    """
    return render(request, 'armonicos/crear_armonico.html')


def crear_armonico_unico(request):
    """
    Crea un archivo armonico de forma única, depura el archivo armonico y mostrando un mensaje de éxito o error en la vista de armonicos.
    """
    return procesar_archivo_unico(request, 'armonico', depuracion_armonico, 'vista_armonicos')


def crear_armonico_lote(request):
    """
    Crea un archivo armonico en lote, depura el archivo armonico y mostrando un mensaje de éxito o error en la vista de armonicos.
    """
    return procesar_archivos_lote(request, 'armonico', depuracion_armonico, 'vista_armonicos')


def eliminar_armonico(request, archivo_id):
    """
    Elimina un archivo armonico y redirige a la vista de armonicos.
    """
    return eliminar_archivo(request, archivo_id, 'vista_armonicos')


def depuracion_armonico(archivo_excel):
    """
    Depura el archivo armonico

    1. Selecciona las filas y columnas necesarias. 
    2. Ajusta el encabezado del df seleccionado.
    3. Convierte los datos a tipo numérico y llena NaN con 0.
    4. Cuenta los valores mayores a 5 por columna.
    5. Calcula el porcentaje de valores mayores a 5 por columna.
    6. Crea un objeto ArchivoInfo con la información del archivo.
    """

    # Leer el archivo cargado
    df = leer_archivo(archivo_excel.archivo.path)

    # Controlamos la lectura del archivo, para que sea correcta.
    if df is None:
        raise ValueError("No se pudo leer el archivo.")

    # print(df.to_string(index=False))
    # print("\nDataFrame Original:")
    # print(df)

    # Seleccionar las filas y columnas necesarias
    filas = slice(11, -1)
    columnas = slice(10, None)
    df_seleccionado = seleccionar_filas_columnas(df, filas, columnas)

    # print("\nDataFrame Seleccionado:")
    # print(df_seleccionado)

    # Ajustar el encabezado del df seleccionado
    df_seleccionado = ajustar_encabezado(df_seleccionado)

    # Convertir los datos a tipo numérico y llenar NaN con 0
    df_seleccionado = df_seleccionado.apply(
        pd.to_numeric, errors='coerce').fillna(0)

    # print("\nDataFrame Seleccionado con Encabezado Ajustado sin índices:")
    # print(df_seleccionado)

    # Contar los valores mayores a 5 por columna
    valores_mayores = contar_valores_mayores(df_seleccionado, 5)

    # print("\nValores mayores a 5 por columna:")
    # print(valores_mayores)

    # Obtener el total de filas para calcular el porcentaje de valores mayores a 5
    total_filas = df_seleccionado.shape[0]
    porcentaje_valores_mayores = calcular_porcentaje_valores_mayores(
        valores_mayores, total_filas)

    # print("\nPorcentaje de valores mayores a 5 por columna:")
    # print(porcentaje_valores_mayores)

    # Crear un diccionario con los datos de las columnas, asegurándose de convertir a tipos nativos de Python (numericos)
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

# Tendencias


def vista_tendencias(request):
    """
    Visita la página de tendencias, obtenemos todos los datos de la base de datos con la temática de tendencias y mostramos en la vista tendencias.html
    """
    archivos_formateados = obtener_archivos_por_categoria('tendencia')
    return render(request, 'tendencias/tendencias.html', {'archivos': archivos_formateados})


def vista_tendencia_detalle(request, archivo_id):
    """
    Visita la página de detalle de tendencias, obtenemos el archivo seleccionado y mostramos en la vista "tendencia_detalle.html"
    """


def vista_crear_tendencia(request):
    """
    Visita la página de crear tendencia, mostramos la vista "crear_tendencia.html"
    """
    return render(request, 'tendencias/crear_tendencia.html')


def crear_tendencia_unico(request):
    """
    Crea un archivo tendencia de forma única, depura el archivo tendencia y mostrando un mensaje de éxito o error en la vista de tendencias.
    """
    return procesar_archivo_unico(request, 'tendencia', depuracion_tendencia, 'vista_tendencias')


def crear_tendencia_lote(request):
    """
    Crea un archivo tendencia en lote, depura el archivo tendencia y mostrando un mensaje de éxito o error en la vista de tendencias.
    """
    return procesar_archivos_lote(request, 'tendencia', depuracion_tendencia, 'vista_tendencias')


def eliminar_tendencia(request, archivo_id):
    """
    Elimina un archivo tendencia y redirige a la vista de tendencias.
    """
    return eliminar_archivo(request, archivo_id, 'vista_tendencias')


def depuracion_tendencia(archivo_excel):
    print("Procesando archivo de tendencia...")


# --- METODOS ---
def obtener_archivos_por_categoria(categoria):
    """
    Obtiene y formatea los archivos de una categoría específica.
    """

    # Obtener todos los archivos de categoria "armonico" o "tendencia" ordenado ascendentemente por la fecha de subida
    archivos = Archivo.objects.filter(
        categoria=categoria).order_by('subido_el')

    archivos_formateados = [
        {
            'id': archivo.id,
            'archivo': archivo.archivo.name.split('/')[-1],
            'subido_el': format_datetime(localtime(archivo.subido_el), format='dd MMMM yyyy, hh:mm a', locale='es_ES')
        }
        for archivo in archivos
    ]
    return archivos_formateados


def procesar_archivo_unico(request, categoria, tipo_depuracion, redireccion_vista):
    """
    Procesa un archivo de forma única.
    """
    if request.method == 'POST':
        if 'archivo_unico' in request.FILES:

            # Obtener el archivo de la solicitud
            archivo = request.FILES['archivo_unico']

            # Crear un nuevo objeto a partir de la categoria, 'armonicos' o 'tendencia'
            nuevo_archivo = Archivo(archivo=archivo, categoria=categoria)

            # Guardar el archivo en la base de datos
            nuevo_archivo.save()

            # Procesar el archivo
            try:
                # Procesar el archivo y mostrar un mensaje de éxito
                tipo_depuracion(nuevo_archivo)
                messages.success(request, 'Archivo procesado correctamente.')
                print("\nArchivo procesado correctamente!\n")
                return redirect(redireccion_vista)

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
            # Mostrar un mensaje de error si no se seleccionó un archivo
            messages.error(request, 'Por favor, seleccione un archivo .xlsx.')

    # Renderizar la vista de crear armonico o tendencia
    return render(request, 'armonicos/crear_armonico.html' if categoria == 'armonico' else 'tendencias/crear_tendencia.html')


def procesar_archivos_lote(request, categoria, tipo_depuracion, redireccion_vista):
    """
    Procesa archivos en lote.
    """
    if request.method == 'POST':
        if 'archivos_lote' in request.FILES:
            # Obtener los archivos de la solicitud
            archivos = request.FILES.getlist('archivos_lote')

            # Para cada archivo en la lista de archivos
            for archivo in archivos:

                # Crear un nuevo archivo a partir del archivo actual
                nuevo_archivo = Archivo(archivo=archivo, categoria=categoria)

                # Guardar el archivo en la base de datos
                nuevo_archivo.save()

                try:
                    # Procesar el archivo y mostrar un mensaje de éxito
                    tipo_depuracion(nuevo_archivo)
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

            # Redirigir a la página de armonicos o tendencias
            return redirect(redireccion_vista)
        else:
            # Mostrar un mensaje de error si no se seleccionaron archivos
            messages.error(
                request, 'Por favor, seleccione archivos para cargar.')
    else:
        # Mostrar un mensaje de error si el formulario no es válido
        messages.error(request, 'Error al procesar el formulario.')

    # Renderizar la vista de crear armonico o tendencia
    return render(request, 'armonicos/crear_armonico.html' if categoria == 'armonico' else 'tendencias/crear_tendencia.html')


def eliminar_archivo(request, archivo_id, redireccion_vista):
    """
    Elimina un archivo y redirige a la vista de armonicos o tendencias.
    """
    # Obtener el archivo evitando que el servidor colapse
    archivo = get_object_or_404(Archivo, id=archivo_id)

    # Si la solicitud es POST, eliminar el archivo
    if request.method == 'POST':

        # Eliminar el archivo
        archivo.delete()

        # Mostrar un mensaje de éxito en el frontend
        messages.success(request, 'Archivo eliminado correctamente.')

        # Mostrar mensaje en el backend
        print("\nArchivo eliminado correctamente.\n")

        # Redirigir a la página con el mensaje
        return redirect(redireccion_vista)
