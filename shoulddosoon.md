# Rigol DHO824 MCP Tools - Implementation Roadmap

This document lists MCP tools to be added to the Rigol DHO824 MCP server, organized by priority. Each tool provides complete, end-to-end functionality in a single call, following the MCP design philosophy of minimizing tool invocations.

**Note:** Only tools not yet implemented in `src/rigol_dho824_mcp/server.py` are listed here.

---

## Priority 1: Protocol Triggers & Decode

### Serial Protocol Triggers

#### 1. `configure_rs232_trigger`
**SCPI:** `:TRIGger:RS232:*`

Trigger on UART/RS232 serial data patterns.

**Complete SCPI sequence:**
```
:TRIGger:MODE RS232
:TRIGger:RS232:SOURce <channel>
:TRIGger:RS232:WHEN {STARt|STOP|DATA|ERRor}
:TRIGger:RS232:DATA <byte>         # For DATA mode
:TRIGger:RS232:BAUD <rate>
:TRIGger:RS232:PARity {NONE|EVEN|ODD|MARK|SPACe}
:TRIGger:RS232:STOP {1|1.5|2}
:TRIGger:RS232:POL {POSitive|NEGative}
:TRIGger:RS232:LEVel <voltage>
```

**Parameters:**
- `channel`: Source channel (1-4)
- `when`: Trigger condition ("START", "STOP", "DATA", "ERROR")
- `data_value`: Data byte to match (0-255, only for DATA mode)
- `baud_rate`: Baud rate (2400-115200)
- `parity`: Parity setting
- `stop_bits`: Stop bit count (1, 1.5, or 2)
- `polarity`: Signal polarity
- `level`: Trigger level in volts

**Returns:** Complete RS232 trigger configuration

---

#### 2. `configure_i2c_trigger`
**SCPI:** `:TRIGger:IIC:*`

Trigger on I2C bus events (start, stop, address, data).

**Complete SCPI sequence:**
```
:TRIGger:MODE IIC
:TRIGger:IIC:SCL <channel>         # Clock line
:TRIGger:IIC:SDA <channel>         # Data line
:TRIGger:IIC:WHEN {STARt|RESTart|STOP|NACK|ADDRess|DATA|AERR}
:TRIGger:IIC:ADDRess <addr>        # For ADDRess mode (7 or 10 bit)
:TRIGger:IIC:DATA <byte>           # For DATA mode
:TRIGger:IIC:AWIDth {7|10}         # Address width
:TRIGger:IIC:DIR {READ|WRITe|RWRIte}
:TRIGger:IIC:CLEVel <voltage>
:TRIGger:IIC:DLEVel <voltage>
```

**Parameters:**
- `scl_channel`: SCL (clock) channel (1-4)
- `sda_channel`: SDA (data) channel (1-4)
- `when`: Trigger condition
- `address`: I2C address (for ADDRess mode)
- `data_value`: Data byte (for DATA mode)
- `address_width`: 7-bit or 10-bit addressing
- `direction`: Transfer direction
- `clock_level`: SCL threshold voltage
- `data_level`: SDA threshold voltage

**Returns:** Complete I2C trigger configuration

---

#### 3. `configure_spi_trigger`
**SCPI:** `:TRIGger:SPI:*`

Trigger on SPI bus data patterns.

**Complete SCPI sequence:**
```
:TRIGger:MODE SPI
:TRIGger:SPI:SCLKsource <channel>
:TRIGger:SPI:MISOsource <channel>
:TRIGger:SPI:CSSource <channel>
:TRIGger:SPI:SLOPe {POSitive|NEGative}
:TRIGger:SPI:WHEN {TIMeout}
:TRIGger:SPI:TIMeout <time>
:TRIGger:SPI:WIDth {8|16|24|32}
:TRIGger:SPI:DATA <value>
:TRIGger:SPI:CLEVel <voltage>
:TRIGger:SPI:MLEVel <voltage>
:TRIGger:SPI:SLEVel <voltage>
```

**Parameters:**
- `sclk_channel`: Clock channel (1-4)
- `miso_channel`: MISO channel (1-4, optional)
- `cs_channel`: Chip select channel (1-4, optional)
- `clock_slope`: Clock edge ("POSITIVE" or "NEGATIVE")
- `when`: Trigger condition ("TIMEOUT", etc.)
- `timeout`: Timeout duration in seconds
- `data_width`: Data width in bits (8, 16, 24, 32)
- `data_value`: Data pattern to match
- `clock_level`: SCLK threshold voltage
- `miso_level`: MISO threshold voltage
- `cs_level`: CS threshold voltage

