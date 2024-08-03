import pandas as pd
from calidad_producto.models import Analizador

def leer_archivo(ruta_archivo, hoja=0, encabezado=None):
    """
    Lee un archivo xlsx o xls y devuelve un DataFrame.

    Parámetros:
    ruta_archivo (str): La ruta del archivo xlsx o xls.
    hoja (str o int): Nombre o índice de la hoja a leer. Por defecto es 0 (primera hoja).
    encabezado (int o None): La fila a utilizar como encabezado (0-indexado). None para no usar encabezado.

    Retorna:
    DataFrame o None: El DataFrame leído o None si ocurre un error.
    """
    try:
        if ruta_archivo.endswith('.xlsx'):
            df = pd.read_excel(ruta_archivo, header=encabezado,
                               sheet_name=hoja, engine='openpyxl')
        elif ruta_archivo.endswith('.xls'):
            df = pd.read_excel(ruta_archivo, header=encabezado,
                               sheet_name=hoja, engine='xlrd')
        else:
            print("El formato del archivo no es soportado.")
            return None
    except FileNotFoundError:
        print("El archivo no se encontró.")
        return None
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {e}")
        return None
    return df


def seleccionar_filas_columnas(df, filas, columnas):
    """
    Selecciona el rango de filas y columnas necesarias de un DataFrame.

    Parámetros:
    df (DataFrame): El DataFrame original.
    filas (slice): Rango de filas a seleccionar.
    columnas (slice): Rango de columnas a seleccionar.

    Retorna:
    DataFrame: El DataFrame resultante con las filas y columnas seleccionadas.
    """
    df_seleccionado = df.iloc[filas, columnas]
    return df_seleccionado


def ajustar_encabezado(df):
    """
    Ajusta el encabezado de un DataFrame.

    Parámetros:
    df (DataFrame): El DataFrame con los datos.

    Retorna:
    DataFrame: El DataFrame con el encabezado ajustado.
    """
    df.columns = df.iloc[0]
    df = df[1:]  # Eliminar la primera fila
    df.reset_index(drop=True, inplace=True)  # Reiniciar los índices
    return df


def normalizar_encabezados_sonel(df):
    """
    Normaliza los encabezados de un DataFrame eliminando sufijos específicos, reemplazando 'instant' por 'inst',
    y eliminando el contenido dentro de los corchetes al final de los nombres de las columnas.

    Parámetros:
        df (DataFrame): El DataFrame con los datos.

    Retorna:
        DataFrame: El DataFrame con los encabezados normalizados.
    """
    # Eliminar sufijos como ". <número> min"
    df.columns = df.columns.str.replace(r'\.\s*\d+\s*min', '', regex=True)

    # Reemplazar 'instant' por 'inst'
    df.columns = df.columns.str.replace(r'\binstant\b', 'inst', regex=True)

    # Eliminar el contenido dentro de corchetes y los corchetes mismos
    df.columns = df.columns.str.replace(r'\[.*?\]', '', regex=True)

    # Eliminar posibles espacios en blanco al final de los nombres de las columnas
    df.columns = df.columns.str.strip()

    return df


def normalizar_encabezados_aemc(df):
    """
    Normaliza los encabezados de un DataFrame eliminando sufijos específicos. Para el caso del analizador
    AEMC, se eliminan los sufijos el encabezado de desbiacion, ya que tienen "()" y el contenido
    de estas.

    Parámetros:
        df (DataFrame): El DataFrame con los datos.

    Retorna:
        DataFrame: El DataFrame con los encabezados normalizados.
    """

    # Eliminar el contenido dentro de los paréntesis y los paréntesis mismos
    df.columns = df.columns.str.replace(r'\(.*?\)', '', regex=True)

    # Eliminar posibles espacios en blanco al final de los nombres de las columnas
    df.columns = df.columns.str.strip()

    return df


def normalizar_encabezados_metrel(df):
    """
    Normaliza los encabezados de un DataFrame eliminando sufijos específicos. Para el caso del analizador
    AEMC, se eliminan los sufijos el encabezado, ya que tienen "()" y "[]" y el contenido
    de estas.

    Parámetros:
        df (DataFrame): El DataFrame con los datos.

    Retorna:
        DataFrame: El DataFrame con los encabezados normalizados.
    """

    # Eliminar el contenido dentro de los corchetes y los corchetes mismos
    df.columns = df.columns.str.replace(r'\[.*?\]', '', regex=True)

    # Eliminar posibles espacios en blanco al final de los nombres de las columnas
    df.columns = df.columns.str.strip()

    return df


