# AioBloconomics

## Asynchronous wrapper for the [Bloconomics API](https://blockonomics.co)

## About

Used AioHTTP for the asynchronous requests and Pydantic for the data validation.

**Requirements:**

- python>=3.11
- aiohttp>=3.9.3
- pydantic>=2.6.4

## MRE

```python
from aioblockonomics import AioBlockonomics
from aioblockonomics.models import Payment
from aioblockonomics.enums import CurrencyCode
from aiohttp import web

API_KEY = ""


async def get_payment(
        payment: Payment, app: web.Application, blockonomics: AioBlockonomics
) -> None:
    print(
        f"Payment received: {payment.value} satoshi on address {payment.addr}. Status: {payment.status}"
    )
    print(f"Payment in BTC: {payment.btc_value}")
    btc_price = await blockonomics.get_btc_price(CurrencyCode.USD)
    print(f"BTC price in {CurrencyCode.USD}: {btc_price}")
    print(
        f"Payment in {CurrencyCode.USD}: {payment.convert_to_fiat(btc_price)}"
    )


async def on_shutdown(app: web.Application) -> None:
    blockonomics: AioBlockonomics = app["blockonomics"]
    await blockonomics.session.close()


def main() -> None:
    app = web.Application()

    blockonomics = AioBlockonomics(API_KEY)
    blockonomics.register_payment_handler(get_payment)
    app.add_routes([web.get("/payment", blockonomics.handle_payment_updates)])
    app["blockonomics"] = blockonomics
    app.on_shutdown.append(on_shutdown)

    return web.run_app(app)


if __name__ == "__main__":
    main()
```