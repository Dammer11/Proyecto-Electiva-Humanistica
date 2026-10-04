/* =========================================================
   ANÁLISIS DE LESIÓN
   ========================================================= */

const imagenInput = document.getElementById("imagenInput");
const btnSeleccionar = document.getElementById("btnSeleccionar");
const btnCambiarImagen = document.getElementById("btnCambiarImagen");

const zonaCarga = document.getElementById("zonaCarga");
const vistaPrevia = document.getElementById("vistaPrevia");
const imagenSeleccionada = document.getElementById("imagenSeleccionada");
const nombreImagen = document.getElementById("nombreImagen");

const btnAnalizar = document.getElementById("btnAnalizar");


/* =========================================================
   SELECCIONAR IMAGEN
   ========================================================= */

if (imagenInput && btnSeleccionar) {

    btnSeleccionar.addEventListener("click", function () {
        imagenInput.click();
    });

}


/* =========================================================
   PROCESAR IMAGEN SELECCIONADA
   ========================================================= */

if (imagenInput) {

    imagenInput.addEventListener("change", function () {

        const archivo = this.files[0];

        if (!archivo) {
            return;
        }

        // Comprobar que sea una imagen
        if (!archivo.type.startsWith("image/")) {

            alert("Por favor, selecciona un archivo de imagen.");

            this.value = "";

            return;
        }


        // Crear vista previa
        const lector = new FileReader();

        lector.onload = function (evento) {

            imagenSeleccionada.src = evento.target.result;

            nombreImagen.textContent = archivo.name;

            zonaCarga.style.display = "none";

            vistaPrevia.style.display = "flex";

        };

        lector.readAsDataURL(archivo);

    });

}


/* =========================================================
   CAMBIAR IMAGEN
   ========================================================= */

if (btnCambiarImagen) {

    btnCambiarImagen.addEventListener("click", function () {

        imagenInput.value = "";

        zonaCarga.style.display = "block";

        vistaPrevia.style.display = "none";

        imagenSeleccionada.src = "";

        nombreImagen.textContent = "";

        imagenInput.click();

    });

}


/* =========================================================
   OPCIONES DE CAMBIOS
   ========================================================= */

const opcionesCambios = document.querySelectorAll(
    'input[name="cambios"]'
);

opcionesCambios.forEach(function (opcion) {

    opcion.addEventListener("change", function () {

        const opcionNinguno = document.querySelector(
            'input[name="cambios"][value="ninguno"]'
        );

        // Si selecciona "Ninguno"
        if (this.value === "ninguno" && this.checked) {

            opcionesCambios.forEach(function (otraOpcion) {

                if (otraOpcion.value !== "ninguno") {
                    otraOpcion.checked = false;
                }

            });

        }


        // Si selecciona cualquier otro cambio
        if (this.value !== "ninguno" && this.checked) {

            if (opcionNinguno) {
                opcionNinguno.checked = false;
            }

        }

    });

});


/* =========================================================
   BOTÓN ANALIZAR
   ========================================================= */

if (btnAnalizar) {

    btnAnalizar.addEventListener("click", async function () {

        // Comprobar imagen
        if (!imagenInput || !imagenInput.files.length) {

            alert(
                "Primero debes seleccionar una imagen de la lesión."
            );

            return;
        }


        // Obtener archivo seleccionado
        const imagen = imagenInput.files[0];


        // Obtener ubicación
        const ubicacion = document.getElementById("ubicacion");


        // Obtener tiempo
        const tiempo = document.getElementById("tiempo");


        // Validar ubicación
        if (!ubicacion || ubicacion.value === "") {

            alert(
                "Selecciona la ubicación de la lesión."
            );

            ubicacion.focus();

            return;
        }


        // Validar tiempo
        if (!tiempo || tiempo.value === "") {

            alert(
                "Selecciona hace cuánto notaste la lesión."
            );

            tiempo.focus();

            return;
        }


        // Obtener cambios seleccionados
        const cambios = [];

        document.querySelectorAll(
            'input[name="cambios"]:checked'
        ).forEach(function (checkbox) {

            cambios.push(checkbox.value);

        });


        // Desactivar botón mientras se analiza
        btnAnalizar.disabled = true;

        btnAnalizar.textContent = "Analizando...";


        try {

            // Crear datos para enviar al backend
            const datos = new FormData();


            // Agregar imagen
            datos.append(
                "imagen",
                imagen
            );


            // Agregar información de la lesión
            datos.append(
                "ubicacion",
                ubicacion.value
            );


            datos.append(
                "tiempo",
                tiempo.value
            );


            datos.append(
                "cambios",
                JSON.stringify(cambios)
            );


            console.log("Enviando imagen al backend...");


            // Enviar información a Flask
            const respuesta = await fetch(
                "https://skincheck-zmd0.onrender.com/predict",
                {
                    method: "POST",
                    body: datos
                }
            );


            // Convertir respuesta a JSON
            const resultado = await respuesta.json();


            console.log(
                "Respuesta del backend:",
                resultado
            );


            // Comprobar si Flask devolvió un error
            if (!respuesta.ok) {

                throw new Error(
                    resultado.error ||
                    "No fue posible analizar la imagen."
                );

            }


            // Guardar resultado
            localStorage.setItem(
                "resultadoSkinCheck",
                JSON.stringify({

                    resultado: resultado.resultado,

                    benign: resultado.benign,

                    malignant: resultado.malignant,

                    ubicacion: ubicacion.value,

                    tiempo: tiempo.value,

                    cambios: cambios

                })
            );


            // Ir a la página de resultados
            window.location.href = "resultado.html";


        } catch (error) {

            console.error(
                "Error al conectar con el backend:",
                error
            );


            alert(
                "No fue posible conectar con el servidor de SkinCheck."
            );


            // Reactivar botón
            btnAnalizar.disabled = false;

            btnAnalizar.textContent = "Analizar imagen";

        }

    });

}