def calcular_porcentaje_desviacion(df, columna):
    """
    Calcula el porcentaje de desviación de los valores de una columna.

    Parámetros:
        df (DataFrame): El DataFrame con los datos.
        columna (str): El nombre de la columna a analizar.

    Retorna:
        float: El porcentaje de desviación de los valores de la columna.
    """

    if columna not in df.columns:
        print(f"La columna '{columna}' no se encuentra en el DataFrame.")
        return None

    valores_superiores = df[df[columna] > 129.5][columna]
    valores_inferiores = df[df[columna] < 110.4][columna]
    total_valores = df[columna].count()
    porcentaje_desviacion = (
        (valores_superiores.count() + valores_inferiores.count()) / total_valores) * 100
    return round(porcentaje_desviacion, 4)


def calular_porcentaje_flicker(df, columna):
    """
    Calcula el porcentaje de flicker de los valores de una columna.

    Parámetros:
        df (DataFrame): El DataFrame con los datos.
        columna (str): El nombre de la columna a analizar.

    Retorna:
        float: El porcentaje de flicker de los valores de la columna.
    """

    if columna not in df.columns:
        print(f"La columna '{columna}' no se encuentra en el DataFrame.")
        return None

    valores_flicker = df[df[columna] > 1][columna]
    total_valores = df[columna].count()
    porcentaje_flicker = (valores_flicker.count() / total_valores) * 100
    return round(porcentaje_flicker, 4)


def calcular_porcentaje_vthd(df, columna):
    """
    Calcula el porcentaje de VTHD de los valores de una columna.

    Parámetros:
        df (DataFrame): El DataFrame con los datos.
        columna (str): El nombre de la columna a analizar.

    Retorna:
        float: El porcentaje de VTHD de los valores de la columna.
    """

    if columna not in df.columns:
        print(f"La columna '{columna}' no se encuentra en el DataFrame.")
        return None

    valores_vthd = df[df[columna] > 8][columna]
    total_valores = df[columna].count()
    porcentaje_vthd = (valores_vthd.count() / total_valores) * 100
    return round(porcentaje_vthd, 4)


def obtener_informacion(df, valores_columna):
    """
    Extrae la información relevante del DataFrame procesado.

    Parámetros:
        df (DataFrame): El DataFrame procesado.
        valores_columna (dict): Diccionario con los nombres de las columnas.

    Retorna:
        informacion (dict): Un diccionario con la información extraída.
    """

    informacion = {}

    # DESVIACION DE VOLTAJE
    for fase in ['a', 'b', 'c']:
        columna_voltaje = valores_columna.get(f'voltaje_{fase}')
        if columna_voltaje:
            valor_desviacion = calcular_porcentaje_desviacion(
                df, columna_voltaje)
            if valor_desviacion is not None:
                informacion[f'porcentaje_desviacion_voltaje_fase_{fase}'] = valor_desviacion

    # FLICKER
    for fase in ['a', 'b', 'c']:
        columna_flicker = valores_columna.get(f'flicker_{fase}')
        if columna_flicker:
            valor_flicker = calular_porcentaje_flicker(df, columna_flicker)
            if valor_flicker is not None:
                informacion[f'porcentaje_flicker_fase_{fase}'] = valor_flicker

    # VTHD
    for fase in ['a', 'b', 'c']:
        columna_vthd = valores_columna.get(f'vthd_{fase}')
        if columna_vthd:
            valor_vthd = calcular_porcentaje_vthd(
                df, columna_vthd)
            if valor_vthd is not None:
                informacion[f'porcentaje_vthd_fase_{fase}'] = valor_vthd

    # DESVALANCE
    # Solamente para trifásico
    columna_desbalance = valores_columna.get('desbalance')
    if columna_desbalance:
        valor_desbalance = calular_desbalance(df, columna_desbalance)
        if valor_desbalance is not None:
            informacion[f'porcentaje_desbalance'] = valor_desbalance

    return informacion


