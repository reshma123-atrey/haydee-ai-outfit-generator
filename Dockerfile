FROM python:3.12-slim

# Install ImageMagick and system dependencies required for Wand
RUN apt-get update && apt-get install -y --no-install-recommends \
    imagemagick \
    libmagickwand-dev \
    && rm -rf /var/lib/apt/lists/*

# Fix ImageMagick policy to allow reading/writing PDF/DDS/etc if needed
# (By default it's usually fine, but some slim setups need policy tweaks)

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel packaging
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Set default entrypoint
ENTRYPOINT ["python", "main.py"]
