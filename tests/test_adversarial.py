import pytest
from core.adversarial import FraudEvasionEngine

def test_evasion_optimization(evasion_engine, sample_order):
    original_score = evasion_engine.detection_model(sample_order)
    evaded_order, new_score = evasion_engine.optimize(sample_order)
    
    assert new_score < original_score
    assert "order_id" in evaded_order
    assert evaded_order["order_id"] == sample_order["order_id"]
    
    # Verify that some fields were modified
    modified_fields = [key for key in sample_order if sample_order[key] != evaded_order.get(key)]
    assert len(modified_fields) > 0

def test_ip_perturbation(evasion_engine):
    original_ip = "192.168.1.100"
    perturbed_ip = evasion_engine._perturb_ip(original_ip)
    
    assert perturbed_ip != original_ip
    assert len(perturbed_ip.split(".")) == 4
    assert all(0 <= int(part) <= 255 for part in perturbed_ip.split("."))

def test_order_perturbation(evasion_engine, sample_order):
    perturbed_order = evasion_engine._perturb_order(sample_order.copy())
    
    # Verify core identifiers remain the same
    assert perturbed_order["order_id"] == sample_order["order_id"]
    assert perturbed_order["user_id"] == sample_order["user_id"]
    
    # Verify some fields were changed
    changed = False
    for key in ["amount", "ip", "shipping_country"]:
        if perturbed_order[key] != sample_order[key]:
            changed = True
            break
    assert changed

def test_detection_model(evasion_engine, sample_order):
    # Test with normal order
    normal_score = evasion_engine.detection_model(sample_order)
    assert 0 <= normal_score <= 1
    
    # Test with obvious fraud
    fraud_order = sample_order.copy()
    fraud_order["items"] = [{"sku": "TEST_ITEM", "price": 1.00, "quantity": 1}]
    fraud_order["billing_country"] = "US"
    fraud_order["shipping_country"] = "NG"
    fraud_score = evasion_engine.detection_model(fraud_order)
    
    assert fraud_score > normal_score
    assert fraud_score > 0.7