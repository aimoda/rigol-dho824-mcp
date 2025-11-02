# Rigol DHO824 MCP Server

[![PyPI version](https://img.shields.io/pypi/v/rigol-dho824-mcp.svg)](https://pypi.org/project/rigol-dho824-mcp/)
[![GHCR](https://ghcr-badge.yuchanns.xyz/aimoda/rigol-dho824-mcp/tags?n=4&label=ghcr)](https://github.com/aimoda/rigol-dho824-mcp/pkgs/container/rigol-dho824-mcp)

An MCP (Model Context Protocol) server for controlling and querying the Rigol DHO824 oscilloscope.

![Demo of oscilloscope in action](https://raw.githubusercontent.com/aimoda/rigol-dho824-mcp/main/demo.webp)

Built by [ai.moda](https://www.ai.moda/en/?utm_campaign=rigol-dho824-mcp).

## Hardware Requirements

### Supported Models

This project **only supports DHO804/DHO824** oscilloscopes (identical hardware). We recommend purchasing a **DHO804**.

### Firmware Requirements

**IMPORTANT:** The DHO804 must be flashed to DHO824 firmware before using this MCP server. Use the [rigol_vendor_bin](https://github.com/zelea2/rigol_vendor_bin) project to flash your oscilloscope.

**Supported Firmware Version:** 00.01.04

This is the only firmware version we test and support. Other firmware versions may work but are not guaranteed.

### Compatibility Note

Other Rigol oscilloscope models may work with this MCP server, but we have no way to test them or guarantee functionality. Use with other models at your own risk.

## Installation

The recommended way to use this MCP server is via Docker, which eliminates dependency management and provides isolation.

### Quick Start

Pull the pre-built image from GitHub Container Registry:

```bash
docker pull ghcr.io/aimoda/rigol-dho824-mcp:latest
```

### Using Environment Variables with Docker

**IMPORTANT:** You must provide the `RIGOL_RESOURCE` environment variable with your oscilloscope's IP address (e.g., `TCPIP0::192.168.1.100::inst0::INSTR`).

You can configure the Docker container with environment variables in two ways:

1. **Hardcoded values** (shown in examples below): `-e RIGOL_RESOURCE="TCPIP0::192.168.1.100::inst0::INSTR"`
2. **Pass-through from host** (recommended): `-e RIGOL_RESOURCE` (without `=value`)

When you use `-e VARIABLE_NAME` without a value, Docker automatically passes through the variable from your host environment. This is useful if you have environment variables already set in your shell (e.g., in `~/.bashrc` or `~/.zshrc`).

### Environment Variables

- `RIGOL_RESOURCE`: **Required** - VISA resource string for connecting to the oscilloscope (e.g., `TCPIP0::192.168.1.100::inst0::INSTR`)
- `RIGOL_TEMP_DIR`: **Required for Docker** - Host-side path for returned file paths. The container always writes to `/tmp/rigol` internally and translates paths to this value in responses. Must match the host path in your `-v` mount. Outside Docker, this sets the directory for temporary files (waveforms, screenshots); if not set, uses system default temp directory.
- `VISA_TIMEOUT`: Communication timeout in milliseconds (default: 30000)
- `RIGOL_BEEPER_ENABLED`: Enable/disable oscilloscope beeper sounds (default: false)
- `RIGOL_AUTO_SCREENSHOT`: Automatically capture screenshot after each MCP tool execution for visualization/debugging (default: false). Screenshots are saved with human-readable timestamp format (e.g., `auto_screenshot_20251030_143045_123.png`) for chronological sorting.

## MCP Client Configuration

<details>
  <summary>Claude Code</summary>

**Option 1: Using `.mcp.json` file**

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
        "RIGOL_AUTO_SCREENSHOT",
        "-e",
        "RIGOL_TEMP_DIR",
        "ghcr.io/aimoda/rigol-dho824-mcp:latest"
      ],
      "env": {
        "RIGOL_RESOURCE": "TCPIP0::192.168.1.100::inst0::INSTR",
        "VISA_TIMEOUT": "30000",
        "RIGOL_BEEPER_ENABLED": "false",
        "RIGOL_AUTO_SCREENSHOT": "false",
        "RIGOL_TEMP_DIR": "/tmp/rigol-data"
      }
    }
  }
}
```

**Option 2: Using CLI**

```bash
claude mcp add --scope local rigol-dho824 -- \
  docker run -i --rm \
  -v /tmp/rigol-data:/tmp/rigol \
  -e RIGOL_RESOURCE="TCPIP0::192.168.1.100::inst0::INSTR" \
  -e VISA_TIMEOUT=30000 \
  -e RIGOL_BEEPER_ENABLED=false \
  -e RIGOL_AUTO_SCREENSHOT=false \
  -e RIGOL_TEMP_DIR=/tmp/rigol-data \
  ghcr.io/aimoda/rigol-dho824-mcp:latest
```

Replace `192.168.1.100` with your oscilloscope's IP address.

</details>

<details>
  <summary>Codex</summary>

```bash
codex mcp add rigol-dho824 -- \
  docker run -i --rm \
  -v /tmp/rigol-data:/tmp/rigol \
  -e RIGOL_RESOURCE="TCPIP0::192.168.1.100::inst0::INSTR" \
  -e VISA_TIMEOUT=30000 \
  -e RIGOL_BEEPER_ENABLED=false \
  -e RIGOL_AUTO_SCREENSHOT=false \
  -e RIGOL_TEMP_DIR=/tmp/rigol-data \
  ghcr.io/aimoda/rigol-dho824-mcp:latest
```

Replace `192.168.1.100` with your oscilloscope's IP address.

</details>

**Note:** After adding the server to your MCP client, restart the client to load the MCP server. The server will translate container paths (`/tmp/rigol/*`) to host paths (`/tmp/rigol-data/*`) in all returned file paths.

### Your first prompt

Enter the following prompt in your MCP Client to verify your setup:

```
Capture a waveform from channel 1 of my oscilloscope
```

Your MCP client should connect to the oscilloscope and capture the waveform data.

### Accessing Temp Files in Docker

The container writes temporary files (waveform captures, screenshots) to `/tmp/rigol` internally. To access these files from your host machine:

1. **Create a directory on your host** for storing temporary files:
   ```bash
   mkdir -p /tmp/rigol-data
   ```

2. **Mount this directory as a volume** and **set `RIGOL_TEMP_DIR`** in your Docker configuration:
   ```bash
   docker run -i --rm \
     -v /tmp/rigol-data:/tmp/rigol \
     -e RIGOL_TEMP_DIR=/tmp/rigol-data \
     ...
   ```

The server automatically translates all returned file paths from the container path (`/tmp/rigol/*`) to the host path (`/tmp/rigol-data/*`), so you can directly access files at the paths shown in tool responses.

**Important notes:**
- The host directory (`/tmp/rigol-data` in examples) must exist before starting the server
- `RIGOL_TEMP_DIR` must match the host-side path in your `-v` mount
- Temporary files are **not automatically cleaned up**
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

### Add to MCP Client

After completing the setup steps above, add the local development MCP server to your MCP client:

**Claude Code:**
```bash
claude mcp add --scope local rigol-dho824 -- <path-to-this-repo>/venv/bin/rigol-dho824-mcp
```

**Codex CLI:**
```bash
codex mcp add \
  --env RIGOL_RESOURCE="TCPIP0::192.168.1.100::inst0::INSTR" \
  --env VISA_TIMEOUT="30000" \
  --env RIGOL_BEEPER_ENABLED="false" \
  --env RIGOL_AUTO_SCREENSHOT="false" \
  rigol-dho824 -- <path-to-this-repo>/venv/bin/rigol-dho824-mcp
```

Replace:
- `<path-to-this-repo>` with the actual path to this repository
- `192.168.1.100` with your oscilloscope's IP address

**Note:** Unlike Claude Code, Codex requires explicit environment variables via `--env` flags (before the server name) as it runs MCP servers in a sanitized environment.

### Development Scripts

The `scripts/` directory contains utilities for development:
- `convert_png_to_webp.sh` - Convert PNG frame sequences to animated WebP (e.g., `./scripts/convert_png_to_webp.sh "~/screenshots/*.png" output.webp`)

## Development Configuration

The server can be configured using environment variables. Create a `.env` file from the example:

```bash
cp .env.example .env
```

Then edit `.env` to set your configuration:

- `RIGOL_RESOURCE`: VISA resource string for the oscilloscope (required)
  - Example: `TCPIP0::192.168.1.100::inst0::INSTR`
- `VISA_TIMEOUT`: Communication timeout in milliseconds (default: 5000)

## Running the Server (Development)

For local development and testing, you can run the server directly with Python:

### STDIO Transport
```bash
# Set resource string via environment variable
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

<!-- mcp-name: io.github.aimoda/rigol-dho824-mcp -->
