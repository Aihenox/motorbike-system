// ==========================================
// DASHBOARD PRINCIPAL LAVADERO
// ==========================================

// ==========================================
// VARIABLES GLOBALES
// ==========================================
let cortesias = [];

let mostrarTodas = false;

// ==========================================
// RELOJ
// ==========================================
function actualizarFechaHora(){

    const ahora = new Date();

    const dia = String(
        ahora.getDate()
    ).padStart(2,"0");

    const mes = String(
        ahora.getMonth()+1
    ).padStart(2,"0");

    const anio = ahora.getFullYear();

    const horas = String(
        ahora.getHours()
    ).padStart(2,"0");

    const minutos = String(
        ahora.getMinutes()
    ).padStart(2,"0");

    const segundos = String(
        ahora.getSeconds()
    ).padStart(2,"0");

    document.getElementById(

        "fechaHora"

    ).textContent =

        `${dia}/${mes}/${anio} ${horas}:${minutos}:${segundos}`;

}

// ==========================================
// CARGAR CORTESIAS
// ==========================================
async function cargarCortesias(){

    try{

        const response = await fetch(

            "/lavadero/cortesias"

        );

        const data = await response.json();
        console.log("Cortesías:", data);
        if(

            data.success

        ){

            cortesias = data.cortesias;

            renderizarCortesias();

        }

    }

    catch(error){

        console.error(

            error

        );

    }

}

// ==========================================
// MOSTRAR CORTESIAS
// ==========================================
function renderizarCortesias(){

    const listaMostrar = mostrarTodas

    ? cortesias

    : cortesias.slice(0, 5);

    const badge = document.getElementById(

        "lblTotalCortesias"

    );

    const lista = document.getElementById(

        "listaCortesias"

    );

    badge.textContent = cortesias.length;

    lista.innerHTML = "";

    if(

        cortesias.length === 0

    ){

        lista.innerHTML = `

            <div
                class="text-center text-muted">

                No hay vehículos próximos
                a una cortesía.

            </div>

        `;

        return;

    }

    listaMostrar.forEach(item=>{

        lista.innerHTML += `

            <div class="mb-3">

                <div class="d-flex justify-content-between">

                    <strong>

                        ${item.placa}

                    </strong>

                    <span>

                        ${item.avance}/5

                    </span>

                </div>

                <div class="progress mt-1">

                    <div

                        class="progress-bar bg-success"

                        style="width:${item.progreso}%">

                        ${item.progreso}%

                    </div>

                </div>

                <small class="text-muted">

                    ${item.lavados_totales} lavados registrados

                </small>

            </div>

        `;

    });

    // ==========================================
    // BOTON MOSTRAR MAS
    // ==========================================
    if(cortesias.length > 5){

        lista.innerHTML += `

            <div class="text-center mt-3">

                <button

                    id="btnMostrarCortesias"

                    class="btn btn-sm btn-outline-success">

                    ${

                        mostrarTodas

                        ? "Mostrar menos ▲"

                        : `Mostrar ${cortesias.length - 5} más ▼`

                    }

                </button>

            </div>

        `;

        document.getElementById(

            "btnMostrarCortesias"

        ).addEventListener(

            "click",

            () => {

                mostrarTodas = !mostrarTodas;

                renderizarCortesias();

            }

        );

    }

}

// ==========================================
// EVENTO LOAD
// ==========================================
window.addEventListener(

    "load",

    () => {

        actualizarFechaHora();

        setInterval(

            actualizarFechaHora,

            1000

        );

        cargarCortesias();

    }

);