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


def contar_valores_mayores(df, numero):
    """
    Cuenta cuántos valores mayores que un número específico hay por columna.
    """
    valores_mayores = (df > numero).sum()
    return valores_mayores


def calcular_porcentaje_valores_mayores(valores_mayores, total_filas):
    """
    Calcula el porcentaje de valores mayores a un número específico por columna.
    """
    porcentaje_valores_mayores = (valores_mayores / total_filas) * 100
    return porcentaje_valores_mayores
