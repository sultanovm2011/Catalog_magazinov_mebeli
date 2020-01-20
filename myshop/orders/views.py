from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import OrderCreated
from django.core.mail import send_mail
from django.conf import settings



def OrderCreate(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            #send_mail('Заказ Оформлен',
            #'Войдите в админ панель, если хотите посмотреть свой заказ.\n'
            #'Номер вашего заказа ' + str(order.id) + '.\n'
            #'Спасибо за покупку.',
            #settings.EMAIL_HOST_USER,
            #[order.email],
            #fail_silently=False)
    # Асинхронная отправка сообщения
            OrderCreated(order.id)
            cart.clear()
            return render(request, 'orders/order/created.html', {'order': order})

    form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart,
                                                        'form': form})
