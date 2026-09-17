let preguntas = [
    {
        texto: "¿La lesión tiene bordes irregulares?",
        imagen: "img/ejemplo1.jpg"
    },
    {
        texto: "¿Tiene varios colores (negro, marrón, rojo)?",
        imagen: "img/ejemplo2.jpg"
    },
    {
        texto: "¿Ha cambiado de tamaño recientemente?",
        imagen: "img/ejemplo3.jpg"
    }
];

let indice = 0;
let respuestasSi = 0;

function responder(respuesta) {
    if (respuesta === "si") {
        respuestasSi++;
    }

    indice++;

    if (indice < preguntas.length) {
        document.getElementById("pregunta").innerText = preguntas[indice].texto;
        document.getElementById("imagen").src = preguntas[indice].imagen;
    } else {
        localStorage.setItem("resultado", respuestasSi);
        window.location.href = "resultado.html";
    }
}

if (window.location.pathname.includes("resultado.html")) {
    let resultado = localStorage.getItem("resultado");

    let texto = "";

    if (resultado >= 2) {
        texto = "Posible riesgo. Se recomienda consultar a un dermatólogo.";
    } else {
        texto = "Riesgo bajo, pero mantén vigilancia.";
    }

    document.getElementById("resultadoTexto").innerText = texto;
}



function abrirPopup(tipo) {
    const titulo = document.getElementById("popup-titulo");
    const texto = document.getElementById("popup-texto");
    const popup = document.getElementById("popup-info");

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

            El sistema de preguntas del prototipo permite guiar al usuario mediante
            respuestas simples de “sí” o “no”, generando una recomendación preventiva
            según las respuestas seleccionadas.

            <br><br>

            Este resultado no debe entenderse como diagnóstico médico. Su función es
            promover la detección temprana, la prevención y la consulta oportuna con un
            médico o dermatólogo.
        `;
    }

    popup.classList.add("activo");
}
function cerrarPopup() {
    const popup = document.getElementById("popup-info");

    popup.classList.remove("activo");
}
window.addEventListener("click", function(e) {

    const popup = document.getElementById("popup-info");

    if (e.target === popup) {
        cerrarPopup();
    }
});