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

                width:50mm;

                margin:0;

                padding:0.5mm;

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

                margin-bottom:1px;
            }

            .subtitulo{

                font-size:11px;

                font-weight:bold;

                margin-bottom:8px;
            }

            .direccion{

                font-size:11px;

                font-weight:bold;

                margin-bottom:2px;
            }

            .telefonos{

                font-size:9px;

                font-weight:bold;

                margin-bottom:10px;
            }

            .linea{

                border-top:1px dashed #000;

                margin:5px 0;
            }

            .titulo{

                font-size:13px;

                font-weight:bold;

                margin-bottom:8px;

                text-align:center;
            }

            .ticket{

                font-size:20px;

                font-weight:bold;

                text-align:center;

                margin:8px 0;
            }

            .dato{

                margin:4px 0;

                font-size:11px;

                line-height:1;
            }

            .dato span{

                font-weight:bold;
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

                margin-top:5px;

                text-align:center;

                font-size:11px;

                font-weight:bold;
            }

            .total{

                text-align:center;

                font-size:20px;

                font-weight:bold;

                margin:18px 0;
            }

            .pagado{

                text-align:center;

                font-size:16px;

                font-weight:bold;

                margin-top:10px;
            }

            @media print {

                @page {

                    size: 58mm auto;

                    margin: 0;
                }

                html,
                body {

                    width: 58mm !important;

                    min-height: auto !important;

                    height: auto !important;

                    margin: 0 !important;

                    padding: 2mm !important;

                    overflow: hidden !important;
                }

                .linea:last-of-type {

                    margin-bottom: 0 !important;
                }

                .footer {

                    margin-bottom: 0 !important;

                    padding-bottom: 0 !important;
                }
            }

        </style>

    `;
}