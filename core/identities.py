from faker import Faker
import random
import uuid
from datetime import datetime, timedelta
from jinja2 import Environment, FileSystemLoader
import os
import json
from ..utils import helpers

class IdentityFactory:
    PERSONA_TYPES = ["low_risk", "burner", "sleeper_agent", "premium_fraudster"]
    
    def __init__(self, geo_distribution=None):
        self.faker = Faker()
        self.geo_distribution = geo_distribution or {"USA": 0.6, "NGA": 0.2, "RUS": 0.2}
        
        # Setup template environment
        template_path = os.path.join(os.path.dirname(__file__), '..', 'templates')
        self.env = Environment(loader=FileSystemLoader(template_path))
        self.identity_template = self.env.get_template("identity_template.json")
    
    def create_identity(self, persona_type="sleeper_agent", history_depth="6m"):
        if persona_type not in self.PERSONA_TYPES:
            raise ValueError(f"Invalid persona type. Choose from: {', '.join(self.PERSONA_TYPES)}")
            
        # Select country based on distribution
        countries = list(self.geo_distribution.keys())
        weights = list(self.geo_distribution.values())
        country = random.choices(countries, weights=weights, k=1)[0]
        
        # Generate base identity
        first_name = self.faker.first_name_male() if random.random() > 0.5 else self.faker.first_name_female()
        last_name = self.faker.last_name()
        email = f"{first_name[0]}{last_name}{random.randint(10,99)}@{self.faker.free_email_domain()}".lower()
        username = f"{first_name}{last_name}{random.randint(1,99)}"
        
        # Generate context for template
        creation_date = datetime.now() - timedelta(days=random.randint(180, 1080))
        context = {
            "uuid": str(uuid.uuid4()),
            "creation_date": creation_date.isoformat(),
            "persona": persona_type,
            "first_name": first_name,
            "last_name": last_name,
            "dob": self.faker.date_of_birth(minimum_age=18, maximum_age=65).isoformat(),
            "gender": "male" if random.random() > 0.5 else "female",
            "email": email,
            "phone": self.faker.phone_number(),
            "username": username,
            "password_pattern": self._get_password_pattern(persona_type),
            "breached_count": random.randint(0, 5) if persona_type != "low_risk" else 0,
            "avg_order_value": self._get_avg_order_value(persona_type),
            "preferred_categories": self._get_preferred_categories(persona_type),
            "chargeback_rate": self._get_chargeback_rate(persona_type),
            "activity_times": self._get_activity_times(persona_type),
            "browsing_habits": self._get_browsing_habits(persona_type),
            "risk_tolerance": self._get_risk_tolerance(persona_type),
            "social_media": self._get_social_media(persona_type),
            "associations": self._get_associations(persona_type),
            "fraud_history": self._get_fraud_history(persona_type),
            "synthetic_score": self._get_synthetic_score(persona_type)
        }
        
        # Render identity from template
        identity_json = self.identity_template.render(**context)
        return json.loads(identity_json)
    
    def _get_password_pattern(self, persona_type):
        patterns = {
            "low_risk": "Strong: mix of letters, numbers, symbols",
            "burner": "Weak: common words or sequences",
            "sleeper_agent": "Moderate: personal info + numbers",
            "premium_fraudster": "Strong: but reused across sites"
        }
        return patterns[persona_type]
    
    def _get_avg_order_value(self, persona_type):
        ranges = {
            "low_risk": (50, 200),
            "burner": (10, 100),
            "sleeper_agent": (100, 500),
            "premium_fraudster": (500, 2000)
        }
        return random.randint(*ranges[persona_type])
    
    # ... (similar methods for other context fields) ...
    
    def _get_fraud_history(self, persona_type):
        if persona_type == "low_risk":
            return []
        
        history = []
        types = ["card_testing", "account_takeover", "refund_abuse"]
        outcomes = ["success", "failed", "blocked"]
        
        for _ in range(random.randint(1, 5)):
            history.append({
                "date": self.faker.date_this_year().isoformat(),
                "type": random.choice(types),
                "method": random.choice(["stolen_card", "phishing", "credential_stuffing"]),
                "outcome": random.choice(outcomes)
            })
        return history
    
    def _get_synthetic_score(self, persona_type):
        scores = {
            "low_risk": random.uniform(0.0, 0.2),
            "burner": random.uniform(0.7, 1.0),
            "sleeper_agent": random.uniform(0.4, 0.6),
            "premium_fraudster": random.uniform(0.3, 0.5)
        }
        return scores[persona_type]