**Returns:** Complete SPI trigger configuration

---

#### 4. `configure_can_trigger`
**SCPI:** `:TRIGger:CAN:*`

Trigger on CAN bus frames and errors.

**Complete SCPI sequence:**
```
:TRIGger:MODE CAN
:TRIGger:CAN:SOURce <channel>
:TRIGger:CAN:BAUD <rate>
:TRIGger:CAN:SIGNal {RX|TX|DIFF}
:TRIGger:CAN:WHEN {STARt|FRAM|IDENt|DATA|IDDA|ERRor|END|ACK}
:TRIGger:CAN:SAMPoint <percent>
:TRIGger:CAN:FTYPE {DATA|REMote}
:TRIGger:CAN:ITYPE {STANdard|EXTended}
:TRIGger:CAN:ID <id>
:TRIGger:CAN:DATA <bytes>
:TRIGger:CAN:LEVel <voltage>
```

**Parameters:**
- `channel`: Source channel (1-4)
- `baud_rate`: CAN baud rate
- `signal_type`: Signal type (RX, TX, or differential)
- `when`: Trigger condition
- `sample_point`: Sample point percentage
- `frame_type`: DATA or REMOTE frame
- `id_type`: STANDARD (11-bit) or EXTENDED (29-bit)
- `identifier`: CAN identifier
- `data_bytes`: Data pattern
- `level`: Trigger level voltage

**Returns:** Complete CAN trigger configuration

---

#### 5. `configure_lin_trigger`
**SCPI:** `:TRIGger:LIN:*`

Trigger on LIN bus frames and errors.

**Complete SCPI sequence:**
```
:TRIGger:MODE LIN
:TRIGger:LIN:SOURce <channel>
:TRIGger:LIN:STANdard {1P0|2P0|2P1|2P2}
:TRIGger:LIN:BAUD <rate>
:TRIGger:LIN:WHEN {SYNC|IDENtifier|DATA|IDDA|ERRor|AWAK}
:TRIGger:LIN:ERRType {SYNError|PARError|CHKError|TOUTerror}
:TRIGger:LIN:ID <id>
:TRIGger:LIN:DATA <bytes>
:TRIGger:LIN:LEVel <voltage>
```

**Parameters:**
- `channel`: Source channel (1-4)
- `standard`: LIN version (1.0, 2.0, 2.1, 2.2)
- `baud_rate`: LIN baud rate
- `when`: Trigger condition
- `error_type`: Error type (for ERRor mode)
- `identifier`: LIN identifier (0-63)
- `data_bytes`: Data pattern
- `level`: Trigger level voltage

**Returns:** Complete LIN trigger configuration

---

### Bus Decode Configuration

#### 6. `configure_parallel_bus`
**SCPI:** `:BUS<n>:PARallel:*`

Configure parallel bus decode (up to 8 bits).

**Complete SCPI sequence:**
```
:BUS<n>:MODE PARallel
:BUS<n>:PARallel:BIT<m>:SOURce <channel>
:BUS<n>:PARallel:CLOCk <channel>
:BUS<n>:PARallel:WIDth <bits>
:BUS<n>:PARallel:CLOCk:POLarity {POSitive|NEGative}
:BUS<n>:PARallel:BITOrder {LSB|MSB}
```

**Parameters:**
- `bus_number`: Bus number (1-4)
- `bit_assignments`: Dictionary mapping bit positions to channels, e.g., {0: 1, 1: 2, 2: 3}
- `clock_channel`: Clock channel (optional)
- `width`: Bus width in bits (1-8)
- `clock_polarity`: Clock edge ("POSITIVE" or "NEGATIVE")
- `bit_order`: Bit endianness ("LSB" or "MSB")

**Returns:** Complete parallel bus configuration

---

#### 7. `configure_rs232_bus`
**SCPI:** `:BUS<n>:RS232:*`

Configure UART/RS232 bus decode.

**Complete SCPI sequence:**
```
:BUS<n>:MODE RS232
:BUS<n>:RS232:TX <channel>
:BUS<n>:RS232:RX <channel>
:BUS<n>:RS232:POLarity {POSitive|NEGative}
:BUS<n>:RS232:PARity {NONE|EVEN|ODD|MARK|SPACe}
:BUS<n>:RS232:BITOrder {LSB|MSB}
:BUS<n>:RS232:BAUD <rate>
:BUS<n>:RS232:DATa {5|6|7|8|9}
:BUS<n>:RS232:STOP {1|1.5|2}
```

