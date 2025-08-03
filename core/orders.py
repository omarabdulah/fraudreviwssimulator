from faker import Faker
import random
import uuid
from datetime import datetime, timedelta
from jinja2 import Environment, FileSystemLoader
import os
import json
from ..utils import helpers

class OrderSimulator:
    FRAUD_TYPES = ["card_testing", "account_takeover", "triangulation", "refund_abuse"]
    
    def __init__(self):
        self.faker = Faker()
        
        # Setup template environment
        template_path = os.path.join(os.path.dirname(__file__), '..', 'templates')
        self.env = Environment(loader=FileSystemLoader(template_path))
        self.order_template = self.env.get_template("order_template.json")
    
    def generate(self, fraud_type="card_testing", count=10, success_rate=0.3):
        if fraud_type not in self.FRAUD_TYPES:
            raise ValueError(f"Invalid fraud type. Choose from: {', '.join(self.FRAUD_TYPES)}")
            
        orders = []
        base_date = datetime.now()
        
        for _ in range(count):
            order_id = str(uuid.uuid4())
            user_id = f"fraudster_{random.randint(1000,9999)}" if fraud_type != "account_takeover" else self.faker.user_name()
            shipping_differs = fraud_type == "triangulation" or random.random() > 0.7
            
            # Generate items based on fraud type
            items = self._generate_items(fraud_type)
            subtotal = sum(item["price"] * item["quantity"] for item in items)
            shipping_cost = 0 if fraud_type == "card_testing" else random.uniform(5, 20)
            tax = subtotal * 0.08
            total = subtotal + shipping_cost + tax
            
            context = {
                "uuid": order_id,
                "timestamp": (base_date - timedelta(minutes=random.randint(0, 60))).isoformat(),
                "user_id": user_id,
                "email": self.faker.email(),
                "ip": self.faker.ipv4(),
                "user_agent": self.faker.user_agent(),
                "first_name": self.faker.first_name(),
                "last_name": self.faker.last_name(),
                "street_address": self.faker.street_address(),
                "city": self.faker.city(),
                "state": self.faker.state_abbr(),
                "zipcode": self.faker.zipcode(),
                "country_code": self.faker.country_code(),
                "phone_number": self.faker.phone_number(),
                "shipping_differs": shipping_differs,
                "ship_first_name": self.faker.first_name() if shipping_differs else "",
                "ship_last_name": self.faker.last_name() if shipping_differs else "",
                "ship_street_address": self.faker.street_address() if shipping_differs else "",
                "ship_city": self.faker.city() if shipping_differs else "",
                "ship_state": self.faker.state_abbr() if shipping_differs else "",
                "ship_zipcode": self.faker.zipcode() if shipping_differs else "",
                "ship_country_code": self.faker.country_code() if shipping_differs else "",
                "payment_type": self._get_payment_method(fraud_type),
                "card_type": random.choice(["Visa", "Mastercard", "Amex"]),
                "last4": str(random.randint(1000, 9999)),
                "exp_date": f"{random.randint(1,12):02d}/{random.randint(23,28)}",
                "paypal_id": f"PPID{random.randint(100000,999999)}",
                "crypto_address": self.faker.sha256(),
                "items": items,
                "subtotal": round(subtotal, 2),
                "shipping_cost": round(shipping_cost, 2),
                "tax": round(tax, 2),
                "total": round(total, 2),
                "velocity_score": random.uniform(0, 1),
                "geo_mismatch": 1 if shipping_differs else 0,
                "browser_fp": self.faker.sha256(),
                "device_id": str(uuid.uuid4()),
                "fraud_type": fraud_type,
                "is_successful": random.random() < success_rate
            }
            
            # Render order from template
            order_json = self.order_template.render(**context)
            orders.append(json.loads(order_json))
        return orders
    
    def _generate_items(self, fraud_type):
        if fraud_type == "card_testing":
            return [{
                "sku": "TEST_ITEM",
                "name": "Test Product",
                "price": 1.00,
                "quantity": 1
            }]
        elif fraud_type == "refund_abuse":
            return [{
                "sku": f"REF{random.randint(100,999)}",
                "name": f"Designer {random.choice(['Shirt', 'Dress', 'Handbag'])}",
                "price": round(random.uniform(100, 500), 2),
                "quantity": 1
            }]
        else:
            count = random.randint(1, 5)
            return [{
                "sku": self.faker.bothify("??-####"),
                "name": self.faker.catch_phrase(),
                "price": round(random.uniform(10, 500), 2),
                "quantity": random.randint(1, 3)
            } for _ in range(count)]
    
    def _get_payment_method(self, fraud_type):
        if fraud_type == "triangulation":
            return "paypal"
        elif fraud_type == "card_testing":
            return "credit_card"
        elif fraud_type == "refund_abuse":
            return random.choice(["credit_card", "paypal"])
        else:
            return random.choice(["credit_card", "paypal", "crypto"])