import tensorflow as tf
import numpy as np

from pathlib import Path
from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)


# ============================================================
# CONFIGURACIÓN
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATASET_DIR = BASE_DIR / "dataset"
TEST_DIR = DATASET_DIR / "test"

MODELO_PATH = BASE_DIR / "modelo_skincheck.keras"

IMG_SIZE = (224, 224)
BATCH_SIZE = 32


print("=" * 60)
print("EVALUACIÓN DEL MODELO SKINCHECK")
print("=" * 60)


# ============================================================
# COMPROBAR ARCHIVOS
# ============================================================

if not MODELO_PATH.exists():
    raise FileNotFoundError(
        f"No se encontró el modelo: {MODELO_PATH}"
    )

if not TEST_DIR.exists():
    raise FileNotFoundError(
        f"No se encontró el dataset de test: {TEST_DIR}"
    )


print("\nModelo encontrado:")
print(MODELO_PATH)

print("\nDataset de prueba encontrado:")
print(TEST_DIR)


# ============================================================
# CARGAR DATASET DE TEST
# ============================================================

print("\nCargando imágenes de prueba...")

test_dataset = tf.keras.utils.image_dataset_from_directory(
    TEST_DIR,
    labels="inferred",
    label_mode="binary",
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=False
)

class_names = test_dataset.class_names

print("\nClases detectadas:")
print(class_names)


# ============================================================
# CARGAR MODELO
# ============================================================

print("\nCargando modelo...")

model = tf.keras.models.load_model(MODELO_PATH)

print("Modelo cargado correctamente.")


# ============================================================
# EVALUACIÓN GENERAL
# ============================================================

print("\n")
print("=" * 60)
print("MÉTRICAS GENERALES")
print("=" * 60)

resultados = model.evaluate(
    test_dataset,
    return_dict=True
)

for nombre, valor in resultados.items():
    print(f"{nombre}: {valor:.4f}")


# ============================================================
# OBTENER ETIQUETAS REALES
# ============================================================

print("\nObteniendo etiquetas reales...")

y_true = []

for _, etiquetas in test_dataset:
    y_true.extend(etiquetas.numpy().flatten())

y_true = np.array(y_true).astype(int)


# ============================================================
# OBTENER PREDICCIONES
# ============================================================

print("Generando predicciones...")

predicciones = model.predict(test_dataset)

y_scores = predicciones.flatten()

y_pred = (y_scores >= 0.5).astype(int)


# ============================================================
# MÉTRICAS CON SCIKIT-LEARN
# ============================================================

accuracy = accuracy_score(y_true, y_pred)

precision = precision_score(
    y_true,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y_true,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y_true,
    y_pred,
    zero_division=0
)

auc = roc_auc_score(
    y_true,
    y_scores
)


print("\n")
print("=" * 60)
print("RESULTADOS DEL MODELO")
print("=" * 60)

print(f"\nAccuracy:  {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"F1-score:  {f1:.4f}")
print(f"AUC:       {auc:.4f}")


# ============================================================
# MATRIZ DE CONFUSIÓN
# ============================================================

matriz = confusion_matrix(
    y_true,
    y_pred
)

print("\n")
print("=" * 60)
print("MATRIZ DE CONFUSIÓN")
print("=" * 60)

print("\n                Predicción")
print(f"                 {class_names[0]:>10} {class_names[1]:>10}")

print(
    f"Real {class_names[0]:>10} "
    f"{matriz[0][0]:>10} {matriz[0][1]:>10}"
)

print(
    f"Real {class_names[1]:>10} "
    f"{matriz[1][0]:>10} {matriz[1][1]:>10}"
)


# ============================================================
# INFORME POR CLASE
# ============================================================

print("\n")
print("=" * 60)
print("INFORME DE CLASIFICACIÓN")
print("=" * 60)

print(
    classification_report(
        y_true,
        y_pred,
        target_names=class_names,
        zero_division=0
    )
)


# ============================================================
# GUARDAR MATRIZ DE CONFUSIÓN
# ============================================================

ruta_matriz = BASE_DIR / "matriz_confusion.txt"

with open(ruta_matriz, "w", encoding="utf-8") as archivo:

    archivo.write("MATRIZ DE CONFUSIÓN - SKINCHECK\n\n")

    archivo.write(
        f"                Predicción\n"
        f"                 {class_names[0]:>10} "
        f"{class_names[1]:>10}\n"
    )

    archivo.write(
        f"Real {class_names[0]:>10} "
        f"{matriz[0][0]:>10} {matriz[0][1]:>10}\n"
    )

    archivo.write(
        f"Real {class_names[1]:>10} "
        f"{matriz[1][0]:>10} {matriz[1][1]:>10}\n"
    )

print("\nMatriz guardada en:")
print(ruta_matriz)


print("\n")
print("=" * 60)
print("EVALUACIÓN FINALIZADA")
print("=" * 60)