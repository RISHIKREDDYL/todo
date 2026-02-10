FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create non-root user
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Copy application files
COPY main.py .
COPY static/ static/

# Create data directory and set ownership
RUN mkdir -p /app/data && chown -R appuser:appgroup /app/data

# Create volume mount point for database persistence
VOLUME /app/data

# Set environment variable for database path
ENV DATABASE_PATH=/app/data/todos.db

# Switch to non-root user
USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
