import logging 
from telegram import Update 
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackContext 
import gspread 
from oauth2client.service_account import ServiceAccountCredentials

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO) 
logger = logging.getLogger(__name__) 

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None: 
    await update.message.reply_text('Привет родитель, введи номер ученика от 1 до 3')

    
async def handle_message(update: Update, context: CallbackContext) -> None: 
    number = update.message.text

    scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"] 
    credentials_json = 'credentials.json' 
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_json, scope) 
    client = gspread.authorize(credentials) 
    spreadsheet_url = '' 
    spreadsheet = client.open_by_url(spreadsheet_url)

    sheet = spreadsheet.sheet1 

    records = sheet.get_all_values() 

    record_found = False 
    for record in records:
        if record[0] == number:
            record_found = True
            await context.bot.send_message(chat_id=update.effective_chat.id, text='{}'.format(record))
            break

    if not record_found: 
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Запись с таким номером не существует') 
    
def error(update: Update, context: CallbackContext) -> None: 
        logger.warning('Update "%s" caused error "%s"', update, context.error)
def main() -> None: 
    # Create the Application and pass it your bot's token. 
    application = Application.builder().token("").build()

   # on different commands - answer in Telegram 
    application.add_handler(CommandHandler("start", start)) 

    # on non command i.e message - echo the message on Telegram 
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)) 

    # Run the bot until the user presses Ctrl-C 
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__': 
    main()