**Parameters:**
- `bus_number`: Bus number (1-4)
- `tx_channel`: TX channel (optional)
- `rx_channel`: RX channel (optional)
- `polarity`: Signal polarity
- `parity`: Parity setting
- `bit_order`: Bit endianness
- `baud_rate`: Baud rate
- `data_bits`: Data bits (5-9)
- `stop_bits`: Stop bits (1, 1.5, 2)

**Returns:** Complete RS232 bus decode configuration

---

#### 8. `configure_i2c_bus`
**SCPI:** `:BUS<n>:IIC:*`

Configure I2C bus decode.

**Complete SCPI sequence:**
```
:BUS<n>:MODE IIC
:BUS<n>:IIC:SCL <channel>
:BUS<n>:IIC:SDA <channel>
:BUS<n>:IIC:AWIDth {7|10}
```

**Parameters:**
- `bus_number`: Bus number (1-4)
- `scl_channel`: SCL channel
- `sda_channel`: SDA channel
- `address_width`: Address width (7 or 10 bits)

**Returns:** Complete I2C bus decode configuration

---

#### 9. `configure_spi_bus`
**SCPI:** `:BUS<n>:SPI:*`

Configure SPI bus decode.

**Complete SCPI sequence:**
```
:BUS<n>:MODE SPI
:BUS<n>:SPI:SCLK <channel>
:BUS<n>:SPI:MISO <channel>
:BUS<n>:SPI:MOSI <channel>
:BUS<n>:SPI:SS <channel>
:BUS<n>:SPI:POLarity {POSitive|NEGative}
:BUS<n>:SPI:DATa {4|8|16|24|32}
:BUS<n>:SPI:BITOrder {LSB|MSB}
:BUS<n>:SPI:MODE {CPOL0CPHA0|CPOL0CPHA1|CPOL1CPHA0|CPOL1CPHA1}
:BUS<n>:SPI:TIMeout <time>
```

**Parameters:**
- `bus_number`: Bus number (1-4)
- `sclk_channel`: Clock channel
- `miso_channel`: MISO channel (optional)
- `mosi_channel`: MOSI channel (optional)
- `ss_channel`: Slave select channel (optional)
- `clock_polarity`: Clock polarity
- `data_bits`: Data width (4, 8, 16, 24, 32)
- `bit_order`: Bit endianness
- `spi_mode`: SPI mode (CPOL/CPHA combination)
- `timeout`: Frame timeout in seconds

**Returns:** Complete SPI bus decode configuration

---

#### 10. `configure_can_bus`
**SCPI:** `:BUS<n>:CAN:*`

Configure CAN bus decode.

**Complete SCPI sequence:**
```
:BUS<n>:MODE CAN
:BUS<n>:CAN:SOURce <channel>
:BUS<n>:CAN:SIGNal {RX|TX|DIFF}
:BUS<n>:CAN:BAUD <rate>
:BUS<n>:CAN:SAMPoint <percent>
```

**Parameters:**
- `bus_number`: Bus number (1-4)
- `source_channel`: Source channel
- `signal_type`: Signal type (RX, TX, DIFF)
- `baud_rate`: CAN baud rate
- `sample_point`: Sample point percentage (5-95%)

**Returns:** Complete CAN bus decode configuration

---

#### 11. `configure_lin_bus`
**SCPI:** `:BUS<n>:LIN:*`

Configure LIN bus decode.

**Complete SCPI sequence:**
```
:BUS<n>:MODE LIN
:BUS<n>:LIN:SOURce <channel>
:BUS<n>:LIN:PARity {ENHanced|CLASsic}
:BUS<n>:LIN:STANdard {1P0|2P0|2P1|2P2}
```

**Parameters:**
- `bus_number`: Bus number (1-4)
- `source_channel`: Source channel
- `parity`: Parity mode (enhanced or classic)
- `standard`: LIN version

**Returns:** Complete LIN bus decode configuration

---

#### 12. `set_bus_display`
**SCPI:** `:BUS<n>:DISPlay {ON|OFF}`

Enable or disable bus decode display on screen.

**Parameters:**
- `bus_number`: Bus number (1-4)
- `enabled`: Boolean to show/hide decode

**Returns:** Bus display status

---

#### 13. `set_bus_format`
**SCPI:** `:BUS<n>:FORMat {HEX|DEC|BIN|ASCii}`

