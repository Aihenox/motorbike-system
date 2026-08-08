// ==========================================
// HEADER EMPRESA
// ==========================================
function generarHeaderTicket(){

    return `

        <div class="center">

            <img
                src="/static/img/logo.png"
                class="logo"
            >

            <div class="empresa">

                ESPUMOSO MOTORBIKE

            </div>

            <div class="subtitulo">

                PARQUEADERO Y LAVADERO

            </div>

            <div class="direccion">

                Cra 11 Calle 22 Esquina

            </div>

            <div class="telefonos">

                Tel: 3207081059

                <br>

                WhatsApp: 3217343167

            </div>

        </div>

    `;
}


// ==========================================
// ESTILOS BASE
// ==========================================
function generarEstilosTicket(){

    return `

        <style>

            *{

                margin:0;

                padding:0;

                box-sizing:border-box;
            }

            @page{

                size:58mm auto;

                margin:0;
            }

            html,
            body{

                width:58mm;

                margin:0;

                padding:2mm;

                font-family:'Courier New', monospace;

                overflow:hidden;
            }

            .center{

                text-align:center;
            }

            .logo{

                width:60px;

                margin-bottom:6px;
            }

            .empresa{

                font-size:14px;

                font-weight:bold;
            }

            .subtitulo{

                font-size:11px;

                font-weight:bold;

                margin-bottom:8px;
            }

            .direccion{

                font-size:11px;

                font-weight:bold;
            }

            .telefonos{

                font-size:9px;

                font-weight:bold;

                margin-bottom:10px;
            }

            .linea{

                border-top:1px dashed #000;

                margin:6px 0;
            }

            .titulo{

                font-size:13px;

                font-weight:bold;

                text-align:center;

                margin-bottom:8px;
            }

            .ticket{

                font-size:20px;

                font-weight:bold;

                text-align:center;

                margin:10px 0;
            }

            .dato{

                margin:4px 0;

                font-size:11px;
            }

            .barcode{

                text-align:center;

                margin-top:10px;
            }

            .mensaje{

                text-align:center;

                margin-top:10px;

                font-size:12px;

                font-weight:bold;
            }

            .footer{

                margin-top:10px;

                text-align:center;

                font-size:11px;

                font-weight:bold;
            }

            .total{

                text-align:center;

                font-size:20px;

                font-weight:bold;

                margin:15px 0;
            }

            .pagado{

                text-align:center;

                font-size:16px;

                font-weight:bold;

                margin-top:10px;
            }

        </style>

    `;
}

// ==========================================
// ABRIR TICKET
// ==========================================
function abrirTicket(html, ticketId){

    const ventana = window.open(
        "",
        "_blank",
        "width=250,height=700"
    );

    ventana.document.write(html);

    ventana.document.close();

    // ==========================================
    // CUANDO CARGA
    // ==========================================
    ventana.onload = function(){

        const script = ventana.document.createElement(
            "script"
        );

        script.src =
            "https://cdn.jsdelivr.net/npm/jsbarcode@3.11.6/dist/JsBarcode.all.min.js";

        script.onload = function(){

            ventana.JsBarcode(

                ventana.document.getElementById(
                    "barcode"
                ),

                String(ticketId).padStart(
                    6,
                    "0"
                ),

                {

                    format: "CODE128",

                    width: 2,

                    height: 50,

                    displayValue: true,

                    fontSize: 16,

                    margin: 10
                }
            );

            ventana.print();
        };

        ventana.document.head.appendChild(
            script
        );
    };
}

