from flask import Flask, request, jsonify
from flask_cors import CORS

import tensorflow as tf
import numpy as np

from PIL import Image
from pathlib import Path

app = Flask(__name__)
CORS(app)

BASE_DIR = Path(__file__).resolve().parent.parent
MODELO_PATH = BASE_DIR / "modelo_skincheck.keras"
IMG_SIZE = (224, 224)

print("Cargando modelo SkinCheck...")
modelo = tf.keras.models.load_model(MODELO_PATH)
print("Modelo cargado correctamente.")


@app.route("/")
def inicio():
    return "Backend de SkinCheck funcionando correctamente."


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
        imagen = Image.open(archivo).convert("RGB")
        imagen = imagen.resize(IMG_SIZE)

        imagen_array = np.array(imagen).astype("float32")

        imagen_array = tf.keras.applications.mobilenet_v2.preprocess_input(
            imagen_array
        )

        imagen_array = np.expand_dims(imagen_array, axis=0)

        prediccion = modelo.predict(
            imagen_array,
            verbose=0
        )

        puntuacion_maligna = float(prediccion[0][0])
        puntuacion_benigna = 1 - puntuacion_maligna

        if puntuacion_maligna >= 0.5:
            resultado = "malignant"
        else:
            resultado = "benign"

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


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )