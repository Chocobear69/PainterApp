import config
import telebot
from aiohttp import web
import ssl

WEBHOOK_LISTEN = "0.0.0.0"
WEBHOOK_PORT = 443

WEBHOOK_SSL_CERT = "./webhook_cert.pem"
WEBHOOK_SSL_PRIV = "./webhook_pkey.pem"

API_TOKEN = config.token
bot = telebot.TeleBot(API_TOKEN)

app = web.Application()


async def handle(request):
    if request.match_info.get("token") == bot.token:
        request_body_dict = await request.json()
        update = telebot.types.Update.de_json(request_body_dict)
        bot.process_new_updates([update])
        return web.Response()
    else:
        return web.Response(status=403)

app.router.add_post("/{token}/", handle)

help_string = ["*Some bot* - just a bot.\n\n", "/start - greetings\n", "/help - shows this help"]


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.send_message(message.chat.id, "What is up")


@bot.message_handler(commands=["help"])
def send_help(message):
    bot.send_message(message.chat.id, "No help for you, Nigger", parse_mode="Markdown")


context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV)

# start aiohttp server (our bot)
web.run_app(
    app,
    host=WEBHOOK_LISTEN,
    port=WEBHOOK_PORT,
    ssl_context=context,
)
