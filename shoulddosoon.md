# Rigol DHO824 MCP Tools - Implementation Roadmap

This document lists MCP tools to be added to the Rigol DHO824 MCP server, organized by priority. Each tool provides complete, end-to-end functionality in a single call, following the MCP design philosophy of minimizing tool invocations.

**Note:** Only tools not yet implemented in `src/rigol_dho824_mcp/server.py` are listed here.

---

## Priority 1: Waveform Recording (Segmented Memory)

Waveform recording captures multiple triggered waveforms into segmented memory for later analysis.

#### 1. `start_waveform_recording`
**SCPI:** `:RECord:WRECord:*`

Start recording waveforms to segmented memory.

**Complete SCPI sequence:**
```
:RECord:WRECord:ENABle ON
:RECord:WRECord:FRAMes <count>       # Or :RECord:WRECord:FRAMes:MAX
:RECord:WRECord:FINTerval <time>
:RECord:WRECord:OPERate RUN
```

**Parameters:**
- `max_frames`: Number of frames to record (or "MAX" for maximum)
- `frame_interval`: Time interval between frames in seconds (optional)

**Returns:** Dictionary with recording status and configuration

**Note:** This starts recording. Waveforms are captured on each trigger event.

---

#### 2. `stop_waveform_recording`
**SCPI:** `:RECord:WRECord:OPERate STOP`

Stop waveform recording.

**Returns:** Recording status with frames captured count

---

#### 3. `get_recording_status`
**SCPI:** `:RECord:WRECord:*?`

Query recording status and settings.

**Complete SCPI query:**
```
:RECord:WRECord:ENABle?
:RECord:WRECord:FRAMes?
:RECord:WRECord:FMAX?
:RECord:WRECord:OPERate?
```

**Returns:** Dictionary with enable status, frames recorded, max frames, and operation state

---

#### 4. `replay_recorded_frames`
**SCPI:** `:RECord:WREPlay:*`

Configure and control recorded waveform playback.

**Complete SCPI sequence:**
```
:RECord:WREPlay:FCURrent <frame>     # Jump to specific frame
:RECord:WREPlay:FSTart <frame>       # Set start frame
:RECord:WREPlay:FEND <frame>         # Set end frame
:RECord:WREPlay:FINTerval <time>     # Playback interval
:RECord:WREPlay:MODE {ONCE|LOOP}     # Playback mode
:RECord:WREPlay:DIRection {FORWard|BACKward}
:RECord:WREPlay:OPERate {PLAY|PAUSE|STEP}
```

**Parameters:**
- `current_frame`: Frame to display (optional)
- `start_frame`: First frame for playback (optional)
- `end_frame`: Last frame for playback (optional)
- `interval`: Time between frames during playback (optional)
- `mode`: Playback mode - "ONCE" or "LOOP" (optional)
- `direction`: Play direction - "FORWARD" or "BACKWARD" (optional)
- `operation`: Playback control - "PLAY", "PAUSE", or "STEP" (optional)

**Returns:** Dictionary with current playback configuration and frame info

**Use cases:**
- Step through captured anomalies
- Analyze intermittent events
- Create slow-motion playback of fast events

---

## Priority 2: Reference Waveforms

Reference waveforms allow saving and comparing waveforms on-screen.

#### 5. `save_reference_waveform`
**SCPI:** `:REFerence:SAVE <source>,<ref_slot>`

Save current waveform as reference.

**Parameters:**
- `source`: Source to save ("CHAN1"-"CHAN4", "MATH1"-"MATH4")
- `ref_slot`: Reference slot number (1-10)

**Returns:** Save confirmation with slot info

---

#### 6. `configure_reference_display`
**SCPI:** `:REFerence:*`

Configure reference waveform display.

**Complete SCPI sequence:**
```
:REFerence:SOURce <ref_slot>
:REFerence:CURRent {ON|OFF}
:REFerence:VSCale <scale>
:REFerence:VOFFset <offset>
```

**Parameters:**
- `ref_slot`: Reference slot (1-10)
- `enabled`: Show/hide reference
- `vertical_scale`: Vertical scale multiplier (optional)
- `vertical_offset`: Vertical offset in divisions (optional)

**Returns:** Reference display configuration

---

## Priority 3: System Utilities

#### 7. `reset_instrument`
**SCPI:** `*RST` or `:SYSTem:RESet`

Perform factory reset of oscilloscope.

**Returns:** Action confirmation

**Warning:** This resets ALL settings to factory defaults.

---

#### 8. `get_system_error`
**SCPI:** `:SYSTem:ERRor[:NEXT]?`

Query and clear next error from error queue.

**Returns:** Dictionary with error code and message

**Note:** Call repeatedly until error code is 0 to read all errors.

