"""MCP server for Rigol DHO824 oscilloscope with proper type definitions."""

import os
import time
from datetime import datetime, timezone
from enum import Enum
from typing import Optional, TypedDict, Annotated, List, Literal
import numpy as np
from pydantic import Field
from fastmcp import FastMCP
from dotenv import load_dotenv
import pyvisa


# === ENUMS FOR CONSTRAINED VALUES ===

class BandwidthLimit(str, Enum):
    """Bandwidth limit options for DHO800 series oscilloscopes."""
    OFF = "OFF"  # Full bandwidth (no limiting)
    MHZ_20 = "20MHz"  # 20 MHz bandwidth limit (user-friendly)


# Channel representation: accept only integers 1-4 for clarity
ChannelNumber = Annotated[int, Field(ge=1, le=4, description="Channel number (1-4)", examples=[1, 2, 3, 4])]


class Coupling(str, Enum):
    """All coupling modes for channels and triggers."""
    AC = "AC"
    DC = "DC"
    GND = "GND"
    LF_REJECT = "LFReject"  # Trigger only
    HF_REJECT = "HFReject"  # Trigger only


# Probe ratio: accept plain numeric value (e.g., 1, 10, 100).
ProbeRatioField = Annotated[float, Field(description="Probe attenuation ratio (numeric)", examples=[1, 10, 100, 1000])]

# Type aliases for specific coupling uses (user-facing string values)
ChannelCoupling = Literal["AC", "DC", "GND"]
TriggerCouplingType = Literal["AC", "DC", "LFReject", "HFReject"]

# Common field type aliases for deduplication
VerticalScaleField = Annotated[float, Field(description="Vertical scale in V/div")]
VerticalOffsetField = Annotated[float, Field(description="Vertical offset in volts")]
TimeOffsetField = Annotated[float, Field(description="Time offset in seconds")]

# Units field aliases for different contexts
VoltageUnitsField = Annotated[str, Field(description="Voltage units (V, mV, μV, nV)")]
TimeUnitsField = Annotated[str, Field(description="Time units (s, ms, μs, ns)")]
SampleRateUnitsField = Annotated[str, Field(description="Sample rate units (Sa/s, MSa/s, GSa/s)")]
GenericUnitsField = Annotated[str, Field(description="Measurement units")]

# Human-readable string fields
HumanReadableMemoryField = Annotated[str, Field(description="Human-readable memory depth")]
HumanReadableTimeField = Annotated[str, Field(description="Human-readable time scale")]
HumanReadableSampleRateField = Annotated[str, Field(description="Human-readable sample rate")]


class AcquisitionType(str, Enum):
    """Acquisition type modes."""
    NORMAL = "NORMAL"
    AVERAGE = "AVERAGE"
    PEAK = "PEAK"
    ULTRA = "ULTRA"


class TriggerStatus(str, Enum):
    """Trigger status states."""
    TRIGGERED = "triggered"
    WAITING = "waiting"
    RUNNING = "running"
    AUTO = "auto"
    STOPPED = "stopped"


class TriggerMode(str, Enum):
    """Trigger modes."""
    EDGE = "EDGE"
    PULSE = "PULSE"
    SLOPE = "SLOPE"
    VIDEO = "VIDEO"
    PATTERN = "PATTERN"
    RS232 = "RS232"
    I2C = "I2C"
    SPI = "SPI"
    CAN = "CAN"
    LIN = "LIN"
    FLEXRAY = "FLEXRAY"
    CANFD = "CANFD"


class TriggerSlope(str, Enum):
    """Trigger edge slopes (user-facing)."""
    POSITIVE = "POSITIVE"  # Rising edge
    NEGATIVE = "NEGATIVE"  # Falling edge
    EITHER = "EITHER"      # Either edge (rising or falling)


class AcquisitionAction(str, Enum):
    """Acquisition control actions."""
    RUN = "run"
    STOP = "stop"
    SINGLE = "single"


class SystemAction(str, Enum):
    """System control actions."""
    FORCE_TRIGGER = "force_trigger"
    AUTO_SETUP = "auto_setup"
    CLEAR_DISPLAY = "clear_display"




class TriggerSweep(str, Enum):
    """Trigger sweep modes."""
    AUTO = "AUTO"  # Auto trigger
    NORMAL = "NORMal"  # Normal trigger
    SINGLE = "SINGle"  # Single trigger


class WaveformMode(str, Enum):
    """Waveform reading modes."""
    NORMAL = "NORMal"  # Read displayed waveform
    MAXIMUM = "MAXimum"  # Read maximum waveform data
    RAW = "RAW"  # Read raw waveform data from memory


class WaveformFormat(str, Enum):
    """Waveform data formats."""
    WORD = "WORD"  # 16-bit word format
    BYTE = "BYTE"  # 8-bit byte format
    ASCII = "ASCii"  # ASCII format


class PulsePolarity(str, Enum):
    """Pulse trigger polarity."""
    POSITIVE = "POSitive"
    NEGATIVE = "NEGative"


class PulseWhen(str, Enum):
    """Pulse trigger conditions."""
    GREATER = "GREater"  # Pulse width greater than
    LESS = "LESS"  # Pulse width less than
    WITHIN = "WITHin"  # Pulse width within range



class MemoryDepth(str, Enum):
    """Memory depth options."""
    AUTO = "AUTO"
    K1 = "1K"
    K10 = "10K"
    K100 = "100K"
    M1 = "1M"
    M5 = "5M"  # Added 5M option from documentation
    M10 = "10M"
    M25 = "25M"
    M50 = "50M"


# === TYPE DEFINITIONS FOR RESULTS ===

# Identity results
class ModelNumberResult(TypedDict):
    """Result containing the oscilloscope model number."""
    model: Annotated[str, Field(description="The oscilloscope model number", examples=["DHO824", "DHO804", "DHO914", "DHO924"])]


class SoftwareVersionResult(TypedDict):
    """Result containing the oscilloscope software version."""
    version: Annotated[str, Field(description="The firmware/software version", examples=["00.02.01.SP2", "00.01.05", "00.02.00.SP1"])]


class SerialNumberResult(TypedDict):
    """Result containing the oscilloscope serial number."""
    serial: Annotated[str, Field(description="The unique serial number", examples=["DHO8240000001", "DHO8040000123", "DHO9140000456"])]


