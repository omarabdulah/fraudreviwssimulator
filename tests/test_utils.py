import pytest
from utils.helpers import (
    generate_device_fingerprint,
    generate_credit_card,
    generate_ip_address,
    anonymize_data,
    detect_fraud_pattern
)

def test_device_fingerprint():
    fingerprint = generate_device_fingerprint()
    
    assert isinstance(fingerprint, dict)
    assert "user_agent" in fingerprint
    assert "screen_resolution" in fingerprint
    assert "timezone" in fingerprint
    assert "plugins" in fingerprint
    assert isinstance(fingerprint["plugins"], list)
    assert len(fingerprint["plugins"]) > 0
    assert "fonts" in fingerprint
    assert "canvas_hash" in fingerprint
    assert len(fingerprint["canvas_hash"]) == 64  # SHA256 length
    assert "webgl_hash" in fingerprint
    assert len(fingerprint["webgl_hash"]) == 32  # MD5 length

def test_credit_card_generation():
    # Test Visa
    visa_card = generate_credit_card("4")
    assert visa_card.startswith("4")
    assert len(visa_card) == 16
    assert luhn_check(visa_card)
    
    # Test Mastercard
    mastercard = generate_credit_card("5")
    assert mastercard.startswith("5")
    assert len(mastercard) == 16
    assert luhn_check(mastercard)
    
    # Test Amex
    amex = generate_credit_card("3")
    assert amex.startswith("3")
    assert len(amex) == 15
    assert luhn_check(amex)

def luhn_check(card_number):
    """Validate credit card number using Luhn algorithm"""
    total = 0
    reverse_digits = card_number[::-1]
    for i, digit in enumerate(reverse_digits):
        n = int(digit)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return total % 10 == 0

def test_ip_generation():
    # Test country-specific IPs
    us_ip = generate_ip_address("US")
    assert us_ip.startswith(("12.", "34.", "56.", "78.", "90."))
    
    ng_ip = generate_ip_address("NG")
    assert ng_ip.startswith(("41.", "105."))
    
    # Test random IP
    random_ip = generate_ip_address()
    parts = random_ip.split(".")
    assert len(parts) == 4
    assert 1 <= int(parts[0]) <= 255
    assert 0 <= int(parts[1]) <= 255
    assert 0 <= int(parts[2]) <= 255
    assert 0 <= int(parts[3]) <= 255

def test_anonymize_data():
    data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "+1-555-1234",
        "address": "123 Main St",
        "credit_card": "4111-1111-1111-1111",
        "order_details": {
            "items": [{"name": "Product 1"}],
            "payment": {"type": "credit_card"}
        },
        "safe_field": "public info"
    }
    
    anonymized = anonymize_data(data)
    
    assert anonymized["name"] == "REDACTED_NAME"
    assert anonymized["email"].startswith("user_") and "@example.com" in anonymized["email"]
    assert anonymized["phone"] == "REDACTED_PHONE"
    assert anonymized["address"] == "REDACTED_ADDRESS"
    assert anonymized["credit_card"] == "XXXX-XXXX-XXXX-1111"
    assert anonymized["order_details"]["items"][0]["name"] == "Product 1"  # Should remain
    assert anonymized["safe_field"] == "public info"

def test_fraud_pattern_detection():
    # Card testing pattern
    order = {
        "items": [{"sku": "TEST_ITEM"}],
        "total": 1.00
    }
    patterns = detect_fraud_pattern(order)
    assert "card_testing" in patterns
    
    # Geo mismatch pattern
    order = {
        "billing_country": "US",
        "shipping_country": "NG"
    }
    patterns = detect_fraud_pattern(order)
    assert "geo_mismatch" in patterns
    
    # High value pattern
    order = {"total": 1500.00}
    patterns = detect_fraud_pattern(order)
    assert "high_value" in patterns
    
    # Normal order
    order = {
        "items": [{"sku": "PROD_123"}],
        "billing_country": "US",
        "shipping_country": "US",
        "total": 100.00
    }
    patterns = detect_fraud_pattern(order)
    assert "normal" in patterns