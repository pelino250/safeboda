import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from users.models import Passenger, Rider

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate the database with dummy data for testing Redis caching'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=50,
            help='Number of users to create (default: 50)',
        )
        parser.add_argument(
            '--passengers',
            type=int,
            default=30,
            help='Number of passengers to create (default: 30)',
        )
        parser.add_argument(
            '--riders',
            type=int,
            default=20,
            help='Number of riders to create (default: 20)',
        )

    def handle(self, *args, **options):
        users_count = options['users']
        passengers_count = options['passengers']
        riders_count = options['riders']

        self.stdout.write(
            self.style.SUCCESS(f'Starting to create {users_count} users, {passengers_count} passengers, and {riders_count} riders...')
        )

        # Create users
        created_users = []
        for i in range(users_count):
            email = f'user{i+1}@safeboda.com'
            if not User.objects.filter(email=email).exists():
                user_type = 'passenger' if i < passengers_count else 'rider' if i < passengers_count + riders_count else random.choice(['passenger', 'rider'])
                user = User.objects.create_user(
                    email=email,
                    password='testpass123',
                    first_name=f'FirstName{i+1}',
                    last_name=f'LastName{i+1}',
                    user_type=user_type,
                    phone_number=f'+256{700000000 + i}',
                    is_active=True
                )
                created_users.append(user)

        self.stdout.write(
            self.style.SUCCESS(f'Created {len(created_users)} users')
        )

        # Create passengers
        passenger_users = [u for u in created_users if u.user_type == 'passenger'][:passengers_count]
        created_passengers = []
        
        home_addresses = [
            'Kampala Central, Uganda',
            'Nakawa Division, Kampala',
            'Kawempe Division, Kampala',
            'Makindye Division, Kampala',
            'Rubaga Division, Kampala',
            'Entebbe Road, Kampala',
            'Ntinda, Kampala',
            'Bugolobi, Kampala',
            'Kololo, Kampala',
            'Muyenga, Kampala'
        ]
        
        payment_methods = ['momo', 'cash', 'card']
        languages = ['en', 'sw', 'lg']

        for i, user in enumerate(passenger_users):
            if not hasattr(user, 'passenger_profile'):
                passenger = Passenger.objects.create(
                    user=user,
                    passenger_id=f'PASS{1000 + i}',
                    preferred_payment_method=random.choice(payment_methods),
                    home_address=random.choice(home_addresses),
                    preferred_language=random.choice(languages),
                    emergency_contact=f'+256{750000000 + i}',
                    is_verified=random.choice([True, False])
                )
                created_passengers.append(passenger)

        self.stdout.write(
            self.style.SUCCESS(f'Created {len(created_passengers)} passengers')
        )

        # Create riders
        rider_users = [u for u in created_users if u.user_type == 'rider'][:riders_count]
        created_riders = []
        
        verification_statuses = ['pending', 'approved', 'rejected', 'suspended']
        kampala_coordinates = [
            ('0.3476', '32.5825'),  # Kampala Central
            ('0.3560', '32.6169'),  # Ntinda
            ('0.3167', '32.5833'),  # Entebbe Road
            ('0.3311', '32.5811'),  # Nakawa
            ('0.3736', '32.5467'),  # Kawempe
            ('0.2906', '32.5489'),  # Makindye
            ('0.3189', '32.5342'),  # Rubaga
            ('0.3344', '32.6078'),  # Bugolobi
            ('0.3275', '32.5975'),  # Kololo
            ('0.2958', '32.6011'),  # Muyenga
        ]

        for i, user in enumerate(rider_users):
            if not hasattr(user, 'rider_profile'):
                lat, lon = random.choice(kampala_coordinates)
                # Add some randomness to coordinates
                lat = str(float(lat) + random.uniform(-0.01, 0.01))
                lon = str(float(lon) + random.uniform(-0.01, 0.01))
                
                rider = Rider.objects.create(
                    user=user,
                    license_number=f'DL{10000 + i}',
                    verification_status=random.choice(verification_statuses),
                    verification_notes=f'Verification notes for rider {i+1}',
                    is_available=random.choice([True, False]),
                    current_latitude=lat,
                    current_longitude=lon,
                    average_rating=round(random.uniform(3.0, 5.0), 1)
                )
                created_riders.append(rider)

        self.stdout.write(
            self.style.SUCCESS(f'Created {len(created_riders)} riders')
        )

        # Display summary
        approved_riders = len([r for r in created_riders if r.verification_status == 'approved'])
        available_riders = len([r for r in created_riders if r.is_available and r.verification_status == 'approved'])

        self.stdout.write(
            self.style.SUCCESS(
                f'\nDummy data creation completed!\n'
                f'Total users: {User.objects.count()}\n'
                f'Total passengers: {Passenger.objects.count()}\n'
                f'Total riders: {Rider.objects.count()}\n'
                f'Approved riders: {approved_riders}\n'
                f'Available approved riders: {available_riders}\n'
                f'\nYou can now test Redis caching with the available_riders endpoint!'
            )
        )