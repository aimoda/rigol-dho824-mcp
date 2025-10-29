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

# Create non-root user
RUN useradd -m -u 1000 mcp && \
    mkdir -p /app && \
    chown -R mcp:mcp /app

WORKDIR /app

# Copy installed package from builder
COPY --from=builder /install /usr/local

# Switch to non-root user
USER mcp

# Set default environment variables (can be overridden)
ENV VISA_TIMEOUT=30000
ENV RIGOL_BEEPER_ENABLED=false

# Default to stdio mode for MCP compatibility
# Users MUST provide RIGOL_RESOURCE via docker run -e RIGOL_RESOURCE=...
CMD ["rigol-dho824-mcp"]
