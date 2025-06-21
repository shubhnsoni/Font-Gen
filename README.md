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

## Sharing previews

To share a generated font preview with others, request `/share/<font_id>` from the backend. It returns a JSON payload containing a public URL that anyone can open to view the preview image in the browser.
