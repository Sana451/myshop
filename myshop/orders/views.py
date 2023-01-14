from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .forms import OrderCreateForm
from .models import OrderItem, Order
from cart.cart import Cart
from django.urls import reverse
from .tasks import order_created


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


