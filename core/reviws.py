from faker import Faker
from transformers import pipeline
import random
import os
from jinja2 import Environment, FileSystemLoader
import json

class ReviewGenerator:
    def __init__(self, config_file="configs/default.yaml"):
        self.faker = Faker()
        self.config = self._load_config(config_file)
        self.generator = pipeline("text-generation", model="gpt2")
        
        # Setup template environment
        template_path = os.path.join(os.path.dirname(__file__), '..', 'templates')
        self.env = Environment(loader=FileSystemLoader(template_path))
        self.review_template = self.env.get_template("review_template.jinja2")
        
    def _load_config(self, config_file):
        # Load config from YAML file
        return {
            "suspiciousness_levels": ["low", "medium", "high"],
            "product_categories": ["Electronics", "Home & Kitchen", "Fashion", "Beauty"]
        }
    
    def generate(self, product_name, count=5, suspiciousness="medium"):
        if suspiciousness not in self.config["suspiciousness_levels"]:
            raise ValueError(f"Invalid suspiciousness level. Choose from: {', '.join(self.config['suspiciousness_levels'])}")
            
        reviews = []
        category = random.choice(self.config["product_categories"])
        
        for _ in range(count):
            context = {
                "product_name": product_name,
                "category": category,
                "rating": 5 if suspiciousness != "low" else random.randint(4,5),
                "suspiciousness": suspiciousness,
                "days": random.randint(1, 90),
                "urgent": random.choice([True, False]),
                "use_case": self._get_use_case(category)
            }
            
            review_text = self.review_template.render(**context)
            reviews.append({
                "id": self.faker.uuid4(),
                "product": product_name,
                "rating": context["rating"],
                "text": review_text,
                "author": self.faker.name(),
                "date": self.faker.date_this_year(),
                "suspiciousness": suspiciousness
            })
        return reviews
    
    def _get_use_case(self, category):
        use_cases = {
            "Electronics": ["work", "entertainment", "communication"],
            "Home & Kitchen": ["cook", "clean", "decorate"],
            "Fashion": ["dress", "accessorize", "express myself"],
            "Beauty": ["look better", "feel confident", "take care of my skin"]
        }
        return random.choice(use_cases.get(category, ["use it"]))