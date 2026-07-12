let graficaDashboard = null;

// ==========================================
// CARGAR DASHBOARD
// ==========================================
async function cargarDashboard(){

    try{

        const filtros = obtenerFiltrosDashboard();

        const response = await fetch(

            "/lavadero/dashboard",

            {

                method:"POST",

                headers:{

                    "Content-Type":"application/json"

                },

                body:JSON.stringify(

                    filtros

                )

            }

        );

        const data = await response.json();

        document.getElementById(

            "lblTotal"

        ).textContent = data.total;

        document.getElementById(

            "lblMotos"

        ).textContent = data.motos;

        document.getElementById(

            "lblCarros"

        ).textContent = data.carros;

        document.getElementById(

            "lblPromedio"

        ).textContent = data.promedio;

        const grafica = prepararDatosGrafica(

            data.grafica

        );

        dibujarGrafica(

            grafica.labels,

            grafica.motos,

            grafica.carros,

            grafica.detalle

        );

    }

    catch(error){

        console.error(error);

    }

}

// ==========================================
// PREPARAR DATOS GRAFICA
// ==========================================
function prepararDatosGrafica(datos){

    const mapa = {};

    datos.forEach(item =>{

        if(!mapa[item.fecha]){

            mapa[item.fecha]={

                Moto:0,

                Carro:0,

                detalle:{

                    Moto:{},

                    Carro:{}

                }
            };

        }

        mapa[item.fecha][item.vehiculo] +=

            item.cantidad;

        mapa[item.fecha]
            .detalle[item.vehiculo][item.responsable] =

                item.cantidad;

    });

    const labels=[];

    const motos=[];

    const carros=[];

    Object.keys(mapa).forEach(fecha=>{

        labels.push(fecha);

        motos.push(

            mapa[fecha].Moto

        );

        carros.push(

            mapa[fecha].Carro

        );

    });

    const detalle=[];

    Object.keys(mapa).forEach(fecha=>{

        detalle.push(

            mapa[fecha].detalle

        );

    });

    return{

        labels,

        motos,

        carros,

        detalle

    };

}

// ==========================================
// OBTENER FILTROS DASHBOARD
// ==========================================
function obtenerFiltrosDashboard(){

    const vehiculos = [];

    if(document.getElementById("chkMoto").checked){

        vehiculos.push("Moto");

    }

    if(document.getElementById("chkCarro").checked){

        vehiculos.push("Carro");

    }

    const responsables = [];

    if(document.getElementById("chkAngela").checked){

        responsables.push("Angela");

    }

    if(document.getElementById("chkAngelica").checked){

        responsables.push("Angelica");

    }

    if(document.getElementById("chkAngie").checked){

        responsables.push("Angie");

    }

    if(document.getElementById("chkKarime").checked){

        responsables.push("Karime");

    }

    return{

        vehiculos,

        responsables,

        periodo:

            document.getElementById(
                "periodoDashboard"
            ).value,

        fecha_inicio:

            document.getElementById(
                "dashboardFechaInicio"
            ).value,

        fecha_fin:

            document.getElementById(
                "dashboardFechaFin"
            ).value
    };

}

