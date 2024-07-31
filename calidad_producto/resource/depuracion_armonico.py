import pandas as pd


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


def normalizar_encabezados(df):
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


def contar_valores_mayores(df, numero):
    """
    Cuenta cuántos valores mayores que un número específico hay por columna.

    Parámetros:
        df (DataFrame): El DataFrame con los datos.
        numero (int o float): El número a comparar.

    Retorna:
        Series: La cantidad de valores mayores a 'numero' por columna.
    """
    valores_mayores = (df > numero).sum()
    return valores_mayores


def calcular_porcentaje_valores_mayores(valores_mayores, total_filas):
    """
    Calcula el porcentaje de valores mayores a un número específico por columna.

    Parámetros:
        valores_mayores (Series): La cantidad de valores mayores a un número por columna.
        total_filas (int): El número total de filas.

    Retorna:
        Series: El porcentaje de valores mayores a un número por columna.
    """
    porcentaje_valores_mayores = (valores_mayores / total_filas) * 100
    return porcentaje_valores_mayores


def obtener_datos(df_seleccionado, valores_mayores, porcentaje_valores_mayores, valor_porcentaje):
    """
    Obtiene un conjunto de datos de información general con valores mayores a un porcentaje específico.

    Parámetros:
        df_seleccionado (DataFrame): El DataFrame seleccionado.
        valores_mayores (Series): La cantidad de valores mayores a un número específico por columna.
        porcentaje_valores_mayores (Series): El porcentaje de valores mayores a un número específico por columna.
        valor_porcentaje (int): El porcentaje mínimo para considerar un valor mayor, en este caso 5.

    Retorna:    
        dict: Un diccionario con la información general de columnas con valores mayores al porcentaje especificado.
    """

    informacion = {
        columna: {
            'conteo': int(valores_mayores[columna]),
            'porcentaje': float(porcentaje_valores_mayores[columna].round(5))
        }
        for columna in df_seleccionado.columns
        if porcentaje_valores_mayores[columna] > valor_porcentaje
    }
    return informacion


def sonel(ruta_archivo, filas=slice(None, None), columnas=slice(None, None), valor_porcentaje=0):
    """
    Función principal para analizar un archivo de Sonel monofásico.

    Parámetros:
        ruta_archivo (str): La ruta del archivo xlsx o xls.
        filas (slice): Rango de filas a seleccionar. Por defecto selecciona todas las filas.
        columnas (slice): Rango de columnas a seleccionar. Por defecto selecciona todas las columnas.
        valor_porcentaje (int): El porcentaje mínimo para considerar un valor mayor. Por defecto es 0.

    Retorna:
        dict, dict: Dos diccionarios con la información general y los resultados de valores mayores.
    """

    df = leer_archivo(ruta_archivo)

    if df is None:
        print("No se pudo leer el archivo.")

    else:
        # Seleccionar las filas y columnas deseadas
        df_seleccionado = seleccionar_filas_columnas(df, filas, columnas)

        # Ajustar encabezado del df
        df_seleccionado = ajustar_encabezado(df_seleccionado)

        # Convertir los datos a tipo numérico y llenar NaN con 0
        df_seleccionado = df_seleccionado.apply(
            pd.to_numeric, errors='coerce').fillna(0)

        # Normalizar encabezados
        df_seleccionado = normalizar_encabezados(df_seleccionado)

        # Contar valores mayores a 5 por columna
        valores_mayores = contar_valores_mayores(
            df_seleccionado, valor_porcentaje)

        # Calcular porcentaje de valores mayores a 5 por columna
        total_filas = df_seleccionado.shape[0]  # Número total de filas
        porcentaje_valores_mayores = calcular_porcentaje_valores_mayores(
            valores_mayores, total_filas)

        # Obtener información general y resultados de valores mayores a 5
        informacion = obtener_datos(
            df_seleccionado, valores_mayores, porcentaje_valores_mayores, valor_porcentaje)

        return informacion


def aemc(ruta_archivo, filas=slice(None, None), columnas=slice(None, None), valor_porcentaje=0):
    """
    Función principal para analizar un archivo de AEMC monofásico.

    Parámetros:
        ruta_archivo (str): La ruta del archivo xlsx o xls.
        filas (slice): Rango de filas a seleccionar. Por defecto selecciona todas las filas.
        columnas (slice): Rango de columnas a seleccionar. Por defecto selecciona todas las columnas.
        valor_porcentaje (int): El porcentaje mínimo para considerar un valor mayor. Por defecto es 0.

    Retorna:
        dict: Diccionario con la información general que conrresponde a los valores mayores.
    """

    df = leer_archivo(ruta_archivo)
    if df is None:
        print("No se pudo leer el archivo.")

    else:

        # Seleccionar las filas y columnas deseadas
        df_seleccionado = seleccionar_filas_columnas(df, filas, columnas)

        # Ajustar encabezado del df
        df_seleccionado = ajustar_encabezado(df_seleccionado)

        # Convertir los datos a tipo numérico y llenar NaN con 0
        df_seleccionado = df_seleccionado.apply(
            pd.to_numeric, errors='coerce').fillna(0)

        # Eliminar la primera fila y resetear los índices
        df_seleccionado = df_seleccionado.iloc[1:]
        df_seleccionado.reset_index(drop=True, inplace=True)

        # Contar valores mayores a 5 por columna
        valores_mayores = contar_valores_mayores(
            df_seleccionado, valor_porcentaje)

        # Calcular porcentaje de valores mayores a 5 por columna
        total_filas = df_seleccionado.shape[0]  # Número total de filas
        porcentaje_valores_mayores = calcular_porcentaje_valores_mayores(
            valores_mayores, total_filas)

        # Obtener información general de los valores mayores a 5
        informacion = obtener_datos(
            df_seleccionado, valores_mayores, porcentaje_valores_mayores, valor_porcentaje)

        return informacion


def metrel(ruta_archivo, filas=slice(None, None), columnas=slice(None, None), valor_porcentaje=0):
    pass


def tipo_analizador(ruta_archivo, analizador, valor_porcentaje):
    """
    Función que selecciona el tipo de analizador a utilizar.

    Parámetros:
        ruta_archivo (str): La ruta del archivo xlsx o xls.
        analizador (str): El tipo de analizador a utilizar.
        valor_porcentaje (int): El porcentaje mínimo para considerar un valor mayor.

    Retorna:
        tuple: Una tupla con la información general y los resultados de valores mayores.
    """
    
    def manejador_sonel():
        print("Analizando archivo con Sonel...")
        filas = slice(None, None)
        columnas = slice(3, None)
        return sonel(ruta_archivo, filas, columnas, valor_porcentaje)

    def manejador_aemc():
        print("Analizando archivo con AEMC...")
        filas = slice(1, None)
        columnas = slice(2, None)
        return aemc(ruta_archivo, filas, columnas, valor_porcentaje)

    def manejar_metrel():
        print("Analizando archivo con Metrel ...")
        filas = slice(1, None)
        columnas = slice(2, None)
        return metrel(ruta_archivo, filas, columnas, valor_porcentaje)

    def manejador_no_soportado():
        print("Analizador no soportado.")
        return None

    # Diccionario de manejadores
    manejadores = {
        "SONEL": manejador_sonel,
        "AEMC": manejador_aemc,
        "METREL": manejar_metrel
    }

    # Seleccionar el manejador adecuado y si no se encuentra, mostrar un mensaje de error
    manejador = manejadores.get(analizador, manejador_no_soportado)

    return manejador()
