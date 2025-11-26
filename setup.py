#!/usr/bin/env python3
"""
Coffee Shop Telegram Bot Setup Script
"""

import os
import sys
import json

def setup_bot():
    """Setup the coffee shop bot"""
    print("🍵 Coffee Shop Telegram Bot Setup")
    print("=" * 40)
    
    # Check if requirements are installed
    try:
        import telegram
        print("✅ python-telegram-bot is installed")
    except ImportError:
        print("❌ python-telegram-bot not found")
        print("Installing requirements...")
        os.system(f"{sys.executable} -m pip install -r requirements.txt")
    
    # Create configuration file if it doesn't exist
    if not os.path.exists("config.py"):
        print("\nCreating configuration file...")
        with open("config.py", "w") as f:
            f.write('''# Telegram Bot Configuration

# Bot token from @BotFather
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# Staff chat ID for order notifications
STAFF_CHAT_ID = "YOUR_STAFF_CHAT_ID_HERE"

# Bot settings
BOT_NAME = "Coffee Shop Bot"
WELCOME_MESSAGE = "Welcome to our Coffee Shop! 🍵\\n\\nI can help you place a take-away order. Just follow the simple steps."

# Order settings
ORDER_PREFIX = "COFFEE"
ORDER_COUNTER_START = 1000

# Pickup time options (in minutes)
PICKUP_TIMES = [10, 20, 30]

# Contact sharing message
CONTACT_REQUEST_MESSAGE = "Please share your contact information so we can reach you if needed.\\n\\nTap the button below to share your contact."

# Confirmation messages
ORDER_CONFIRMED_MESSAGE = "✅ Your order is accepted!\\n\\nThe barista is preparing it.\\nPickup time: {pickup_time}\\nOrder number: {order_number}\\n\\nThank you for choosing us! ☕"

STAFF_ORDER_MESSAGE = """🆕 NEW ORDER #{order_number}

👤 Customer: {customer_name}
📞 Phone: {phone_number}

📋 Items:
{items}

🕐 Pickup time: {pickup_time}
💬 User ID: {user_id}
"""''')
        print("✅ Configuration file created")
        print("⚠️  Please edit config.py with your bot token and staff chat ID")
    
    # Create sample data directory
    if not os.path.exists("data"):
        os.makedirs("data")
        print("✅ Created data directory")
    
    print("\n🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Get your bot token from @BotFather on Telegram")
    print("2. Add the token to config.py")
    print("3. Get your staff chat ID")
    print("4. Add the staff chat ID to config.py")
    print("5. Run the bot with: python bot.py")
    print("\nFor testing, you can use the demo mode below.")

def demo_mode():
    """Run bot in demo mode with test data"""
    print("\n🎮 DEMO MODE")
    print("=" * 20)
    print("This will create a demo environment with sample data.")
    
    # Create demo config
    demo_config = '''# Demo Configuration
BOT_TOKEN = "demo_token_12345"
STAFF_CHAT_ID = "demo_staff_chat"
BOT_NAME = "Demo Coffee Bot"
WELCOME_MESSAGE = "Welcome to Demo Coffee Shop! 🍵"
ORDER_PREFIX = "DEMO"
ORDER_COUNTER_START = 1000
PICKUP_TIMES = [10, 20, 30]
CONTACT_REQUEST_MESSAGE = "Please share your contact:"
ORDER_CONFIRMED_MESSAGE = "✅ Order #{order_number} confirmed! Pickup: {pickup_time}"
STAFF_ORDER_MESSAGE = "DEMO ORDER: {order_number} for {customer_name}"
'''
    
    with open("demo_config.py", "w") as f:
        f.write(demo_config)
    
    print("✅ Demo configuration created")
    print("⚠️  This is just a demo - you need real bot token to run actual bot")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo_mode()
    else:
        setup_bot()