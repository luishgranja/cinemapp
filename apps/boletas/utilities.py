import io

from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF
from datetime import datetime
import locale
from django.core import signing
from django.core.signing import Signer
from django.urls import reverse



def generar_pdf_boleta(boleta):
    response = HttpResponse(content_type='application/force-download')
    response['Content-Disposition'] = 'inline; filename="Boleta - "' + str(boleta.id) + '-' + str(boleta.cedula) + '".pdf"'\
        .format(title="Boleta - " + str(boleta.id) + str(boleta.cedula))

    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Configuracion de pagina
    p.setPageSize((200, 350))

    # Signature data
    code = signing.dumps(str(boleta.id), compress=True)
    url = reverse('boletas:validar_boleta', args=[code])

    # Path
    # TODO Cambiar dependiendo de dominio
    path = 'http://localhost:8000'

    # signer = Signer()
    # value = signer.sign(str(boleta.id))
    # url = reverse('boletas:validar_boleta', args=[value])

    # codigo QR
    qr = QrCodeWidget(path + url, barLevel='H')
    b = qr.getBounds()
    w = b[2] - b[0]
    h = b[3] - b[1]
    d = Drawing(45, 45, transform=[45. / w, 0, 0, 45. / h, 0, 0])
    d.add(qr)
    renderPDF.draw(d, p, 140, 300)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.

    # titulo
    p.setFont("Helvetica", 14)
    p.drawCentredString(100, 320, "CINEMAPP")

    # pelicula
    p.setFont("Helvetica", 8)
    p.drawString(20, 300, "Pelicula")

    p.setFillColor(colors.black)
    len_pelicula = len(str(boleta.funcion.pelicula.nombre))
    rec_size = 8 * len_pelicula
    if rec_size > 200:
        rec_size = 180
    p.rect(20, 276, rec_size, 14, fill=1)
    p.setFillColor(colors.white)
    p.setFont("Helvetica", 10)
    p.drawString(20, 280, boleta.funcion.pelicula.nombre)

    # Español en Windows
    # locale.setlocale(locale.LC_ALL, "esp")
    # Español en Linux
    locale.setlocale(locale.LC_ALL, "es_ES.UTF-8")
    # funcion
    p.setFillColor(colors.black)
    p.setFont("Helvetica", 8)
    p.drawString(20, 260, "Fecha función")
    p.setFont("Helvetica", 12)

    p.drawString(20, 240, str(boleta.funcion.fecha_funcion.strftime("%A %d %B %Y "))
                 + str(boleta.funcion.hora_funcion.strftime("%H:%M")))

    # ubicacion
    p.setFillColor(colors.black)
    p.setFont("Helvetica", 8)
    p.drawString(20, 220, "Ubicación")

    p.rect(20, 196, 80, 14, fill=1)
    p.setFillColor(colors.white)
    p.setFont("Helvetica", 12)
    p.drawString(20, 200, str(boleta.funcion.sala))

    # silla
    p.setFillColor(colors.black)
    p.setFont("Helvetica", 8)
    p.drawString(20, 180, "Silla")

    p.rect(20, 156, 20, 14, fill=1)
    p.setFillColor(colors.white)
    p.setFont("Helvetica", 12)
    p.drawString(20, 160, boleta.silla.nombre)

    # valor total
    p.setFillColor(colors.black)
    p.setFont("Helvetica", 8)
    p.drawString(20, 140, "Valor total")
    p.drawString(20, 130, "$" + str(boleta.total))

    # fecha compra
    p.drawString(20, 110, "Fecha compra")
    p.drawString(20, 100, str(boleta.fecha_compra.strftime("%d-%m-%Y %H:%M")))

    p.drawString(20, 80, "Sucursal")
    p.drawString(20, 70, boleta.funcion.sala.sucursal.nombre)

    p.drawString(20, 50, "Cliente")
    p.drawString(20, 40, boleta.cedula)

    p.drawString(80, 20, "Contacto")
    p.drawString(50, 10, "ayuda@cinemapp.com")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response