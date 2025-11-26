# Coffee Shop Menu Data

MENU_CATEGORIES = {
    "coffee": {
        "name": "☕ Coffee",
        "items": {
            "espresso": {"name": "Espresso", "price": 2.50},
            "americano": {"name": "Americano", "price": 3.00},
            "cappuccino": {"name": "Cappuccino", "price": 3.50},
            "latte": {"name": "Latte", "price": 3.50},
            "flat_white": {"name": "Flat White", "price": 3.50},
            "macchiato": {"name": "Macchiato", "price": 3.00},
            "mocha": {"name": "Mocha", "price": 4.00},
            "cold_brew": {"name": "Cold Brew", "price": 4.50}
        }
    },
    "desserts": {
        "name": "🍰 Desserts",
        "items": {
            "tiramisu": {"name": "Tiramisu", "price": 5.50},
            "cheesecake": {"name": "Cheesecake", "price": 4.50},
            "brownie": {"name": "Chocolate Brownie", "price": 3.50},
            "croissant": {"name": "Croissant", "price": 3.00},
            "muffin": {"name": "Muffin", "price": 3.50},
            "cookie": {"name": "Chocolate Cookie", "price": 2.50},
            "apple_pie": {"name": "Apple Pie", "price": 4.00},
            "donut": {"name": "Donut", "price": 3.00}
        }
    },
    "food": {
        "name": "🥪 Food",
        "items": {
            "sandwich": {"name": "Club Sandwich", "price": 6.50},
            "panini": {"name": "Grilled Panini", "price": 5.50},
            "salad": {"name": "Caesar Salad", "price": 7.00},
            "wrap": {"name": "Chicken Wrap", "price": 6.00},
            "quiche": {"name": "Quiche Lorraine", "price": 5.00},
            "bagel": {"name": "Bagel with Cream Cheese", "price": 4.50},
            "soup": {"name": "Soup of the Day", "price": 4.00},
            "avocado_toast": {"name": "Avocado Toast", "price": 6.50}
        }
    },
    "drinks": {
        "name": "🥤 Drinks",
        "items": {
            "water": {"name": "Mineral Water", "price": 1.50},
            "soda": {"name": "Soft Drink", "price": 2.50},
            "juice": {"name": "Fresh Juice", "price": 4.00},
            "tea": {"name": "Herbal Tea", "price": 2.50},
            "smoothie": {"name": "Fruit Smoothie", "price": 5.00},
            "lemonade": {"name": "Fresh Lemonade", "price": 3.50},
            "iced_tea": {"name": "Iced Tea", "price": 3.00},
            "milkshake": {"name": "Milkshake", "price": 4.50}
        }
    }
}

def get_category_name(category_key):
    """Get display name for category"""
    return MENU_CATEGORIES.get(category_key, {}).get("name", category_key)

def get_category_items(category_key):
    """Get all items in a category"""
    return MENU_CATEGORIES.get(category_key, {}).get("items", {})

def get_item_details(category_key, item_key):
    """Get details for a specific item"""
    items = get_category_items(category_key)
    return items.get(item_key, {})

def get_all_categories():
    """Get all available categories"""
    return list(MENU_CATEGORIES.keys())

def format_price(price):
    """Format price with currency"""
    return f"${price:.2f}"