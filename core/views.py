from django.shortcuts import get_object_or_404, redirect, render
from .models import Item, Order, OrderItem
from django.views.generic import ListView, DetailView
from django.utils import timezone

# Create your views here.


class HomeView(ListView):
    model = Item
    template_name = "home-page.html"


class ItemDetailView(DetailView):
    model = Item
    template_name = 'product-page.html'


def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.item.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
        else:
            order.item.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
    return redirect("core:product-page", slug=slug)


def checkout_page(request):
    return render(request, 'checkout-page.html')
