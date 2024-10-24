# AioBloconomics

## Asynchronous wrapper for the [Bloconomics API](https://blockonomics.co)

## About

Used AioHTTP for the asynchronous requests and adaptix for the data validation.


## MRE

```python
from typing import AsyncIterator

from aiohttp import web

from aioblockonomics import AioBlockonomics
from aioblockonomics.enums import CurrencyCode
from aioblockonomics.models.payment import Payment

API_KEY = ""
BLOCKONOMICS_KEY = web.AppKey("blockonomics", AioBlockonomics)
MY_SECRET = ""


async def get_blockonomics(app: web.Application) -> AsyncIterator[None]:
    app[BLOCKONOMICS_KEY] = AioBlockonomics(API_KEY)
    yield
    await app[BLOCKONOMICS_KEY].session.close()


async def handle_payment(request: web.Request) -> web.Response:
    blockonomics = request.app[BLOCKONOMICS_KEY]
    payment = blockonomics.response_body_factory.load(await request.json(), Payment)
    if payment.secret != MY_SECRET:
        raise web.HTTPUnauthorized()

    rate = await blockonomics.get_btc_price(CurrencyCode.USD)
    print(f"Payed USDT: {payment.value / 10**8 / rate} USD")

    return web.Response()


def main() -> None:
    app = web.Application()
    app.cleanup_ctx.append(get_blockonomics)
    app.add_routes([web.get("/payment", handle_payment)])
    return web.run_app(app)


if __name__ == "__main__":
    main()
```