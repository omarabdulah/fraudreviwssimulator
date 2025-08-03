from core.reviews import ReviewGenerator
from core.orders import OrderSimulator
from core.identities import IdentityFactory
from core.adversarial import FraudEvasionEngine
import json

def main():
    print("FraudReviwsSimulator - E-commerce Fraud Simulation Toolkit")
    
    # Generate fake reviews
    print("\n=== Generating Fake Reviews ===")
    review_gen = ReviewGenerator()
    reviews = review_gen.generate("Premium Smartphone", count=2, suspiciousness="high")
    print(json.dumps(reviews, indent=2))
    
    # Generate fraud orders
    print("\n=== Generating Fraud Orders ===")
    order_sim = OrderSimulator()
    orders = order_sim.generate(fraud_type="card_testing", count=2)
    print(json.dumps(orders, indent=2))
    
    # Generate synthetic identities
    print("\n=== Generating Synthetic Identities ===")
    identity_factory = IdentityFactory()
    identity = identity_factory.create_identity(persona_type="premium_fraudster")
    print(json.dumps(identity, indent=2))
    
    # Evasion demo
    print("\n=== Adversarial Evasion Demo ===")
    if orders:
        original_order = orders[0]
        evasion_engine = FraudEvasionEngine()
        evaded_order, score = evasion_engine.optimize(original_order)
        
        print("\nOriginal Order Score:", evasion_engine.detection_model(original_order))
        print("Evaded Order Score:", score)
        print("Modified Fields:")
        for key in original_order:
            if original_order[key] != evaded_order[key]:
                print(f"  {key}: {original_order[key]} => {evaded_order[key]}")

if __name__ == "__main__":
    main()