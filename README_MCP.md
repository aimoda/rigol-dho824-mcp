# Rigol DHO824 MCP Server

An MCP (Model Context Protocol) server for controlling and querying the Rigol DHO824 oscilloscope.

## Features

Currently provides three MCP tools for querying oscilloscope information:
- `get_model_number` - Returns the oscilloscope model (e.g., "DHO824")
- `get_software_version` - Returns the firmware version
- `get_serial_number` - Returns the device serial number

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure the connection (optional):
```bash
cp .env.example .env
# Edit .env to set your oscilloscope's VISA resource string
```

## Configuration

The server can be configured using environment variables:

- `RIGOL_RESOURCE`: VISA resource string for the oscilloscope
  - USB example: `USB0::0x1AB1::0x0515::DHO824XXXXXXXXX::INSTR`
  - LAN example: `TCPIP0::192.168.1.100::inst0::INSTR`
  - Leave empty for auto-discovery

- `VISA_TIMEOUT`: Communication timeout in milliseconds (default: 5000)

## Usage

### Running as stdio server (for Claude Desktop, etc.):
```bash
python -m rigol_dho824_mcp.server
```

### Running as HTTP server:
```bash
python -m rigol_dho824_mcp.server --http --port 8000
```

### Using with Claude Desktop

Add to your Claude Desktop configuration (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "rigol-dho824": {
      "command": "python",
      "args": ["-m", "rigol_dho824_mcp.server"],
      "env": {
        "RIGOL_RESOURCE": "USB0::0x1AB1::0x0515::DHO824XXXXXXXXX::INSTR"
      }
    }
  }
}
```

## Requirements

- Python 3.9+
- PyVISA for instrument communication
- FastMCP for MCP server framework
- A connected Rigol DHO824 oscilloscope (USB or LAN)

## Future Enhancements

This is a base implementation. Future versions could add:
- Waveform capture and data retrieval
- Trigger configuration
- Channel settings control
- Measurement functions
- Screenshot capture
- And much more from the extensive SCPI command set