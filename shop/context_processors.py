from .models import Order

def cart_item_count(request):
    if request.user.is_authenticated:
        try:
            order = Order.objects.get(user=request.user, completed=False)
            count = sum(item.quantity for item in order.items.all())
        except Order.DoesNotExist:
            count = 0
    else:
        count = 0
    return {'cart_item_count': count}