def calular_desbalance(df, columna):
    """
    Calcula el porcentaje de desvalance de los valores de una columna.

    Parámetros:
        df (DataFrame): El DataFrame con los datos.
        columna (str): El nombre de la columna a analizar.

    Retorna:
        float: El porcentaje de desvalance de los valores de la columna.
    """

    if columna not in df.columns:
        print(f"La columna '{columna}' no se encuentra en el DataFrame.")
        return None

    valores_desvalance = df[df[columna] > 2][columna]
    total_valores = df[columna].count()
    porcentaje_desvalance = (valores_desvalance.count() / total_valores) * 100
    return round(porcentaje_desvalance, 4)


def sonel(ruta_archivo, filas=slice(None, None), columnas=slice(None, None), valores_columna=None):
    """
    Procesa un archivo Sonel y extrae la información relevante.

    Parámetros:
        ruta_archivo (str): Ruta al archivo a procesar.
        filas (slice): Filtro para seleccionar las filas deseadas.
        columnas (slice): Filtro para seleccionar las columnas deseadas.
        valores_columna (dict): Diccionario con los nombres de las columnas.

    Retorna:
        informacion (dict): Un diccionario con la información procesada.
    """

    # Leer el archivo
    df = leer_archivo(ruta_archivo)

    # Si el dataframe es None, mostrar un mensaje de error y salir
    if df is None:
        print("No se pudo leer el archivo.")
        return None

    # Procesamiento del DataFrame
    print("\nDF")
    print(df)

    # Seleccionar las filas y columnas deseadas
    df_seleccionado = seleccionar_filas_columnas(df, filas, columnas)

    # Ajustar el encabezado del DataFrame
    df_seleccionado = ajustar_encabezado(df_seleccionado)

    # Normalizar enbacezados SONEL
    df_seleccionado = normalizar_encabezados_sonel(df_seleccionado)

    # Convertir los datos a tipo numérico y llenar NaN con 0
    df_seleccionado = df_seleccionado.apply(
        pd.to_numeric, errors='coerce').fillna(0)

    print("\nDF Resultante")
    print(df_seleccionado)

    # Obtener información procesada
    informacion = obtener_informacion(df_seleccionado, valores_columna)

    return informacion


def aemc(ruta_archivo, filas=slice(None, None), columnas=slice(None, None), valores_columna=None):
    """
    Procesa un archivo AEMC y extrae la información relevante.

    Parámetros:
        ruta_archivo (str): Ruta al archivo a procesar.
        filas (slice): Filtro para seleccionar las filas deseadas.
        columnas (slice): Filtro para seleccionar las columnas deseadas.
        valores_columna (dict): Diccionario con los nombres de las columnas.

    Retorna:
        informacion (dict): Un diccionario con la información procesada.
    """

    # Leer el archivo
    df = leer_archivo(ruta_archivo)

    # Si el dataframe es None, mostrar un mensaje de error y salir
    if df is None:
        print("No se pudo leer el archivo.")
        return None

    print("\nDF")
    print(df)

    # Seleccionar las filas y columnas deseadas
    df_seleccionado = seleccionar_filas_columnas(df, filas, columnas)

    # Ajustar el encabezado del DataFrame
    df_seleccionado = ajustar_encabezado(df_seleccionado)

    # Eliminar la 1da y la 2era fila y resetear los indices
    df_seleccionado = df_seleccionado.iloc[1:]
    df_seleccionado = df_seleccionado.iloc[1:]
    df_seleccionado.reset_index(drop=True, inplace=True)

    # Normalizar encabezados AEMC
    df_seleccionado = normalizar_encabezados_aemc(df_seleccionado)

    # Convertir los datos a tipo numérico y llenar NaN con 0
    df_seleccionado = df_seleccionado.apply(
        pd.to_numeric, errors='coerce').fillna(0)

    print("\nDF Resultado")
    print(df_seleccionado)

    # Obtener la inoformación procesada
    informacion = obtener_informacion(df_seleccionado, valores_columna)

    return informacion


