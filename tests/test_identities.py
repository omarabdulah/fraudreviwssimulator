import pytest
from core.identities import IdentityFactory

def test_identity_creation(identity_factory):
    for persona in IdentityFactory.PERSONA_TYPES:
        identity = identity_factory.create_identity(persona_type=persona)
        
        assert "identity_id" in identity
        assert "persona_type" in identity
        assert identity["persona_type"] == persona
        assert "basic_info" in identity
        assert "contact_info" in identity
        assert "digital_footprint" in identity
        assert "financial_profile" in identity
        assert "behavioral_patterns" in identity
        assert "fraud_metadata" in identity

def test_persona_specific_values(identity_factory):
    # Test low-risk persona
    identity = identity_factory.create_identity("low_risk")
    assert identity["fraud_metadata"]["synthetic_score"] < 0.3
    assert identity["financial_profile"]["chargeback_rate"] == 0
    assert identity["digital_footprint"]["account_credentials"]["breached_count"] == 0
    
    # Test burner persona
    identity = identity_factory.create_identity("burner")
    assert identity["fraud_metadata"]["synthetic_score"] > 0.7
    assert identity["financial_profile"]["avg_order_value"] < 100
    assert "Weak" in identity["digital_footprint"]["account_credentials"]["password_pattern"]

def test_geographic_distribution(identity_factory):
    countries = {"USA": 0, "NGA": 0, "RUS": 0, "CHN": 0}
    
    for _ in range(100):
        identity = identity_factory.create_identity()
        for address in identity["contact_info"]["addresses"]:
            country = address["country"]
            if country in countries:
                countries[country] += 1
    
    total = sum(countries.values())
    assert countries["USA"] / total > 0.5  # Should be >50% based on config
    assert countries["NGA"] / total > 0.15  # Should be >15%
    assert countries["RUS"] / total > 0.05  # Should be >5%

def test_fraud_history(identity_factory):
    # Low risk should have no fraud history
    identity = identity_factory.create_identity("low_risk")
    assert len(identity["fraud_metadata"]["fraud_history"]) == 0
    
    # Premium fraudster should have fraud history
    identity = identity_factory.create_identity("premium_fraudster")
    assert 1 <= len(identity["fraud_metadata"]["fraud_history"]) <= 5
    for incident in identity["fraud_metadata"]["fraud_history"]:
        assert incident["type"] in ["card_testing", "account_takeover", "refund_abuse"]