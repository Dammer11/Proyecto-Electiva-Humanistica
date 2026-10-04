import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from pathlib import Path


# ============================================================
# CONFIGURACIÓN
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = BASE_DIR / "dataset"

TRAIN_DIR = DATASET_DIR / "train"
TEST_DIR = DATASET_DIR / "test"

IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 10
SEED = 123


print("=" * 60)
print("ENTRENAMIENTO DEL MODELO SKINCHECK")
print("=" * 60)


# ============================================================
# COMPROBAR DATASET
# ============================================================

print("\nComprobando dataset...")

print(f"Train: {TRAIN_DIR}")
print(f"Test:  {TEST_DIR}")

if not TRAIN_DIR.exists():
    raise FileNotFoundError(f"No se encontró la carpeta train: {TRAIN_DIR}")

if not TEST_DIR.exists():
    raise FileNotFoundError(f"No se encontró la carpeta test: {TEST_DIR}")

print("Dataset encontrado correctamente.")


# ============================================================
# CARGAR DATASET DE ENTRENAMIENTO
# ============================================================

print("\nCargando imágenes de entrenamiento...")

train_dataset = tf.keras.utils.image_dataset_from_directory(
    TRAIN_DIR,
    labels="inferred",
    label_mode="binary",
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=True,
    seed=SEED,
    validation_split=0.20,
    subset="training"
)


# ============================================================
# CARGAR DATASET DE VALIDACIÓN
# ============================================================

print("\nCargando imágenes de validación...")

validation_dataset = tf.keras.utils.image_dataset_from_directory(
    TRAIN_DIR,
    labels="inferred",
    label_mode="binary",
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=True,
    seed=SEED,
    validation_split=0.20,
    subset="validation"
)


# ============================================================
# CARGAR DATASET DE PRUEBA
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


# ============================================================
# MOSTRAR CLASES
# ============================================================

print("\nClases detectadas:")

class_names = train_dataset.class_names

print(class_names)

print("\nAsignación de clases:")

for numero, clase in enumerate(class_names):
    print(f"{numero} = {clase}")


# ============================================================
# MEJORAR RENDIMIENTO DEL DATASET
# ============================================================

AUTOTUNE = tf.data.AUTOTUNE

train_dataset = train_dataset.prefetch(buffer_size=AUTOTUNE)
validation_dataset = validation_dataset.prefetch(buffer_size=AUTOTUNE)
test_dataset = test_dataset.prefetch(buffer_size=AUTOTUNE)


# ============================================================
# DATA AUGMENTATION
# ============================================================

data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.05),
    layers.RandomZoom(0.10),
], name="data_augmentation")


# ============================================================
# MODELO MOBILENETV2
# ============================================================

print("\nCargando MobileNetV2...")

base_model = MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights="imagenet"
)


# Congelamos inicialmente MobileNetV2
base_model.trainable = False


# ============================================================
# CONSTRUIR MODELO
# ============================================================

inputs = layers.Input(shape=(224, 224, 3))

x = data_augmentation(inputs)

x = preprocess_input(x)

x = base_model(x, training=False)

x = layers.GlobalAveragePooling2D()(x)

x = layers.Dropout(0.30)(x)

outputs = layers.Dense(
    1,
    activation="sigmoid"
)(x)


model = models.Model(
    inputs,
    outputs,
    name="SkinCheck_MobileNetV2"
)


# ============================================================
# COMPILAR MODELO
# ============================================================

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
    loss="binary_crossentropy",
    metrics=[
        "accuracy",
        tf.keras.metrics.Precision(name="precision"),
        tf.keras.metrics.Recall(name="recall"),
        tf.keras.metrics.AUC(name="auc")
    ]
)


# ============================================================
# MOSTRAR RESUMEN
# ============================================================

print("\nResumen del modelo:")

model.summary()


# ============================================================
# CALLBACKS
# ============================================================

modelo_salida = BASE_DIR / "modelo_skincheck.keras"

callbacks = [

    tf.keras.callbacks.EarlyStopping(
        monitor="val_loss",
        patience=3,
        restore_best_weights=True
    ),

    tf.keras.callbacks.ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.5,
        patience=2,
        min_lr=0.000001
    ),

    tf.keras.callbacks.ModelCheckpoint(
        filepath=modelo_salida,
        monitor="val_loss",
        save_best_only=True
    )
]


# ============================================================
# ENTRENAMIENTO
# ============================================================

print("\n")
print("=" * 60)
print("COMENZANDO ENTRENAMIENTO")
print("=" * 60)

history = model.fit(
    train_dataset,
    validation_data=validation_dataset,
    epochs=EPOCHS,
    callbacks=callbacks
)


# ============================================================
# EVALUACIÓN FINAL
# ============================================================

print("\n")
print("=" * 60)
print("EVALUACIÓN CON EL DATASET DE TEST")
print("=" * 60)

resultados = model.evaluate(
    test_dataset,
    return_dict=True
)

for nombre, valor in resultados.items():
    print(f"{nombre}: {valor:.4f}")


# ============================================================
# GUARDAR MODELO FINAL
# ============================================================

model.save(modelo_salida)

print("\n")
print("=" * 60)
print("ENTRENAMIENTO FINALIZADO")
print("=" * 60)

print(f"\nModelo guardado en:")
print(modelo_salida)