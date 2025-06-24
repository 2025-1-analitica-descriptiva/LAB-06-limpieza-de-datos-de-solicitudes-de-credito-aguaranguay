"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""
import pandas as pd

def ajustar_formato_fecha(fecha):

    """
    Función para corregir formato de fechas inconsistentes (d/m/a vs a/m/d)
    """
    partes = fecha.split('/')
    if len(partes[0]) == 4:
        fecha_ajustada = '/'.join(reversed(partes))
    else:
        fecha_ajustada = '/'.join(partes)
    return fecha_ajustada

def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
    # Cargar el archivo original
    df = pd.read_csv("files/input/solicitudes_de_credito.csv", sep=";")

    # Eliminar filas con valores faltantes
    df = df.dropna()

    # Estandarizar columnas de texto: minúsculas
    df["sexo"] = df["sexo"].str.lower()
    df["tipo_de_emprendimiento"] = df["tipo_de_emprendimiento"].str.lower()
    df["idea_negocio"] = df["idea_negocio"].str.lower()
    df["barrio"] = df["barrio"].str.lower()
    df["línea_credito"] = df["línea_credito"].str.lower()

    # Reemplazar guiones y guiones bajos por espacios en campos clave
    reemplazos = ['_', '-']
    for simbolo in reemplazos:
        df["idea_negocio"] = df["idea_negocio"].str.replace(simbolo, ' ', regex=False)
        df["barrio"] = df["barrio"].str.replace(simbolo, ' ', regex=False)
        df["línea_credito"] = df["línea_credito"].str.replace(simbolo, ' ', regex=False)

    # Arreglar fechas en formato mixto
    df["fecha_de_beneficio"] = df["fecha_de_beneficio"].apply(ajustar_formato_fecha)

    # Limpiar monto_del_credito quitando $, comas y espacios
    limpiar = [' ', '$', ',']
    for char in limpiar:
        df["monto_del_credito"] = df["monto_del_credito"].str.replace(char, '', regex=False)
    df["monto_del_credito"] = df["monto_del_credito"].astype(float)

    # Eliminar duplicados basados en todas las columnas relevantes
    df = df.drop_duplicates(subset=[
        "sexo", "tipo_de_emprendimiento", "idea_negocio", "barrio", "estrato",
        "comuna_ciudadano", "fecha_de_beneficio", "monto_del_credito", "línea_credito"
    ]).dropna()

    # Exportar el archivo limpio
    df.to_csv("files/output/solicitudes_de_credito.csv", sep=";", index=False)

pregunta_01()