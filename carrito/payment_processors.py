# Autor: Viviana Arango Tabares

import os
from abc import ABC, abstractmethod
from django.conf import settings
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


class ProcesadorPago(ABC):
    @abstractmethod
    def procesar(self, order, datos_pago=None):
        pass


class PagoTarjeta(ProcesadorPago):
    def procesar(self, order, datos_pago=None):
        return {
            'status': 'completed',
            'transaction_id': f'TARJETA-{order.id}',
            'payment_file': None,
        }


class PagoTransferencia(ProcesadorPago):
    def procesar(self, order, datos_pago=None):
        return {
            'status': 'pending',
            'transaction_id': f'TRANSFERENCIA-{order.id}',
            'payment_file': None,
        }


class PagoChequePDF(ProcesadorPago):
    def procesar(self, order, datos_pago=None):
        folder = os.path.join(settings.MEDIA_ROOT, 'cheques')
        os.makedirs(folder, exist_ok=True)

        filename = f'cheque_order_{order.id}.pdf'
        filepath = os.path.join(folder, filename)

        pdf = canvas.Canvas(filepath, pagesize=letter)
        width, height = letter

        pdf.setFont("Helvetica-Bold", 18)
        pdf.drawString(70, height - 80, "Cheque de pago - Afrodite")

        pdf.setFont("Helvetica", 12)
        pdf.drawString(70, height - 130, f"Orden: #{order.id}")
        pdf.drawString(70, height - 155, f"Cliente: {order.user.username}")
        pdf.drawString(70, height - 180, f"Monto: ${order.total}")
        pdf.drawString(70, height - 205, "Paguese a: Afrodite Beauty S.A.S.")
        pdf.drawString(70, height - 230, "Banco: Bancolombia")
        pdf.drawString(70, height - 255, "Cuenta: 123-456789-00")
        pdf.drawString(70, height - 300, "Documento generado como simulación académica.")

        pdf.showPage()
        pdf.save()

        return {
            'status': 'pending',
            'transaction_id': f'CHEQUE-{order.id}',
            'payment_file': f'cheques/{filename}',
        }


def obtener_procesador_pago(metodo_pago):
    if metodo_pago == 'card':
        return PagoTarjeta()

    if metodo_pago == 'transfer':
        return PagoTransferencia()

    if metodo_pago == 'check':
        return PagoChequePDF()

    raise ValueError('Metodo de pago no soportado')