# Channel results
class ChannelEnableResult(TypedDict):
    """Result for channel enable/disable operations."""
    channel: ChannelNumber
    enabled: Annotated[bool, Field(description="Whether the channel is enabled")]


class ChannelCouplingResult(TypedDict):
    """Result for channel coupling settings."""
    channel: ChannelNumber
    coupling: Annotated[ChannelCoupling, Field(description="Coupling mode")]


class ChannelProbeResult(TypedDict):
    """Result for channel probe settings."""
    channel: ChannelNumber
    probe_ratio: ProbeRatioField


class ChannelBandwidthResult(TypedDict):
    """Result for channel bandwidth settings."""
    channel: ChannelNumber
    bandwidth_limit: Annotated[Literal["OFF", "20MHz"], Field(description="Bandwidth limit setting")]


class ChannelStatusResult(TypedDict):
    """Comprehensive channel status."""
    channel: ChannelNumber
    enabled: Annotated[bool, Field(description="Whether channel is enabled")]
    coupling: Annotated[ChannelCoupling, Field(description="Coupling mode")]
    probe_ratio: ProbeRatioField
    bandwidth_limit: Annotated[Literal["OFF", "20MHz"], Field(description="Bandwidth limit")]
    vertical_scale: VerticalScaleField
    vertical_offset: VerticalOffsetField
    invert: Annotated[bool, Field(description="Whether channel is inverted")]
    units: GenericUnitsField


class VerticalScaleResult(TypedDict):
    """Result for vertical scale settings."""
    channel: ChannelNumber
    vertical_scale: VerticalScaleField
    units: GenericUnitsField


class VerticalOffsetResult(TypedDict):
    """Result for vertical offset settings."""
    channel: ChannelNumber
    vertical_offset: VerticalOffsetField
    units: GenericUnitsField


# Timebase results
class TimebaseScaleResult(TypedDict):
    """Result for timebase scale settings."""
    time_per_div: Annotated[float, Field(description="Time per division in seconds")]
    time_per_div_str: HumanReadableTimeField


class TimebaseOffsetResult(TypedDict):
    """Result for timebase offset settings."""
    time_offset: TimeOffsetField
    units: TimeUnitsField


# Acquisition results
class AcquisitionStatusResult(TypedDict):
    """Result for acquisition control operations."""
    action: Annotated[AcquisitionAction, Field(description="Action performed")]
    trigger_status: Annotated[TriggerStatus, Field(description="Current trigger status")]


class MemoryDepthResult(TypedDict):
    """Result for memory depth settings."""
    memory_depth: Annotated[float, Field(description="Memory depth in points")]
    memory_depth_str: HumanReadableMemoryField


class AcquisitionTypeResult(TypedDict):
    """Result for acquisition type settings."""
    acquisition_type: Annotated[AcquisitionType, Field(description="Acquisition type mode")]


class SampleRateResult(TypedDict):
    """Result for sample rate queries."""
    sample_rate: Annotated[float, Field(description="Sample rate in Sa/s")]
    sample_rate_str: HumanReadableSampleRateField
    units: SampleRateUnitsField


# Trigger results
class TriggerStatusResult(TypedDict):
    """Current trigger status information."""
    trigger_status: Annotated[TriggerStatus, Field(description="Trigger status")]
    raw_trigger_status: Annotated[str, Field(description="Raw status from scope")]
    trigger_mode: Annotated[TriggerMode, Field(description="Current trigger mode")]
    # Optional edge trigger fields
    channel: Annotated[Optional[ChannelNumber], Field(description="Trigger source channel (1-4)")]
    trigger_level: Annotated[Optional[float], Field(description="Trigger level (volts) for edge trigger")]
    trigger_slope: Annotated[Optional[TriggerSlope], Field(description="Trigger slope for edge trigger")]


class TriggerModeResult(TypedDict):
    """Result for trigger mode settings."""
    trigger_mode: Annotated[TriggerMode, Field(description="Trigger mode")]


class TriggerSourceResult(TypedDict):
    """Result for trigger source settings."""
    channel: ChannelNumber


class TriggerLevelResult(TypedDict):
    """Result for trigger level settings."""
    trigger_level: Annotated[float, Field(description="Trigger level in volts")]
    units: VoltageUnitsField


class TriggerSlopeResult(TypedDict):
    """Result for trigger slope settings."""
    trigger_slope: Annotated[TriggerSlope, Field(description="Trigger slope (POSITIVE, NEGATIVE, or EITHER)")]


# Action results
class ActionResult(TypedDict):
    """Result for simple action operations."""
    action: Annotated[SystemAction, Field(description="Action performed")]


# Waveform data
class WaveformChannelData(TypedDict):
    """Data for a single channel waveform capture."""
    channel: ChannelNumber
    raw_data: Annotated[List[int], Field(description="Raw ADC values (16-bit unsigned integers)")]
    truncated: Annotated[bool, Field(description="True if any ADC values reached saturation (65535), indicating possible clipping")]
    # Conversion parameters for voltage calculation: voltage = (raw_value - y_origin - y_reference) * y_increment
    y_increment: Annotated[float, Field(description="Vertical increment for raw-to-voltage conversion")]
    y_origin: Annotated[float, Field(description="Vertical origin offset for raw-to-voltage conversion")]
    y_reference: Annotated[float, Field(description="Vertical reference offset for raw-to-voltage conversion")]
    # Time calculation parameters: time = sample_index * x_increment + x_origin
    x_increment: Annotated[float, Field(description="Time increment between samples (seconds)")]
    x_origin: Annotated[float, Field(description="Time origin offset (seconds)")]
    # Channel settings
    vertical_scale: VerticalScaleField
    vertical_offset: VerticalOffsetField
    probe_ratio: ProbeRatioField
    # Acquisition info
    sample_rate: Annotated[float, Field(description="Sample rate in Sa/s")]
    points: Annotated[int, Field(description="Number of data points")]
    timestamp: Annotated[str, Field(description="ISO format timestamp")]


# === OSCILLOSCOPE CONNECTION CLASS ===