Set bus decode display format.

**Parameters:**
- `bus_number`: Bus number (1-4)
- `format`: Display format ("HEX", "DEC", "BIN", "ASCII")

**Returns:** Current bus format

---

#### 14. `get_bus_decoded_data`
**SCPI:** `:BUS<n>:DATA?`

Retrieve decoded bus data from screen.

**Parameters:**
- `bus_number`: Bus number (1-4)

**Returns:** Decoded bus data string

---

#### 15. `export_bus_data`
**SCPI:** `:BUS<n>:EEXPort <filepath>`

Export decoded bus data to CSV file on scope storage, then download via FTP.

**Parameters:**
- `bus_number`: Bus number (1-4)
- `local_filepath`: Local path to save CSV file

**Returns:** Dictionary with file path and number of bytes downloaded

**Note:** This tool handles the complete workflow: export on scope → download via FTP → save locally.

---

## Priority 3: Advanced Acquisition & Channel Settings

### Acquisition Settings

#### 16. `set_acquisition_averages`
**SCPI:** `:ACQuire:AVERages <count>`

Set number of averages when acquisition type is AVERAGE.

**Parameters:**
- `averages`: Number of averages (2-65536, power of 2 recommended)

**Returns:** Current averages count

**Note:** Only applies when `:ACQ:TYPE` is set to `AVERages`. Use with `set_acquisition_type("AVERAGE")`.

---

#### 17. `configure_ultra_acquisition`
**SCPI:** `:ACQuire:ULTRa:*`

Configure Ultra Acquisition mode for high-speed waveform capture.

**Complete SCPI sequence:**
```
:ACQuire:TYPE ULTRa
:ACQuire:ULTRa:MODE {EDGE|PULSe}
:ACQuire:ULTRa:TIMeout <time>
:ACQuire:ULTRa:FMAX <count>
```

**Parameters:**
- `mode`: Ultra mode ("EDGE" or "PULSE")
- `timeout`: Timeout duration in seconds
- `max_frames`: Maximum frames to capture

**Returns:** Complete Ultra Acquisition configuration

**Note:** Ultra Acquisition mode captures waveforms at maximum speed for anomaly detection.

---

### Channel Settings

#### 18. `set_channel_invert`
**SCPI:** `:CHANnel<n>:INVert {ON|OFF}`

Invert channel waveform display (multiply by -1).

**Parameters:**
- `channel`: Channel number (1-4)
- `inverted`: Boolean to invert

**Returns:** Channel invert status

---

#### 19. `set_channel_label`
**SCPI:** `:CHANnel<n>:LABel:CONTent <text>`

Set custom channel label text.

**Parameters:**
- `channel`: Channel number (1-4)
- `label`: Custom label string (max 4 characters)

**Returns:** Current channel label

---

#### 20. `set_channel_label_visible`
**SCPI:** `:CHANnel<n>:LABel:SHOW {ON|OFF}`

Show or hide custom channel label.

**Parameters:**
- `channel`: Channel number (1-4)
- `visible`: Boolean to show/hide

**Returns:** Label visibility status

---

#### 21. `set_channel_vernier`
**SCPI:** `:CHANnel<n>:VERNier {ON|OFF}`

Enable fine (vernier) or coarse vertical scale adjustment.

**Parameters:**
- `channel`: Channel number (1-4)
- `fine_mode`: Boolean - True for fine adjustment, False for coarse (1-2-5 sequence)

**Returns:** Vernier mode status

**Note:** When vernier is ON, vertical scale can be set to any value. When OFF, scale follows 1-2-5 sequence.

---

#### 22. `set_channel_units`
**SCPI:** `:CHANnel<n>:UNITs {VOLt|WATT|AMPere|UNKNown}`

Set voltage display units for channel.

**Parameters:**
- `channel`: Channel number (1-4)
- `units`: Unit type ("VOLT", "WATT", "AMPERE", "UNKNOWN")

**Returns:** Current channel units

---

### Timebase Settings

#### 23. `set_timebase_mode`
**SCPI:** `:TIMebase:MODE {MAIN|XY|ROLL}`

Set timebase display mode.

- **MAIN**: Normal YT mode
- **XY**: Lissajous/XY mode (Ch1 = X axis, Ch2 = Y axis)
- **ROLL**: Slow sweep roll mode (for low frequencies)

**Parameters:**
- `mode`: Timebase mode ("MAIN", "XY", "ROLL")

