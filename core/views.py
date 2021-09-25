from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from .models import Item, Order, OrderItem
from django.views.generic import ListView, DetailView
from django.utils import timezone

# Create your views here.


class HomeView(ListView):
    model = Item
    paginate_by = 8
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
            messages.info(
                request, "This item quantity was updated.")
        else:
            messages.info(request, "This item was added to your cart.")
            order.item.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.item.add(order_item)
        messages.info(request, "This item was added to your cart.")
    return redirect("core:product-page", slug=slug)


def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.item.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.item.remove(order_item)
            messages.info(request, "This item was removed from your cart.")
            return redirect("core:product-page", slug=slug)
        else:
            messages.info(request, "This item was not in your cart.")
            return redirect("core:product-page", slug=slug)
    else:
        messages.info(request, "You do not have an active order.")
        return redirect("core:product-page", slug=slug)


def checkout_page(request):
    return render(request, 'checkout-page.html')
