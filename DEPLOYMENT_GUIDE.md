# Coffee Shop Telegram Bot - Deployment Guide

## Overview

This is a complete Telegram bot system for coffee shop take-away orders. The bot follows a simple, minimalistic flow without payments or complex features.

## Features Implemented

✅ **Core Order Flow**
- Category selection (Coffee, Desserts, Food, Drinks)
- Item selection with dynamic lists
- Quantity selection (1, 2, 3, manual entry)
- Additional items option
- Pickup time selection (10, 20, 30 min, manual)
- Contact sharing via Telegram
- Order confirmation and staff notifications

✅ **Additional Features**
- Repeat last order functionality
- Order history and storage
- Staff chat integration
- Order ID auto-generation
- Inline keyboard navigation

✅ **Technical Features**
- Conversation state management
- Error handling and logging
- Data persistence
- Contact sharing integration
- Message editing for smooth flow

## Quick Start

### 1. Prerequisites

- Python 3.7+
- Telegram Bot Token (from @BotFather)
- Staff Chat ID for notifications

### 2. Installation

```bash
# Clone or download the bot files
cd coffee-shop-bot

# Install dependencies
pip install -r requirements.txt

# Run setup script
python setup.py
```

### 3. Configuration

Edit `config.py` with your settings:

```python
# Required settings
BOT_TOKEN = "123456789:ABCdefGHIjklMNOpqrSTUvwxyz"  # From @BotFather
STAFF_CHAT_ID = "-1001234567890"  # Your staff group/chat ID

# Optional customizations
BOT_NAME = "Your Coffee Shop Bot"
WELCOME_MESSAGE = "Welcome to our coffee shop!"
```

### 4. Getting Required IDs

#### Bot Token
1. Message @BotFather on Telegram
2. Create new bot with `/newbot`
3. Copy the token provided

#### Staff Chat ID
1. Add your bot to the staff group/chat
2. Send a message in the group
3. Visit: `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
4. Find the chat ID (negative number for groups)

### 5. Running the Bot

```bash
python bot.py
```

The bot will start and begin polling for messages.

## Bot Commands

- `/start` - Begin order process
- `/menu` - View menu categories
- `/repeat` - Repeat last order
- `/help` - Show help information

## Order Flow Details

### 1. Category Selection
Users choose from 4 main categories:
- ☕ Coffee (8 items)
- 🍰 Desserts (8 items)
- 🥪 Food (8 items)
- 🥤 Drinks (8 items)

### 2. Item Selection
Dynamic item lists based on selected category. Each item shows name and price.

### 3. Quantity Selection
Quick buttons for 1, 2, 3 or manual entry option.

### 4. Additional Items
Users can add more items or proceed to checkout.

### 5. Pickup Time
Predefined options (10, 20, 30 minutes) or manual entry.

### 6. Contact Information
Uses Telegram's built-in contact sharing feature for phone numbers.

### 7. Order Confirmation
Complete order summary with confirm/cancel options.

### 8. Staff Notification
Order details sent to configured staff chat including:
- Order number
- Customer name and phone
- Items with quantities and prices
- Pickup time
- User ID for reference

## Customization

### Menu Items
Edit `menu.py` to customize:
- Category names and emojis
- Menu items and prices
- Item descriptions

### Messages
Edit `config.py` to customize:
- Welcome messages
- Confirmation texts
- Staff notification format
- Button labels

### Order Settings
Edit `config.py` to change:
- Order prefix (default: "COFFEE")
- Starting order number
- Pickup time options

## Data Storage

- Orders stored in `orders.json`
- User session data in memory
- Automatic order ID generation
- Order history tracking

## Testing

### Demo Mode
Run the setup script in demo mode:
```bash
python setup.py demo
```

This creates a demo configuration for testing the bot structure.

### Testing Checklist

1. ✅ Bot responds to `/start`
2. ✅ Category selection works
3. ✅ Item selection displays correctly
4. ✅ Quantity selection functions
5. ✅ Additional items flow works
6. ✅ Pickup time selection
7. ✅ Contact sharing integration
8. ✅ Order confirmation
9. ✅ Staff notifications sent
10. ✅ Repeat order functionality

## Troubleshooting

### Common Issues

1. **Bot not responding**
   - Check bot token in config.py
   - Ensure bot is started with `python bot.py`

2. **Staff not receiving notifications**
   - Verify staff chat ID in config.py
   - Ensure bot is added to staff group
   - Check bot has permission to send messages

3. **Contact sharing not working**
   - User must tap the "Share Contact" button
   - Some Telegram clients may have restrictions

4. **Order flow stuck**
   - Users can restart with `/start`
   - Check logs for error messages

### Logs

Bot logs are displayed in console. Check for:
- Error messages
- Warning messages
- Successful order processing
- Staff notification status

## Production Deployment

### Server Requirements

- Python 3.7+ environment
- Stable internet connection
- Sufficient storage for logs

### Running Continuously

Use process managers like:
- systemd (Linux)
- PM2 (Node.js style)
- Docker containers
- Cloud platforms (Heroku, AWS, etc.)

### Monitoring

- Monitor bot logs for errors
- Track order volumes
- Monitor staff notification delivery
- Regular backup of order data

## Security Considerations

- Keep bot token secure
- Validate user inputs
- Limit order quantities
- Monitor for abuse
- Regular security updates

## Support

For issues and questions:
1. Check this deployment guide
2. Review bot logs
3. Test with demo mode
4. Verify configuration settings

## License

This bot is provided as-is for coffee shop use. Customize as needed for your specific requirements.