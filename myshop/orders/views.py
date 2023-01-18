# import weasyprint
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string

from .forms import OrderCreateForm
from .models import OrderItem, Order
from cart.cart import Cart
from django.urls import reverse
from .tasks import order_created

from xhtml2pdf import pisa
from io import BytesIO
from django.template.loader import get_template


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
            cart.clear()
            # launch asynchronous task
            order = Order.objects.get(id=order.id)
            subject = f'Order nr. {order.id}'
            message = f'Dear {order.first_name},\n\n' \
                      f'You have successfully placed an order.' \
                      f'Your order ID is {order.id}.'
            send_mail(subject, message, 'admin@myShopBerries.com', [order.email])
            order_created.delay(order.id)
            # set the order in the session
            request.session['order_id'] = order.id
            # redirect for payment
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'form': form})


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order': order})


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    template = get_template('orders/order/pdf.html')
    context = {"order": order, "pagesize": "A4"}
    html = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(html.encode('utf-8'), dest=result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type="application/pdf")
    else:
        return HttpResponse("Errors")
