# <p align="center"> API - Steam Marketplace </p>


<p align="center"> <img src="https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXQ9QVcJY8gulReQ0HdUuqkw9aDARJnJBdUvrOmIAJu7P_JYzpHoorvzIbbwq6iYrrVxDsG7ZEkiLzDoNzwiQG3qkA5Mm_3IY6TcA5qY1rOug_p36ruph0/360fx360f" width="350" height="350" alt="Chicken Strike!"/> </p>

_<p align="center"> An unofficial API to get data from the Steam Marketplace </p>_

## Start

1. Run API
    ```bash
    cd api/
    uvicorn src.main:app --reload --workers 1 --host 0.0.0.0 --port 8000
    ```