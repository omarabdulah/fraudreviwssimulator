import random
import numpy as np
from ..utils import helpers

class FraudEvasionEngine:
    def __init__(self, detection_model=None):
        self.detection_model = detection_model or self._default_detector
        
    def optimize(self, original_order, max_attempts=100):
        best_order = original_order.copy()
        best_score = self.detection_model(original_order)
        
        for _ in range(max_attempts):
            candidate = self._perturb_order(original_order.copy())
            score = self.detection_model(candidate)
            
            if score < best_score:
                best_order = candidate
                best_score = score
                
        return best_order, best_score
    
    def _perturb_order(self, order):
        perturbations = {
            "amount": lambda x: max(1, x * random.uniform(0.7, 1.3)),
            "ip": self._perturb_ip,
            "shipping_country": lambda x: x if random.random() > 0.3 else "US"
        }
        
        for key, func in perturbations.items():
            if key in order:
                order[key] = func(order[key])
                
        return order
    
    def _perturb_ip(self, ip):
        if random.random() > 0.7:
            # Change country entirely
            return helpers.generate_ip_address(random.choice(["US", "GB", "DE", "CA"]))
        else:
            # Keep same country but perturb
            country = self._infer_country_from_ip(ip)
            return helpers.generate_ip_address(country)
    
    def _infer_country_from_ip(self, ip):
        """Simple country inference from IP"""
        first_octet = int(ip.split(".")[0])
        if 1 <= first_octet <= 126:
            return "US"
        elif 127 <= first_octet <= 191:
            return "EU"
        elif 192 <= first_octet <= 223:
            return "AS"
        else:
            return random.choice(["US", "GB", "DE", "CA"])
    
    def _default_detector(self, order):
        # Simple heuristic-based detection
        risk = 0
        if order["billing_country"] != order["shipping_country"]:
            risk += 0.3
        if order["amount"] > 1000:
            risk += 0.2
        if "TEST_ITEM" in [item["sku"] for item in order["items"]]:
            risk += 0.5
        return min(1.0, risk)