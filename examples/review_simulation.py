from core.reviews import ReviewGenerator
import json

# Generate different types of reviews
review_gen = ReviewGenerator()

print("Low Suspiciousness Reviews:")
print(json.dumps(review_gen.generate("Coffee Maker", suspiciousness="low", count=2), indent=2))

print("\nHigh Suspiciousness Reviews:")
print(json.dumps(review_gen.generate("Smart Watch", suspiciousness="high", count=2), indent=2))