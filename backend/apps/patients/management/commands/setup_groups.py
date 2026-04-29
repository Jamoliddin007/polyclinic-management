"""
Boshlang'ich foydalanuvchi guruhlarini (rollarini) yaratish.

Ishlatish:
    python manage.py setup_groups
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


GROUP_PERMISSIONS = {
    'admin': '*',  # hammasini
    'registrator': [
        # Patients
        ('patient', ['add', 'change', 'view']),
        ('discountcategory', ['view']),
        # Doctors
        ('doctor', ['view']),
        ('specialty', ['view']),
        ('qualification', ['view']),
        # Visits
        ('visit', ['add', 'change', 'view']),
        ('visitprocedure', ['add', 'change', 'delete', 'view']),
        ('visitconsultation', ['add', 'change', 'delete', 'view']),
        ('proceduretype', ['view']),
        # Billing
        ('payment', ['add', 'change', 'view']),
    ],
    'doctor': [
        ('patient', ['view']),
        ('visit', ['change', 'view']),
        ('visitprocedure', ['view']),
        ('visitconsultation', ['view']),
        ('proceduretype', ['view']),
    ],
}


class Command(BaseCommand):
    help = "Admin, Registrator, Doctor rollarini va ruxsatlarini yaratadi"

    def handle(self, *args, **options):
        for group_name, perms in GROUP_PERMISSIONS.items():
            group, created = Group.objects.get_or_create(name=group_name)
            verb = 'yaratildi' if created else 'mavjud'
            self.stdout.write(self.style.SUCCESS(f'➜ "{group_name}" guruhi {verb}'))

            if perms == '*':
                group.permissions.set(Permission.objects.all())
                self.stdout.write(f'  → barcha ruxsatlar berildi ({Permission.objects.count()} ta)')
                continue

            permissions_to_add = []
            for model_name, actions in perms:
                try:
                    ct = ContentType.objects.get(model=model_name)
                except ContentType.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'  ⚠ {model_name} topilmadi (migrate qildingizmi?)'))
                    continue

                for action in actions:
                    codename = f'{action}_{model_name}'
                    try:
                        permission = Permission.objects.get(content_type=ct, codename=codename)
                        permissions_to_add.append(permission)
                    except Permission.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f'  ⚠ {codename} topilmadi'))

            group.permissions.set(permissions_to_add)
            self.stdout.write(f'  → {len(permissions_to_add)} ta ruxsat berildi')

        self.stdout.write(self.style.SUCCESS('\n✅ Tayyor! Endi:'))
        self.stdout.write('   1. Admin panelda foydalanuvchi yarating')
        self.stdout.write('   2. Unga kerakli guruhni biriktiring (admin/registrator/doctor)')
