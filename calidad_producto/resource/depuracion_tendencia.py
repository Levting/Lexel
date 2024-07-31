import pandas as pd


def leer_archivo(ruta_archivo, hoja=0, encabezado=None):
    """
    Lee un archivo xlsx y devuelve un DataFrame.

    Parámetros:
    ruta_archivo (str): La ruta del archivo xlsx.
    nombre_hoja (str o int): Nombre o índice de la hoja a leer. Por defecto es 0 (primera hoja).
    encabezado (int o None): La fila a utilizar como encabezado (0-indexado). None para no usar encabezado.

    Retorna:
    DataFrame o None: El DataFrame leído o None si ocurre un error.
    """
    try:
        df = pd.read_excel(ruta_archivo, header=encabezado, sheet_name=hoja,
                           engine='openpyxl')  # Leer sin encabezado
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
    return round(porcentaje_desviacion, 3)


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
    return round(porcentaje_flicker, 3)


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
    return round(porcentaje_vthd, 3)
