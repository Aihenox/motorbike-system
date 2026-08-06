// ==========================================
// ABRIR TICKET LAVADERO
// ==========================================
function abrirTicketLavadero(html){

    const ventana = window.open(

        "",

        "ticket_lavado",

        "width=250,height=700"
    );

    if(!ventana){

        alert(
            "Permita ventanas emergentes para imprimir."
        );

        return;
    }

    ventana.document.open();

    ventana.document.write(
        html
    );

    ventana.document.close();

    setTimeout(() => {

        ventana.focus();

        ventana.print();

    }, 500);
}


// ==========================================
// GENERAR TICKET LAVADERO
// ==========================================
function generarTicketLavadero(data){

    let cortesia = "";

    if(data.gratis){

        cortesia = `

            <div class="linea"></div>

            <div
                style="
                    text-align:center;
                    font-size:16px;
                    font-weight:bold;
                "
            >

                🎉 LAVADO DE CORTESÍA

            </div>

            <div
                style="
                    text-align:center;
                    margin-top:5px;
                "
            >

                Cliente frecuente

            </div>

        `;
    }

    return `

    <html>

    <head>

        <title>

            Recibo Lavadero

        </title>

        ${generarEstilosTicket()}

    </head>

    <body>

        ${generarHeaderTicket()}

        <div class="linea"></div>

        <div class="titulo">

            RECIBO DE LAVADO

        </div>

        <div class="linea"></div>

        <div class="dato">

            <strong>PLACA:</strong>

            <strong>${data.placa}</strong>

        </div>

        <div class="dato">

            <span>

                VEHÍCULO:

            </span>

            <strong>

                ${data.vehiculo}

            </strong>

        </div>

        <div class="dato">

            <span>

                SERVICIO:

            </span>

            <strong>

                ${data.tipo_lavado}

            </strong>

        </div>

        <div class="dato">

            <span>

                RESPONSABLE:

            </span>

            <strong>

                ${data.responsable}

            </strong>

        </div>

        <div class="dato">

            <span>

                FECHA:

            </span>

            <strong>

                ${data.fecha}

            </strong>

        </div>

        ${cortesia}

        <div class="linea"></div>

        <div class="total">

            $ ${data.valor}

        </div>

        <div class="pagado">

            ✓ SERVICIO REGISTRADO

        </div>

        <div class="linea"></div>

        <div class="footer">

            ¡Gracias por preferirnos!

        </div>

    </body>

    </html>

    `;
}