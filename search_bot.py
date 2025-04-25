import gspread
from google.oauth2.service_account import Credentials
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Google Sheets API setup
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file("telegrambotproject-457814-962524ef2697.json", scopes=scope)
client = gspread.authorize(creds)
sheet = client.open("Digital Shop Advance").sheet1

# Telegram Bot Functions
async def Hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello!Welcome to Digital Shop Send me a keyword using /<your keyword>")

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please send a keyword like: /search nighty")
        return

    keyword = " ".join(context.args).strip().lower()
    all_rows = sheet.get_all_values()

    for row in all_rows[1:]:  # Skip header row
        if row[0].strip().lower() == keyword:
            product_name = row[1]
            product_link = row[2]
            image_link = row[3]

            await update.message.reply_text(
                f"🛍️ *{product_name}*\n🔗 [View Product]({product_link})\n🖼️ Image: {image_link}",
                parse_mode='Markdown',
                disable_web_page_preview=False
            )
            return

    await update.message.reply_text("❌ No product found for this keyword.")

# Start the bot
app = ApplicationBuilder().token("7643830745:AAGNIaU2KmlMRRvnUcBdbW1Usi90kRVsjOw").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("search", search))
app.run_polling()
