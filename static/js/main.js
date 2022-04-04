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

function empleados() {
    var empleados = document.querySelector(".div-reportes");
    if (empleados.style.display === "none") {
        empleados.style.display = "block";
    } else {
        empleados.style.display = "none";
    }
}
// Grafico
const ctx = document.getElementById('myChart');
const myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Incompletos', 'Completados', 'En Progreso'],
        datasets: [{
            label: '# of Votes',
            data: [12, 19, 3],
            backgroundColor: [
                'red',
                'green',
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




// Esto es para cambiar los colores de la tabla
var x;

x = document.getElementById("texto").textContent;
x1 = document.getElementById("texto1").textContent;
x2 = document.getElementById("texto2").textContent;
if (x = "Completado") {
    document.getElementById("estado").style.backgroundColor = "green";
    document.getElementById("texto").style.color = "White";
}
if (x1 = "Incompleto") {
    document.getElementById("Incompleto").style.backgroundColor = "red";
    document.getElementById("texto1").style.color = "White";
}
if (x2 = "Progreso") {
    document.getElementById("Progreso").style.backgroundColor = "yellow";
    document.getElementById("texto2").style.color = "black";
}