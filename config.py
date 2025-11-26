# Telegram Bot Configuration

# Bot token from @BotFather
BOT_TOKEN = "8219320444:AAGtXKl5qBM6w0UMlcCB2QJ3Hh2KMu4Hryc"

# Staff chat ID for order notifications
STAFF_CHAT_ID = "YOUR_STAFF_CHAT_ID_HERE"

# Bot settings
BOT_NAME = "Coffee Shop Bot"
WELCOME_MESSAGE = "Welcome to our Coffee Shop! 🍵\n\nI can help you place a take-away order. Just follow the simple steps."

# Order settings
ORDER_PREFIX = "COFFEE"
ORDER_COUNTER_START = 1000

# Pickup time options (in minutes)
PICKUP_TIMES = [10, 20, 30]

# Contact sharing message
CONTACT_REQUEST_MESSAGE = "Please share your contact information so we can reach you if needed.\n\nTap the button below to share your contact."

# Confirmation messages
ORDER_CONFIRMED_MESSAGE = "✅ Your order is accepted!\n\nThe barista is preparing it.\nPickup time: {pickup_time}\nOrder number: {order_number}\n\nThank you for choosing us! ☕"

STAFF_ORDER_MESSAGE = """🆕 NEW ORDER #{order_number}

👤 Customer: {customer_name}
📞 Phone: {phone_number}

📋 Items:
{items}

🕐 Pickup time: {pickup_time}
💬 User ID: {user_id}
"""
