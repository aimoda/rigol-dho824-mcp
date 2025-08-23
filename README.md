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

## Configuration

The server can be configured using environment variables. Create a `.env` file from the example:

```bash
cp .env.example .env
```

Then edit `.env` to set your configuration:

- `RIGOL_RESOURCE`: VISA resource string for the oscilloscope
  - USB example: `USB0::0x1AB1::0x0515::DHO824XXXXXXXXX::INSTR`
  - LAN example: `TCPIP0::192.168.1.100::inst0::INSTR`
  - Leave empty for auto-discovery
- `VISA_TIMEOUT`: Communication timeout in milliseconds (default: 5000)

## Running the Server

### STDIO Transport (for Claude Desktop)
```bash
# Auto-discover oscilloscope
python -m rigol_dho824_mcp.server

# Or set resource string via environment variable
export RIGOL_RESOURCE="USB0::0x1AB1::0x0515::DHO824XXXXXXXXX::INSTR"
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

