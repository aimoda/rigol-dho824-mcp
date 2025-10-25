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

## Avoiding Type Annotation Duplication

**IMPORTANT**: Always reuse existing type aliases instead of duplicating `Annotated[type, Field(...)]` patterns.

### Before Adding New Type Annotations

1. **Search for existing type aliases** - Check the type alias sections at the top of `server.py` (currently lines 30-110) for reusable types
2. **Look for similar patterns** - Search for the description text you're about to use (e.g., `grep "Trigger level in volts"`)
3. **Reuse when possible** - If an existing type alias matches your needs, use it

### When to Create New Type Aliases

Create a new type alias if:
- The same `Annotated[type, Field(description=...)]` pattern will be used **2 or more times**
- The field represents a common concept across multiple tools/results
- The description and type are semantically identical

### How to Create Type Aliases

```python
# GOOD: Create reusable type aliases
TriggerLevelField = Annotated[float, Field(description="Trigger level in volts")]
UpperTimeLimitField = Annotated[float, Field(description="Upper time limit in seconds")]

# Then use them everywhere:
class SomeResult(TypedDict):
    level: TriggerLevelField
    time: UpperTimeLimitField

@server.tool
async def some_tool(level: TriggerLevelField, time: UpperTimeLimitField):
    ...
```

```python
# BAD: Duplicating the same annotation
class Result1(TypedDict):
    level: Annotated[float, Field(description="Trigger level in volts")]

class Result2(TypedDict):
    level: Annotated[float, Field(description="Trigger level in volts")]  # Duplicate!

@server.tool
async def tool1(level: Annotated[float, Field(description="Trigger level in volts")]):  # Duplicate!
    ...
```

### Organizing Type Aliases

Group related type aliases together with clear comments:

```python
# Voltage-related fields
TriggerLevelField = Annotated[...]
UpperVoltageLevelField = Annotated[...]

# Time-related fields
UpperTimeLimitField = Annotated[...]
IdleTimeField = Annotated[...]
```

### Naming Conventions

- Use descriptive names ending in `Field` for field-specific types
- Use semantic names that indicate the field's purpose (e.g., `TriggerLevelField` not `FloatField1`)
- Keep names concise but clear
