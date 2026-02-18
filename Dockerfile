FROM ghcr.io/astral-sh/uv:0.10.3-python3.14-alpine AS build
# Explicitly set the default shell to sh (this is the default on Linux images anyway)
SHELL ["/bin/sh", "-c"]

# Set environment variables to use system-wide installation
ENV UV_SYSTEM_PYTHON="true"
ENV UV_PROJECT_ENVIRONMENT="/usr/local/"
ENV PATH="/usr/local/bin:$PATH"

WORKDIR /app

# Copy dependency files (pyproject.toml and uv.lock) for caching
COPY pyproject.toml uv.lock ./

# Install production dependencies using uv sync --no-dev
# --locked ensures deterministic installs based on the lock file
COPY . /app
RUN uv sync --locked --no-dev

# Stage 2: Runtime stage
FROM python:3.14-alpine3.23

# Set the same environment variables as the build stage
ENV UV_SYSTEM_PYTHON="true"
ENV UV_PROJECT_ENVIRONMENT="/usr/local/"
ENV PATH="/usr/local/bin:$PATH"

WORKDIR /app

# Copy installed packages from the build stage
COPY --from=build /usr/local/bin /usr/local/bin
COPY --from=build /usr/local/lib /usr/local/lib

# Copy application source code
COPY . .

# Append /app to the PYTHONPATH environment variable
ENV PYTHONPATH="$PYTHONPATH:."

EXPOSE 8000

# Command to run your application
CMD uv run python src/main.py



#FROM python:3.14-slim
#
#WORKDIR /src
#
#COPY requirements22.txt ./
#RUN pip install --no-cache-dir -r requirements22.txt
#
#COPY . .
#
#EXPOSE 5432
#EXPOSE 8000
#
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]