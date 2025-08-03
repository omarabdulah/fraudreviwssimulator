import random
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import json
from datetime import datetime

class FraudDetectionAuditor:
    def __init__(self, detection_function=None):
        """
        Initialize with an optional fraud detection function
        If none is provided, a default heuristic will be used
        """
        self.detection_function = detection_function or self.default_detector
        
    def run_simulation(self, orders, reviews=None, output_format='dict'):
        """
        Run a simulation test against fraud detection system
        
        orders: list of orders (mix of legitimate and fraudulent)
        reviews: optional list of reviews (for fake review detection)
        """
        results = {
            'orders': [],
            'reviews': [],
            'metrics': self._calculate_metrics(orders, reviews),
            'visualizations': self._generate_visualizations(orders)
        }
        
        # Process orders
        for order in orders:
            result = {
                'order_id': order.get('order_id'),
                'fraud_type': order.get('fraud_type'),
                'is_successful': order.get('is_successful', False),
                'detection_score': self.detection_function(order),
                'detected': None,
                'timestamp': datetime.now().isoformat()
            }
            result['detected'] = result['detection_score'] > 0.7
            results['orders'].append(result)
        
        # Process reviews if provided
        if reviews:
            for review in reviews:
                results['reviews'].append({
                    'review_id': review.get('id'),
                    'suspiciousness': review.get('suspiciousness'),
                    'text': review.get('text')[:50] + '...' if review.get('text') else None,
                    'detection_score': self._review_detection_score(review),
                    'timestamp': datetime.now().isoformat()
                })
        
        if output_format == 'json':
            return json.dumps(results, indent=2)
        elif output_format == 'html':
            return self._generate_html_report(results)
        else:
            return results
    
    def default_detector(self, order):
        """
        Default heuristic-based fraud detector
        """
        risk_score = 0.0
        
        # Country mismatch
        if order.get('billing_country') != order.get('shipping_country'):
            risk_score += 0.3
        
        # High value order
        if order.get('amount', 0) > 1000:
            risk_score += 0.2
        
        # Test items
        for item in order.get('items', []):
            if 'TEST' in item.get('sku', '').upper():
                risk_score += 0.4
        
        # High velocity
        if order.get('velocity', {}).get('orders', 0) > 5:
            risk_score += min(0.3, order['velocity']['orders'] * 0.06)
        
        return min(1.0, risk_score)
    
    def _review_detection_score(self, review):
        """
        Simple fake review detector
        """
        score = 0.0
        text = review.get('text', '').lower()
        
        # Suspicious phrases
        suspicious_phrases = [
            'best ever', 'amazing', 'perfect', 'life changing',
            'highly recommend', 'must buy', 'love it'
        ]
        
        for phrase in suspicious_phrases:
            if phrase in text:
                score += 0.2
        
        # All caps words
        if any(word.isupper() and len(word) > 3 for word in text.split()):
            score += 0.3
        
        # Rating 5 with short text
        if review.get('rating') == 5 and len(text.split()) < 10:
            score += 0.2
            
        return min(1.0, score)
    
    def _calculate_metrics(self, orders, reviews=None):
        """Calculate key performance metrics"""
        metrics = {'orders': {}, 'reviews': {}}
        
        # Order metrics
        fraud_orders = [o for o in orders if o.get('fraud_type') != 'legitimate']
        legit_orders = [o for o in orders if o.get('fraud_type') == 'legitimate']
        
        if fraud_orders:
            success_rate = sum(o.get('is_successful', False) for o in fraud_orders) / len(fraud_orders)
            metrics['orders']['fraud_success_rate'] = success_rate
            metrics['orders']['fraud_count'] = len(fraud_orders)
        
        if legit_orders:
            metrics['orders']['legitimate_count'] = len(legit_orders)
        
        # Review metrics
        if reviews:
            suspicious_reviews = [r for r in reviews if r.get('suspiciousness') in ['medium', 'high']]
            metrics['reviews']['suspicious_count'] = len(suspicious_reviews)
            metrics['reviews']['total_count'] = len(reviews)
        
        return metrics
    
    def _generate_visualizations(self, orders):
        """Generate visualizations for the report"""
        vis = {}
        
        # Fraud type distribution
        fraud_types = {}
        for order in orders:
            if order.get('fraud_type') != 'legitimate':
                fraud_type = order.get('fraud_type', 'unknown')
                fraud_types[fraud_type] = fraud_types.get(fraud_type, 0) + 1
        
        if fraud_types:
            plt.figure(figsize=(10, 5))
            plt.bar(fraud_types.keys(), fraud_types.values())
            plt.title('Fraud Type Distribution')
            plt.ylabel('Count')
            vis['fraud_type_distribution'] = self._fig_to_base64()
            plt.close()
        
        # Amount distribution
        amounts = [o.get('amount', 0) for o in orders]
        if amounts:
            plt.figure(figsize=(10, 5))
            plt.hist(amounts, bins=20)
            plt.title('Order Amount Distribution')
            plt.xlabel('Amount')
            plt.ylabel('Frequency')
            vis['amount_distribution'] = self._fig_to_base64()
            plt.close()
        
        return vis
    
    def _generate_html_report(self, results):
        """Generate HTML report (simplified version)"""
        # This would be a complete HTML template in a real implementation
        return f"<html><body>Report generated at {datetime.now()}</body></html>"
    
    def _fig_to_base64(self):
        """Convert matplotlib figure to base64 encoded image"""
        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        return img_base64