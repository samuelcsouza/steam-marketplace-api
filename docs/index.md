## Steam Marketplace API

<p align="center"> <img src="https://imgur.com/9SCUZGV.png" alt="Chicken Strike!"/> </p>

An unofficial API to get data from the Steam Marketplace.

### Installing and Run

You can get a time series from any item of steam marketplace with this API.

To run locally, go to [Github Repository](https://github.com/samuelcsouza/steam-marketplace-api), clone it and run via uvicorn.

```bash
# Clone Repo
git clone https://github.com/samuelcsouza/steam-marketplace-api.git

# Create a Virtual Env (Optional)
virtualenv venv -p python3
source venv/bin/activate

# Install dependencies
pip3 install -r api/requirements.txt

# Run API
cd api/
uvicorn src.main:app --reload --workers 1 --host 0.0.0.0 --port 8002
```

The API will be avaiable on port 8002 in your localhost [http://0.0.0.0:8002](http://0.0.0.0:8002)

### Usage

You can access the swagger documentation via [/docs](http://0.0.0.0:8002/docs) endpoint.

The endpoint [/marketplace](http://0.0.0.0:8002/marketplace) give a time series from an item what do you want. However, you need to provide an **application ID** in this route. The **application ID** refers to a game Id into Steam Platform, and a full list you can found [here](https://developer.valvesoftware.com/wiki/Steam_Application_IDs).

The parameters are:

- **[str] item**: A full name of item on Steam's Marketplace;
- **[bool] fill _(opitional)_**: Fill missing values?

#### Examples

- **CS:GO**: `http://0.0.0.0:8002/marketplace/730/?item=AK-47 | Safari Mesh (Factory New)&fill=true`
- **Team Fortress 2**: `http://0.0.0.0:8002/marketplace/440/?item=Mann Co. Supply Crate Key&fill=true`
- **Dota 2**: `http://0.0.0.0:8002/marketplace/570/?item=Magus Apex&fill=true`

Feel free to open a Pull Request or Fork this!

made with :blue_heart:
