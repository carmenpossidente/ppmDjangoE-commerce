from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from shop.models import Product, Order


class Command(BaseCommand):
    help = 'Assegna correttamente i permessi ai gruppi'

    def handle(self, *args, **options):
        # Lista esplicita di tutti i permessi necessari
        PERMISSIONS_MAP = {
            'Customers': [
                ('view_product', 'Product'),
                ('view_order', 'Order'),
            ],
            'Managers': [
                ('add_product', 'Product'),
                ('change_product', 'Product'),
                ('delete_product', 'Product'),
                ('view_product', 'Product'),
                ('add_order', 'Order'),
                ('change_order', 'Order'),
                ('delete_order', 'Order'),
                ('view_order', 'Order'),
            ]
        }

        for group_name, perms in PERMISSIONS_MAP.items():
            group, _ = Group.objects.get_or_create(name=group_name)
            group.permissions.clear()  # Resetta eventuali permessi esistenti

            for codename, model_name in perms:
                try:
                    content_type = ContentType.objects.get(
                        app_label='shop',
                        model=model_name.lower()
                    )
                    perm = Permission.objects.get(
                        content_type=content_type,
                        codename=codename
                    )
                    group.permissions.add(perm)
                except Exception as e:
                    self.stdout.write(self.style.ERROR(
                        f'Permesso non trovato: {codename} per {model_name}. Errore: {e}'
                    ))

        self.stdout.write(self.style.SUCCESS(
            f'✅ Permessi assegnati correttamente a: {", ".join(PERMISSIONS_MAP.keys())}'
        ))