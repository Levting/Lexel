import pandas as pd


def leer_archivo(file_path):
    """
    Lee un archivo xlsx y devuelve un DataFrame.
    """
    try:
        df = pd.read_excel(file_path, header=None,
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
    """
    df_seleccionado = df.iloc[filas, columnas]
    return df_seleccionado


def ajustar_encabezado(df):
    """
    Ajusta el DataFrame para usar la primera fila como encabezado de las columnas.
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
