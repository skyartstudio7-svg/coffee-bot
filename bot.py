# Coffee Shop Telegram Bot

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import config
from menu import MENU_CATEGORIES, get_category_name, get_category_items, get_item_details, format_price
from order_manager import order_manager

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states
CATEGORY, ITEM, QUANTITY, ADDITIONAL_ITEMS, PICKUP_TIME, CONTACT, CONFIRMATION = range(7)

# Store user data
user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the conversation and show menu categories"""
    user = update.effective_user
    user_id = user.id
    
    # Initialize user data
    user_data[user_id] = {
        'current_order': {},
        'last_order': order_manager.get_last_user_order(user_id)
    }
    
    welcome_text = f"{config.WELCOME_MESSAGE}\n\nWhat would you like to order?"
    
    # Create category buttons
    keyboard = []
    for category_key, category_data in MENU_CATEGORIES.items():
        keyboard.append([InlineKeyboardButton(category_data['name'], callback_data=f"category_{category_key}")])
    
    # Add repeat order button if user has previous orders
    if user_data[user_id]['last_order']:
        keyboard.append([InlineKeyboardButton("🔄 Repeat Last Order", callback_data="repeat_order")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
    else:
        await update.callback_query.message.edit_text(welcome_text, reply_markup=reply_markup)
    
    return CATEGORY

async def handle_category_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle category selection"""
    query = update.callback_query
    user_id = query.from_user.id
    
    await query.answer()
    
    if query.data == "repeat_order":
        return await handle_repeat_order(update, context)
    
    category_key = query.data.replace("category_", "")
    
    # Store selected category
    if user_id not in user_data:
        user_data[user_id] = {'current_order': {}}
    
    user_data[user_id]['current_order']['category'] = category_key
    user_data[user_id]['current_order']['items'] = []
    
    # Show items in the category
    items = get_category_items(category_key)
    keyboard = []
    
    for item_key, item_data in items.items():
        button_text = f"{item_data['name']} - {format_price(item_data['price'])}"
        keyboard.append([InlineKeyboardButton(button_text, callback_data=f"item_{item_key}")])
    
    keyboard.append([InlineKeyboardButton("🔙 Back to Categories", callback_data="back_to_categories")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    category_name = get_category_name(category_key)
    
    await query.message.edit_text(
        f"{category_name}\n\nPlease select an item:",
        reply_markup=reply_markup
    )
    
    return ITEM

async def handle_item_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle item selection"""
    query = update.callback_query
    user_id = query.from_user.id
    
    await query.answer()
    
    if query.data == "back_to_categories":
        return await start(update, context)
    
    item_key = query.data.replace("item_", "")
    category_key = user_data[user_id]['current_order']['category']
    item_details = get_item_details(category_key, item_key)
    
    # Store selected item
    user_data[user_id]['current_order']['selected_item'] = {
        'key': item_key,
        'name': item_details['name'],
        'price': item_details['price']
    }
    
    # Show quantity options
    keyboard = [
        [InlineKeyboardButton("1", callback_data="qty_1"),
         InlineKeyboardButton("2", callback_data="qty_2"),
         InlineKeyboardButton("3", callback_data="qty_3")],
        [InlineKeyboardButton("Enter manually", callback_data="qty_manual")],
        [InlineKeyboardButton("🔙 Back to Items", callback_data="back_to_items")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.edit_text(
        f"{item_details['name']}\n\nHow many would you like?",
        reply_markup=reply_markup
    )
    
    return QUANTITY

async def handle_quantity_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle quantity selection"""
    query = update.callback_query
    user_id = query.from_user.id
    
    await query.answer()
    
    if query.data == "back_to_items":
        return await handle_category_selection(update, context)
    
    if query.data == "qty_manual":
        await query.message.edit_text("Please enter the quantity:")
        return QUANTITY
    
    quantity = int(query.data.replace("qty_", ""))
    
    # Add item to order
    selected_item = user_data[user_id]['current_order']['selected_item']
    selected_item['quantity'] = quantity
    user_data[user_id]['current_order']['items'].append(selected_item)
    
    # Ask about additional items
    keyboard = [
        [InlineKeyboardButton("Add more items", callback_data="add_more")],
        [InlineKeyboardButton("Proceed to checkout", callback_data="proceed_checkout")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.edit_text(
        f"Added {quantity}x {selected_item['name']} to your order.\n\nWould you like to add more items?",
        reply_markup=reply_markup
    )
    
    return ADDITIONAL_ITEMS

async def handle_additional_items(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle additional items decision"""
    query = update.callback_query
    user_id = query.from_user.id
    
    await query.answer()
    
    if query.data == "add_more":
        return await start(update, context)
    else:  # proceed_checkout
        # Show pickup time options
        keyboard = []
        for minutes in config.PICKUP_TIMES:
            keyboard.append([InlineKeyboardButton(f"In {minutes} minutes", callback_data=f"pickup_{minutes}")])
        
        keyboard.append([InlineKeyboardButton("Enter time manually", callback_data="pickup_manual")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.message.edit_text(
            "When would you like to pick up your order?",
            reply_markup=reply_markup
        )
        
        return PICKUP_TIME

async def handle_pickup_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle pickup time selection"""
    query = update.callback_query
    user_id = query.from_user.id
    
    await query.answer()
    
    if query.data == "pickup_manual":
        await query.message.edit_text("Please enter pickup time (e.g., '15 minutes', 'in 30 minutes'):")
        return PICKUP_TIME
    
    minutes = int(query.data.replace("pickup_", ""))
    pickup_time = f"In {minutes} minutes"
    
    # Store pickup time
    user_data[user_id]['current_order']['pickup_time'] = pickup_time
    
    # Request contact information
    contact_button = KeyboardButton("📱 Share Contact", request_contact=True)
    keyboard = ReplyKeyboardMarkup([[contact_button]], resize_keyboard=True, one_time_keyboard=True)
    
    await query.message.delete()
    await context.bot.send_message(
        user_id,
        config.CONTACT_REQUEST_MESSAGE,
        reply_markup=keyboard
    )
    
    return CONTACT

async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle contact information"""
    user = update.effective_user
    user_id = user.id
    
    if update.message.contact:
        phone_number = update.message.contact.phone_number
        user_name = user.full_name
    else:
        # Fallback if contact sharing is not available
        phone_number = "Not provided"
        user_name = user.full_name
    
    # Store contact info
    user_data[user_id]['current_order']['phone_number'] = phone_number
    user_data[user_id]['current_order']['user_name'] = user_name
    
    # Show order summary
    order = user_data[user_id]['current_order']
    
    summary_text = "📋 ORDER SUMMARY\n\n"
    total = 0
    
    for item in order['items']:
        item_total = item['quantity'] * item['price']
        total += item_total
        summary_text += f"• {item['name']} x{item['quantity']} - {format_price(item_total)}\n"
    
    summary_text += f"\n💰 Total: {format_price(total)}\n"
    summary_text += f"🕐 Pickup time: {order['pickup_time']}\n"
    summary_text += f"👤 Customer: {user_name}\n"
    summary_text += f"📞 Phone: {phone_number}\n\n"
    summary_text += "Please confirm your order:"
    
    keyboard = [
        [InlineKeyboardButton("✅ Confirm Order", callback_data="confirm_order")],
        [InlineKeyboardButton("❌ Cancel", callback_data="cancel_order")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(summary_text, reply_markup=reply_markup)
    
    return CONFIRMATION

async def handle_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle order confirmation"""
    query = update.callback_query
    user_id = query.from_user.id
    
    await query.answer()
    
    if query.data == "cancel_order":
        await query.message.edit_text("Order cancelled. You can start a new order anytime with /start")
        return ConversationHandler.END
    
    # Create order
    order = user_data[user_id]['current_order']
    
    order_data = order_manager.create_order(
        user_id=user_id,
        user_name=order['user_name'],
        phone_number=order['phone_number'],
        items=order['items'],
        pickup_time=order['pickup_time']
    )
    
    # Send notification to staff
    staff_message = config.STAFF_ORDER_MESSAGE.format(
        order_number=order_data['order_id'],
        customer_name=order['user_name'],
        phone_number=order['phone_number'],
        items=order_manager.format_order_for_staff(order_data)['items'],
        pickup_time=order['pickup_time'],
        user_id=user_id
    )
    
    try:
        await context.bot.send_message(config.STAFF_CHAT_ID, staff_message)
    except Exception as e:
        logger.error(f"Failed to send staff notification: {e}")
    
    # Send confirmation to user
    confirmation_message = config.ORDER_CONFIRMED_MESSAGE.format(
        pickup_time=order['pickup_time'],
        order_number=order_data['order_id']
    )
    
    await query.message.edit_text(confirmation_message)
    
    # Clean up user data
    user_data[user_id]['last_order'] = order_data
    user_data[user_id]['current_order'] = {}
    
    return ConversationHandler.END

async def handle_repeat_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle repeat last order"""
    query = update.callback_query
    user_id = query.from_user.id
    
    await query.answer()
    
    last_order = user_data[user_id]['last_order']
    
    if not last_order:
        await query.message.edit_text("No previous order found. Please start a new order.")
        return ConversationHandler.END
    
    # Create new order with same details
    order_data = order_manager.create_order(
        user_id=user_id,
        user_name=last_order['user_name'],
        phone_number=last_order['phone_number'],
        items=last_order['items'],
        pickup_time=last_order['pickup_time']
    )
    
    # Send notification to staff
    staff_message = config.STAFF_ORDER_MESSAGE.format(
        order_number=order_data['order_id'],
        customer_name=last_order['user_name'],
        phone_number=last_order['phone_number'],
        items=order_manager.format_order_for_staff(order_data)['items'],
        pickup_time=last_order['pickup_time'],
        user_id=user_id
    )
    
    try:
        await context.bot.send_message(config.STAFF_CHAT_ID, staff_message)
    except Exception as e:
        logger.error(f"Failed to send staff notification: {e}")
    
    # Send confirmation to user
    confirmation_message = config.ORDER_CONFIRMED_MESSAGE.format(
        pickup_time=last_order['pickup_time'],
        order_number=order_data['order_id']
    )
    
    await query.message.edit_text(confirmation_message)
    
    return ConversationHandler.END

async def handle_text_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages in different states"""
    user_id = update.effective_user.id
    
    # Handle manual quantity input
    if update.message.text and update.message.text.isdigit():
        quantity = int(update.message.text)
        if 1 <= quantity <= 20:  # Reasonable quantity limit
            # Add item to order
            selected_item = user_data[user_id]['current_order']['selected_item']
            selected_item['quantity'] = quantity
            user_data[user_id]['current_order']['items'].append(selected_item)
            
            # Ask about additional items
            keyboard = [
                [InlineKeyboardButton("Add more items", callback_data="add_more")],
                [InlineKeyboardButton("Proceed to checkout", callback_data="proceed_checkout")]
            ]
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                f"Added {quantity}x {selected_item['name']} to your order.\n\nWould you like to add more items?",
                reply_markup=reply_markup
            )
            
            return ADDITIONAL_ITEMS
    
    # Handle manual pickup time input
    if "minutes" in update.message.text.lower() or "min" in update.message.text.lower():
        pickup_time = update.message.text
        user_data[user_id]['current_order']['pickup_time'] = pickup_time
        
        # Request contact information
        contact_button = KeyboardButton("📱 Share Contact", request_contact=True)
        keyboard = ReplyKeyboardMarkup([[contact_button]], resize_keyboard=True, one_time_keyboard=True)
        
        await context.bot.send_message(
            user_id,
            config.CONTACT_REQUEST_MESSAGE,
            reply_markup=keyboard
        )
        
        return CONTACT
    
    # Default response
    await update.message.reply_text("Please use the buttons provided or type /start to begin a new order.")
    return None

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send help message"""
    help_text = """☕ Coffee Shop Bot Help

Commands:
• /start - Start ordering
• /help - Show this help
• /menu - View menu categories
• /repeat - Repeat your last order

How to order:
1. Choose a category (Coffee, Desserts, Food, Drinks)
2. Select your item
3. Choose quantity
4. Add more items or proceed
5. Select pickup time
6. Share your contact
7. Confirm your order

That's it! Your order will be sent to our staff."""
    
    await update.message.reply_text(help_text)

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show menu categories"""
    return await start(update, context)

async def repeat_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Repeat last order command"""
    user_id = update.effective_user.id
    
    if user_id not in user_data:
        user_data[user_id] = {'current_order': {}, 'last_order': None}
    
    user_data[user_id]['last_order'] = order_manager.get_last_user_order(user_id)
    
    if not user_data[user_id]['last_order']:
        await update.message.reply_text("No previous order found. Please start a new order with /start")
        return
    
    # Create new order with same details
    last_order = user_data[user_id]['last_order']
    
    order_data = order_manager.create_order(
        user_id=user_id,
        user_name=last_order['user_name'],
        phone_number=last_order['phone_number'],
        items=last_order['items'],
        pickup_time=last_order['pickup_time']
    )
    
    # Send notification to staff
    staff_message = config.STAFF_ORDER_MESSAGE.format(
        order_number=order_data['order_id'],
        customer_name=last_order['user_name'],
        phone_number=last_order['phone_number'],
        items=order_manager.format_order_for_staff(order_data)['items'],
        pickup_time=last_order['pickup_time'],
        user_id=user_id
    )
    
    try:
        await context.bot.send_message(config.STAFF_CHAT_ID, staff_message)
    except Exception as e:
        logger.error(f"Failed to send staff notification: {e}")
    
    # Send confirmation to user
    confirmation_message = config.ORDER_CONFIRMED_MESSAGE.format(
        pickup_time=last_order['pickup_time'],
        order_number=order_data['order_id']
    )
    
    await update.message.reply_text(confirmation_message)

def main():
    """Start the bot"""
    # Create application
    application = Application.builder().token(config.BOT_TOKEN).build()
    
    # Create conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CATEGORY: [CallbackQueryHandler(handle_category_selection)],
            ITEM: [CallbackQueryHandler(handle_item_selection)],
            QUANTITY: [
                CallbackQueryHandler(handle_quantity_selection),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_messages)
            ],
            ADDITIONAL_ITEMS: [CallbackQueryHandler(handle_additional_items)],
            PICKUP_TIME: [
                CallbackQueryHandler(handle_pickup_time),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_messages)
            ],
            CONTACT: [MessageHandler(filters.CONTACT | filters.TEXT, handle_contact)],
            CONFIRMATION: [CallbackQueryHandler(handle_confirmation)]
        },
        fallbacks=[CommandHandler('start', start), CommandHandler('help', help_command)]
    )
    
    # Add handlers
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('menu', menu_command))
    application.add_handler(CommandHandler('repeat', repeat_command))
    
    # Start the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()