/* =========================================================
   POPUPS DE INFORMACIÓN
   ========================================================= */

function abrirPopup(tipo) {

    const titulo = document.getElementById("popup-titulo");
    const texto = document.getElementById("popup-texto");
    const popup = document.getElementById("popup-info");

    if (!titulo || !texto || !popup) {
        return;
    }


    if (tipo === "informacion") {

        titulo.innerText = "Información clara";

        texto.innerHTML = `
            El cáncer de piel es una enfermedad que aparece cuando las células de la piel
            crecen de forma anormal. Esto puede ocurrir principalmente por la exposición
            prolongada a la radiación ultravioleta del sol o de fuentes artificiales.

            <br><br>

            Esta página busca explicar de forma sencilla los conceptos principales sobre
            el cáncer de piel, sus señales de alerta y sus tipos más comunes:
            carcinoma basocelular, carcinoma espinocelular y melanoma.

            <br><br>

            La información está escrita para usuarios sin conocimientos médicos, por lo
            que se evita el uso excesivo de términos técnicos y se prioriza una explicación
            clara, visual y fácil de comprender.
        `;

    }


    if (tipo === "visual") {

        titulo.innerText = "Apoyo visual";

        texto.innerHTML = `
            El apoyo visual permite que el usuario observe ejemplos de lesiones cutáneas
            y pueda relacionarlos con señales de alerta como cambios de color, forma,
            tamaño, bordes irregulares o heridas que no cicatrizan.

            <br><br>

            En el prototipo, las imágenes funcionan como material educativo y de referencia.
            Su objetivo es facilitar la comparación visual y mejorar la comprensión del
            usuario durante el proceso de orientación.

            <br><br>

            Es importante aclarar que una imagen por sí sola no permite confirmar si una
            lesión es benigna o maligna. La valoración definitiva siempre debe realizarla
            un profesional de la salud.
        `;

    }


    if (tipo === "orientacion") {

        titulo.innerText = "Orientación temprana";

        texto.innerHTML = `
            La orientación temprana consiste en ayudar al usuario a reconocer señales que
            podrían indicar la necesidad de una consulta médica. Entre estas señales se
            encuentran los cambios recientes en lunares, manchas nuevas, lesiones que
            sangran, heridas que no cicatrizan o alteraciones visibles en la piel.

            <br><br>

            El sistema de evaluación del prototipo permite complementar el análisis de una
            imagen con información proporcionada por el usuario sobre la lesión.

            <br><br>

            Este resultado no debe entenderse como diagnóstico médico. Su función es
            promover la detección temprana, la prevención y la consulta oportuna con un
            médico o dermatólogo.
        `;

    }


    popup.classList.add("activo");
}


/* ==================================================
   CERRAR POPUP
   ============================== */

function cerrarPopup() {

    const popup = document.getElementById("popup-info");

    if (!popup) {
        return;
    }

    popup.classList.remove("activo");
}


/* ====================================================
   CERRAR POPUP AL HACER CLIC FUERA
   ================================================ */

window.addEventListener("click", function (e) {

    const popup = document.getElementById("popup-info");

    if (!popup) {
        return;
    }

    if (e.target === popup) {
        cerrarPopup();
    }

});

// ============================================
// MOSTRAR RESULTADO DE SKINCHECK
// ========================================

const resultadoGuardado = localStorage.getItem(
    "resultadoSkinCheck"
);

if (resultadoGuardado) {

    const datos = JSON.parse(resultadoGuardado);


    // Resultado principal
    const resultadoTexto =
        document.getElementById("resultadoTexto");


    if (resultadoTexto) {

        if (datos.resultado === "malignant") {

            resultadoTexto.textContent =
                "Clasificación del modelo: posible patrón maligno";

        } else {

            resultadoTexto.textContent =
                "Clasificación del modelo: posible patrón benigno";

        }

    }


    // Porcentaje benigno
    const porcentajeBenigno =
        document.getElementById("porcentajeBenigno");


    if (porcentajeBenigno) {

        porcentajeBenigno.textContent =
            (datos.benign * 100).toFixed(1) + "%";

    }


    // Porcentaje maligno
    const porcentajeMaligno =
        document.getElementById("porcentajeMaligno");


    if (porcentajeMaligno) {

        porcentajeMaligno.textContent =
            (datos.malignant * 100).toFixed(1) + "%";

    }


    // Ubicación
    const resultadoUbicacion =
        document.getElementById("resultadoUbicacion");


    if (resultadoUbicacion) {

        resultadoUbicacion.textContent =
            datos.ubicacion || "No especificada";

    }


    // Tiempo
    const resultadoTiempo =
        document.getElementById("resultadoTiempo");


    if (resultadoTiempo) {

        resultadoTiempo.textContent =
            datos.tiempo || "No especificado";

    }


    // Cambios observados
    const resultadoCambios =
        document.getElementById("resultadoCambios");


    if (resultadoCambios) {

        if (
            datos.cambios &&
            datos.cambios.length > 0
        ) {

            resultadoCambios.textContent =
                datos.cambios.join(", ");

        } else {

            resultadoCambios.textContent =
                "Ninguno indicado";

        }

    }

}