**Returns:** Current timebase mode

---

#### 24. `enable_delayed_timebase`
**SCPI:** `:TIMebase:DELay:ENABle {ON|OFF}`

Enable or disable delayed/zoom timebase (zoomed window).

**Parameters:**
- `enabled`: Boolean to enable zoom window

**Returns:** Delayed timebase status

---

#### 25. `set_delayed_timebase_scale`
**SCPI:** `:TIMebase:DELay:SCALe <time>`

Set zoom window horizontal scale (time/div).

**Parameters:**
- `time_per_div`: Zoom window time per division in seconds

**Returns:** Delayed timebase scale

**Note:** Must enable delayed timebase first with `enable_delayed_timebase(True)`.

---

#### 26. `set_delayed_timebase_offset`
**SCPI:** `:TIMebase:DELay:OFFSet <time>`

Set zoom window horizontal position.

**Parameters:**
- `time_offset`: Zoom window offset in seconds

**Returns:** Delayed timebase offset

**Note:** Must enable delayed timebase first with `enable_delayed_timebase(True)`.

---

#### 27. `set_timebase_vernier`
**SCPI:** `:TIMebase:VERNier {ON|OFF}`

Enable fine (vernier) or coarse timebase adjustment.

**Parameters:**
- `fine_mode`: Boolean - True for fine adjustment, False for coarse (1-2-5 sequence)

**Returns:** Timebase vernier status

---

## Priority 4: Hardware Counter (Frequency/Period/Totalize)

The hardware counter provides high-precision frequency/period measurements independent of the main acquisition system.

**Note:** There are two counter implementations in the DHO800:
1. `:COUNter:*` - Dedicated hardware counter (Priority 5 - these tools)
2. `:MEASure:COUNter:*` - Measurement subsystem counter (lower priority, skip for now)

The dedicated hardware counter (`:COUNter:*`) provides superior accuracy and should be prioritized.

---

#### 28. `configure_hardware_counter`
**SCPI:** `:COUNter:*`

Configure hardware frequency counter in a single call.

**Complete SCPI sequence:**
```
:COUNter:ENABle {ON|OFF}
:COUNter:SOURce <channel>
:COUNter:MODE {FREQuency|PERiod|TOTalize}
:COUNter:NDIGits {5|6}
:COUNter:TOTalize:ENABle {ON|OFF}
```

**Parameters:**
- `enabled`: Boolean to enable counter
- `channel`: Source channel (1-4)
- `mode`: Measurement mode ("FREQUENCY", "PERIOD", "TOTALIZE")
- `digits`: Resolution (5 or 6 digits)
- `totalize_enabled`: Enable statistics (only for FREQUENCY/PERIOD modes)

**Returns:** Dictionary with complete counter configuration and current reading

**Modes:**
- **FREQUENCY**: Measures signal frequency (Hz)
- **PERIOD**: Measures signal period (seconds)
- **TOTALIZE**: Counts total rising/falling edges

**Use cases:**
- High-accuracy frequency measurement (6-digit precision)
- Period measurement for low-frequency signals
- Edge counting for event totalization

---

#### 29. `get_hardware_counter_value`
**SCPI:** `:COUNter:CURRent?`

Get current hardware counter reading.

**Returns:** Dictionary with value and unit

**Note:** Counter must be enabled first. Units depend on mode (Hz for frequency, seconds for period, count for totalize).

---

#### 30. `reset_counter_totalize`
**SCPI:** `:COUNter:TOTalize:CLEar`

Clear/reset the totalize counter and statistics.

**Returns:** Action confirmation

**Note:** Only applies when counter is in statistics mode (`:COUNter:TOTalize:ENABle ON`).

---

## Priority 5: Waveform Recording (Segmented Memory)

Waveform recording captures multiple triggered waveforms into segmented memory for later analysis.

#### 31. `start_waveform_recording`
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

#### 32. `stop_waveform_recording`
**SCPI:** `:RECord:WRECord:OPERate STOP`

Stop waveform recording.

**Returns:** Recording status with frames captured count

---

#### 33. `get_recording_status`
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

#### 34. `replay_recorded_frames`
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

#### 35. `export_recorded_frame`
**SCPI:** `:RECord:WREPlay:FCURrent + :WAV:DATA?`

Export specific recorded frame as waveform data.

**Complete workflow:**
```
:RECord:WREPlay:FCURrent <frame>     # Navigate to frame
:WAV:SOUR <channel>                  # Set source
:WAV:MODE RAW                        # Raw mode
:WAV:FORM WORD                       # 16-bit format
:WAV:DATA?                           # Read data
```