class RigolDHO824:
    """Class to manage communication with Rigol DHO824 oscilloscope."""
    
    def __init__(self, resource_string: Optional[str] = None, timeout: int = 5000):
        """
        Initialize the oscilloscope connection.
        
        Args:
            resource_string: VISA resource string for the oscilloscope
            timeout: Communication timeout in milliseconds
        """
        self.rm = pyvisa.ResourceManager()
        self.instrument = None
        self.resource_string = resource_string
        self.timeout = timeout
        self._identity = None
        
    def connect(self) -> bool:
        """
        Connect to the oscilloscope.
        
        Returns:
            True if connection successful, False otherwise
        """
        # If already connected, test if connection is still alive
        if self.instrument is not None:
            try:
                # Test if connection is still alive with a simple query
                self.instrument.query('*OPC?')
                # self.instrument.write('*OPC')
                return True
            except:
                # Connection is dead, proceed to reconnect
                print("Connection dead")
                self.disconnect()
        
        print("Opening up new connection")
        try:
            if self.resource_string:
                # Use provided resource string
                self.instrument = self.rm.open_resource(self.resource_string)
            else:
                # Auto-discover Rigol oscilloscope
                resources = self.rm.list_resources()
                rigol_resources = [r for r in resources if 'RIGOL' in r.upper() or '0x1AB1' in r]
                
                if not rigol_resources:
                    return False
                    
                # Try to connect to first Rigol device found
                self.instrument = self.rm.open_resource(rigol_resources[0])
                
            self.instrument.timeout = self.timeout

            # Set proper termination characters for SCPI communication
            self.instrument.read_termination = '\n'
            self.instrument.write_termination = '\n'

            # Clear the instrument's input and output buffers
            # self.instrument.clear()

            # Ensure synchronization - wait for all operations to complete
            self.instrument.write('*OPC')
            
            # Test connection and cache identity
            self._identity = self.instrument.query('*IDN?').strip()
            
            return True
            
        except Exception:
            return False
    
    def disconnect(self):
        """Disconnect from the oscilloscope."""
        if self.instrument:
            try:
                self.instrument.close()
            except:
                pass
            self.instrument = None
            
    def get_identity(self) -> Optional[str]:
        """
        Get the full identity string from the oscilloscope.
        
        Returns:
            Identity string or None if not connected
        """
        if not self.instrument:
            return None
            
        if self._identity is None:
            try:
                self._identity = self.instrument.query('*IDN?').strip()
            except:
                return None
                
        return self._identity
    
    def parse_identity(self):
        """
        Parse the identity string into components.
        
        Returns:
            Dictionary with manufacturer, model, serial, version or None if parsing fails
        """
        identity = self.get_identity()
        if not identity:
            return None
            
        # Format: RIGOL TECHNOLOGIES,<model>,<serial>,<version>
        parts = identity.split(',')
        if len(parts) >= 4:
            return {
                'manufacturer': parts[0],
                'model': parts[1],
                'serial': parts[2],
                'version': parts[3]
            }
        return None


