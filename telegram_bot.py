import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters

import telegram_func as tgf
from db import Database

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Initialize database
db = Database()

def start(update: Update, context: CallbackContext):
    # Introduce the bot and show the available functions
    user_name = update.effective_user.first_name
    text = f"Hello, {user_name}! I'm your remote team management bot. Here are the available functions:"
    keyboard = [
        [InlineKeyboardButton("Add Task", callback_data="add_task"), InlineKeyboardButton("Task List", callback_data="task_list")],
        [InlineKeyboardButton("Add Event", callback_data="add_event"), InlineKeyboardButton("Event List", callback_data="event_list")],
        [InlineKeyboardButton("Upload File", callback_data="upload_file"), InlineKeyboardButton("File List", callback_data="file_list")],
        [InlineKeyboardButton("Delete Task", callback_data="delete_task"), InlineKeyboardButton("Delete Event", callback_data="delete_event"), InlineKeyboardButton("Delete File", callback_data="delete_file")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(text, reply_markup=reply_markup)

def handle_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == "add_task":
        reply_keyboard = [['2023-04-25', '2023-04-26'], ['2023-04-27', '2023-04-28'], ['2023-04-29', '2023-04-30']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        query.message.reply_text("Please select the task deadline:", reply_markup=markup)
        context.user_data["state"] = "add_task"

    # Implement other callback functions similarly
def handle_reply(update: Update, context: CallbackContext):
    user = update.message.from_user
    state = context.user_data.get("state")

    if state == "add_task":
        task_deadline = update.message.text
        context.user_data["task_deadline"] = task_deadline
        update.message.reply_text("Please enter the task name:")
        context.user_data["state"] = "add_task_name"

    elif state == "add_task_name":
        task_name = update.message.text
        task_deadline = context.user_data.get("task_deadline")
        db.add_task(user.id, task_name, task_deadline)
        update.message.reply_text(f"Task '{task_name}' with deadline '{task_deadline}' has been added.")
        context.user_data["state"] = None

    # Implement other reply states similarly

def main():
    updater = Updater("5884394290:AAHSK-A43E-IhrI2wqF5Ylsi6p_otLwpe8E")

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(handle_callback))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_reply))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
