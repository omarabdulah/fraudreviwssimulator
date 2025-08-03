import pytest
from core.reviews import ReviewGenerator
from core.orders import OrderSimulator
from core.identities import IdentityFactory
from core.adversarial import FraudEvasionEngine
from utils.helpers import generate_device_fingerprint, generate_credit_card

@pytest.fixture
def review_generator():
    return ReviewGenerator()

@pytest.fixture
def order_simulator():
    return OrderSimulator()

@pytest.fixture
def identity_factory():
    return IdentityFactory()

@pytest.fixture
def evasion_engine():
    return FraudEvasionEngine()

@pytest.fixture
def sample_order():
    return {
        "order_id": "ord_12345",
        "amount": 150.00,
        "ip": "192.168.1.1",
        "billing_country": "US",
        "shipping_country": "US",
        "items": [{"sku": "PROD_001", "price": 150.00, "quantity": 1}],
        "payment_method": "credit_card"
    }