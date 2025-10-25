# Claude Instructions

## Reference Manuals

**IMPORTANT**: Before implementing any oscilloscope control code, always search the `manuals/` directory first.

This directory contains official Rigol documentation, SCPI command references, and programming guides that should guide your implementation approach. Look for:

- SCPI command syntax and parameters
- Programming examples and patterns
- Valid value ranges and constraints
- Waveform data formats and structures
- File transfer protocols (FTP, PyVISA)
- Device capabilities and limitations

Use these references to ensure correct SCPI commands and proper device communication before writing new code.

## MCP Tool Design Philosophy

**IMPORTANT**: When implementing MCP tools, design each tool to provide complete, end-to-end functionality in a single call.

Users should accomplish their goals with minimal tool invocations. Avoid creating tool chains where multiple tools must be called sequentially to complete one logical operation.

### Good Design Example
```python
# GOOD: Single tool provides complete functionality
@server.tool("capture_waveform")
async def capture_waveform(channel: int) -> dict:
    """Capture waveform data and return it directly to the user."""
    # 1. Configure oscilloscope
    # 2. Capture waveform
    # 3. Transfer data
    # 4. Process and format
    # 5. Return complete result
    return {"data": waveform_data, "metadata": {...}}
```

### Poor Design Example
```python
# BAD: Requires multiple tool calls for one task
@server.tool("start_capture")      # Step 1
@server.tool("wait_for_capture")   # Step 2
@server.tool("transfer_waveform")  # Step 3
@server.tool("get_waveform_data")  # Step 4
```

### Guidelines
- Each tool should encapsulate a complete user-facing operation
- Handle all intermediate steps internally (device communication, file transfers, data processing)
- Return processed, ready-to-use results
- Minimize the need for users to orchestrate complex tool sequences
- Think: "What does the user actually want to accomplish?" not "What are the technical steps?"

## Type Checking

**IMPORTANT**: After writing or modifying Python code, always run `pyright` to check for type errors and fix any issues found.

```bash
# Run type checking
pyright

# Or if installed in venv
./venv/bin/pyright
```