def create_server() -> FastMCP:
    """Create the FastMCP server with oscilloscope tools."""
    
    # Load environment variables
    load_dotenv()
    
    # Get configuration from environment
    resource_string = os.getenv('RIGOL_RESOURCE', '')
    timeout = int(os.getenv('VISA_TIMEOUT', '5000'))
    
    # Create MCP server
    mcp = FastMCP("rigol-dho824", stateless_http=True)
    
    # Create oscilloscope instance
    scope = RigolDHO824(resource_string if resource_string else None, timeout)
    
    # === HELPER FUNCTIONS FOR ENUM MAPPING ===
    
    def map_trigger_status(raw_status: str) -> TriggerStatus:
        """Map raw trigger status to enum."""
        status_map = {
            "TD": TriggerStatus.TRIGGERED,
            "WAIT": TriggerStatus.WAITING,
            "RUN": TriggerStatus.RUNNING,
            "AUTO": TriggerStatus.AUTO,
            "STOP": TriggerStatus.STOPPED
        }
        return status_map.get(raw_status, TriggerStatus.STOPPED)
    
    def map_trigger_slope_response(raw_slope: str) -> TriggerSlope:
        """Map SCPI slope response to user-facing TriggerSlope values."""
        slope_map = {
            "POS": TriggerSlope.POSITIVE,
            "NEG": TriggerSlope.NEGATIVE,
            "RFAL": TriggerSlope.EITHER,
            "EITH": TriggerSlope.EITHER,  # Some firmware replies with EITH
        }
        return slope_map.get(raw_slope, TriggerSlope.POSITIVE)  # Default to POSITIVE
    
    def map_coupling_mode(raw_coupling: str) -> str:
        """Map raw coupling mode to user-facing string (AC/DC/GND)."""
        coupling = raw_coupling.upper()
        if coupling in ["AC", "DC", "GND"]:
            return coupling
        return "GND"
    
    def map_acquisition_type(raw_type: str) -> AcquisitionType:
        """Map raw acquisition type to enum."""
        type_map = {
            "NORM": AcquisitionType.NORMAL,
            "AVER": AcquisitionType.AVERAGE,
            "PEAK": AcquisitionType.PEAK,
            "ULTR": AcquisitionType.ULTRA
        }
        return type_map.get(raw_type, AcquisitionType.NORMAL)

    def map_trigger_mode(raw_mode: str) -> TriggerMode:
        """Map SCPI trigger mode response to TriggerMode enum."""
        for tm in TriggerMode:
            if raw_mode == tm.value or raw_mode == tm.value[:4].upper():
                return tm
        return TriggerMode.EDGE
    
    # === IDENTITY TOOLS ===
    
    @mcp.tool
    async def get_model_number() -> ModelNumberResult:
        """
        Get the model number of the connected Rigol oscilloscope.
        
        Returns the model identifier (e.g., 'DHO824') from the oscilloscope's
        identity string.
        """
        try:
            if not scope.connect():
                raise Exception("Failed to connect to oscilloscope. Check connection and RIGOL_RESOURCE environment variable.")
            
            identity_parts = scope.parse_identity()
            if not identity_parts:
                raise Exception("Failed to parse oscilloscope identity")
            
            return ModelNumberResult(
                model=identity_parts['model']
            )
            
        except Exception as e:
            raise Exception(f"Error getting model number: {str(e)}") from e
        finally:
            scope.disconnect()
    
    @mcp.tool
    async def get_software_version() -> SoftwareVersionResult:
        """
        Get the software/firmware version of the connected Rigol oscilloscope.
        
        Returns the software version string from the oscilloscope's
        identity information.
        """
        try:
            if not scope.connect():
                raise Exception("Failed to connect to oscilloscope. Check connection and RIGOL_RESOURCE environment variable.")
            
            identity_parts = scope.parse_identity()
            if not identity_parts:
                raise Exception("Failed to parse oscilloscope identity")
            
            return SoftwareVersionResult(
                version=identity_parts['version']
            )
            
        except Exception as e:
            raise Exception(f"Error getting software version: {str(e)}") from e
        finally:
            scope.disconnect()
    
    @mcp.tool
    async def get_serial_number() -> SerialNumberResult:
        """
        Get the serial number of the connected Rigol oscilloscope.
        
        Returns the unique serial number identifier from the oscilloscope's
        identity string.
        """
        try:
            if not scope.connect():
                raise Exception("Failed to connect to oscilloscope. Check connection and RIGOL_RESOURCE environment variable.")
            
            identity_parts = scope.parse_identity()
            if not identity_parts:
                raise Exception("Failed to parse oscilloscope identity")
            
            return SerialNumberResult(
                serial=identity_parts['serial']
            )
            
        except Exception as e:
            raise Exception(f"Error getting serial number: {str(e)}") from e
        finally:
            scope.disconnect()
    
    # === WAVEFORM CAPTURE TOOLS ===
    
    @mcp.tool
    async def capture_waveform(
        channels: Annotated[List[ChannelNumber], Field(description="List of channels to capture (1-4)", examples=[[1], [1, 2]])] = [1]
    ) -> List[WaveformChannelData]:
        """
        Capture raw waveform data from specified channels.
        
        Captures data in RAW mode with WORD format (16-bit) for maximum accuracy.
        Reads all available points from oscilloscope memory (up to 50M points depending on settings).
        Returns raw ADC values along with all parameters needed for voltage conversion.
        The 'truncated' field indicates if any ADC values reached saturation (65535),
        which suggests the signal may be clipped and vertical scale adjustment may be needed.
        
        Voltage conversion formula: voltage = (raw_value - y_origin - y_reference) * y_increment
        Time calculation formula: time = sample_index * x_increment + x_origin
        
        Args:
            channels: List of channel numbers to capture (1-4), defaults to [1]
            
        Returns:
            List of raw waveform data with conversion parameters for each channel
        """
        try:
            if not scope.connect():
                raise Exception("Failed to connect to oscilloscope")
            
            # Channels are already validated by the enum type
            
            results = []
            
            # Stop acquisition once for all channels
            scope.instrument.write(':STOP')
            
            for channel in channels:
                # Check if channel is enabled
                channel_enabled = int(scope.instrument.query(f':CHAN{channel}:DISP?'))
                if not channel_enabled:
                    continue
                    
                try:
                    # Set source channel
                    scope.instrument.write(f':WAV:SOUR CHAN{channel}')
                    
                    # Configure for RAW mode with WORD format (16-bit)
                    scope.instrument.write(':WAV:MODE RAW')
                    scope.instrument.write(':WAV:FORM WORD')
                    
                    # Query memory depth to determine available points
                    memory_depth = float(scope.instrument.query(':ACQ:MDEP?'))
                    
                    # Set read range to full memory depth
                    max_points = int(memory_depth)  # Read all available points
                    scope.instrument.write(':WAV:STAR 1')
                    scope.instrument.write(f':WAV:STOP {max_points}')
                    
                    # Query waveform parameters for conversion
                    y_increment = float(scope.instrument.query(':WAV:YINC?'))
                    y_origin = float(scope.instrument.query(':WAV:YOR?'))
                    y_reference = float(scope.instrument.query(':WAV:YREF?'))
                    x_increment = float(scope.instrument.query(':WAV:XINC?'))
                    x_origin = float(scope.instrument.query(':WAV:XOR?'))
                    
                    # Query channel settings
                    vertical_scale = float(scope.instrument.query(f':CHAN{channel}:SCAL?'))
                    vertical_offset = float(scope.instrument.query(f':CHAN{channel}:OFFS?'))
                    probe_ratio = float(scope.instrument.query(f':CHAN{channel}:PROB?'))
                    
                    # Query sample rate
                    sample_rate = float(scope.instrument.query(':ACQ:SRAT?'))
                    
                    # Capture the waveform data (16-bit unsigned integers)
                    raw_data = scope.instrument.query_binary_values(
                        ':WAV:DATA?', 
                        datatype='H',  # Unsigned 16-bit
                        is_big_endian=False
                    )
                    
                    # Check for ADC saturation using numpy for efficiency (65535 is max value for 16-bit unsigned)
                    truncated = bool(np.max(raw_data) == 65535) if raw_data else False
                    
                    results.append(WaveformChannelData(
                        channel=channel,
                        raw_data=raw_data,  # Return raw ADC values directly
                        truncated=truncated,  # Indicate if any values hit ADC saturation
                        y_increment=y_increment,
                        y_origin=y_origin,
                        y_reference=y_reference,
                        x_increment=x_increment,
                        x_origin=x_origin,
                        vertical_scale=vertical_scale,
                        vertical_offset=vertical_offset,
                        probe_ratio=probe_ratio,
                        sample_rate=sample_rate,
                        points=len(raw_data),
                        timestamp=datetime.now(timezone.utc).isoformat()
                    ))
                except Exception as e:
                    # Skip channels with errors
                    continue
            
            return results
            
        except Exception as e:
            raise Exception(f"Error capturing waveform: {str(e)}") from e
        finally:
            scope.disconnect()
    
    # === CHANNEL CONTROL TOOLS ===
    
    @mcp.tool
    async def set_channel_enable(
        channel: ChannelNumber,
        enabled: Annotated[bool, Field(description="True to enable, False to disable")]
    ) -> ChannelEnableResult:
        """
        Enable or disable a channel display.
        
        Args:
            channel: Channel number (1-4)
            enabled: True to enable, False to disable
            
        Returns:
            Channel enable status
        """
        try:
            if not scope.connect():
                raise Exception("Failed to connect to oscilloscope")
            
            state = "ON" if enabled else "OFF"
            scope.instrument.write(f':CHAN{channel}:DISP {state}')
            
            # Verify the setting
            actual_state = int(scope.instrument.query(f':CHAN{channel}:DISP?'))
            
            return ChannelEnableResult(
                channel=channel,
                enabled=bool(actual_state)
            )
            
        except Exception as e:
            raise Exception(f"Error setting channel enable: {str(e)}") from e
        finally:
            scope.disconnect()
    
    @mcp.tool
    async def set_channel_coupling(
        channel: ChannelNumber,
        coupling: Annotated[ChannelCoupling, Field(description="Coupling mode: AC, DC, or GND")]
    ) -> ChannelCouplingResult:
        """
        Set channel coupling mode.
        
        Args:
            channel: Channel number (1-4)
            coupling: Coupling mode (AC, DC, or GND)
            
        Returns:
            Channel coupling setting
        """
        try:
            if not scope.connect():
                raise Exception("Failed to connect to oscilloscope")
            
            # Use enum value directly
            scope.instrument.write(f':CHAN{channel}:COUP {coupling}')
            
            # Verify the setting
            actual_coupling = scope.instrument.query(f':CHAN{channel}:COUP?').strip()
            
            return ChannelCouplingResult(
                channel=channel,
                coupling=map_coupling_mode(actual_coupling)
            )
            
        except Exception as e:
            raise Exception(f"Error setting channel coupling: {str(e)}") from e
        finally:
            scope.disconnect()
    
    @mcp.tool
    async def set_channel_probe(
        channel: ChannelNumber,
        probe_ratio: ProbeRatioField
    ) -> ChannelProbeResult:
        """
        Set channel probe attenuation ratio.
        
        Args:
            channel: Channel number (1-4)
            probe_ratio: Probe ratio (e.g., 1, 10, 100, 1000)
            
        Returns:
            Channel probe setting
        """
        try:
            if not scope.connect():
                raise Exception("Failed to connect to oscilloscope")
            
            # Format as integer if it's a whole number, otherwise as float
            probe_value = int(probe_ratio) if float(probe_ratio).is_integer() else float(probe_ratio)
            scope.instrument.write(f':CHAN{channel}:PROB {probe_value}')
            
            # Verify the setting
            actual_ratio = float(scope.instrument.query(f':CHAN{channel}:PROB?'))
            
            return ChannelProbeResult(
                channel=channel,
                probe_ratio=actual_ratio
            )
            
        except Exception as e:
            raise Exception(f"Error setting channel probe: {str(e)}") from e
        finally:
            scope.disconnect()
    
    @mcp.tool
    async def set_channel_bandwidth(
        channel: ChannelNumber,
        bandwidth_limit: Annotated[Optional[Literal["OFF", "20MHz"]], Field(description="Bandwidth limit: OFF or 20MHz. Default is OFF")] = None
    ) -> ChannelBandwidthResult:
        """
        Set channel bandwidth limit to reduce noise and filter high frequencies.
        
        The bandwidth limit attenuates high frequency components in the signal that
        are greater than the specified limit. This is useful for reducing noise in
        displayed waveforms while preserving the lower frequency components of interest.
        
        The DHO800 series supports:
        - OFF: Full bandwidth (no limiting)
        - 20MHz: 20 MHz bandwidth limit
        
        Note: Bandwidth limiting not only reduces noise but also attenuates or eliminates
        the high frequency components of the signal.
        
        Args:
            channel: Channel number (1-4)
            bandwidth_limit: Bandwidth limit setting (OFF or 20MHz). Defaults to OFF
            
        Returns:
            Channel bandwidth setting
        """
        try:
            if not scope.connect():
                raise Exception("Failed to connect to oscilloscope")
            
            if bandwidth_limit is None:
                bandwidth_limit = "OFF"
            
            # Map user-friendly value to SCPI
            bw_value = "20M" if bandwidth_limit == "20MHz" else "OFF"
            scope.instrument.write(f':CHAN{channel}:BWL {bw_value}')
            
            # Verify the setting
            actual_bw = scope.instrument.query(f':CHAN{channel}:BWL?').strip()
            
            # Map response to enum
            result_bw = "20MHz" if actual_bw == "20M" else "OFF"
            
            return ChannelBandwidthResult(
                channel=channel,
                bandwidth_limit=result_bw
            )
            
        except Exception as e:
            raise Exception(f"Error setting channel bandwidth: {str(e)}") from e
        finally:
            scope.disconnect()
    
    @mcp.tool
    async def get_channel_status(
        channel: ChannelNumber
    ) -> ChannelStatusResult:
        """
        Get comprehensive channel status and settings.
        
        Args:
            channel: Channel number (1-4)
            
        Returns:
            All channel settings
        """
        try:
            if not scope.connect():
                raise Exception("Failed to connect to oscilloscope")
            
            # Query all channel settings
            enabled = bool(int(scope.instrument.query(f':CHAN{channel}:DISP?')))
            coupling = scope.instrument.query(f':CHAN{channel}:COUP?').strip()
            probe_ratio = float(scope.instrument.query(f':CHAN{channel}:PROB?'))
            bw_limit = scope.instrument.query(f':CHAN{channel}:BWL?').strip()
            vertical_scale = float(scope.instrument.query(f':CHAN{channel}:SCAL?'))
            vertical_offset = float(scope.instrument.query(f':CHAN{channel}:OFFS?'))
            invert = bool(int(scope.instrument.query(f':CHAN{channel}:INV?')))
            units = scope.instrument.query(f':CHAN{channel}:UNIT?').strip()
            
            # Map bandwidth limit
            bandwidth_limit = "20MHz" if bw_limit == "20M" else "OFF"
            
            return ChannelStatusResult(
                channel=channel,
                enabled=enabled,
                coupling=map_coupling_mode(coupling),
                probe_ratio=probe_ratio,
                bandwidth_limit=bandwidth_limit,
                vertical_scale=vertical_scale,
                vertical_offset=vertical_offset,
                invert=invert,
                units=units
            )
            
        except Exception as e:
            raise Exception(f"Error getting channel status: {str(e)}") from e
        finally:
            scope.disconnect()
    
    # === SCALE ADJUSTMENT TOOLS ===
    
    @mcp.tool
    async def set_vertical_scale(
        channel: ChannelNumber,
        vertical_scale: VerticalScaleField
    ) -> VerticalScaleResult:
        """
        Set channel vertical scale (V/div).
        
        Args:
            channel: Channel number (1-4)
            vertical_scale: Vertical scale in V/div
            
        Returns:
            Vertical scale setting
        """
        try:
            if not scope.connect():
                raise Exception("Failed to connect to oscilloscope")
            
            # Valid scales follow 1-2-5 sequence
            valid_scales = [
                1e-3, 2e-3, 5e-3,  # mV range
                1e-2, 2e-2, 5e-2,
                1e-1, 2e-1, 5e-1,
                1, 2, 5,           # V range
                10, 20, 50,
                100
            ]
            
            # Find closest valid scale
            scale = vertical_scale
            if scale not in valid_scales:
                scale = valid_scales[np.argmin(np.abs(np.array(valid_scales) - scale))]
            
            scope.instrument.write(f':CHAN{channel}:SCAL {scale}')
            
            # Verify the setting
            actual_scale = float(scope.instrument.query(f':CHAN{channel}:SCAL?'))
            
            return VerticalScaleResult(
                channel=channel,
                vertical_scale=actual_scale,
                units="V/div"
            )
            
        except Exception as e:
            raise Exception(f"Error setting vertical scale: {str(e)}") from e
        finally:
            scope.disconnect()
    
    @mcp.tool
    async def set_vertical_offset(
        channel: ChannelNumber,
        vertical_offset: VerticalOffsetField
    ) -> VerticalOffsetResult:
        """
        Set channel vertical offset.
        
        Args:
            channel: Channel number (1-4)
            vertical_offset: Vertical offset in volts
            
        Returns:
            Vertical offset setting
        """
        try:
            if not scope.connect():
                raise Exception("Failed to connect to oscilloscope")
            
            scope.instrument.write(f':CHAN{channel}:OFFS {vertical_offset}')
            
            # Verify the setting
            actual_offset = float(scope.instrument.query(f':CHAN{channel}:OFFS?'))
            
            return VerticalOffsetResult(
                channel=channel,
                vertical_offset=actual_offset,
                units="V"
            )
            
        except Exception as e:
            raise Exception(f"Error setting vertical offset: {str(e)}") from e
        finally:
            scope.disconnect()
    
    @mcp.tool
    async def set_timebase_scale(
        time_per_div: Annotated[float, Field(description="Time per division in seconds")]
    ) -> TimebaseScaleResult:
        """
        Set horizontal timebase scale.
        
        Args:
            time_per_div: Time per division in seconds
            
        Returns:
            Timebase scale setting
        """
        try:
            if not scope.connect():
                raise Exception("Failed to connect to oscilloscope")
            
            scope.instrument.write(f':TIM:MAIN:SCAL {time_per_div}')
            
            # Verify the setting
            actual_scale = float(scope.instrument.query(':TIM:MAIN:SCAL?'))
            
            # Convert to human-readable format
            if actual_scale >= 1:
                scale_str = f"{actual_scale:.2f} s/div"
            elif actual_scale >= 1e-3:
                scale_str = f"{actual_scale*1e3:.2f} ms/div"
            elif actual_scale >= 1e-6:
                scale_str = f"{actual_scale*1e6:.2f} μs/div"
            else:
                scale_str = f"{actual_scale*1e9:.2f} ns/div"
            
            return TimebaseScaleResult(
                time_per_div=actual_scale,
                time_per_div_str=scale_str
            )
            
        except Exception as e:
            raise Exception(f"Error setting timebase scale: {str(e)}") from e
        finally:
            scope.disconnect()
    
    @mcp.tool
    async def set_timebase_offset(
        time_offset: TimeOffsetField
    ) -> TimebaseOffsetResult:
        """
        Set horizontal timebase offset.
        
        Args:
            time_offset: Time offset in seconds
            
        Returns:
            Timebase offset setting
        """
        try:
            if not scope.connect():
                raise Exception("Failed to connect to oscilloscope")
            
            scope.instrument.write(f':TIM:MAIN:OFFS {time_offset}')
            
            # Verify the setting
            actual_offset = float(scope.instrument.query(':TIM:MAIN:OFFS?'))
            
            return TimebaseOffsetResult(
                time_offset=actual_offset,
                units="s"
            )
            
        except Exception as e:
            raise Exception(f"Error setting timebase offset: {str(e)}") from e
        finally:
            scope.disconnect()
    
    # === ACQUISITION CONTROL TOOLS ===
    
    @mcp.tool
    async def run_acquisition() -> AcquisitionStatusResult:
        """
        Start continuous acquisition (RUN mode).
        
        Returns:
            Acquisition status
        """
        try:
            if not scope.connect():
                raise Exception("Failed to connect to oscilloscope")
            
            scope.instrument.write(':RUN')
            
            # Give it a moment to start
            time.sleep(0.1)
            
            # Check trigger status
            status = scope.instrument.query(':TRIG:STAT?').strip()
            
            return AcquisitionStatusResult(
                action=AcquisitionAction.RUN,
                trigger_status=map_trigger_status(status)
            )
            
        except Exception as e:
            raise Exception(f"Error starting acquisition: {str(e)}") from e
        finally:
            scope.disconnect()
    
    @mcp.tool
    async def stop_acquisition() -> AcquisitionStatusResult:
        """
        Stop acquisition (STOP mode).
        
        Returns:
            Acquisition status
        """
        try:
            if not scope.connect():
                raise Exception("Failed to connect to oscilloscope")
            
            scope.instrument.write(':STOP')
            
            # Give it a moment to stop
            time.sleep(0.1)
            
            # Check trigger status
            status = scope.instrument.query(':TRIG:STAT?').strip()
            
            return AcquisitionStatusResult(
                action=AcquisitionAction.STOP,
                trigger_status=map_trigger_status(status)
            )
            
        except Exception as e:
            raise Exception(f"Error stopping acquisition: {str(e)}") from e
        finally:
            scope.disconnect()
    
    @mcp.tool
    async def single_acquisition() -> AcquisitionStatusResult:
        """
        Perform single acquisition (SINGLE mode).
        
        Returns:
            Acquisition status
        """
        try:
            if not scope.connect():
                raise Exception("Failed to connect to oscilloscope")
            
            scope.instrument.write(':SING')
            
            # Give it a moment to arm
            time.sleep(0.1)
            
            # Check trigger status
            status = scope.instrument.query(':TRIG:STAT?').strip()
            
            return AcquisitionStatusResult(
                action=AcquisitionAction.SINGLE,
                trigger_status=map_trigger_status(status)
            )
            
        except Exception as e:
            raise Exception(f"Error performing single acquisition: {str(e)}") from e
        finally:
            scope.disconnect()
    
    @mcp.tool
    async def force_trigger() -> ActionResult:
        """
        Force a trigger event.
        
        Returns:
            Action confirmation
        """
        try:
            if not scope.connect():
                raise Exception("Failed to connect to oscilloscope")
            
            scope.instrument.write(':TFOR')
            
            return ActionResult(
                action=SystemAction.FORCE_TRIGGER
            )
            
        except Exception as e:
            raise Exception(f"Error forcing trigger: {str(e)}") from e
        finally:
            scope.disconnect()
    
    @mcp.tool
    async def get_trigger_status() -> TriggerStatusResult:
        """
        Get current trigger status.
        
        Returns:
            Trigger status and settings
        """
        try:
            if not scope.connect():
                raise Exception("Failed to connect to oscilloscope")
            
            # Query trigger status
            status = scope.instrument.query(':TRIG:STAT?').strip()
            
            # Get additional trigger info
            mode = scope.instrument.query(':TRIG:MODE?').strip()
            
            result: TriggerStatusResult = {
                "trigger_status": map_trigger_status(status),
                "raw_trigger_status": status,
                "trigger_mode": map_trigger_mode(mode),
                "channel": None,
                "trigger_level": None,
                "trigger_slope": None,
            }
            
            # If edge trigger, get edge-specific settings
            if mode in ["EDGE", "EDG"]:
                actual_source = scope.instrument.query(':TRIG:EDGE:SOUR?').strip()
                if actual_source.startswith("CHAN") or actual_source.startswith("CH"):
                    # Last character is channel number
                    result["channel"] = int(actual_source[-1])
                result["trigger_level"] = float(scope.instrument.query(':TRIG:EDGE:LEV?'))
                raw_slope = scope.instrument.query(':TRIG:EDGE:SLOP?').strip()
                result["trigger_slope"] = map_trigger_slope_response(raw_slope)
            
            return result
            
        except Exception as e:
            raise Exception(f"Error getting trigger status: {str(e)}") from e
        finally:
            scope.disconnect()
    
    # === TRIGGER CONFIGURATION TOOLS ===
    
    @mcp.tool
    async def set_trigger_mode(
        trigger_mode: Annotated[TriggerMode, Field(description="Trigger mode")]
    ) -> TriggerModeResult:
        """
        Set trigger mode.
        
        Args:
            trigger_mode: Trigger mode
            
        Returns:
            Trigger mode setting
        """
        try:
            if not scope.connect():
                raise Exception("Failed to connect to oscilloscope")
            
            scope.instrument.write(f':TRIG:MODE {trigger_mode.value}')
            
            # Verify the setting
            actual_mode = scope.instrument.query(':TRIG:MODE?').strip()
            
            # Map to enum - handle abbreviated responses
            for tm in TriggerMode:
                if actual_mode == tm.value or actual_mode == tm.value[:4]:
                    return TriggerModeResult(trigger_mode=tm)
            
            # Default to EDGE if unknown
            return TriggerModeResult(trigger_mode=TriggerMode.EDGE)
            
        except Exception as e:
            raise Exception(f"Error setting trigger mode: {str(e)}") from e
        finally:
            scope.disconnect()
    
    @mcp.tool
    async def set_trigger_source(
        channel: ChannelNumber
    ) -> TriggerSourceResult:
        """
        Set trigger source for edge trigger.
        
        Args:
            channel: Trigger source channel (1-4)
            
        Returns:
            Trigger source setting
        """
        try:
            if not scope.connect():
                raise Exception("Failed to connect to oscilloscope")
            
            # Ensure we're in edge trigger mode
            current_mode = scope.instrument.query(':TRIG:MODE?').strip()
            if current_mode not in ["EDGE", "EDG"]:
                scope.instrument.write(':TRIG:MODE EDGE')
            
            # Use the channel's SCPI format
            scope.instrument.write(f':TRIG:EDGE:SOUR CHAN{channel}')
            
            # Verify the setting
            actual_source = scope.instrument.query(':TRIG:EDGE:SOUR?').strip()
            
            # Map back to channel number
            if actual_source.startswith("CHAN") or actual_source.startswith("CH"):
                channel_num = int(actual_source[-1])
            else:
                channel_num = 1
            
            return TriggerSourceResult(channel=channel_num)
            
        except Exception as e:
            raise Exception(f"Error setting trigger source: {str(e)}") from e
        finally:
            scope.disconnect()
    
    @mcp.tool
    async def set_trigger_level(
        trigger_level: Annotated[float, Field(description="Trigger level in volts")],
        channel: Annotated[Optional[ChannelNumber], Field(description="Optional trigger source channel (1-4)")] = None
    ) -> TriggerLevelResult:
        """
        Set trigger level voltage.
        
        Args:
            trigger_level: Trigger level in volts
            channel: Optional channel to set level for (defaults to current source)
            
        Returns:
            Trigger level setting
        """
        try:
            if not scope.connect():
                raise Exception("Failed to connect to oscilloscope")
            
            # If source specified, set it first
            if channel:
                # Ensure we're in edge trigger mode
                current_mode = scope.instrument.query(':TRIG:MODE?').strip()
                if current_mode not in ["EDGE", "EDG"]:
                    scope.instrument.write(':TRIG:MODE EDGE')
                
                # Set the source
                scope.instrument.write(f':TRIG:EDGE:SOUR CHAN{channel}')
            
            scope.instrument.write(f':TRIG:EDGE:LEV {trigger_level}')
            
            # Verify the setting
            actual_level = float(scope.instrument.query(':TRIG:EDGE:LEV?'))
            
            return TriggerLevelResult(trigger_level=actual_level, units="V")
            
        except Exception as e:
            raise Exception(f"Error setting trigger level: {str(e)}") from e
        finally:
            scope.disconnect()
    
    @mcp.tool
    async def set_trigger_slope(
        trigger_slope: Annotated[TriggerSlope, Field(description="Edge slope: POSITIVE, NEGATIVE, or EITHER")]
    ) -> TriggerSlopeResult:
        """
        Set trigger edge slope.
        
        Args:
            trigger_slope: Edge slope (POSITIVE, NEGATIVE, or EITHER)
            
        Returns:
            Trigger slope setting
        """
        try:
            if not scope.connect():
                raise Exception("Failed to connect to oscilloscope")
            
            # Map user-facing slope to SCPI value
            slope_map = {
                TriggerSlope.POSITIVE: "POS",
                TriggerSlope.NEGATIVE: "NEG",
                TriggerSlope.EITHER: "RFAL",
            }
            scope.instrument.write(f':TRIG:EDGE:SLOP {slope_map[trigger_slope]}')
            
            # Verify the setting
            actual_slope = scope.instrument.query(':TRIG:EDGE:SLOP?').strip()
            
            # Map back to friendly names
            result_slope = map_trigger_slope_response(actual_slope)
            
            return TriggerSlopeResult(trigger_slope=result_slope)
            
        except Exception as e:
            raise Exception(f"Error setting trigger slope: {str(e)}") from e
        finally:
            scope.disconnect()
    
    # === MEMORY & ACQUISITION SETTINGS ===
    
    @mcp.tool
    async def set_memory_depth(
        memory_depth: Annotated[MemoryDepth, Field(description="Memory depth setting")]
    ) -> MemoryDepthResult:
        """
        Set acquisition memory depth.
        
        Args:
            memory_depth: Memory depth
            
        Returns:
            Memory depth setting
        """
        try:
            if not scope.connect():
                raise Exception("Failed to connect to oscilloscope")
            
            scope.instrument.write(f':ACQ:MDEP {memory_depth.value}')
            
            # Verify the setting
            actual_depth = float(scope.instrument.query(':ACQ:MDEP?'))
            
            # Convert to human-readable format
            if actual_depth >= 1e6:
                depth_str = f"{actual_depth/1e6:.0f}M"
            elif actual_depth >= 1e3:
                depth_str = f"{actual_depth/1e3:.0f}K"
            else:
                depth_str = f"{actual_depth:.0f}"
            
            return MemoryDepthResult(
                memory_depth=actual_depth,
                memory_depth_str=depth_str
            )
            
        except Exception as e:
            raise Exception(f"Error setting memory depth: {str(e)}") from e
        finally:
            scope.disconnect()
    
    @mcp.tool
    async def set_acquisition_type(
        acquisition_type: Annotated[AcquisitionType, Field(description="Acquisition type")]
    ) -> AcquisitionTypeResult:
        """
        Set acquisition type.
        
        Args:
            acquisition_type: Acquisition type
            
        Returns:
            Acquisition type setting
        """
        try:
            if not scope.connect():
                raise Exception("Failed to connect to oscilloscope")
            
            # Map enum to SCPI format
            type_map = {
                AcquisitionType.NORMAL: "NORMal",
                AcquisitionType.AVERAGE: "AVERages",
                AcquisitionType.PEAK: "PEAK",
                AcquisitionType.ULTRA: "ULTRa"
            }
            
            scpi_type = type_map[acquisition_type]
            scope.instrument.write(f':ACQ:TYPE {scpi_type}')
            
            # Verify the setting
            actual_type = scope.instrument.query(':ACQ:TYPE?').strip()
            
            return AcquisitionTypeResult(
                acquisition_type=map_acquisition_type(actual_type)
            )
            
        except Exception as e:
            raise Exception(f"Error setting acquisition type: {str(e)}") from e
        finally:
            scope.disconnect()
    
    @mcp.tool
    async def get_sample_rate() -> SampleRateResult:
        """
        Get current sample rate.
        
        Returns:
            Sample rate information
        """
        try:
            if not scope.connect():
                raise Exception("Failed to connect to oscilloscope")
            
            sample_rate = float(scope.instrument.query(':ACQ:SRAT?'))
            
            # Convert to human-readable format
            if sample_rate >= 1e9:
                rate_str = f"{sample_rate/1e9:.2f} GSa/s"
            elif sample_rate >= 1e6:
                rate_str = f"{sample_rate/1e6:.2f} MSa/s"
            elif sample_rate >= 1e3:
                rate_str = f"{sample_rate/1e3:.2f} kSa/s"
            else:
                rate_str = f"{sample_rate:.2f} Sa/s"
            
            return SampleRateResult(
                sample_rate=sample_rate,
                sample_rate_str=rate_str,
                units="Sa/s"
            )
            
        except Exception as e:
            raise Exception(f"Error getting sample rate: {str(e)}") from e
        finally:
            scope.disconnect()
    
    # === UTILITY TOOLS ===
    
    @mcp.tool
    async def auto_setup() -> ActionResult:
        """
        Perform automatic setup of the oscilloscope.
        
        Automatically configures vertical scale, horizontal scale, and trigger
        settings for optimal display of the input signal.
        
        Returns:
            Action confirmation
        """
        try:
            if not scope.connect():
                raise Exception("Failed to connect to oscilloscope")
            
            scope.instrument.write(':AUT')
            
            # Auto setup takes a moment
            time.sleep(2)
            
            return ActionResult(
                action=SystemAction.AUTO_SETUP
            )
            
        except Exception as e:
            raise Exception(f"Error performing auto setup: {str(e)}") from e
        finally:
            scope.disconnect()
    
    @mcp.tool
    async def clear_display() -> ActionResult:
        """
        Clear the oscilloscope display.
        
        Returns:
            Action confirmation
        """
        try:
            if not scope.connect():
                raise Exception("Failed to connect to oscilloscope")
            
            scope.instrument.write(':CLE')
            
            return ActionResult(
                action=SystemAction.CLEAR_DISPLAY
            )
            
        except Exception as e:
            raise Exception(f"Error clearing display: {str(e)}") from e
        finally:
            scope.disconnect()
    
    return mcp


def main():
    """Run the MCP server."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Rigol DHO824 MCP Server")
    parser.add_argument("--http", action="store_true", help="Use HTTP transport instead of stdio")
    parser.add_argument("--host", default="127.0.0.1", help="Host for HTTP transport (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8000, help="Port for HTTP transport (default: 8000)")
    parser.add_argument("--path", default="/mcp", help="Path for HTTP transport (default: /mcp)")
    
    args = parser.parse_args()
    
    # Create the server
    mcp = create_server()
    
    if args.http:
        # Run with HTTP transport
        mcp.run(
            transport="http",
            host=args.host,
            port=args.port,
            path=args.path
        )
    else:
        # Default to stdio transport
        mcp.run()


if __name__ == "__main__":
    main()