// ==========================================
// TICKET INGRESO
// ==========================================
function generarTicketIngreso(data){

    return `

    <html>

    <head>

        <title>
            Ticket Ingreso
        </title>

        ${generarEstilosTicket()}

    </head>

    <body>

        ${generarHeaderTicket()}

        <div class="linea"></div>

        <div class="titulo">

            RECIBO DE INGRESO

        </div>

        <div class="ticket">

            #${String(data.ticket).padStart(6, "0")}

        </div>

        <div class="linea"></div>

        <div class="dato">

            <strong>PLACA:</strong>

            <strong>${data.placa}</strong>

        </div>

        <div class="dato">

            <strong>VEHÍCULO:</strong>

            <strong>${data.tipo}</strong>

        </div>

        <div class="dato">

            <strong>INGRESO:</strong>

            <Strong>${data.hora}</strong>

        </div>

        <div class="linea"></div>

        <div class="barcode">

            <svg id="barcode"></svg>

        </div>

        <div class="mensaje">

            CONSERVE SU TICKET

        </div>

        <div class="linea"></div>

        <div class="footer">

            ¡Gracias por preferirnos!

        </div>

    </body>

    </html>

    `;
}


// ==========================================
// TICKET SALIDA
// ==========================================
function generarTicketSalida(data){

    return `

    <html>

    <head>

        <title>
            Ticket Salida
        </title>

        ${generarEstilosTicket()}

    </head>

    <body>

        ${generarHeaderTicket()}

        <div class="linea"></div>

        <!-- TITULO -->
        <div class="titulo">

            RECIBO DE SALIDA

        </div>

        <!-- TICKET -->
        <div class="ticket">

            #${String(data.ticket).padStart(6, "0")}

        </div>

        <div class="linea"></div>

        <!-- DATOS -->
        <div class="dato">

            <span>
                PLACA:
            </span>

            <strong>
                ${data.placa}
            </strong>

        </div>

        <div class="dato">

            <span>
                VEHÍCULO:
            </span>

            <strong>
                ${data.tipo}
            </strong>

        </div>

        <div class="dato">

            <span>
                INGRESO:
            </span>

            <strong>
                ${data.hora_ingreso}
            </strong>

        </div>

        <div class="dato">

            <span>
                SALIDA:
            </span>

            <strong>
                ${data.hora_salida}
            </strong>

        </div>

        <div class="dato">

            <span>
                TIEMPO:
            </span>

            <strong>
                ${data.tiempo}
            </strong>

        </div>

        <div class="linea"></div>

        <!-- TOTAL -->
        <div class="total">

            $ ${data.valor}

        </div>

        <!-- PAGADO -->
        <div class="pagado">

            ✓ PAGO REALIZADO

        </div>

        <div class="linea"></div>

        <!-- FOOTER -->
        <div class="footer">

            ¡Gracias por su visita!

        </div>

    </body>

    </html>

    `;
}

// ==========================================
// TICKET MENSUALIDAD
// ==========================================
function generarTicketMensualidad(data){

    return `

    <html>

    <head>

        <title>

            Mensualidad

        </title>

        ${generarEstilosTicket()}

    </head>

    <body>

        ${generarHeaderTicket()}

        <div class="linea"></div>

        <div class="titulo">

            MENSUALIDAD

        </div>

        <div class="ticket">

            ${data.placa}

        </div>

        <div class="linea"></div>

        <div class="dato">

            <strong>PROPIETARIO:</strong><br>

            <strong>${data.propietario}</strong>

        </div>

        <div class="dato">

            <strong>VEHÍCULO:</strong>

            <strong>${data.tipo}</strong>

        </div>

        <div class="dato">

            <strong>PLACA:</strong>

            <strong>${data.placa}</strong>

        </div>

        <div class="linea"></div>

        <div class="dato">

            <strong>INICIO:</strong>

            <strong>${data.fecha_inicio}</strong>

        </div>

        <div class="dato">

            <strong>VENCE:</strong>

            <strong>${data.fecha_fin}</strong>

        </div>

        <div class="dato">

            <strong>ESTADO:</strong>

            <strong>${data.estado}</strong>

        </div>

        <div class="footer">

            Gracias por preferirnos

        </div>

    </body>

    </html>

    `;
}