# Order Management System

import json
import os
from datetime import datetime
from config import ORDER_PREFIX, ORDER_COUNTER_START

class OrderManager:
    def __init__(self, storage_file="orders.json"):
        self.storage_file = storage_file
        self.orders = self.load_orders()
        self.current_order_id = self.get_next_order_id()
    
    def load_orders(self):
        """Load orders from storage file"""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_orders(self):
        """Save orders to storage file"""
        with open(self.storage_file, 'w') as f:
            json.dump(self.orders, f, indent=2)
    
    def get_next_order_id(self):
        """Generate next order ID"""
        if not self.orders:
            return ORDER_COUNTER_START
        max_id = max(int(key.split('_')[1]) for key in self.orders.keys())
        return max_id + 1
    
    def create_order(self, user_id, user_name, phone_number, items, pickup_time):
        """Create a new order"""
        order_id = f"{ORDER_PREFIX}_{self.current_order_id:04d}"
        
        order_data = {
            "order_id": order_id,
            "user_id": user_id,
            "user_name": user_name,
            "phone_number": phone_number,
            "items": items,
            "pickup_time": pickup_time,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "completed_at": None
        }
        
        self.orders[order_id] = order_data
        self.current_order_id += 1
        self.save_orders()
        
        return order_data
    
    def get_order(self, order_id):
        """Get order by ID"""
        return self.orders.get(order_id)
    
    def get_user_orders(self, user_id):
        """Get all orders for a user"""
        return [order for order in self.orders.values() if order['user_id'] == user_id]
    
    def get_last_user_order(self, user_id):
        """Get the most recent order for a user"""
        user_orders = self.get_user_orders(user_id)
        if user_orders:
            return max(user_orders, key=lambda x: x['created_at'])
        return None
    
    def complete_order(self, order_id):
        """Mark order as completed"""
        if order_id in self.orders:
            self.orders[order_id]['status'] = 'completed'
            self.orders[order_id]['completed_at'] = datetime.now().isoformat()
            self.save_orders()
            return True
        return False
    
    def format_order_for_staff(self, order_data):
        """Format order for staff notification"""
        items_text = ""
        total = 0
        
        for item in order_data['items']:
            item_total = item['quantity'] * item['price']
            total += item_total
            items_text += f"• {item['name']} x{item['quantity']} - ${item_total:.2f}\n"
        
        items_text += f"\n💰 Total: ${total:.2f}"
        
        return {
            "order_number": order_data['order_id'],
            "customer_name": order_data['user_name'],
            "phone_number": order_data['phone_number'],
            "items": items_text,
            "pickup_time": order_data['pickup_time'],
            "user_id": order_data['user_id']
        }

# Global order manager instance
order_manager = OrderManager()