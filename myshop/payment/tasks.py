import time
from io import BytesIO
from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from orders.models import Order
from xhtml2pdf import pisa
from io import BytesIO
from django.template.loader import get_template


def payment_completed(order_id):
    """
    Task to send an e-mail notification when an order is successfully paid in synchronous mode.
    """
    print('payment_completed')
    order = Order.objects.get(id=order_id)
    # create invoice e-mail
    subject = f'My Shop - Invoice no. {order.id}'
    message = 'Please, find attached the invoice for your recent purchase.'
    # generate PDF
    template = 'orders/order/pdf.html'
    context = {"order": order}
    html = render_to_string(template, context)
    send_mail(subject, html_message=html, from_email='admin@myShopBerries.com', fail_silently=False, message=message,
              recipient_list=[order.email])


# @shared_task
# def payment_completed(order_id):
#     """
#     Task to send an e-mail notification when an order is successfully paid asynchronous mode.
#     """
#     order = Order.objects.get(id=order_id)
#     # create invoice e-mail
#     subject = f'My Shop - Invoice no. {order.id}'
#     message = 'Please, find attached the invoice for your recent purchase.'
#     email = EmailMessage(subject,
#                      message,
#                      'admin@myshop.com',
#                      [order.email])
#     # generate PDF
#     html = render_to_string('orders/order/pdf.html', {'order': order})
#     out = BytesIO()
#     stylesheets = [weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')]
#     weasyprint.HTML(string=html).write_pdf(out,
#                                        stylesheets=stylesheets)
#     # attach PDF file
#     email.attach(f'order_{order.id}.pdf',
#              out.getvalue(),
#              'application/pdf')
#     # send e-mail
#     email.send()
