from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.db.models import Q, Sum
from .models import Product, Category, Order, OrderItem, Size, Wishlist
from .forms import CheckoutForm
from django.http import JsonResponse
from django.contrib.auth.mixins import UserPassesTestMixin


# Vista principale (Home + Ricerca)
class ProductListView(ListView):
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'
    paginate_by = 10


    def get_queryset(self):
        queryset = Product.objects.filter(available=True).select_related('category')
        query = self.request.GET.get('q')
        category = self.request.GET.get('category')
        price_min = self.request.GET.get('price_min')
        price_max = self.request.GET.get('price_max')
        order_by = self.request.GET.get('order_by')
        materials = self.request.GET.getlist('material')


        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(category__name__icontains=query)
            )

        if category:
            queryset = queryset.filter(category__slug=category)

        if price_min:
            queryset = queryset.filter(price__gte=price_min)

        if price_max:
            queryset = queryset.filter(price__lte=price_max)

        if order_by == 'price_asc':
            queryset = queryset.order_by('price')
        elif order_by == 'price_desc':
            queryset = queryset.order_by('-price')
        elif order_by == 'newest':
            queryset = queryset.order_by('-created_at')
        elif order_by == 'bestseller':
            queryset = queryset.order_by('-total_sold')

        if materials:
            queryset = queryset.filter(materials__name__in=materials)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_filters'] = self.request.GET
        materials = list(set(
            str(mat) for mat in
            Product.objects.exclude(materials__isnull=True)
            .values_list('materials__name', flat=True)
        ))

        context['materials'] = sorted(materials)  # Ordina alfabeticamente
        context['selected_materials'] = self.request.GET.getlist('material')  # Mantieni i materiali selezionati

        return context



# Vista dettaglio prodotto
class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'object'



from django.http import JsonResponse

@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Validazione taglia
    if product.requires_size:
        size_id = request.POST.get('size')
        if not size_id:
            msg = "Seleziona una taglia per procedere"
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': msg}, status=400)
            messages.error(request, msg)
            return redirect('product-detail', pk=product_id)

        try:
            size = product.sizes.get(id=size_id)
        except Size.DoesNotExist:
            msg = "Taglia non valida per questo prodotto"
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': msg}, status=400)
            messages.error(request, msg)
            return redirect('product-detail', pk=product_id)
    else:
        size_id = None

    # Recupera o crea l'ordine attivo
    order, _ = Order.objects.get_or_create(user=request.user, completed=False)
    existing_item = order.items.filter(product=product, size_id=size_id).first()

    if existing_item:
        existing_item.quantity += 1
        existing_item.save()
        msg = f"Aggiornata quantità per {product.name}"
    else:
        OrderItem.objects.create(
            order=order,
            product=product,
            size_id=size_id,
            price=product.price,
            quantity=1
        )
        msg = f"{product.name} aggiunto al carrello"

    cart_count = order.items.aggregate(total=Sum('quantity'))['total'] or 0

    # Risposta AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'message': msg,
            'cart_count': cart_count
        })

    messages.success(request, msg)
    return redirect(request.META.get('HTTP_REFERER', 'home'))


class CartView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'shop/cart.html'

    def get_object(self):
        return Order.objects.get_or_create(
            user=self.request.user,
            completed=False
        )[0]


@login_required(login_url='login')
def remove_from_cart(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id, order__user=request.user)
    item.delete()
    messages.success(request, "Prodotto rimosso dal carrello")
    return redirect('cart-view')


@login_required(login_url='login')
def update_quantity(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id, order__user=request.user)
    new_quantity = int(request.POST.get('quantity', 1))

    if new_quantity > 0:
        item.quantity = new_quantity

        if item.product.requires_size:
            size_id = request.POST.get('size')
            if size_id:
                new_size = get_object_or_404(Size, id=size_id)
                item.size = new_size

        item.save()
    else:
        item.delete()

    return redirect('cart-view')

# Checkout e ordini
class CheckoutView(LoginRequiredMixin, CreateView):
    template_name = 'shop/checkout.html'
    form_class = CheckoutForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = Order.objects.get(user=self.request.user, completed=False)
        return context


    def form_valid(self, form):
        order = Order.objects.get(user=self.request.user, completed=False)
        order.shipping_address = form.cleaned_data['shipping_address']
        order.shipping_city = form.cleaned_data['shipping_city']
        order.shipping_postal_code = form.cleaned_data['shipping_postal_code']

        order.payment_method = self.request.POST.get('payment_method')

        order.completed = True
        order.save()

        messages.success(self.request, "Ordine completato con successo!")
        return redirect('order-confirmation', pk=order.pk)


class OrderHistoryView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'shop/order_history.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, completed=True).order_by('created_at')


class OrderConfirmationView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'shop/order_confirmation.html'
    context_object_name = 'order'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, completed=True)


# Gestione prodotti (admin)
class ProductManageView(PermissionRequiredMixin, ListView):
    model = Product
    template_name = 'shop/manage_products.html'
    permission_required = 'shop.change_product'


@login_required
def wishlist_toggle(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)

    if product in wishlist.products.all():
        wishlist.products.remove(product)
        action = 'removed'
    else:
        wishlist.products.add(product)
        action = 'added'

    return JsonResponse({
        'status': 'success',
        'action': action,
        'count': wishlist.products.count()
    })


class WishlistView(LoginRequiredMixin, ListView):
    template_name = 'shop/wishlist.html'
    context_object_name = 'products'

    def get_queryset(self):
        # Questa riga crea automaticamente la wishlist se non esiste
        wishlist, created = Wishlist.objects.get_or_create(user=self.request.user)
        return wishlist.products.all()



class ManagerDashboardView(UserPassesTestMixin, ListView):
    template_name = 'shop/manager_dashboard.html'
    model = Product

    def test_func(self):
        return self.request.user.is_store_manager

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pending_orders'] = Order.objects.filter(completed=False).count()
        return context