import pandas as pd
from django.contrib import messages
from .models import Archivo, Categoria, Tipo, Analizador
from django.utils.timezone import localtime
from babel.dates import format_datetime
from django.shortcuts import render, redirect, get_object_or_404
from .resource import depuracion_armonico as arm
from .resource import depuracion_tendencia as ten

from django.db import DatabaseError
from pandas.errors import EmptyDataError


def index(request):
    """
    Visita la página "Calidad del Producto"
    """
    return render(request, 'calidad_producto/index.html')

# ---------- ARMÓNICOS ----------


def vista_armonicos(request):
    """
    Visita la página de armonicos
    """
    archivos_formateados = obtener_archivos_por_categoria(1)
    return render(request, 'armonicos/armonicos.html', {'archivos': archivos_formateados})


def vista_armonico_detalle(request, archivo_id):
    """
    Visita la página de detalle de armonicos, obtenemos el archivo seleccionado y mostramos en la vista "armonico_detalle.html"
    """

    # Obtener el archivo evitando que el servidor colapse
    archivo = get_object_or_404(Archivo, id=archivo_id)

    # Mostrar solamente el nombre del archivo, sin el "archivo/" al inicio
    nombre_archivo = archivo.archivo.url.split('/')[-1]

    # Obtener la informacion de archivo
    archivo_info = archivo.informacion

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
    categoria_id = 1  # Armonico
    tipo_id = 2  # Monofásico
    analizador_id = 3  # SONEL
    # analizador_id = 2  # AEMC
    # analizador_id = 3  # METREL
    valor_porcentaje = 5
    return procesar_archivo_unico(request, categoria_id, tipo_id, analizador_id, valor_porcentaje, depuracion_armonico, 'vista_armonicos')


def crear_armonico_lote(request):
    """
    Crea un archivo armonico en lote, depura el archivo armonico y mostrando un mensaje de éxito o error en la vista de armonicos.
    """
    categoria_id = 1  # Armonico
    tipo_id = 1  # Monofásico
    analizador_id = 1  # Sonel
    valor_porcentaje = 5
    return procesar_archivos_lote(request, categoria_id, tipo_id, analizador_id, valor_porcentaje, depuracion_armonico, 'vista_armonicos')


def eliminar_armonico(request, archivo_id):
    """
    Elimina un archivo armonico y redirige a la vista de armonicos.
    """
    return eliminar_archivo(request, archivo_id, 'vista_armonicos')


def depuracion_armonico(nuevo_archivo, analizador, valor_porcentaje):
    """
    Depura un archivo armonico.

    Parámetros:
        nuevo_archivo: El archivo a depurar.
        analizador: El analizador a utilizar.
        valor_porcentaje: El valor del porcentaje a utilizar.

    Retorna:
        La información depurada del archivo.

    """

    # Obtener la ruta del archivo
    ruta_archivo = nuevo_archivo.archivo.path

    # Obtener el nombre del analizador
    analizador = analizador.nombre

    # Obtener la informacion del analizador
    informacion = arm.tipo_analizador(
        analizador, ruta_archivo, valor_porcentaje)
    
    # Actualizar la información del archivo
    nuevo_archivo.informacion = informacion

    # Guardar los cambios en la base de datos
    nuevo_archivo.save()

# ---------- TENDENCIA ----------


def vista_tendencias(request):
    """
    Visita la página de tendencias, obtenemos todos los datos de la base de datos con la temática de tendencias y mostramos en la vista tendencias.html
    """
    archivos_formateados = obtener_archivos_por_categoria(2)
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
def obtener_archivos_por_categoria(categoria_id):
    """
    Obtiene y formatea los archivos de una categoría específica.
    """

    # Obtener categoria de la base de datos
    categoria = Categoria.objects.get(id=categoria_id)

    # Obtener todos los archivos de categoria "armonico" o "tendencia" ordenado ascendentemente por la fecha de subida
    archivos = Archivo.objects.filter(
        categoria=categoria).order_by('subido_el')

    archivos_formateados = [
        {
            'id': archivo.id,
            'archivo': archivo.archivo.name.split('/')[-1],
            'subido_el': format_datetime(localtime(archivo.subido_el), format='dd MMMM yyyy, hh:mm a', locale='es_ES'),
            'tipo': archivo.tipo.nombre,
            'analizador': archivo.analizador.nombre,
        }
        for archivo in archivos
    ]
    return archivos_formateados


