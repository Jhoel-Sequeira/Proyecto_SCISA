addEventListener('DOMContentLoaded', () => {
    const btn_menu = document.querySelector('.btn_menu')
    if (btn_menu) {
        btn_menu.addEventListener('click', () => {
            const menu_items = document.querySelector('.menu_items')
            menu_items.classList.toggle('show')
        })
    }


})

function empleados() {
    var empleados = document.querySelector(".div-empleados");
    if (empleados.style.display === "none") {
        empleados.style.display = "block";
    } else {
        empleados.style.display = "none";
    }
}

function calendario() {
    var calendario = document.querySelector(".div-calendario");
    if (calendario.style.display === "none") {
        calendario.style.display = "block";
    } else {
        calendario.style.display = "none";
    }
}