---

#### 9. `save_setup`
**SCPI:** `:SAVE:SETup <filepath>`

Save current oscilloscope setup to internal storage, then download via FTP.

**Parameters:**
- `setup_name`: Setup filename (without extension)
- `local_filepath`: Local path to save setup file

**Returns:** Dictionary with file path and bytes downloaded

**Note:** Setup files preserve all scope settings (channels, trigger, timebase, etc.).

---

#### 10. `load_setup`
**SCPI:** `:LOAD:SETup <filepath>`

Upload setup file via FTP, then load into oscilloscope.

**Parameters:**
- `local_filepath`: Local path to setup file

**Returns:** Load confirmation

**Note:** Complete workflow - upload to scope via FTP, then load from internal storage.

---

#### 11. `set_autoset_options`
**SCPI:** `:AUToset:*`

Configure autoset behavior.

**Complete SCPI sequence:**
```
:AUToset:PEAK {ON|OFF}       # Enable peak detect
:AUToset:OPENch {ON|OFF}     # Auto-enable channels
```

**Parameters:**
- `peak_detect`: Enable peak detect in autoset (optional)
- `auto_enable_channels`: Auto-enable channels with signals (optional)

**Returns:** Autoset configuration

---

## Priority 4: Display Settings

#### 12. `configure_display`
**SCPI:** `:DISPlay:*`

Configure display appearance.

**Complete SCPI sequence:**
```
:DISPlay:GRID {FULL|HALF|NONE}
:DISPlay:WBRightness <percent>   # Waveform brightness
:DISPlay:GBRightness <percent>   # Grid brightness
```

**Parameters:**
- `grid_type`: Grid style - "FULL", "HALF", or "NONE" (optional)
- `waveform_brightness`: Waveform brightness 0-100% (optional)
- `grid_brightness`: Grid brightness 0-100% (optional)

**Returns:** Display configuration

---

## Priority 5: XY Mode (Lissajous)

#### 13. `configure_xy_mode`
**SCPI:** `:TIMebase:XY:*`

Configure XY (Lissajous) display mode.

**Complete SCPI sequence:**
```
:TIMebase:MODE XY
:TIMebase:XY:X <channel>
:TIMebase:XY:Y <channel>
:TIMebase:XY:Z <channel>     # Optional intensity modulation
```

**Parameters:**
- `enabled`: Enable XY mode
- `x_channel`: X-axis channel (1-4)
- `y_channel`: Y-axis channel (1-4)
- `z_channel`: Z-axis (intensity) channel (optional, 1-4)

**Returns:** XY mode configuration

**Use cases:**
- Phase relationship analysis
- Frequency comparison
- Amplitude modulation visualization

---

## Summary by Category

### High Priority (Implement First)
**Waveform Recording (4 tools):** Items 1-4
- Segmented memory capture and playback
- Excellent for intermittent event analysis
- Playback control capabilities
- *Note: Frame export implemented in `capture_waveform` tool*

### Medium Priority
**Reference Waveforms (2 tools):** Items 5-6
- Save and display reference waveforms
- Useful for comparison and quality control

**System Utilities (5 tools):** Items 7-11
- Reset, error handling, setup save/load
- Autoset configuration

### Lower Priority
**Display Settings (1 tool):** Item 12
- Grid and brightness configuration

**XY Mode (1 tool):** Item 13
- Lissajous/XY display for phase analysis

---

## Implementation Notes

### Design Philosophy
Each tool should provide **complete, end-to-end functionality**:
- Configure all related SCPI settings in a single call
- Handle file transfers (FTP) internally
- Return processed, ready-to-use results
- Minimize the need for multiple tool invocations

### Example: Good vs Bad Design

**❌ BAD - Multiple tool calls required:**
```python
enable_hardware_counter()
set_counter_source(1)
set_counter_mode("FREQUENCY")
set_counter_digits(6)
get_counter_value()
```

**✅ GOOD - Single comprehensive tool:**
```python
configure_hardware_counter(
    enabled=True,
    channel=1,
    mode="FREQUENCY",
    digits=6
)  # Returns configuration AND current reading
```

### Verification Strategy
1. Read programming guide section for each command
2. Test all parameters with actual hardware
3. Verify SCPI command syntax matches documentation
4. Ensure return types include all relevant information
5. Add proper type hints and validation

---

## Total: 13 Remaining Tools

This represents the remaining unimplemented features after completing Priority 1 tools (advanced acquisition & channel settings, hardware counter), all protocol triggers, and bus decode tools. These focus on waveform recording, reference waveforms, system management, and display settings.

**Note:** Frame export functionality has been implemented directly in the `capture_waveform` tool, which now supports exporting frames from both Waveform Recording and Ultra Acquisition modes.
