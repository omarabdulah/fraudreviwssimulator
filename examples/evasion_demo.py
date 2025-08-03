from core.orders import OrderSimulator
from core.adversarial import FraudEvasionEngine

# Generate a fraudulent order
order_sim = OrderSimulator()
fraud_order = order_sim.generate(fraud_type="card_testing", count=1)[0]

# Create evasion engine
evasion_engine = FraudEvasionEngine()

# Show original detection score
original_score = evasion_engine.detection_model(fraud_order)
print(f"Original Fraud Score: {original_score:.2f}")

# Optimize order to evade detection
evaded_order, new_score = evasion_engine.optimize(fraud_order)

print(f"Evaded Fraud Score: {new_score:.2f}")
print("Modifications:")
for key in fraud_order:
    if fraud_order[key] != evaded_order[key]:
        print(f"  {key}: {fraud_order[key]} → {evaded_order[key]}")