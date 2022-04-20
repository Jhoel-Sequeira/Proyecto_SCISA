addEventListener('DOMContentLoaded', () => {
    const btn_menu = document.querySelector('.btn_menu')
    if (btn_menu) {
        btn_menu.addEventListener('click', () => {
            const menu_items = document.querySelector('.menu_items')
            menu_items.classList.toggle('show')
        })
    }
    
})
    
$(Document).ready(function() {
    $("#exampleModal").modal("show")
})
var canvas = document.getElementById("signature");
var w = window.innerWidth;
var h = window.innerHeight;

// Como el lienzo no tiene ningún tamaño, lo especificaremos con JS
// El ancho del canvas será el ancho del dispositivo.
canvas.width = w;
// La altura del lienzo será (casi) la tercera parte de la altura de la pantalla.
canvas.height = h/2.5;

var signaturePad = new SignaturePad(canvas,{
    dotSize: 1
});
document.getElementById("export").addEventListener("click",function(e){
    // Siéntete libre de hacer lo que quieras con la imagen
    // como exportar a un servidor o incluso guardarlo en el dispositivo.
    var imageURI = signaturePad.toDataURL();    
    document.getElementById("preview").src = imageURI;
},false);

document.getElementById("reset").addEventListener("click",function(e){
    // Limpia el lienzo
    signaturePad.clear();
},false);

function reportes() {
    var reportes = document.querySelector(".div-reportes");
    if (reportes.style.display === "none") {
        reportes.style.display = "block";
    } else {
        reportes.style.display = "none";
    }
}

function notificacion() {
    var solicitud = document.querySelector(".div-notificacion");
    if (solicitud.style.display === "none") {
        solicitud.style.display = "block";
    } else {
        solicitud.style.display = "none";
    }
}
function notificacion1() {
    var solicitud = document.querySelector(".div-notificacion1");
    if (solicitud.style.display === "none") {
        solicitud.style.display = "block";
    } else {
        solicitud.style.display = "none";
    }
}
function notificacion1emp() {
    var solicitud = document.querySelector(".div-notificacion1emp");
    if (solicitud.style.display === "none") {
        solicitud.style.display = "block";
    } else {
        solicitud.style.display = "none";
    }
}
function solicitud() {
    var solicitud = document.querySelector(".div-solicitud");
    if (solicitud.style.display === "none") {
        solicitud.style.display = "block";
    } else {
        solicitud.style.display = "none";
    }
}
function reporte() {
    var solicitud = document.querySelector(".div-reportes");
    if (solicitud.style.display === "none") {
        solicitud.style.display = "block";
    } else {
        solicitud.style.display = "none";
    }
}
function reportellen() {
    var solicitud = document.querySelector(".div-reportes-llenar");
    if (solicitud.style.display === "none") {
        solicitud.style.display = "block";
    } else {
        solicitud.style.display = "none";
    }
}

function tareas() {
    var tareas = document.querySelector(".div-tareas");
    if (tareas.style.display === "none") {
        tareas.style.display = "block";
    } else {
        tareas.style.display = "none";
    }
}

function not() {
    var solicitud = document.querySelector(".div-not");
    if (solicitud.style.display === "none") {
        solicitud.style.display = "block";
    } else {
        solicitud.style.display = "none";
    }
}



// Grafico
var1 = document.getElementById('completado').innerHTML
var2 = document.getElementById('incompleto').innerHTML
var3 = document.getElementById('progreso').innerHTML
const ctx = document.getElementById('myChart');
const myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Incompletos', 'Completados', 'En Progreso'],
        datasets: [{
            label: 'Estadi',
            data: [var2, var1, var3],
            backgroundColor: [
                '#c63637',
                '#006c0f',
                'yellow'

            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        },
        plugins: {
            legend: {
                display: false
            }
        }
    }
});