// ==========================================
// DIBUJAR LA GRAFICA
// ==========================================
function dibujarGrafica(labels, motos, carros, detalle){

    const canvas = document.getElementById(
        "graficaDashboardLavadero"
    );

    if(!canvas){
        return;
    }

    if(graficaDashboard){
        graficaDashboard.destroy();
    }

    graficaDashboard = new Chart(

        canvas,

        {

            type: "bar",

            data: {

                labels: labels,

                datasets: [

                    {

                        label: "Moto",

                        data: motos,

                        backgroundColor: "#0d6efd"

                    },

                    {

                        label: "Carro",

                        data: carros,

                        backgroundColor: "#fd7e14"

                    }

                ],
                detalle: detalle
            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                interaction:{

                    mode:"index",

                    intersect:false

                },

                plugins:{

                    tooltip:{

                        callbacks:{

                            label:function(context){

                                const detalle = context.chart.data.detalle;

                                const indice = context.dataIndex;

                                const vehiculo = context.dataset.label;

                                const responsables = detalle[indice][vehiculo];

                                const lineas = [];

                                lineas.push(

                                    vehiculo +

                                    ": " +

                                    context.raw

                                );

                                Object.entries(

                                    responsables

                                )

                                .sort(

                                    (a, b) => b[1] - a[1]

                                )

                                .forEach(

                                    ([nombre, cantidad]) => {

                                        lineas.push(

                                            "   • " +

                                            nombre +

                                            ": " +

                                            cantidad

                                        );

                                    }

                                );

                                return lineas;

                            }

                        }

                    },

                    legend:{

                        position:"bottom"

                    }

                },

                scales:{

                    y:{

                        beginAtZero:true,

                        title:{

                            display:true,

                            text:"Cantidad de lavados"

                        }

                    },

                    x:{

                        title:{

                            display:true,

                            text:"Fecha"

                        }

                    }

                }

            }

        }

    );

}

// ==========================================
// ACTIVAR EVENTOS FILTROS
// ==========================================
function activarEventosDashboard(){

    const controles = document.querySelectorAll(

        "#modalDashboardLavadero input, " +
        "#modalDashboardLavadero select"

    );

    controles.forEach(control => {

        control.addEventListener(

            "change",

            () => {

                // ==========================
                // CAMBIO DE PERIODO
                // ==========================
                if(control.id === "periodoDashboard"){

                    cambiarPeriodoDashboard();

                    return;

                }

                // ==========================
                // FECHA INICIO
                // ==========================
                if(control.id === "dashboardFechaInicio"){

                    const periodo = document.getElementById(
                        "periodoDashboard"
                    ).value;

                    const fechaFin = document.getElementById(
                        "dashboardFechaFin"
                    ).value;

                    if(periodo !== "mes"){

                        document.getElementById(
                            "periodoDashboard"
                        ).value = fechaFin
                            ? "rango"
                            : "dia";

                    }

                }

                // ==========================
                // FECHA FIN
                // ==========================
                if(control.id === "dashboardFechaFin"){

                    const fechaInicio = document.getElementById(
                        "dashboardFechaInicio"
                    ).value;

                    if(!fechaInicio){

                        alert(
                            "Primero seleccione la fecha inicial."
                        );

                        control.value = "";

                        return;

                    }

                    if(control.value){

                        document.getElementById(
                            "periodoDashboard"
                        ).value = "rango";

                    }

                }

                cargarDashboard();

            }

        );

    });
}

// ==========================================
// CAMBIAR PERIODO DASHBOARD
// ==========================================
function cambiarPeriodoDashboard(){

    const periodo = document.getElementById(
        "periodoDashboard"
    ).value;

    const hoy = new Date();

    const fechaHoy = hoy.toISOString()
        .split("T")[0];

    const fechaInicio = document.getElementById("dashboardFechaInicio");
    const fechaFin = document.getElementById("dashboardFechaFin");

    // limpiar
    fechaInicio.value = "";
    fechaFin.value = "";

    switch(periodo){

        case "dia":

            fechaInicio.value = fechaHoy;
            cargarDashboard();
            break;

        case "semana":

            fechaInicio.value = fechaHoy;
            cargarDashboard();
            break;

        case "mes":

            fechaInicio.value = fechaHoy;
            cargarDashboard();
            break;

        case "rango":

            break;

    }

}

// ==========================================
// EVENTO MODAL
// ==========================================
window.addEventListener(

    "load",

    function(){

        activarEventosDashboard();

        const modal = document.getElementById(

            "modalDashboardLavadero"

        );

        if(modal){

            modal.addEventListener(

                "shown.bs.modal",

                () => {

                    document.getElementById(
                        "periodoDashboard"
                    ).value = "semana";

                    cambiarPeriodoDashboard();

                }

            );

        }

    }

);

