"""
Management command to populate Rwanda districts data.
Run with: python manage.py populate_rwanda_districts
"""
from django.core.management.base import BaseCommand
from users.models import District


class Command(BaseCommand):
    help = 'Populate Rwanda districts data'

    def handle(self, *args, **options):
        # Rwanda has 30 districts across 5 provinces
        districts_data = [
            # Kigali City (1 province, 3 districts)
            {'name': 'Gasabo', 'code': 'GAS', 'province': 'Kigali City'},
            {'name': 'Kicukiro', 'code': 'KIC', 'province': 'Kigali City'},
            {'name': 'Nyarugenge', 'code': 'NYA', 'province': 'Kigali City'},

            # Eastern Province (7 districts)
            {'name': 'Bugesera', 'code': 'BUG', 'province': 'Eastern Province'},
            {'name': 'Gatsibo', 'code': 'GAT', 'province': 'Eastern Province'},
            {'name': 'Kayonza', 'code': 'KAY', 'province': 'Eastern Province'},
            {'name': 'Kirehe', 'code': 'KIR', 'province': 'Eastern Province'},
            {'name': 'Ngoma', 'code': 'NGO', 'province': 'Eastern Province'},
            {'name': 'Nyagatare', 'code': 'NYG', 'province': 'Eastern Province'},
            {'name': 'Rwamagana', 'code': 'RWA', 'province': 'Eastern Province'},

            # Northern Province (5 districts)
            {'name': 'Burera', 'code': 'BUR', 'province': 'Northern Province'},
            {'name': 'Gakenke', 'code': 'GAK', 'province': 'Northern Province'},
            {'name': 'Gicumbi', 'code': 'GIC', 'province': 'Northern Province'},
            {'name': 'Musanze', 'code': 'MUS', 'province': 'Northern Province'},
            {'name': 'Rulindo', 'code': 'RUL', 'province': 'Northern Province'},

            # Southern Province (8 districts)
            {'name': 'Gisagara', 'code': 'GIS', 'province': 'Southern Province'},
            {'name': 'Huye', 'code': 'HUY', 'province': 'Southern Province'},
            {'name': 'Kamonyi', 'code': 'KAM', 'province': 'Southern Province'},
            {'name': 'Muhanga', 'code': 'MUH', 'province': 'Southern Province'},
            {'name': 'Nyamagabe', 'code': 'NYM', 'province': 'Southern Province'},
            {'name': 'Nyanza', 'code': 'NYZ', 'province': 'Southern Province'},
            {'name': 'Nyaruguru', 'code': 'NYR', 'province': 'Southern Province'},
            {'name': 'Ruhango', 'code': 'RUH', 'province': 'Southern Province'},

            # Western Province (7 districts)
            {'name': 'Karongi', 'code': 'KAR', 'province': 'Western Province'},
            {'name': 'Ngororero', 'code': 'NGR', 'province': 'Western Province'},
            {'name': 'Nyabihu', 'code': 'NYB', 'province': 'Western Province'},
            {'name': 'Nyamasheke', 'code': 'NYS', 'province': 'Western Province'},
            {'name': 'Rubavu', 'code': 'RUB', 'province': 'Western Province'},
            {'name': 'Rusizi', 'code': 'RUS', 'province': 'Western Province'},
            {'name': 'Rutsiro', 'code': 'RUT', 'province': 'Western Province'},
        ]

        created_count = 0
        updated_count = 0

        for district_data in districts_data:
            district, created = District.objects.update_or_create(
                code=district_data['code'],
                defaults={
                    'name': district_data['name'],
                    'province': district_data['province'],
                    'is_active': True
                }
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created district: {district.name} ({district.code})')
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'Updated district: {district.name} ({district.code})')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully populated Rwanda districts data:'
                f'\n  - Created: {created_count}'
                f'\n  - Updated: {updated_count}'
                f'\n  - Total: {created_count + updated_count}'
            )
        )
