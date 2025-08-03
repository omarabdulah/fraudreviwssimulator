import random
import string
import hashlib
import time
from datetime import datetime, timedelta
import json
import re

def generate_random_string(length=8):
    """Generate a random alphanumeric string"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_device_fingerprint():
    """Generate a realistic browser fingerprint"""
    browser = random.choice(["Chrome", "Firefox", "Safari", "Edge"])
    os = random.choice(["Windows", "MacOS", "Linux", "iOS", "Android"])
    resolution = random.choice(["1920x1080", "1366x768", "1536x864", "1440x900"])
    plugins = random.sample(["Flash", "Java", "Silverlight", "PDF Viewer", "WebGL", "Cookies"], k=3)
    
    fingerprint = {
        "user_agent": f"Mozilla/5.0 ({os}) AppleWebKit/537.36 (KHTML, like Gecko) {browser}/{random.randint(70, 110)}.0",
        "screen_resolution": resolution,
        "timezone": random.choice(["-05:00", "-08:00", "+00:00", "+03:00", "+09:00"]),
        "plugins": plugins,
        "fonts": random.sample(["Arial", "Times New Roman", "Courier New", "Verdana", "Georgia"], k=3),
        "canvas_hash": hashlib.sha256(generate_random_string().encode()).hexdigest(),
        "webgl_hash": hashlib.md5(generate_random_string().encode()).hexdigest()
    }
    return fingerprint

def generate_credit_card(bin_prefix=None):
    """Generate valid test credit card numbers"""
    card_types = {
        "visa": {"prefix": "4", "length": 16},
        "mastercard": {"prefix": "5", "length": 16},
        "amex": {"prefix": "3", "length": 15},
        "discover": {"prefix": "6", "length": 16}
    }
    
    card_type = random.choice(list(card_types.keys()))
    prefix = bin_prefix or card_types[card_type]["prefix"]
    length = card_types[card_type]["length"]
    
    # Generate base number
    number = prefix + ''.join(random.choices(string.digits, k=length - len(prefix) - 1))
    
    # Calculate Luhn check digit
    total = 0
    for i, digit in enumerate(reversed(number)):
        n = int(digit)
        if i % 2 == 0:
            n *= 2
            if n > 9:
                n -= 9
        total += n
    
    check_digit = (10 - (total % 10)) % 10
    return number + str(check_digit)

def generate_ip_address(country_code=None):
    """Generate IP address with optional country code"""
    country_ranges = {
        "US": [("12.", "34."), ("56.", "78."), ("90.", "12.")],
        "GB": [("5.", "152."), ("31.", "185.")],
        "DE": [("46.", "101."), ("78.", "194.")],
        "CN": [("36.", "110."), ("42.", "122.")],
        "RU": [("31.", "134."), ("46.", "178.")],
        "NG": [("41.", "190."), ("105.", "235.")],
    }
    
    if country_code and country_code in country_ranges:
        prefix_range = random.choice(country_ranges[country_code])
        return f"{prefix_range[0]}{random.randint(0,255)}.{random.randint(0,255)}"
    else:
        return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"

def calculate_age(dob):
    """Calculate age from date of birth"""
    today = datetime.now()
    birth_date = datetime.strptime(dob, "%Y-%m-%d")
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

def anonymize_data(data):
    """Anonymize sensitive data in a dictionary"""
    if isinstance(data, dict):
        anonymized = {}
        for key, value in data.items():
            if "name" in key.lower():
                anonymized[key] = "REDACTED_NAME"
            elif "email" in key.lower():
                anonymized[key] = f"user_{hashlib.sha256(value.encode()).hexdigest()[:8]}@example.com"
            elif "phone" in key.lower():
                anonymized[key] = "REDACTED_PHONE"
            elif "address" in key.lower():
                anonymized[key] = "REDACTED_ADDRESS"
            elif "card" in key.lower() or "payment" in key.lower():
                if isinstance(value, str) and re.match(r'\d{4}-\d{4}-\d{4}-\d{4}', value):
                    anonymized[key] = f"XXXX-XXXX-XXXX-{value[-4:]}"
                else:
                    anonymized[key] = "REDACTED_PAYMENT"
            else:
                anonymized[key] = anonymize_data(value)
        return anonymized
    elif isinstance(data, list):
        return [anonymize_data(item) for item in data]
    else:
        return data

def generate_timestamp_range(days=30, count=10):
    """Generate a series of timestamps within a date range"""
    end_time = datetime.now()
    start_time = end_time - timedelta(days=days)
    
    timestamps = []
    for _ in range(count):
        random_seconds = random.randint(0, days * 24 * 3600)
        ts = start_time + timedelta(seconds=random_seconds)
        timestamps.append(ts.isoformat())
    
    return sorted(timestamps)

def format_as_json(data, indent=2):
    """Format data as JSON with consistent formatting"""
    return json.dumps(data, indent=indent, ensure_ascii=False, default=str)

def detect_fraud_pattern(order):
    """Basic fraud pattern detection"""
    patterns = []
    
    # Card testing pattern
    if any(item['sku'] == 'TEST_ITEM' for item in order.get('items', [])):
        patterns.append("card_testing")
    
    # Account takeover pattern
    if order.get('billing_country') != order.get('shipping_country'):
        patterns.append("geo_mismatch")
    
    # High value pattern
    if order.get('total', 0) > 1000:
        patterns.append("high_value")
    
    # Velocity pattern
    if order.get('velocity_score', 0) > 0.7:
        patterns.append("high_velocity")
    
    return patterns if patterns else ["normal"]