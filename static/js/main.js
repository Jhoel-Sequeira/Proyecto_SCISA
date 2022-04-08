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

function solicitud() {
    var solicitud = document.querySelector(".div-solicitud");
    if (solicitud.style.display === "none") {
        solicitud.style.display = "block";
    } else {
        solicitud.style.display = "none";
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
// Esto es para cambiar los colores de la tabla
// var x, x1, x2;
// x = document.querySelector(".textoc").textContent;
// x1 = document.querySelector(".textoi").textContent;
// x2 = document.querySelector(".textop").textContent;



// document.querySelector(".completo").style.backgroundColor = "green";
// document.querySelector(".textoc").style.color = "White";

// document.querySelector(".incompleto").style.backgroundColor = "red";
// document.querySelector(".textoi").style.color = "White";

// document.querySelector(".progreso").style.backgroundColor = "yellow";
// document.querySelector(".textop").style.color = "black";
// vista empleado




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
            label: 'Cantidad de Proyectos',
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
        }
    }
});