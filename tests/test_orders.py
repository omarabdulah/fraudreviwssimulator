import pytest
from core.orders import OrderSimulator

def test_order_generation(order_simulator):
    for fraud_type in OrderSimulator.FRAUD_TYPES:
        orders = order_simulator.generate(fraud_type=fraud_type, count=3)
        assert len(orders) == 3
        
        for order in orders:
            assert order["fraud_type"] == fraud_type
            assert "order_id" in order
            assert "user_id" in order
            assert "amount" in order
            assert "currency" in order
            assert order["currency"] == "USD"
            assert "ip" in order
            assert "billing_country" in order
            assert "shipping_country" in order
            assert "items" in order
            assert len(order["items"]) > 0
            assert "payment_method" in order
            assert "fraud_indicators" in order
            assert "is_successful" in order
            assert isinstance(order["is_successful"], bool)

def test_fraud_specific_patterns(order_simulator):
    # Test card testing pattern
    orders = order_simulator.generate(fraud_type="card_testing", count=5)
    for order in orders:
        assert any(item["sku"] == "TEST_ITEM" for item in order["items"])
        assert order["shipping_cost"] == 0
        assert order["payment_method"] == "credit_card"
    
    # Test triangulation pattern
    orders = order_simulator.generate(fraud_type="triangulation", count=5)
    for order in orders:
        assert order["payment_method"] == "paypal"
        assert order["shipping_address"] != "same_as_billing"

def test_invalid_fraud_type(order_simulator):
    with pytest.raises(ValueError):
        order_simulator.generate(fraud_type="invalid_type")

def test_order_values(order_simulator):
    orders = order_simulator.generate(fraud_type="account_takeover", count=10)
    amounts = [order["total"] for order in orders]
    assert min(amounts) >= 50
    assert max(amounts) <= 2000
    assert sum(amounts) / len(amounts) > 200  # Avg should be higher for ATO

def test_success_rate(order_simulator):
    orders = order_simulator.generate(fraud_type="refund_abuse", count=100, success_rate=0.8)
    successes = sum(1 for order in orders if order["is_successful"])
    success_rate = successes / 100
    assert 0.75 <= success_rate <= 0.85  # Allow some variance