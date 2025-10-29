# Rigol DHO824 MCP Server

An MCP (Model Context Protocol) server for controlling and querying the Rigol DHO824 oscilloscope using PyVISA.

## Installation

The recommended way to use this MCP server is via Docker, which eliminates dependency management and provides isolation.

### Quick Start with Claude Code

Pull the pre-built image from GitHub Container Registry:

```bash
docker pull ghcr.io/aimoda/rigol-dho824-mcp:latest
```

### Configuration

**IMPORTANT:** You must provide the `RIGOL_RESOURCE` environment variable with your oscilloscope's IP address (e.g., `TCPIP0::192.168.1.100::inst0::INSTR`).

#### Using Environment Variables with Docker

You can configure the Docker container with environment variables in two ways:

1. **Hardcoded values** (shown in examples below): `-e RIGOL_RESOURCE="TCPIP0::192.168.1.100::inst0::INSTR"`
2. **Pass-through from host** (recommended): `-e RIGOL_RESOURCE` (without `=value`)

When you use `-e VARIABLE_NAME` without a value, Docker automatically passes through the variable from your host environment. This is useful if you have environment variables already set in your shell (e.g., in `~/.bashrc` or `~/.zshrc`).

Add the Docker-based MCP server to Claude Code using either method:

#### Option 1: Using `claude mcp add` command

```bash
claude mcp add --scope local rigol-dho824 -- \
  docker run -i --rm \
  -v /tmp/rigol-data:/tmp/rigol \
  -e RIGOL_RESOURCE="TCPIP0::192.168.1.100::inst0::INSTR" \
  -e VISA_TIMEOUT=30000 \
  -e RIGOL_BEEPER_ENABLED=false \
  -e RIGOL_TEMP_DIR=/tmp/rigol \
  ghcr.io/aimoda/rigol-dho824-mcp:latest
```

Replace `192.168.1.100` with your oscilloscope's IP address. After adding, restart Claude Code to load the MCP server.

#### Option 2: Using `.mcp.json` file

Create a `.mcp.json` file in your project directory (or copy from `.mcp.json.example`):

```json
{
  "mcpServers": {
    "rigol-dho824": {
      "type": "stdio",
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-v",
        "/tmp/rigol-data:/tmp/rigol",
        "-e",
        "RIGOL_RESOURCE",
        "-e",
        "VISA_TIMEOUT",
        "-e",
        "RIGOL_BEEPER_ENABLED",
        "-e",
        "RIGOL_TEMP_DIR",
        "ghcr.io/aimoda/rigol-dho824-mcp:latest"
      ],
      "env": {
        "RIGOL_RESOURCE": "TCPIP0::192.168.1.100::inst0::INSTR",
        "VISA_TIMEOUT": "30000",
        "RIGOL_BEEPER_ENABLED": "false",
        "RIGOL_TEMP_DIR": "/tmp/rigol"
      }
    }
  }
}
```

Replace `192.168.1.100` with your oscilloscope's IP address.

After configuring, restart Claude Code to load the MCP server.

### Optional Environment Variables

- `VISA_TIMEOUT`: Communication timeout in milliseconds (default: 30000)
- `RIGOL_BEEPER_ENABLED`: Enable/disable oscilloscope beeper sounds (default: false)
- `RIGOL_TEMP_DIR`: Custom directory for temporary files (waveforms, screenshots). If not set, uses system default temp directory. **Required for Docker deployments** if you need to access captured data outside the container.

### Accessing Temp Files in Docker

By default, temporary files (waveform captures, screenshots) are stored inside the Docker container and are inaccessible from the host system. To access these files, you must:

1. **Create a directory on your host** for storing temporary files:
   ```bash
   mkdir -p /tmp/rigol-data
   ```

2. **Mount this directory as a volume** in your Docker configuration (see the `.mcp.json` example above):
   ```json
   "-v",
   "/tmp/rigol-data:/tmp/rigol",
   ```
   This maps the host directory `/tmp/rigol-data` to `/tmp/rigol` inside the container.

3. **Set the `RIGOL_TEMP_DIR` environment variable** to point to the mounted directory inside the container:
   ```json
   "RIGOL_TEMP_DIR": "/tmp/rigol"
   ```

**Important notes:**
- The directory specified in `RIGOL_TEMP_DIR` must exist before starting the server
- Temporary files are **not automatically cleaned up** when using a custom temp directory
- You are responsible for manually cleaning up old waveform and screenshot files
- Files will be organized in subdirectories like `waveform_capture_<timestamp>/` for waveforms and `screenshot_<timestamp>.png` for screenshots

**Example: Manual cleanup**
```bash
# Remove waveform captures older than 7 days
find /tmp/rigol-data -type d -name "waveform_capture_*" -mtime +7 -exec rm -rf {} \;

# Remove screenshots older than 7 days
find /tmp/rigol-data -type f -name "screenshot_*.png" -mtime +7 -delete
```

### Troubleshooting

#### Container exits immediately
- Ensure you're using the `-i` flag (interactive mode)
- Verify `RIGOL_RESOURCE` is set correctly

#### Cannot connect to oscilloscope
- Verify oscilloscope IP address and network connectivity (`ping <ip-address>`)
- Check oscilloscope's remote control settings are enabled

#### Environment variables not working
- Ensure you're using `-e VARIABLE_NAME` in the Docker args array
- Set the actual values in the `env` field of `.mcp.json`

### Building Locally

To build the Docker image yourself:

```bash
docker build -t rigol-dho824-mcp:local .
```

Then use `rigol-dho824-mcp:local` as the image name in your configuration.

## Development Setup

For local development and contributions, you can install the MCP server in a Python virtual environment.

### Create and activate virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install the package
```bash
# Install in editable mode for development
pip install -e .

# Or just install dependencies
pip install -r requirements.txt
```

### Add to Claude Code

After completing the setup steps above, add the local development MCP server to Claude Code:

```bash
claude mcp add --scope local rigol-dho824 -- <path-to-this-repo>/venv/bin/rigol-dho824-mcp
```

Replace `<path-to-this-repo>` with the actual path to this repository.

## Development Configuration

The server can be configured using environment variables. Create a `.env` file from the example:

```bash
cp .env.example .env
```

Then edit `.env` to set your configuration:

- `RIGOL_RESOURCE`: VISA resource string for the oscilloscope
  - Example: `TCPIP0::192.168.1.100::inst0::INSTR`
  - Leave empty for auto-discovery
- `VISA_TIMEOUT`: Communication timeout in milliseconds (default: 5000)

## Running the Server (Development)

For local development and testing, you can run the server directly with Python:

### STDIO Transport
```bash
# Auto-discover oscilloscope
python -m rigol_dho824_mcp.server

# Or set resource string via environment variable
export RIGOL_RESOURCE="TCPIP0::192.168.1.100::inst0::INSTR"
python -m rigol_dho824_mcp.server
```

### HTTP Transport
```bash
# Default HTTP server (http://127.0.0.1:8000/mcp)
python -m rigol_dho824_mcp.server --http

# Custom host and port
python -m rigol_dho824_mcp.server --http --host 0.0.0.0 --port 3000

# Custom path
python -m rigol_dho824_mcp.server --http --path /api/mcp
```

