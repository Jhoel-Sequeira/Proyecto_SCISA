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
var canvas1 = document.getElementById("signature");
var w = window.innerWidth;
var h = window.innerHeight;

// Como el lienzo no tiene ningún tamaño, lo especificaremos con JS
// El ancho del canvas será el ancho del dispositivo.
canvas1.width = w;
// La altura del lienzo será (casi) la tercera parte de la altura de la pantalla.
canvas1.height = h/2.5;

var signaturePad = new SignaturePad(canvas1,{
    dotSize: 1
});
var imageURI;
document.getElementById("reset").addEventListener("click",function(e){
    // Limpia el lienzo
    signaturePad.clear();
},false);
function pdf(){
    alert('dentro')
    
}

document.onreadystatechange = function () {
    if (document.readyState === 'complete') {
    }
}

const saveReport = (event) => {
    event.preventDefault();
    const formData = new FormData(document.getElementById('addReport'));
    /*CREAR EL INPUT CON LA IMAGEN*/
    document.getElementById("export").click();
    const image = document.createElement('input');
    image.setAttribute('type', 'image');
    image.src = imageURI; 
    image.value = imageURI;
    formData.append('signature',image.value);
    const request = new XMLHttpRequest();
    request.open('POST', '/reporte');
    request.onload = () => {
        const data=JSON.parse(request.responseText);
        if(data.status == 200){
            alert('Reporte creado');
            window.location.replace('/home');
        }
        else{
            alert('Error al crear el reporte, revise los datos');
        }
    }
    request.send(formData);
}