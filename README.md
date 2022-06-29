# <p align="center"> API - Steam Marketplace </p>

<p align="center"> <img src="https://imgur.com/9SCUZGV.png" alt="Chicken Strike!"/> </p>

_<p align="center"> An unofficial API to get data from the Steam Marketplace </p>_

## Run API

```bash
cd api/

uvicorn src.main:app --reload --workers 1 --host 0.0.0.0 --port 8000
```

You can access the endpoint via GET request:

```bash
curl http://127.0.0.1:8000/marketplace/
```

The endpoint can receive two params:

1. _item_: Represents the item you want to know the price;
1. _interval_: Sets the interval for the request. Can it be **week**, **month** or **lifetime**. If not been specified, the return be **lifetime**.

## Example

```bash
curl http://127.0.0.1:8000/marketplace?item=AWP | Asiimov&interval=lifetime
```
