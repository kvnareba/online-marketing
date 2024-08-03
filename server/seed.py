
#!/usr/bin/env python3

from app import app
from models import db, User, Customer, Seller, Product, Order, Category
import random
from faker import Faker

from datetime import datetime

fake = Faker()

product_names = [
    "Smartphone", "Laptop", "Headphones", "Camera", "Smartwatch",
    "Tablet", "Gaming Console", "Bluetooth Speaker", "Drone", "Smart TV",
    "Monitor", "Keyboard", "Mouse", "Printer", "Router",
    "External Hard Drive", "Flash Drive", "Power Bank", "Projector", "Fitness Tracker"
]

product_descriptions = [
    "High-end smartphone with excellent features.",
    "Lightweight laptop with powerful performance.",
    "Noise-cancelling over-ear headphones.",
    "DSLR camera with 4K video recording.",
    "Stylish smartwatch with multiple fitness features.",
    "Compact tablet with a sharp display.",
    "Next-gen gaming console with immersive graphics.",
    "Portable Bluetooth speaker with deep bass.",
    "High-performance drone with 1080p camera.",
    "Smart TV with 4K resolution and streaming apps.",
    "Ultra-wide monitor for an enhanced viewing experience.",
    "Mechanical keyboard with RGB lighting.",
    "Wireless mouse with ergonomic design.",
    "All-in-one printer with scanning capabilities.",
    "High-speed router with extended range.",
    "1TB external hard drive for secure backup.",
    "High-speed flash drive for quick data transfer.",
    "Portable power bank with fast charging.",
    "Mini projector with HD resolution.",
    "Advanced fitness tracker with heart rate monitor."
]

image_paths = [
    "images/product1.jpg", "images/product2.jpg", "images/product3.jpg", 
    "images/product4.jpg", "images/product5.jpg", "images/product6.jpg", 
    "images/product7.jpg", "images/product8.jpg", "images/product9.jpg",
    "images/product10.jpg", "images/product11.jpg", "images/product12.jpg",
    "images/product13.jpg", "images/product14.jpg", "images/product15.jpg",
    "images/product16.jpg", "images/product17.jpg", "images/product18.jpg",
    "images/product19.jpg", "images/product20.jpg"
]

def add_user(username, password, role):
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        print(f"User with username {username} already exists. Skipping.")
        return existing_user
    else:
        user = User(username=username, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        print(f"User {username} added successfully.")
        return user

if __name__ == '_main_':
    with app.app_context():
        print("Starting seed...")

        # Drop all tables
        print("Dropping all tables...")
        db.drop_all()
        print("All tables dropped successfully.")

        # Recreate all tables
        print("Creating tables...")
        db.create_all()
        print("Tables created successfully.")

        # Add Admin User
        try:
            admin_username = 'admin'
            admin_password = 'admin_password'  # Use a strong password in production
            add_user(admin_username, admin_password, 'admin')
        except Exception as e:
            print(f"Error adding admin user: {e}")
            db.session.rollback()

        # Add Regular Users (both customers and sellers)
        try:    
            for i in range(5):
                # Add Customers
                username = fake.user_name()
                password = fake.password()
                user = add_user(username, password, 'customer')
                
                existing_customer = Customer.query.filter_by(user_id=user.id).first()
                if existing_customer:
                    print(f"Customer record for user {username} already exists. Skipping.")
                    continue
                
                customer = Customer(
                    user_id=user.id,
                    name=fake.name(),
                    email=fake.email(),
                    address=fake.address(),
                    phone_no=fake.phone_number()
                )
                db.session.add(customer)

            for i in range(5):
                # Add Sellers
                username = fake.user_name()
                password = fake.password()
                user = add_user(username, password, 'seller')

                existing_seller = Seller.query.filter_by(user_id=user.id).first()
                if existing_seller:
                    print(f"Seller record for user {username} already exists. Skipping.")
                    continue

                seller = Seller(
                    user_id=user.id,
                    business_name=fake.company(),
                    business_email=fake.company_email(),
                    business_address=fake.address(),
                )
                db.session.add(seller)

            db.session.commit()
            print("Users, customers, and sellers added successfully.")
        except Exception as e:
            print(f"Error adding users: {e}")
            db.session.rollback()

        # Add Categories
        try:
            categories = ['Electronics', 'Clothing', 'Books', 'Sports', 'Home appliances']
            category_objects = []
            for category in categories:
                new_category = Category(name=category)
                db.session.add(new_category)
                category_objects.append(new_category)
            db.session.commit()
            print("Categories added successfully.")
        except Exception as e:
            print(f"Error adding categories: {e}")
            db.session.rollback()

        # Add Products
        try:
            sellers = Seller.query.all()
            for i in range(len(product_names)):
                seller = random.choice(sellers)
                category = random.choice(category_objects)
                name = product_names[i]
                description = product_descriptions[i]
                price = round(random.uniform(10.0, 1000.0), 2)
                stock = random.randint(1, 100)
                image = image_paths[i % len(image_paths)]

                product = Product(
                    seller_id=seller.id, 
                    name=name, 
                    description=description, 
                    price=price, 
                    stock=stock, 
                    image=image,
                    category_id=category.id
                )
                db.session.add(product)

            db.session.commit()
            print("Products added successfully.")
        except Exception as e:
            print(f"Error adding products: {e}")
            db.session.rollback()

        # Add Orders
        try:
            customers = Customer.query.all()
            products = Product.query.all()
            for i in range(30):
                customer = random.choice(customers)
                product = random.choice(products)
                quantity = random.randint(1, 5)
                total_price = round(product.price * quantity, 2)
                order_date = datetime.now()

                order = Order(
                    customer_id=customer.id, 
                    product_id=product.id, 
                    quantity=quantity, 
                    total_price=total_price, 
                    order_date=order_date
                )
                db.session.add(order)

            db.session.commit()
            print("Orders added successfully.")
        except Exception as e:
            print(f"Error adding orders: {e}")
            db.session.rollback()