def procesar_archivo_unico(request, categoria_id, tipo_id, analizador_id, valor_porcetaje, tipo_depuracion, redireccion_vista):

    if request.method == 'POST':
        if 'archivo_unico' in request.FILES:

            # Obtener el archivo de la solicitud
            archivo = request.FILES['archivo_unico']

            try:
                # Obtener la categoría, tipo y analizador desde la base de datos
                categoria = Categoria.objects.get(id=categoria_id)
                tipo = Tipo.objects.get(id=tipo_id)
                analizador = Analizador.objects.get(id=analizador_id)

                # Crear un nuevo objeto Archivo
                nuevo_archivo = Archivo(
                    archivo=archivo,
                    categoria=categoria,
                    tipo=tipo,
                    analizador=analizador
                )
                print(f"Nuevo Archivo Unico: {nuevo_archivo}")

                # Guardar el archivo en la base de datos
                nuevo_archivo.save()

                # Procesar el archivo
                tipo_depuracion(nuevo_archivo, analizador, valor_porcetaje)

                # Mostrar un mensaje de éxito si el archivo se procesó correctamente
                messages.success(request, 'Archivo procesado correctamente.')

                # Redirigir a la página de armonicos o tendencias
                return redirect(redireccion_vista)

            except (ValueError, EmptyDataError) as e:
                # Mensaje de error si ocurre un error al procesar el archivo.
                messages.error(
                    request, f'Ocurrió un error al procesar el archivo: {e}')
                nuevo_archivo.delete()

            except DatabaseError as e:
                # Mensaje de error si ocurre un error en la base.
                messages.error(request, f'Error de base de datos: {e}')
                nuevo_archivo.delete()

            except Exception as e:
                # Mensaje de error si ocurre un error inesperado.
                messages.error(request, f'Error inesperado: {e}')
                

        else:
            # Mostrar un mensaje de error si no se seleccionó un archivo
            messages.error(request, 'Por favor, seleccione un archivo .xlsx.')

    # Renderizar la vista de crear armonico o tendencia
    return render(request, 'armonicos/crear_armonico.html' if categoria.id == 1 else 'tendencias/crear_tendencia.html')


def procesar_archivos_lote(request, categoria_id, tipo_id, analizador_id, valor_porcenaje, tipo_depuracion, redireccion_vista):
    """
    Procesa archivos en lote.
    """
    if request.method == 'POST':
        if 'archivos_lote' in request.FILES:

            # Obtener los archivos de la solicitud
            archivos = request.FILES.getlist('archivos_lote')

            # Para cada archivo en la lista de archivos
            for archivo in archivos:

                try:
                    # Obtener la categoría, tipo, y analizador desde la base de datos
                    categoria = Categoria.objects.get(id=categoria_id)
                    tipo = Tipo.objects.get(id=tipo_id)
                    analizador = Analizador.objects.get(id=analizador_id)

                    # Crear un nuevo archivo a partir del archivo actual
                    nuevo_archivo = Archivo(
                        archivo=archivo,
                        categoria=categoria,
                        tipo=tipo,
                        analizador=analizador
                    )

                    # Guardar el archivo en la base de datos
                    nuevo_archivo.save()

                    # Procesar el archivo y mostrar un mensaje de éxito
                    tipo_depuracion(nuevo_archivo, analizador, valor_porcenaje)

                    # Mostrar un mensaje de éxito si el archivo se procesó correctamente
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
    return render(request, 'armonicos/crear_armonico.html' if categoria.id == 1 else 'tendencias/crear_tendencia.html')


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
