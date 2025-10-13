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

## Type Checking

**IMPORTANT**: After writing or modifying Python code, always run `pyright` to check for type errors and fix any issues found.

```bash
# Run type checking
pyright

# Or if installed in venv
./venv/bin/pyright
```
