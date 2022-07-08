# <p align="center"> API - Steam Marketplace </p>

<p align="center"> <img src="https://imgur.com/9SCUZGV.png" alt="Chicken Strike!"/> </p>

_<p align="center"> An unofficial API to get data from the Steam Marketplace </p>_

## Run API

### Via Terminal

```bash
cd api/

uvicorn src.main:app --reload --workers 1 --host 0.0.0.0 --port 8002
```

### Via docker-compose

```bash
docker-compose up --build
```

### Example

```bash
wget --no-check-certificate \
  --method GET \
   'http://0.0.0.0:8002/marketplace/?item=AK-47 | Safari Mesh (Factory New)&fill=true'
```

The endpoint receive two parameters:

1. _item_: Represents the item you want to know the price;
1. _fill (optional)_: Fill values with the last observation. _Default is true_.

## References

- [https://steamapi.xpaw.me/](https://steamapi.xpaw.me/)
- [https://steamcommunity.com/dev](https://steamcommunity.com/dev)
- [https://developer.valvesoftware.com/wiki/Steam_Web_API](https://developer.valvesoftware.com/wiki/Steam_Web_API)
- [https://partner.steamgames.com/doc/webapi_overview](https://partner.steamgames.com/doc/webapi_overview)
- [https://developer.valvesoftware.com/wiki/Steam_Application_IDs](https://developer.valvesoftware.com/wiki/Steam_Application_IDs)
