# FontGen AI Studio Starter

This repo contains minimal boilerplate files for every runtime referenced in the universal setup script.

## Running the vertical slice

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the backend:
   ```bash
   python backend.py
   ```
3. Open `index.html` in your browser and try generating fonts. Free users are limited to three generations unless `api_key: "premium"` is provided in the request payload.

## Production usage with Docker

Build the container and run it:

```bash
docker build -t fontgen .
docker run -p 5050:5050 fontgen
```

The API will be available at `http://localhost:5050/`.

