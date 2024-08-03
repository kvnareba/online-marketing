
#!/usr/bin/env python3

from app import app
from models import db, User, Customer, Seller, Product, Order, Category
import random
from faker import Faker

from datetime import datetime

fake = Faker()


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