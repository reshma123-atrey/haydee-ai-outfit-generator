FROM python:3.12-slim

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel packaging
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Set default entrypoint
ENTRYPOINT ["python", "-m", "haydee_outfit_gen.main"]
