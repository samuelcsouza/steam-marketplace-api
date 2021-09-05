# steam-marketplace-api
An unofficial API to get data from the Steam Marketplace.

1. Start API
    ```bash
    cd api/
    uvicorn src.main:app --reload --workers 1 --host 0.0.0.0 --port 8000
    ```