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