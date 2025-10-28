# Rigol DHO824 MCP Server

An MCP (Model Context Protocol) server for controlling and querying the Rigol DHO824 oscilloscope using PyVISA.

## Installation

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

After completing the setup steps above, add the MCP server to Claude Code:

```bash
claude mcp add --scope user rigol-dho824 -- <path-to-this-repo>/venv/bin/rigol-dho824-mcp
```

Replace `<path-to-this-repo>` with the actual path to this repository.

## Docker Deployment

The easiest way to use this MCP server is via Docker, which eliminates dependency management and provides isolation.

### Quick Start

Pull the pre-built image from GitHub Container Registry:

```bash
docker pull ghcr.io/aimoda/rigol-dho824-mcp:latest
```

### Required Configuration

**IMPORTANT:** You must provide the `RIGOL_RESOURCE` environment variable when running the container. This tells the server how to connect to your network-connected oscilloscope.

```bash
docker run -i --rm \
  -e RIGOL_RESOURCE="TCPIP0::192.168.1.100::inst0::INSTR" \
  ghcr.io/aimoda/rigol-dho824-mcp:latest
```

Replace `192.168.1.100` with your oscilloscope's IP address.

### Using with Claude Code

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
        "-e",
        "RIGOL_RESOURCE",
        "-e",
        "VISA_TIMEOUT",
        "-e",
        "RIGOL_BEEPER_ENABLED",
        "ghcr.io/aimoda/rigol-dho824-mcp:latest"
      ],
      "env": {
        "RIGOL_RESOURCE": "TCPIP0::192.168.1.100::inst0::INSTR",
        "VISA_TIMEOUT": "30000",
        "RIGOL_BEEPER_ENABLED": "false"
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

## Configuration

The server can be configured using environment variables. Create a `.env` file from the example:

```bash
cp .env.example .env
```

Then edit `.env` to set your configuration:

- `RIGOL_RESOURCE`: VISA resource string for the oscilloscope
  - Example: `TCPIP0::192.168.1.100::inst0::INSTR`
  - Leave empty for auto-discovery
- `VISA_TIMEOUT`: Communication timeout in milliseconds (default: 5000)

## Running the Server

### STDIO Transport (for Claude Desktop)
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

