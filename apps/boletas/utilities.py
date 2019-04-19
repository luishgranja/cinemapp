import io

from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from datetime import datetime
import locale




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

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.

    # titulo
    p.setFont("Helvetica", 14)
    p.drawCentredString(100, 320, "CINEMAPP")

    # pelicula
    p.setFont("Helvetica", 8)
    p.drawString(20, 300, "Pelicula")

    p.setFillColor(colors.black)
    p.rect(20, 276, 100, 14, fill=1)  # 20caracteres
    p.setFillColor(colors.white)
    p.setFont("Helvetica", 12)
    p.drawString(20, 280, boleta.funcion.pelicula.nombre)

    # funcion
    p.setFillColor(colors.black)
    p.setFont("Helvetica", 8)
    p.drawString(20, 260, "Fecha función")
    p.setFont("Helvetica", 12)
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    p.drawString(20, 240, str(boleta.funcion.fecha_funcion.strftime("%A %d %B %Y "))
                 + str(boleta.funcion.hora_funcion.strftime("%H:%M")))

    # ubicacion
    p.setFillColor(colors.black)
    p.setFont("Helvetica", 8)
    p.drawString(20, 220, "Ubicación")

    p.rect(20, 196, 80, 14, fill=1)  # 20caracteres
    p.setFillColor(colors.white)
    p.setFont("Helvetica", 12)
    p.drawString(20, 200, str(boleta.funcion.sala))

    # silla
    p.setFillColor(colors.black)
    p.setFont("Helvetica", 8)
    p.drawString(20, 180, "Silla")

    p.rect(20, 156, 20, 14, fill=1)  # 20caracteres
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
