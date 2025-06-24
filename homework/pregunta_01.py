"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""
import pandas as pd
from pathlib import Path

def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
    # Rutas de entrada y salida
    input_path  = Path("files/input/solicitudes_de_credito.csv")
    output_path = Path("files/output/solicitudes_de_credito.csv")

    # Leer el CSV original (separador ';')
    df = pd.read_csv(input_path, sep=';')

    # 1. Eliminar columna de índice importado si existe
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])

    # 2. Normalizar nombres de columnas: quitar espacios y pasar a minúsculas
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(' ', '_', regex=False)
    )

    # 3. Limpieza de texto en columnas categóricas
    text_cols = ['sexo', 'tipo_de_emprendimiento', 'idea_negocio', 'barrio', 'línea_credito']
    for col in text_cols:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
                .str.lower()
                .str.replace('-', ' ', regex=False)
                # Quitar puntuación: todo lo que no sea letra, dígito o espacio
                .str.replace(r'[^\w\s]', '', regex=True)
                .replace({'nan': pd.NA})
            )

    # 4. Convertir fecha a datetime
    if 'fecha_de_beneficio' in df.columns:
        df['fecha_de_beneficio'] = pd.to_datetime(
            df['fecha_de_beneficio'],
            format='%d/%m/%Y',
            errors='coerce'
        )

    # 5. Manejo de valores faltantes: eliminar filas con NaN en columnas clave
    key_cols = ['sexo', 'tipo_de_emprendimiento', 'idea_negocio', 'barrio', 'fecha_de_beneficio']
    df = df.dropna(subset=key_cols)

    # 6. Eliminar duplicados exactos
    df = df.drop_duplicates()

    # 7. Resetear índice
    df = df.reset_index(drop=True)

    # Guardar el DataFrame limpio
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, sep=';', index=False)


if __name__ == "__main__":
    pregunta_01()