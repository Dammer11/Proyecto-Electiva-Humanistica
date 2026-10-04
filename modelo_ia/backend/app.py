from flask import Flask, request, jsonify
from flask_cors import CORS

import tensorflow as tf
import numpy as np

from PIL import Image
from pathlib import Path


# ============================================================
# CONFIGURACIÓN
# ============================================================

app = Flask(__name__)

CORS(app)


BASE_DIR = Path(__file__).resolve().parent.parent

MODELO_PATH = BASE_DIR / "modelo_skincheck.keras"

IMG_SIZE = (224, 224)


# ============================================================
# CARGAR MODELO
# ============================================================

print("Cargando modelo SkinCheck...")

modelo = tf.keras.models.load_model(MODELO_PATH)

print("Modelo cargado correctamente.")


# ============================================================
# RUTA PRINCIPAL
# ============================================================

@app.route("/")
def inicio():
    return "Backend de SkinCheck funcionando correctamente."


# ============================================================
# PREDICCIÓN
# ============================================================

@app.route("/predict", methods=["POST"])
def predecir():

    if "imagen" not in request.files:
        return jsonify({
            "error": "No se recibió ninguna imagen."
        }), 400

    archivo = request.files["imagen"]

    if archivo.filename == "":
        return jsonify({
            "error": "No se seleccionó ninguna imagen."
        }), 400

    try:

        # ----------------------------------------------------
        # Abrir imagen
        # ----------------------------------------------------

        imagen = Image.open(archivo).convert("RGB")

        # ----------------------------------------------------
        # Redimensionar
        # ----------------------------------------------------

        imagen = imagen.resize(IMG_SIZE)

        # ----------------------------------------------------
        # Convertir a array
        # ----------------------------------------------------

        imagen_array = np.array(imagen)

        # ----------------------------------------------------
        # Preparar imagen para MobileNetV2
        # ----------------------------------------------------

        imagen_array = imagen_array.astype("float32")

        imagen_array = tf.keras.applications.mobilenet_v2.preprocess_input(
            imagen_array
        )

        # Agregar dimensión del lote
        imagen_array = np.expand_dims(
            imagen_array,
            axis=0
        )

        # ----------------------------------------------------
        # Realizar predicción
        # ----------------------------------------------------

        prediccion = modelo.predict(
            imagen_array,
            verbose=0
        )

        puntuacion_maligna = float(prediccion[0][0])

        puntuacion_benigna = 1 - puntuacion_maligna

        # ----------------------------------------------------
        # Determinar clase
        # ----------------------------------------------------

        if puntuacion_maligna >= 0.5:
            resultado = "malignant"
        else:
            resultado = "benign"

        # ----------------------------------------------------
        # Respuesta
        # ----------------------------------------------------

        return jsonify({
            "resultado": resultado,
            "benign": puntuacion_benigna,
            "malignant": puntuacion_maligna
        })

    except Exception as error:

        print("Error durante la predicción:", error)

        return jsonify({
            "error": "No fue posible analizar la imagen."
        }), 500


# ============================================================
# INICIAR SERVIDOR
# ============================================================

if __name__ == "__main__":
    app.run(
        debug=True
    )