def metrel(ruta_archivo, filas=slice(None, None), columnas=slice(None, None), valores_columna=None):
    """
    Procesa un archivo METREL y extrae la información relevante.

    Parámetros:
        ruta_archivo (str): Ruta al archivo a procesar.
        filas (slice): Filtro para seleccionar las filas deseadas.
        columnas (slice): Filtro para seleccionar las columnas deseadas.
        valores_columna (dict): Diccionario con los nombres de las columnas.

    Retorna:
        informacion (dict): Un diccionario con la información procesada.
    """

    # Leer el archivo
    df = leer_archivo(ruta_archivo)

    # Si el dataframe es None, mostrar un mensaje de error, caso contrario se procesa.
    if df is None:
        print("No se pudo leer el archivo.")
        return None

    print("\nDF")
    print(df)

    # Seleccionar las filas y columnas deseadas
    df_seleccionado = seleccionar_filas_columnas(df, filas, columnas)

    # Ajustar el encabezado del DataFrame
    df_seleccionado = ajustar_encabezado(df_seleccionado)

    # Eliminar la 1da fila y resetear los indices
    df_seleccionado = df_seleccionado.iloc[1:]
    df_seleccionado.reset_index(drop=True, inplace=True)

    # Normalizar encabezados METREL
    df_seleccionado = normalizar_encabezados_metrel(df_seleccionado)

    # Convertir los datos a tipo numérico y llenar NaN con 0
    df_seleccionado = df_seleccionado.apply(
        pd.to_numeric, errors='coerce').fillna(0)

    print("\nDF Resultado")
    print(df_seleccionado)

    # Obtener información procesada
    informacion = obtener_informacion(df_seleccionado, valores_columna)

    return informacion


def obtener_valores_columna(analizador):
    """
    Obtiene los valores de columna del analizador desde la base de datos.
    """
    analizador_obj = Analizador.objects.get(nombre=analizador)
    return {
        'voltaje_a': analizador_obj.voltaje_a,
        'voltaje_b': analizador_obj.voltaje_b,
        'voltaje_c': analizador_obj.voltaje_c,
        'flicker_a': analizador_obj.flicker_a,
        'flicker_b': analizador_obj.flicker_b,
        'flicker_c': analizador_obj.flicker_c,
        'vthd_a': analizador_obj.vthd_a,
        'vthd_b': analizador_obj.vthd_b,
        'vthd_c': analizador_obj.vthd_c,
        'desbalance': analizador_obj.desbalance
    }


def tipo_analizador(analizador, ruta_archivo):
    """
    Función que selecciona el tipo de analizador a utilizar.

    Parámetros:
        analizador (str): El tipo de analizador a utilizar.
        ruta_archivo (str): La ruta del archivo xlsx o xls.

    Retorna:
        tuple: Una tupla con la información general y los resultados de valores mayores.
    """

    def manejador_sonel():
        print("Analizando archivo con Sonel...")
        filas = slice(None, None)
        columnas = slice(2, None)

        # Obtener los valores de las columnas del analizador
        valores_columna = obtener_valores_columna(analizador)

        print(f"Valores columna: {valores_columna}")

        # Obtener la información
        return sonel(ruta_archivo, filas, columnas, valores_columna)

    def manejador_aemc():
        print("Analizando archivo con AEMC...")
        filas = slice(1, None)
        columnas = slice(2, None)

        # Obtener los valores de las columnas del analizador
        valores_columna = obtener_valores_columna(analizador)

        # Obtener la información
        return aemc(ruta_archivo, filas, columnas, valores_columna)

    def manejador_metrel():
        print("Analizando archivo con METREL...")
        filas = slice(None, None)
        columnas = slice(None, None)

        # Obtener los valores de las columnas del analizador
        valores_columna = obtener_valores_columna(analizador)

        # Obtener la información
        return metrel(ruta_archivo, filas, columnas, valores_columna)

    def manejador_no_soportado():
        print("Analizador no soportado.")
        return None

    # Diccionario de manejadores
    manejadores = {
        "SONEL": manejador_sonel,
        "AEMC": manejador_aemc,
        "METREL": manejador_metrel
    }

    # Seleccionar el manejador adecuado y si no se encuentra, mostrar un mensaje de error
    manejador = manejadores.get(analizador, manejador_no_soportado)

    return manejador()