# Build stage
FROM python:3.13-slim AS builder

WORKDIR /build

# Copy only package definition files first for better layer caching
COPY pyproject.toml ./
COPY README.md ./

# Copy source code
COPY src/ ./src/

# Install the package
RUN pip install --no-cache-dir --prefix=/install .

# Runtime stage
FROM python:3.13-slim

# MCP registry validation label
LABEL io.modelcontextprotocol.server.name="io.github.aimoda/rigol-dho824-mcp"
LABEL org.opencontainers.image.licenses="MIT"

# Create non-root user and temp directory
RUN useradd -m -u 1000 mcp && \
    mkdir -p /app /tmp/rigol && \
    chown -R mcp:mcp /app /tmp/rigol

WORKDIR /app

# Copy installed package from builder
COPY --from=builder /install /usr/local

# Switch to non-root user
USER mcp

# Set default environment variables (can be overridden)
ENV VISA_TIMEOUT=30000
ENV RIGOL_BEEPER_ENABLED=false

# Enable container path translation (container paths → host paths)
# This makes the server translate /tmp/rigol paths to host paths specified by RIGOL_TEMP_DIR
ENV RIGOL_CONTAINER_PATH_TRANSLATION=true

# Default to stdio mode for MCP compatibility
# Users MUST provide:
# - RIGOL_RESOURCE: oscilloscope connection string
# - RIGOL_TEMP_DIR: host-side path for returned file paths
CMD ["rigol-dho824-mcp"]
