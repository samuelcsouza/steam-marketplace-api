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
curl http://0.0.0.0:8002/marketplace/?item=AK-47 | Safari Mesh (Factory New)
```

The endpoint receive one param:

1. _item_: Represents the item you want to know the price;

## References

- [https://steamapi.xpaw.me/](https://steamapi.xpaw.me/)
- [https://steamcommunity.com/dev](https://steamcommunity.com/dev)
- [https://developer.valvesoftware.com/wiki/Steam_Web_API](https://developer.valvesoftware.com/wiki/Steam_Web_API)
- [https://partner.steamgames.com/doc/webapi_overview](https://partner.steamgames.com/doc/webapi_overview)
- [https://developer.valvesoftware.com/wiki/Steam_Application_IDs](https://developer.valvesoftware.com/wiki/Steam_Application_IDs)
