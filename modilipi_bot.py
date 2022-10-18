
import logging

import os

from quote2image import convert, get_base64

from telegram import __version__ as TG_VER

from aksharamukha import transliterate

from telegram import ForceReply, Update

from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TOKEN = os.environ['TOKEN']

try:

    from telegram import __version_info__

except ImportError:

    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]


if __version_info__ < (20, 0, 0, "alpha", 1):

    raise RuntimeError(

        f"This example is not compatible with your current PTB version {TG_VER}. To view the "

        f"{TG_VER} version of this example, "

        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"

    )


# Enable logging

logging.basicConfig(

    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO

)

logger = logging.getLogger(__name__)



# Define a few command handlers. These usually take the two arguments update and

# context.

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    """Send a message when the command /start is issued."""

    user = update.effective_user

    await update.message.reply_html(

        rf"नमस्कार {user.mention_html()}, कृपया तुमचा मोडीमधे हवा असणार मजकूर देवनागरीत लिहून पाठवा.",

        reply_markup=ForceReply(selective=True),

    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    """Send a message when the command /help is issued."""

    await update.message.reply_text("Help!")



async def translated_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    text = update.message.text
    translated_text = transliterate.process('Devanagari', 'Modi', text)
    img=convert(
        quote=translated_text,
        fg="white",
        image=os.path.join(BASE_DIR, 'MoDiLipiBot\\background_image', 'background1.png'),
        border_color="white",
        font_size=70,
        width=1200,
        height=670)

    # Save The Image as a Png file
    generated_image = img.save(os.path.join(BASE_DIR, 'MoDiLipiBot\\generated_image', 'quote.png'))
    await update.message.reply_photo(photo=open(os.path.join(BASE_DIR, 'MoDiLipiBot\\generated_image', 'quote.png'), 'rb'))


def main() -> None:

    """Start the bot."""

    # Create the Application and pass it your bot's token.

    application = Application.builder().token(TOKEN).build()


    # on different commands - answer in Telegram

    application.add_handler(CommandHandler("start", start))

    application.add_handler(CommandHandler("help", help_command))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translated_text))


    # Run the bot until the user presses Ctrl-C

    application.run_polling()



if __name__ == "__main__":

    main()