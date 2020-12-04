from aiohttp import web
import ssl

app = web.Application()

WEBHOOK_SSL_CERT = "./webhook_cert.pem"
WEBHOOK_SSL_PRIV = "./webhook_pkey.pem"


context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV)


async def health_check(request):
    return web.Response(text="Hello world")

app.add_routes([
    web.get("/index", health_check, name="index")
])


if __name__ == '__main__':
    app.add_routes([web.get("/health_check/", health_check)])
    web.run_app(
        app,
        host="127.0.0.1",
        port=8080,
        ssl_context=context
    )
