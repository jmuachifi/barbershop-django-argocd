# Stage 1: Build the app with dependencies
FROM python:3.12-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y build-essential libpq-dev curl && \
    pip install --upgrade pip

# Copy requirements and install dependencies globally
COPY barbershop/requirments.txt .
RUN pip install --no-cache-dir -r requirments.txt

# Copy the application code
COPY barbershop /app/barbershop

# Stage 2: Create the final image using Distroless
FROM gcr.io/distroless/python3

WORKDIR /app

# Copy the installed dependencies and application code from the builder stage
COPY --from=builder /usr/local /usr/local
COPY --from=builder /app/barbershop /app/barbershop

# Expose the port
EXPOSE 8000

# Set the entrypoint explicitly for the Python binary in Distroless
ENTRYPOINT ["/usr/local/bin/python3"]

# Set the default command to run the Django app
CMD ["barbershop/manage.py", "runserver", "0.0.0.0:8000"]
