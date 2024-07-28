from random import choice, randint, uniform
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
from products.models import Product
from categories.models import Category
from orders.models import Order, OrderedItem
from groupbuys.models import GroupBuy

User = get_user_model()
fake = Faker()

class Command(BaseCommand):
    help = 'Generate fake data'

    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, default=50, help='Number of users')
        parser.add_argument('--categories', type=int, default=50, help='Number of categories')
        parser.add_argument('--products', type=int, default=50, help='Number of products')
        parser.add_argument('--orders', type=int, default=50, help='Number of orders')
        parser.add_argument('--reviews', type=int, default=50, help='Number of reviews')
        parser.add_argument('--groupbuys', type=int, default=50, help='Number of groupbuys')

    def handle(self, *args, **options):
        self.create_users(options['users'])
        self.create_categories(options['categories'])
        self.create_products(options['products'])
        self.create_orders(options['orders'])
        self.create_reviews(options['reviews'])
        self.create_groupbuys(options['groupbuys'])

    def create_users(self, count):
        for _ in range(count):
            User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password='password123',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
            )
        self.stdout.write(self.style.SUCCESS(f'Successfully created {count} users'))

    def create_categories(self, count):
        for _ in range(count):
            Category.objects.create(
                name=fake.word(),
                description=fake.sentence(),
            )
        self.stdout.write(self.style.SUCCESS(f'Successfully created {count} categories'))

    def create_products(self, count):
        categories = list(Category.objects.all())
        for _ in range(count):
            Product.objects.create(
                name=fake.word(),
                description=fake.paragraph(),
                price=uniform(10, 1000),
                discounted_price=uniform(10, 1000),
                category=choice(categories),
                inventory=randint(0, 100)
            )
        self.stdout.write(self.style.SUCCESS(f'Successfully created {count} products'))

    def create_orders(self, count):
        users = list(User.objects.all())
        products = list(Product.objects.all())
        for _ in range(count):
            user = choice(users)
            order = Order.objects.create(
                user=user,
                total_price=0
            )
            total_price = 0
            for _ in range(randint(1, 5)):  # Random number of items per order
                product = choice(products)
                quantity = randint(1, 3)
                price = product.price * quantity
                OrderedItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=price
                )
                total_price += price
            order.total_price = total_price
            order.save()
        self.stdout.write(self.style.SUCCESS(f'Successfully created {count} orders'))

    def create_reviews(self, count):
        # Implement review creation logic here
        pass

    def create_groupbuys(self, count):
        # Implement groupbuy creation logic here
        pass