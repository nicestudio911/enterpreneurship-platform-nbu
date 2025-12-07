# Logo Setup Instructions

To use your INNOVATEX logo image:

1. **Place your logo file** in the `/frontend/public/` directory with one of these names:
   - `logo.png` (recommended)
   - `logo.jpg` or `logo.jpeg`
   - `logo.svg`

2. **Supported formats:**
   - PNG (recommended for best quality)
   - JPG/JPEG
   - SVG

3. **The app will automatically:**
   - Use `logo.png` if it exists
   - Fall back to `logo.svg` if PNG is not found
   - Display the logo in the navigation bar and on login/signup pages

4. **After adding your logo file:**
   - Rebuild the frontend: `docker compose up -d --build frontend`
   - Or restart the containers: `docker compose restart frontend`

The logo should be optimized for web use (recommended size: 200-300px width for best results).

