from django.urls import path
from . import views
from .views import (
    ProductListView,
    ProductDetailView,
    CartView,
    ProductManageView,
    CheckoutView,
    OrderHistoryView,
    OrderConfirmationView,
    WishlistView,
    ManagerDashboardView,
    add_to_cart,
    update_quantity,
    remove_from_cart,
    wishlist_toggle,
)

urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add-to-cart'),
    path('cart/', CartView.as_view(), name='cart-view'),
    path('manage-products/', ProductManageView.as_view(), name='manage-products'),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove-from-cart'),
    path('cart/update/<int:item_id>/', update_quantity, name='update-quantity'),
    path('prodotto/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add-to-cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('conferma-ordine/<int:pk>/', OrderConfirmationView.as_view(), name='order-confirmation'),
    path('ordini/', OrderHistoryView.as_view(), name='order-history'),
    path('prodotti/', ProductListView.as_view(), name='product-list'),
    path('wishlist/toggle/<int:product_id>/', wishlist_toggle, name='wishlist-toggle'),
    path('wishlist/', WishlistView.as_view(), name='wishlist'),
    path('manager/', ManagerDashboardView.as_view(), name='manager-dashboard'),

]
