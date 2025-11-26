# Coffee Shop Telegram Bot

A minimalistic Telegram bot for coffee shop take-away orders without prepayment or table booking.

## Features

- **Simple Order Flow**: Category → Item → Quantity → Additional Items → Pickup Time → Contact → Confirmation
- **Staff Notifications**: Automatic order notifications to staff chat
- **Repeat Orders**: Users can repeat their last order with one click
- **No Complexity**: No payments, no table booking, no loyalty system

## Project Structure

```
/
├── bot.py              # Main bot script
├── menu.py             # Menu data and categories
├── order_manager.py    # Order storage and management
├── requirements.txt    # Python dependencies
├── config.py          # Configuration settings
└── README.md          # This file
```

## Setup Instructions

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a Telegram bot via @BotFather and get your bot token

3. Configure the bot:
   - Add your bot token to config.py
   - Set your staff chat ID for notifications

4. Run the bot:
   ```bash
   python bot.py
   ```

## Bot Flow

1. **Start**: User initiates conversation with /start
2. **Category Selection**: Choose from Coffee, Desserts, Food, Drinks
3. **Item Selection**: Select specific item from chosen category
4. **Quantity**: Choose quantity (1, 2, 3, or manual entry)
5. **Additional Items**: Option to add more items or proceed
6. **Pickup Time**: Select pickup time (10, 20, 30 min, or manual)
7. **Contact**: Share phone number via Telegram contact sharing
8. **Confirmation**: Review order and confirm
9. **Staff Notification**: Order sent to staff chat
10. **Client Confirmation**: User receives pickup confirmation

## Order Format for Staff

Order notifications to staff include:
- Order number
- Customer name
- Phone number
- Items with quantities
- Pickup time

## Commands

- `/start` - Begin order process
- `/menu` - View menu categories
- `/repeat` - Repeat last order
- `/help` - Show help information