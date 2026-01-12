from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404, redirect, render

from gestion.models import *
import stripe
from django.conf import settings
from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET_KEY

def index(request):
    latest_products = Sales.objects.filter(available=True).order_by('-created')[:3]
    context = {'latest_products': latest_products}
    return render(request, 'user/index.html', context)


def faq(request):
    return render(request, 'user/faq.html')


def condition(request):
    return render(request, 'Conditions_utilisation.html')


def service(request):
    return render(request, 'user/service.html')


def event(request):
    return render(request, 'user/event.html')


def contact(request):
    return render(request, 'user/contact.html')


def logout_view(request):
    logout(request)
    return redirect('index')


def login(request):
    return render(request, 'user/login.html')


def member(request):
    return render(request, 'user/members.html')


def shop(request):
    return render(request, 'user/shop/shop.html')


def shop_14k(request):
    products = Product.objects.filter(available=True, materiaux='Or massif 14k')
    print(products)
    return render(request, 'user/shop/or_massif.html', {'products': products})


def shop_10k(request):
    products = Product.objects.filter(available=True, materiaux='Or massif 10k')
    return render(request, 'user/shop/or_massif_10k.html', {'products': products})


def shop_rempli(request):
    products = Product.objects.filter(available=True, materiaux='Or rempli')
    return render(request, 'user/shop/or_rempli.html', {'products': products})


def shop_argent(request):
    products = Product.objects.filter(available=True, materiaux='Argent sterling')
    return render(request, 'user/shop/argent.html', {'products': products})


def charms(request):
    return render(request, 'user/shop/charms.html')


def boutique(request):
    sales = Sales.objects.filter(available=True).order_by('-created')
    context = {'sales': sales}
    return render(request, 'user/sales/boutique.html', context)


def sale_detail(request, sale_id):
    sale = get_object_or_404(Sales, id=sale_id, available=True)
    return render(request, 'user/sales/sale_detail.html', {'sale': sale})


def _get_cart(request):
    return request.session.setdefault('cart', {})


def _cart_items_with_totals(request):
    cart = _get_cart(request)
    sales = Sales.objects.filter(id__in=cart.keys())
    items = []
    total = Decimal('0.00')
    for sale in sales:
        quantity = int(cart.get(str(sale.id), 0))
        subtotal = sale.price * quantity
        total += subtotal
        items.append({'sale': sale, 'quantity': quantity, 'subtotal': subtotal})
    return items, total


def add_to_cart(request, sale_id):
    sale = get_object_or_404(Sales, id=sale_id, available=True)
    cart = _get_cart(request)
    cart[str(sale_id)] = cart.get(str(sale_id), 0) + 1
    request.session.modified = True
    messages.success(request, f"{sale.name} a été ajouté à votre panier.")
    return redirect('boutique')


def update_cart(request, sale_id):
    sale = get_object_or_404(Sales, id=sale_id, available=True)
    cart = _get_cart(request)
    try:
        quantity = int(request.POST.get('quantity', 1))
    except (TypeError, ValueError):
        quantity = 1
    if quantity > 0:
        cart[str(sale_id)] = quantity
        messages.info(request, f"Quantité mise à jour pour {sale.name}.")
    else:
        cart.pop(str(sale_id), None)
        messages.info(request, f"{sale.name} a été retiré du panier.")
    request.session.modified = True
    return redirect('cart')


def remove_from_cart(request, sale_id):
    sale = get_object_or_404(Sales, id=sale_id, available=True)
    cart = _get_cart(request)
    cart.pop(str(sale_id), None)
    request.session.modified = True
    messages.info(request, f"{sale.name} a été retiré du panier.")
    return redirect('cart')


def cart(request):
    items, total = _cart_items_with_totals(request)
    return render(request, 'user/sales/cart.html', {'cart_items': items, 'total': total})



def checkout(request):
    items, total = _cart_items_with_totals(request)

    if not items:
        return redirect('cart')

    return render(request, 'user/sales/checkout.html', {
        'cart_items': items,
        'total': total,
    })





def create_checkout_session(request):
    items, total = _cart_items_with_totals(request)

    if not items:
        return redirect('cart')

    line_items = []

    for item in items:
        sale = item["sale"]
        line_items.append({
            "price_data": {
                "currency": "cad",
                "product_data": {
                    "name": sale.name,
                },
                "unit_amount": int(sale.price * 100),
            },
            "quantity": item["quantity"],
        })

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url=request.build_absolute_uri(
            reverse("checkout_success")
        ),
        cancel_url=request.build_absolute_uri(
            reverse("checkout_cancel")
        ),
    )

    return redirect(session.url)


def checkout_success(request):
    request.session["cart"] = {}
    request.session.modified = True
    return render(request, "user/sales/checkout_success.html")


def checkout_cancel(request):
    return render(request, "user/sales/checkout_cancel.html")



def create_checkout_session(request):
    cart = request.session.get("cart", {})
    if not cart:
        return redirect("cart")

    line_items = []
    metadata = {}


    sales = Sales.objects.filter(id__in=cart.keys())

    for sale in sales:
        quantity = int(cart[str(sale.id)])
        line_items.append({
            "price_data": {
                "currency": "cad",
                "product_data": {
                    "name": sale.name,
                },
                "unit_amount": int(sale.price * 100),
            },
            "quantity": quantity,
        })
        metadata[str(sale.id)] = quantity  

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url=request.build_absolute_uri(
            reverse("checkout_success")
        ),
        cancel_url=request.build_absolute_uri(
            reverse("checkout_cancel")
        ),
        metadata=metadata,
    )

    return redirect(session.url)


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET
        )
    except Exception:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        if Order.objects.filter(stripe_session_id=session.id).exists():
            return HttpResponse(status=200)

        order = Order.objects.create(
            email=session.customer_details.email,
            total=Decimal(session.amount_total) / 100,
            stripe_session_id=session.id,
            paid=True,
        )

        for sale_id, quantity in session.metadata.items():
            sale = Sales.objects.get(id=sale_id)
            OrderItem.objects.create(
                order=order,
                sale=sale,
                quantity=int(quantity),
                price=sale.price,
            )

    return HttpResponse(status=200)