**Parameters:**
- `frame_number`: Frame to export (1 to max frames)
- `channel`: Channel to export (1-4)
- `local_filepath`: Local path to save JSON file

**Returns:** Dictionary with file path and frame metadata

**Note:** This is similar to `capture_waveform` but operates on recorded frames instead of live acquisition.

---

## Priority 6: Reference Waveforms

Reference waveforms allow saving and comparing waveforms on-screen.

#### 36. `save_reference_waveform`
**SCPI:** `:REFerence:SAVE <source>,<ref_slot>`

Save current waveform as reference.

**Parameters:**
- `source`: Source to save ("CHAN1"-"CHAN4", "MATH1"-"MATH4")
- `ref_slot`: Reference slot number (1-10)

**Returns:** Save confirmation with slot info

---

#### 37. `configure_reference_display`
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

## Priority 7: System Utilities

#### 38. `reset_instrument`
**SCPI:** `*RST` or `:SYSTem:RESet`

Perform factory reset of oscilloscope.

**Returns:** Action confirmation

**Warning:** This resets ALL settings to factory defaults.

---

#### 39. `get_system_error`
**SCPI:** `:SYSTem:ERRor[:NEXT]?`

Query and clear next error from error queue.

**Returns:** Dictionary with error code and message

**Note:** Call repeatedly until error code is 0 to read all errors.

---

#### 40. `save_setup`
**SCPI:** `:SAVE:SETup <filepath>`

Save current oscilloscope setup to internal storage, then download via FTP.

**Parameters:**
- `setup_name`: Setup filename (without extension)
- `local_filepath`: Local path to save setup file

**Returns:** Dictionary with file path and bytes downloaded

**Note:** Setup files preserve all scope settings (channels, trigger, timebase, etc.).

---

#### 41. `load_setup`
**SCPI:** `:LOAD:SETup <filepath>`

Upload setup file via FTP, then load into oscilloscope.

**Parameters:**
- `local_filepath`: Local path to setup file

**Returns:** Load confirmation

**Note:** Complete workflow - upload to scope via FTP, then load from internal storage.

---

#### 42. `set_autoset_options`
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

## Priority 8: Display Settings

#### 43. `configure_display`
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

## Priority 9: XY Mode (Lissajous)

#### 44. `configure_xy_mode`
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

### Critical (Implement First)
**Advanced Trigger Types (5 tools):** Items 1-5 (pulse, slope, runt, timeout, and window triggers)
- Pulse, slope, runt, timeout, and window triggers cover 90% of advanced trigger use cases
- Essential for capturing and analyzing complex signal behaviors

### High Priority (Implement Next)
**Protocol Analysis (10 tools):** Items 16-20 (protocol triggers), 21-26 (bus decode)
- Essential for digital/embedded work
- Hardware-accelerated protocol decode

**Hardware Counter (3 tools):** Items 43-45
- High-precision measurements independent of main acquisition
- Superior to software measurements

### Medium Priority
**Advanced Triggers (6 tools):** Items 10-15 (remaining advanced triggers)
- Specialized trigger types for specific use cases

**Channel/Timebase/Acquisition (12 tools):** Items 31-42
- Fine-tuning and advanced display modes
- Useful but not critical for basic operation

**Waveform Recording (5 tools):** Items 46-50
- Segmented memory capture and playback
- Excellent for intermittent event analysis

### Lower Priority
**Reference Waveforms (2 tools):** Items 51-52
**System Utilities (5 tools):** Items 53-57
**Display/XY Mode (2 tools):** Items 58-59

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
enable_pulse_trigger()
set_pulse_source(1)
set_pulse_when("GREATER")
set_pulse_width(1e-6)
set_pulse_level(1.5)
```

**✅ GOOD - Single comprehensive tool:**
```python
configure_pulse_trigger(
    channel=1,
    polarity="POSITIVE",
    when="GREATER",
    upper_width=1e-6,
    level=1.5
)
```

### Verification Strategy
1. Read programming guide section for each command
2. Test all parameters with actual hardware
3. Verify SCPI command syntax matches documentation
4. Ensure return types include all relevant information
5. Add proper type hints and validation

---

## Total: 55 New Tools

This represents a complete implementation of all hardware-supported features not yet in the MCP server, excluding features better done in Python (math, FFT, measurements, filters, etc.).
