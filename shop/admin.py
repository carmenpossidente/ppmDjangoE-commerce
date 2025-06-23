from pyexpat.errors import messages
from django.core.exceptions import ValidationError
from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Order, OrderItem, Size, Material
from django import forms

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ('product', 'size', 'quantity', 'price', 'get_subtotal')
    readonly_fields = ('get_subtotal',)

    def get_subtotal(self, obj):
        return obj.price * obj.quantity
    get_subtotal.short_description = 'Subtotale'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'completed', 'get_total')
    list_filter = ('completed', 'created_at')
    inlines = [OrderItemInline]

    def get_total(self, obj):
        return sum(item.price * item.quantity for item in obj.items.all())
    get_total.short_description = 'Totale'

class SizeInline(admin.TabularInline):
    model = Product.sizes.through
    extra = 1
    verbose_name = "Taglia disponibile"
    verbose_name_plural = "Taglie disponibili"

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'product_count')
    list_filter = ('type',)
    search_fields = ('name',)
    actions = ['create_default_materials']

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Prodotti associati'

    def create_default_materials(self, request, queryset):
        materials_data = [
            {'name': 'Oro 18K', 'type': 'MT'},
            {'name': 'Oro 14K', 'type': 'MT'},
            {'name': 'Argento 925 placcato oro', 'type': 'MT'},
            {'name': 'Diamante', 'type': 'GS'},
            {'name': 'Zirconia Cubica', 'type': 'GS'},
            {'name': 'Prehnite', 'type': 'GS'},
            {'name': 'Perla', 'type': 'OR'},
        ]

        created = 0
        for data in materials_data:
            _, created_flag = Material.objects.get_or_create(
                name=data['name'],
                defaults={'type': data['type']}
            )
            if created_flag:
                created += 1

        self.message_user(request, f'Creati {created} nuovi materiali standard')
    create_default_materials.short_description = "Crea materiali standard per gioielli"



class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def clean_materials(self):
        materials = self.cleaned_data.get('materials')
        if not materials or not materials.exists():
            raise forms.ValidationError("Seleziona almeno un materiale")
        return materials

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ('name', 'category', 'display_materials', 'price', 'available', 'display_sizes', 'requires_size')
    list_filter = ('category', 'available', 'requires_size')
    search_fields = ('name', 'description', 'materials__name')
    filter_horizontal = ('sizes', 'materials')

    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'category', 'price', 'image', 'available')
        }),
        ('Materiali', {
            'fields': ('materials',),
            'description': 'CTRL+Click per selezionare più materiali'
        }),
        ('Taglie', {
            'fields': ('requires_size', 'sizes'),
            'description': 'Imposta quali taglie sono disponibili per questo prodotto'
        }),
    )

    def display_sizes(self, obj):
        if obj.requires_size:
            return ", ".join([size.name for size in obj.sizes.all()])
        return "N/A"

    display_sizes.short_description = 'Taglie'

    def display_materials(self, obj):
        return ", ".join([material.name for material in obj.materials.all()])

    display_materials.short_description = 'Materiali'

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "sizes":
            obj_id = request.resolver_match.kwargs.get('object_id')
            if obj_id:
                product = Product.objects.get(id=obj_id)
                kwargs["queryset"] = Size.objects.filter(category=product.category)
            else:
                kwargs["queryset"] = Size.objects.none()
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        category = form.cleaned_data.get('category')
        if category:
            obj.requires_size = category.name in ['Anelli', 'Bracciali']
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['materials'].required = True
        form.base_fields['materials'].help_text = "Tenere CTRL per selezionare più materiali"
        return form


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'category', 'product_count')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    actions = ['create_default_sizes']

    def product_count(self, obj):
        return obj.product_set.count()
    product_count.short_description = 'Prodotti associati'

    def create_default_sizes(self, request, queryset):
        anelli, _ = Category.objects.get_or_create(name='Anelli')
        bracciali, _ = Category.objects.get_or_create(name='Bracciali')

        sizes_data = [
            ('8', 'Diametro 16.5mm', anelli),
            ('10', 'Diametro 17.3mm', anelli),
            ('12', 'Diametro 18.1mm', anelli),
            ('14', 'Diametro 18.9mm', anelli),
            ('16', 'Diametro 19.8mm', anelli),
            ('18', 'Diametro 20.6mm', anelli),
            ('S', 'Circonferenza 16cm', bracciali),
            ('M', 'Circonferenza 18cm', bracciali),
        ]

        created = 0
        for name, desc, category in sizes_data:
            _, created_flag = Size.objects.get_or_create(
                name=name,
                defaults={'description': desc, 'category': category}
            )
            if created_flag:
                created += 1

        self.message_user(request, f'Create {created} nuove taglie standard')
    create_default_sizes.short_description = "Crea taglie standard per anelli/bracciali"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_count')
    search_fields = ('name',)

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Numero prodotti'

# OrderItem registrato separatamente per personalizzazione aggiuntiva
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'get_size', 'quantity', 'price')
    list_filter = ('order__completed',)
    search_fields = ('product__name', 'size__name')

    def get_size(self, obj):
        return obj.size.name if obj.size else "-"

    get_size.short_description = 'Taglia'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('order', 'product', 'size')