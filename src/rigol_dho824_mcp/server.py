"""MCP server for Rigol DHO824 oscilloscope with proper type definitions."""

import asyncio
import functools
import hashlib
import io
import os
import tempfile
import json
from datetime import datetime
from enum import Enum
from ftplib import FTP
from typing import Optional, TypedDict, Annotated, List, Literal, cast, Union, Sequence
from typing_extensions import NotRequired
import numpy as np
from pydantic import Field
from fastmcp import FastMCP, Context
from dotenv import load_dotenv
import pyvisa
import pyvisa.resources


# === ENUMS FOR CONSTRAINED VALUES ===


class BandwidthLimit(str, Enum):
    """Bandwidth limit options for DHO800 series oscilloscopes."""

    OFF = "OFF"  # Full bandwidth (no limiting)
    MHZ_20 = "20MHz"  # 20 MHz bandwidth limit (user-friendly)


# Channel representation: accept only integers 1-4 for clarity
ChannelNumber = Annotated[
    int, Field(ge=1, le=4, description="Channel number (1-4)", examples=[1, 2, 3, 4])
]


class Coupling(str, Enum):
    """All coupling modes for channels and triggers."""

    AC = "AC"
    DC = "DC"
    GND = "GND"
    LF_REJECT = "LFReject"  # Trigger only
    HF_REJECT = "HFReject"  # Trigger only


# Probe ratio: accept plain numeric value (e.g., 1, 10, 100).
ProbeRatioField = Annotated[
    float,
    Field(description="Probe attenuation ratio (numeric)", examples=[1, 10, 100, 1000]),
]

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
SampleRateUnitsField = Annotated[
    str, Field(description="Sample rate units (Sa/s, MSa/s, GSa/s)")
]
GenericUnitsField = Annotated[str, Field(description="Measurement units")]

# Human-readable string fields
HumanReadableMemoryField = Annotated[
    str, Field(description="Human-readable memory depth")
]
HumanReadableTimeField = Annotated[str, Field(description="Human-readable time scale")]
HumanReadableSampleRateField = Annotated[
    str, Field(description="Human-readable sample rate")
]

# === TRIGGER-RELATED FIELD TYPE ALIASES ===
# Common field types used across trigger configurations to reduce duplication

# Trigger level and voltage threshold fields
TriggerLevelField = Annotated[float, Field(description="Trigger level in volts")]
UpperVoltageLevelField = Annotated[float, Field(description="Upper voltage threshold")]
LowerVoltageLevelField = Annotated[float, Field(description="Lower voltage threshold")]
StartVoltageLevelField = Annotated[float, Field(description="Start voltage level")]
EndVoltageLevelField = Annotated[float, Field(description="End voltage level")]
SourceAThresholdField = Annotated[float, Field(description="Source A threshold voltage")]
SourceBThresholdField = Annotated[float, Field(description="Source B threshold voltage")]
DataThresholdField = Annotated[float, Field(description="Data threshold voltage")]
ClockThresholdField = Annotated[float, Field(description="Clock threshold voltage")]

# Time limit fields
UpperTimeLimitField = Annotated[float, Field(description="Upper time limit in seconds")]
LowerTimeLimitField = Annotated[float, Field(description="Lower time limit in seconds")]
UpperWidthLimitField = Annotated[float, Field(description="Upper width limit in seconds")]
LowerWidthLimitField = Annotated[float, Field(description="Lower width limit in seconds")]

# Timing-related fields
SetupTimeField = Annotated[float, Field(description="Minimum setup time in seconds")]
HoldTimeField = Annotated[float, Field(description="Minimum hold time in seconds")]
IdleTimeField = Annotated[float, Field(description="Minimum idle time in seconds")]
TimeoutDurationField = Annotated[float, Field(description="Idle time in seconds")]

# Edge and slope fields
EdgeDirectionField = Annotated[str, Field(description="Edge direction")]
EdgeCountField = Annotated[int, Field(description="Which edge number to trigger on")]

# Condition fields
TimeConditionField = Annotated[str, Field(description="Time condition (GREATER, LESS, or WITHIN)")]
WidthConditionField = Annotated[str, Field(description="Width condition (GREATER, LESS, or WITHIN)")]

# === PRIORITY 1 TOOL TYPE ALIASES ===

# Acquisition-related fields
AveragesCountField = Annotated[int, Field(description="Number of averages (2-65536)", ge=2, le=65536)]
UltraTimeoutField = Annotated[float, Field(description="Timeout duration in seconds")]
MaxFramesField = Annotated[int, Field(description="Maximum frames to capture (1-100; MOSaic mode limited to 80)", ge=1, le=100)]

# Recording-related fields
FrameCountField = Annotated[int, Field(description="Number of frames to record", ge=1)]
FrameIntervalField = Annotated[float, Field(description="Time interval between frames in seconds", ge=10e-9, le=1.0)]

# Channel-related fields
ChannelLabelField = Annotated[str, Field(description="Custom label string (max 4 characters)", max_length=4)]

# Delayed timebase fields
DelayedTimeScaleField = Annotated[float, Field(description="Zoom window time per division in seconds")]
DelayedTimeOffsetField = Annotated[float, Field(description="Zoom window offset in seconds")]

# Hardware counter fields
CounterDigitsField = Annotated[int, Field(description="Resolution (5 or 6 digits)", ge=5, le=6)]
CounterValueField = Annotated[float, Field(description="Current counter reading")]


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
    EITHER = "EITHER"  # Either edge (rising or falling)


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
    RESET = "reset"


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


class DVMMode(str, Enum):
    """DVM measurement modes."""

    AC_RMS = "ACRM"  # AC RMS (DC component removed)
    DC = "DC"  # DC average value
    AC_DC_RMS = "DCRM"  # AC+DC RMS (true RMS)

    @classmethod
    def from_user_input(cls, mode: str) -> "DVMMode":
        """Convert user-friendly input to DVMMode enum.

        Accepts various formats: AC_RMS, AC RMS, ACRM, etc.
        """
        mode_map = {
            "AC_RMS": cls.AC_RMS,
            "AC RMS": cls.AC_RMS,
            "ACRM": cls.AC_RMS,
            "DC": cls.DC,
            "AC+DC_RMS": cls.AC_DC_RMS,
            "AC+DC RMS": cls.AC_DC_RMS,
            "DCRM": cls.AC_DC_RMS,
        }
        normalized = mode.upper().replace(" ", "_")
        if normalized not in mode_map:
            raise ValueError(
                f"Invalid DVM mode: {mode}. "
                f"Must be one of: AC_RMS, DC, AC+DC_RMS"
            )
        return mode_map[normalized]

    def to_user_name(self) -> str:
        """Convert SCPI mode to user-friendly name."""
        names = {
            self.AC_RMS: "AC_RMS",
            self.DC: "DC",
            self.AC_DC_RMS: "AC+DC_RMS",
        }
        return names[self]

    def description(self) -> str:
        """Get human-readable description."""
        descriptions = {
            self.AC_RMS: "AC RMS (DC component removed)",
            self.DC: "DC average value",
            self.AC_DC_RMS: "AC+DC RMS (true RMS)",
        }
        return descriptions[self]


class UltraDisplayMode(str, Enum):
    """Display modes for Ultra Acquisition waveform segments."""

    ADJACENT = "ADJacent"  # Segments shown side-by-side in time order
    OVERLAY = "OVERlay"  # All segments overlapped as one waveform
    WATERFALL = "WATerfall"  # Segments in cascaded waterfall display
    PERSPECTIVE = "PERSpective"  # Segments in ladder-like perspective view
    MOSAIC = "MOSaic"  # Segments in grid/mosaic layout


class TimebaseMode(str, Enum):
    """Timebase display modes."""

    MAIN = "MAIN"  # Normal YT mode
    XY = "XY"  # Lissajous/XY mode (Ch1 = X axis, Ch2 = Y axis)
    ROLL = "ROLL"  # Slow sweep roll mode (for low frequencies)


class ChannelUnits(str, Enum):
    """Channel voltage display units."""

    VOLT = "VOLt"
    WATT = "WATT"
    AMPERE = "AMPere"
    UNKNOWN = "UNKNown"


class HardwareCounterMode(str, Enum):
    """Hardware counter measurement modes."""

    FREQUENCY = "FREQuency"  # Measures signal frequency (Hz)
    PERIOD = "PERiod"  # Measures signal period (seconds)
    TOTALIZE = "TOTalize"  # Counts total rising/falling edges


class RecordingOperation(str, Enum):
    """Waveform recording operation states."""

    RUN = "RUN"  # Recording is running
    STOP = "STOP"  # Recording is stopped


class TimeCondition(str, Enum):
    """Time-based trigger conditions (used by multiple trigger types)."""

    GREATER = "GREater"  # Greater than threshold
    LESS = "LESS"  # Less than threshold
    WITHIN = "WITHin"  # Within range


class VideoStandard(str, Enum):
    """Video signal standards."""

    PAL_SECAM = "PALSecam"
    NTSC = "NTSC"
    P480 = "480P"
    P576 = "576P"


class VideoMode(str, Enum):
    """Video trigger modes."""

    ODD_FIELD = "ODDfield"
    EVEN_FIELD = "EVENfield"
    LINE = "LINE"
    ALL_LINES = "ALINes"


class PatternValue(str, Enum):
    """Pattern values for pattern trigger."""

    HIGH = "H"  # High (above threshold)
    LOW = "L"  # Low (below threshold)
    DONT_CARE = "X"  # Don't care
    RISING = "R"  # Rising edge
    FALLING = "F"  # Falling edge


class WindowPosition(str, Enum):
    """Window trigger position modes."""

    EXIT = "EXIT"  # Trigger when signal exits window
    ENTER = "ENTER"  # Trigger when signal enters window
    TIME = "TIME"  # Trigger when signal stays in window for time duration


class SlopeWindow(str, Enum):
    """Slope trigger time measurement windows."""

    TA = "TA"  # Measure from level A
    TB = "TB"  # Measure from level B
    TAB = "TAB"  # Measure from level A to level B


# === PROTOCOL TRIGGER & BUS DECODE ENUMS ===


class RS232When(str, Enum):
    """RS232/UART trigger conditions."""

    START = "STARt"  # Start of frame
    ERROR = "ERRor"  # Error frame
    PARITY_ERROR = "CERRor"  # Check/parity error
    DATA = "DATA"  # Specific data byte


class SerialParity(str, Enum):
    """Serial parity modes for RS232/UART."""

    NONE = "NONE"
    EVEN = "EVEN"
    ODD = "ODD"
    MARK = "MARK"
    SPACE = "SPACe"


class StopBits(str, Enum):
    """Stop bit options for RS232/UART."""

    ONE = "1"
    ONE_HALF = "1.5"
    TWO = "2"


class I2CWhen(str, Enum):
    """I2C trigger conditions."""

    START = "STARt"  # Start condition
    RESTART = "RESTart"  # Restart condition
    STOP = "STOP"  # Stop condition
    NACK = "NACKnowledge"  # Missing acknowledgment
    ADDRESS = "ADDRess"  # Address match
    DATA = "DATA"  # Data match
    ADDRESS_DATA = "ADATa"  # Address and data match


class I2CDirection(str, Enum):
    """I2C transfer direction."""

    READ = "READ"
    WRITE = "WRITe"
    READ_WRITE = "RWRIte"  # Either direction


class AddressWidth(str, Enum):
    """I2C address width options."""

    BITS_7 = "7"
    BITS_10 = "10"


class SPIMode(str, Enum):
    """SPI clock modes (CPOL/CPHA combinations)."""

    MODE_0 = "CPOL0CPHA0"  # CPOL=0, CPHA=0
    MODE_1 = "CPOL0CPHA1"  # CPOL=0, CPHA=1
    MODE_2 = "CPOL1CPHA0"  # CPOL=1, CPHA=0
    MODE_3 = "CPOL1CPHA1"  # CPOL=1, CPHA=1


class CANSignalType(str, Enum):
    """CAN signal type options."""

    RX = "RX"  # CAN RX line
    TX = "TX"  # CAN TX line
    DIFF = "DIFF"  # Differential


class CANWhen(str, Enum):
    """CAN trigger conditions."""

    START = "STARt"  # Start of frame
    FRAME = "FRAM"  # Frame type
    IDENTIFIER = "IDENt"  # Identifier match
    DATA = "DATA"  # Data match
    ID_DATA = "IDDA"  # ID and data match
    ERROR = "ERRor"  # Error frame
    END = "END"  # End of frame
    ACK = "ACK"  # Acknowledge


class CANFrameType(str, Enum):
    """CAN frame types."""

    DATA = "DATA"
    REMOTE = "REMote"


class CANIDType(str, Enum):
    """CAN identifier types."""

    STANDARD = "STANdard"  # 11-bit
    EXTENDED = "EXTended"  # 29-bit


class LINStandard(str, Enum):
    """LIN protocol versions."""

    V1_X = "V1X"
    V2_X = "V2X"
    MIXED = "MIX"


class LINWhen(str, Enum):
    """LIN trigger conditions."""

    SYNC = "SYNC"  # Sync field
    IDENTIFIER = "IDENtifier"  # Identifier
    DATA = "DATA"  # Data
    ID_DATA = "IDDA"  # ID and data
    ERROR = "ERRor"  # Error
    WAKEUP = "AWAK"  # Wakeup signal


class LINErrorType(str, Enum):
    """LIN error types."""

    SYNC_ERROR = "SYNC"
    PARITY_ERROR = "ID"
    CHECKSUM_ERROR = "CHECk"


class BusMode(str, Enum):
    """Bus decode modes."""

    PARALLEL = "PARallel"
    RS232 = "RS232"
    I2C = "IIC"
    SPI = "SPI"
    CAN = "CAN"
    LIN = "LIN"


class BusFormat(str, Enum):
    """Bus decode display formats."""

    HEX = "HEX"
    DEC = "DEC"
    BIN = "BIN"
    ASCII = "ASCii"


class BitOrder(str, Enum):
    """Bit order/endianness."""

    LSB = "LSB"  # Least significant bit first
    MSB = "MSB"  # Most significant bit first


# === PROTOCOL-SPECIFIC TYPE ALIASES ===

# Baud rate field
BaudRateField = Annotated[int, Field(description="Baud rate in bits per second")]

# Data byte/value fields
DataByteField = Annotated[int, Field(ge=0, le=255, description="Data byte value (0-255)")]
DataValueField = Annotated[int, Field(description="Data value to match")]

# Address fields
I2CAddressField = Annotated[int, Field(description="I2C address")]
CANIdentifierField = Annotated[int, Field(description="CAN identifier")]
LINIdentifierField = Annotated[int, Field(ge=0, le=63, description="LIN identifier (0-63)")]

# SPI-specific fields
SPIDataWidthField = Annotated[int, Field(description="Data width in bits (8, 16, 24, 32)")]

# CAN-specific fields
CANSamplePointField = Annotated[int, Field(ge=5, le=95, description="Sample point percentage (5-95%)")]

# Data bits field
DataBitsField = Annotated[int, Field(description="Number of data bits")]

# Bus number field
BusNumberField = Annotated[int, Field(ge=1, le=4, description="Bus number (1-4)", examples=[1, 2, 3, 4])]


# === TYPE DEFINITIONS FOR RESULTS ===


# Identity results
class ModelNumberResult(TypedDict):
    """Result containing the oscilloscope model number."""

    model: Annotated[
        str,
        Field(
            description="The oscilloscope model number",
            examples=["DHO824", "DHO804", "DHO914", "DHO924"],
        ),
    ]


class SoftwareVersionResult(TypedDict):
    """Result containing the oscilloscope software version."""

    version: Annotated[
        str,
        Field(
            description="The firmware/software version",
            examples=["00.02.01.SP2", "00.01.05", "00.02.00.SP1"],
        ),
    ]


class SerialNumberResult(TypedDict):
    """Result containing the oscilloscope serial number."""

    serial: Annotated[
        str,
        Field(
            description="The unique serial number",
            examples=["DHO8240000001", "DHO8040000123", "DHO9140000456"],
        ),
    ]


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
    bandwidth_limit: Annotated[
        Literal["OFF", "20MHz"], Field(description="Bandwidth limit setting")
    ]


class ChannelStatusResult(TypedDict):
    """Comprehensive channel status."""

    channel: ChannelNumber
    enabled: Annotated[bool, Field(description="Whether channel is enabled")]
    coupling: Annotated[ChannelCoupling, Field(description="Coupling mode")]
    probe_ratio: ProbeRatioField
    bandwidth_limit: Annotated[
        Literal["OFF", "20MHz"], Field(description="Bandwidth limit")
    ]
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
    trigger_status: Annotated[
        TriggerStatus, Field(description="Current trigger status")
    ]


class MemoryDepthResult(TypedDict):
    """Result for memory depth settings."""

    memory_depth: Annotated[float, Field(description="Memory depth in points")]
    memory_depth_str: HumanReadableMemoryField


class AcquisitionTypeResult(TypedDict):
    """Result for acquisition type settings."""

    acquisition_type: Annotated[
        AcquisitionType, Field(description="Acquisition type mode")
    ]


class SampleRateResult(TypedDict):
    """Result for sample rate queries."""

    sample_rate: Annotated[float, Field(description="Sample rate in Sa/s")]
    sample_rate_str: HumanReadableSampleRateField
    units: SampleRateUnitsField


# === PRIORITY 1 TOOL RESULTS ===

# Acquisition settings results
class AcquisitionAveragesResult(TypedDict):
    """Result for acquisition averages settings."""

    averages: AveragesCountField
    message: Annotated[str, Field(description="Status message")]


class UltraAcquisitionResult(TypedDict):
    """Result for Ultra Acquisition configuration."""

    display_mode: Annotated[UltraDisplayMode, Field(description="Display mode for waveform segments")]
    timeout: UltraTimeoutField
    max_frames: MaxFramesField
    message: Annotated[str, Field(description="Configuration summary")]


# Channel settings results
class ChannelInvertResult(TypedDict):
    """Result for channel invert settings."""

    channel: ChannelNumber
    inverted: Annotated[bool, Field(description="Channel is inverted")]


class ChannelLabelResult(TypedDict):
    """Result for channel label settings."""

    channel: ChannelNumber
    label: ChannelLabelField


class ChannelLabelVisibilityResult(TypedDict):
    """Result for channel label visibility settings."""

    channel: ChannelNumber
    visible: Annotated[bool, Field(description="Label is visible")]


class ChannelUnitsResult(TypedDict):
    """Result for channel units settings."""

    channel: ChannelNumber
    units: Annotated[ChannelUnits, Field(description="Display units")]


# Timebase settings results
class TimebaseModeResult(TypedDict):
    """Result for timebase mode settings."""

    mode: Annotated[TimebaseMode, Field(description="Timebase mode (MAIN, XY, or ROLL)")]


class DelayedTimebaseEnableResult(TypedDict):
    """Result for delayed timebase enable settings."""

    enabled: Annotated[bool, Field(description="Delayed timebase is enabled")]


class DelayedTimebaseScaleResult(TypedDict):
    """Result for delayed timebase scale settings."""

    time_per_div: DelayedTimeScaleField
    time_per_div_str: HumanReadableTimeField


class DelayedTimebaseOffsetResult(TypedDict):
    """Result for delayed timebase offset settings."""

    time_offset: DelayedTimeOffsetField
    units: TimeUnitsField


# Hardware counter results
class HardwareCounterConfigResult(TypedDict):
    """Result for hardware counter configuration."""

    enabled: Annotated[bool, Field(description="Counter is enabled")]
    channel: ChannelNumber
    mode: Annotated[HardwareCounterMode, Field(description="Counter mode")]
    digits: CounterDigitsField
    totalize_enabled: Annotated[bool, Field(description="Statistics enabled")]
    current_value: Annotated[Optional[float], Field(description="Current counter reading")]
    unit: GenericUnitsField
    message: Annotated[str, Field(description="Configuration summary")]


class HardwareCounterValueResult(TypedDict):
    """Result for hardware counter reading."""

    value: CounterValueField
    unit: GenericUnitsField


class CounterTotalizeResetResult(TypedDict):
    """Result for counter totalize reset."""

    message: Annotated[str, Field(description="Reset confirmation")]


# Trigger results
class TriggerStatusResult(TypedDict):
    """Current trigger status information."""

    trigger_status: Annotated[TriggerStatus, Field(description="Trigger status")]
    raw_trigger_status: Annotated[str, Field(description="Raw status from scope")]
    trigger_mode: Annotated[TriggerMode, Field(description="Current trigger mode")]
    # Optional edge trigger fields
    channel: Annotated[
        Optional[ChannelNumber], Field(description="Trigger source channel (1-4)")
    ]
    trigger_level: Annotated[
        Optional[float], Field(description="Trigger level (volts) for edge trigger")
    ]
    trigger_slope: Annotated[
        Optional[TriggerSlope], Field(description="Trigger slope for edge trigger")
    ]


class TriggerModeResult(TypedDict):
    """Result for trigger mode settings."""

    trigger_mode: Annotated[TriggerMode, Field(description="Trigger mode")]


class TriggerSourceResult(TypedDict):
    """Result for trigger source settings."""

    channel: ChannelNumber


class TriggerLevelResult(TypedDict):
    """Result for trigger level settings."""

    trigger_level: TriggerLevelField
    units: VoltageUnitsField


class TriggerSlopeResult(TypedDict):
    """Result for trigger slope settings."""

    trigger_slope: Annotated[
        TriggerSlope, Field(description="Trigger slope (POSITIVE, NEGATIVE, or EITHER)")
    ]


class TriggerCouplingResult(TypedDict):
    """Result for trigger coupling settings."""

    trigger_coupling: Annotated[
        TriggerCouplingType, Field(description="Trigger coupling mode")
    ]


class TriggerSweepResult(TypedDict):
    """Result for trigger sweep mode settings."""

    trigger_sweep: Annotated[
        TriggerSweep, Field(description="Trigger sweep mode")
    ]


class TriggerHoldoffResult(TypedDict):
    """Result for trigger holdoff settings."""

    holdoff_time: Annotated[float, Field(description="Trigger holdoff time in seconds")]
    holdoff_time_str: Annotated[
        str, Field(description="Human-readable holdoff time")
    ]


class TriggerNoiseRejectResult(TypedDict):
    """Result for trigger noise rejection settings."""

    noise_reject_enabled: Annotated[
        bool, Field(description="Whether noise rejection is enabled")
    ]


# Action results
class ActionResult(TypedDict):
    """Result for simple action operations."""

    action: Annotated[SystemAction, Field(description="Action performed")]


class WaveformRecordingResult(TypedDict):
    """Result for waveform recording operations."""

    enabled: Annotated[bool, Field(description="Whether recording is enabled")]
    operation: Annotated[RecordingOperation, Field(description="Recording operation state")]
    frames: FrameCountField
    frame_interval: FrameIntervalField
    max_frames: Annotated[int, Field(description="Maximum frames available")]


class ScreenshotResult(TypedDict):
    """Result for screenshot capture operations."""

    file_path: Annotated[
        str, Field(description="File path to the saved screenshot PNG file")
    ]


# Waveform data
class WaveformChannelData(TypedDict):
    """Data for a single channel waveform capture."""

    channel: ChannelNumber
    file_path: Annotated[
        str, Field(description="File path to the saved waveform data JSON file")
    ]
    truncated: Annotated[
        bool,
        Field(
            description="True if any ADC values reached saturation (65535), indicating possible clipping"
        ),
    ]
    # Conversion parameters for voltage calculation: voltage = (raw_value - y_origin - y_reference) * y_increment
    y_increment: Annotated[
        float, Field(description="Vertical increment for raw-to-voltage conversion")
    ]
    y_origin: Annotated[
        float, Field(description="Vertical origin offset for raw-to-voltage conversion")
    ]
    y_reference: Annotated[
        float,
        Field(description="Vertical reference offset for raw-to-voltage conversion"),
    ]
    # Time calculation parameters: time = sample_index * x_increment + x_origin
    x_increment: Annotated[
        float, Field(description="Time increment between samples (seconds)")
    ]
    x_origin: Annotated[float, Field(description="Time origin offset (seconds)")]
    # Channel settings
    vertical_scale: VerticalScaleField
    vertical_offset: VerticalOffsetField
    probe_ratio: ProbeRatioField
    # Acquisition info
    sample_rate: Annotated[float, Field(description="Sample rate in Sa/s")]
    points: Annotated[int, Field(description="Number of data points")]


class WaveformCaptureResult(TypedDict):
    """Result for waveform capture operations including channel data and optional WFM file.

    The WFM file is provided for archival purposes and scientific validation. Use the channel
    JSON files for analysis as they contain parsed data with conversion parameters. The WFM
    file should be preserved as ground truth for future verification or audit trails.
    """

    channels: Annotated[
        List[WaveformChannelData], Field(description="List of captured channel data")
    ]
    wfm_file_path: Annotated[
        Optional[str],
        Field(
            description="File path to the saved WFM file (contains all channels). This is the raw oscilloscope format intended for archival and verification purposes, not primary analysis. Use channel JSON files for data processing. None if WFM save failed."
        ),
    ]


# DVM results
class DVMStatusResult(TypedDict):
    """Result for DVM status queries."""

    enabled: Annotated[bool, Field(description="Whether DVM is enabled")]
    source: Annotated[str, Field(description="Source channel identifier (e.g., 'CHAN1')")]
    channel: ChannelNumber
    mode: Annotated[str, Field(description="User-friendly mode name")]
    mode_description: Annotated[str, Field(description="Human-readable mode description")]
    current_reading: Annotated[
        Optional[float], Field(description="Current voltage reading in volts (only present if enabled)")
    ]
    unit: Annotated[str, Field(description="Measurement unit (V)")]


class DVMConfigureResult(TypedDict):
    """Result for DVM configuration operations."""

    enabled: Annotated[bool, Field(description="Whether DVM is enabled")]
    source: Annotated[str, Field(description="Source channel identifier (e.g., 'CHAN1')")]
    channel: ChannelNumber
    mode: Annotated[str, Field(description="User-friendly mode name")]
    mode_description: Annotated[str, Field(description="Human-readable mode description")]
    current_reading: Annotated[
        Optional[float], Field(description="Current voltage reading in volts (only present if enabled)")
    ]
    unit: Annotated[str, Field(description="Measurement unit (V)")]
    message: Annotated[str, Field(description="Configuration status message")]


# Advanced Trigger Results


class PulseTriggerResult(TypedDict):
    """Result for pulse trigger configuration."""

    trigger_mode: Annotated[Literal["PULSE"], Field(description="Trigger mode (PULSE)")]
    channel: ChannelNumber
    polarity: Annotated[str, Field(description="Pulse polarity (POSITIVE or NEGATIVE)")]
    when: WidthConditionField
    upper_width: UpperWidthLimitField
    lower_width: Annotated[
        Optional[float], Field(description="Lower width limit in seconds (for WITHIN)")
    ]
    level: TriggerLevelField


class SlopeTriggerResult(TypedDict):
    """Result for slope trigger configuration."""

    trigger_mode: Annotated[Literal["SLOPE"], Field(description="Trigger mode (SLOPE)")]
    channel: ChannelNumber
    polarity: Annotated[str, Field(description="Slope direction (POSITIVE or NEGATIVE)")]
    when: TimeConditionField
    upper_time: UpperTimeLimitField
    lower_time: Annotated[
        Optional[float], Field(description="Lower time limit in seconds (for WITHIN)")
    ]
    level_a: StartVoltageLevelField
    level_b: EndVoltageLevelField
    window: Annotated[str, Field(description="Measurement window (TA, TB, or TAB)")]


class VideoTriggerResult(TypedDict):
    """Result for video trigger configuration."""

    trigger_mode: Annotated[Literal["VIDEO"], Field(description="Trigger mode (VIDEO)")]
    channel: ChannelNumber
    polarity: Annotated[str, Field(description="Sync polarity (POSITIVE or NEGATIVE)")]
    mode: Annotated[str, Field(description="Video mode")]
    line_number: Annotated[
        Optional[int], Field(description="Line number (for LINE mode)")
    ]
    standard: Annotated[str, Field(description="Video standard")]
    level: TriggerLevelField


class PatternTriggerResult(TypedDict):
    """Result for pattern trigger configuration."""

    trigger_mode: Annotated[Literal["PATTERN"], Field(description="Trigger mode (PATTERN)")]
    pattern: Annotated[
        List[str], Field(description="4-element pattern (H, L, X, R, or F)")
    ]
    levels: Annotated[
        dict[int, float], Field(description="Trigger levels per channel")
    ]


class RuntTriggerResult(TypedDict):
    """Result for runt trigger configuration."""

    trigger_mode: Annotated[Literal["RUNT"], Field(description="Trigger mode (RUNT)")]
    channel: ChannelNumber
    polarity: Annotated[str, Field(description="Runt pulse direction")]
    when: Annotated[str, Field(description="Width qualification")]
    upper_width: UpperWidthLimitField
    lower_width: LowerWidthLimitField
    level_a: UpperVoltageLevelField
    level_b: LowerVoltageLevelField


class TimeoutTriggerResult(TypedDict):
    """Result for timeout trigger configuration."""

    trigger_mode: Annotated[Literal["TIMEOUT"], Field(description="Trigger mode (TIMEOUT)")]
    channel: ChannelNumber
    slope: Annotated[str, Field(description="Edge to start timeout counter")]
    timeout: TimeoutDurationField
    level: TriggerLevelField


class DurationTriggerResult(TypedDict):
    """Result for duration trigger configuration."""

    trigger_mode: Annotated[Literal["DURATION"], Field(description="Trigger mode (DURATION)")]
    channel: ChannelNumber
    pattern_type: Annotated[str, Field(description="Pattern qualifier")]
    when: Annotated[str, Field(description="Duration condition")]
    upper_width: UpperTimeLimitField
    lower_width: LowerTimeLimitField
    level: TriggerLevelField


class SetupHoldTriggerResult(TypedDict):
    """Result for setup/hold trigger configuration."""

    trigger_mode: Annotated[Literal["SETUP_HOLD"], Field(description="Trigger mode (SETUP_HOLD)")]
    data_channel: ChannelNumber
    clock_channel: ChannelNumber
    clock_slope: Annotated[str, Field(description="Clock edge direction")]
    data_pattern: Annotated[str, Field(description="Expected data value (H or L)")]
    setup_time: SetupTimeField
    hold_time: HoldTimeField
    data_level: DataThresholdField
    clock_level: ClockThresholdField


class NthEdgeTriggerResult(TypedDict):
    """Result for Nth edge trigger configuration."""

    trigger_mode: Annotated[Literal["NTH_EDGE"], Field(description="Trigger mode (NTH_EDGE)")]
    channel: ChannelNumber
    slope: Annotated[str, Field(description="Edge direction to count")]
    idle_time: IdleTimeField
    edge_count: EdgeCountField
    level: TriggerLevelField


class WindowTriggerResult(TypedDict):
    """Result for window trigger configuration."""

    trigger_mode: Annotated[Literal["WINDOW"], Field(description="Trigger mode (WINDOW)")]
    channel: ChannelNumber
    slope: EdgeDirectionField
    position: Annotated[str, Field(description="Trigger position (EXIT, ENTER, or TIME)")]
    time: Annotated[
        Optional[float], Field(description="Duration for TIME position mode")
    ]
    level_a: UpperVoltageLevelField
    level_b: LowerVoltageLevelField


class DelayTriggerResult(TypedDict):
    """Result for delay trigger configuration."""

    trigger_mode: Annotated[Literal["DELAY"], Field(description="Trigger mode (DELAY)")]
    source_a_channel: ChannelNumber
    source_b_channel: ChannelNumber
    slope_a: Annotated[str, Field(description="Source A edge direction")]
    slope_b: Annotated[str, Field(description="Source B edge direction")]
    delay_type: Annotated[str, Field(description="Delay condition")]
    upper_time: UpperTimeLimitField
    lower_time: Annotated[
        Optional[float], Field(description="Lower time limit in seconds (for WITHIN)")
    ]
    level_a: SourceAThresholdField
    level_b: SourceBThresholdField


# Protocol Trigger Results


class RS232TriggerResult(TypedDict):
    """Result for RS232/UART trigger configuration."""

    trigger_mode: Annotated[Literal["RS232"], Field(description="Trigger mode (RS232)")]
    channel: ChannelNumber
    when: Annotated[str, Field(description="Trigger condition")]
    data_value: Annotated[Optional[int], Field(description="Data byte to match (for DATA mode)")]
    baud_rate: BaudRateField
    parity: Annotated[str, Field(description="Parity setting")]
    stop_bits: Annotated[str, Field(description="Stop bit count")]
    data_bits: DataBitsField
    polarity: Annotated[str, Field(description="Signal polarity")]
    level: TriggerLevelField


class I2CTriggerResult(TypedDict):
    """Result for I2C trigger configuration."""

    trigger_mode: Annotated[Literal["I2C"], Field(description="Trigger mode (I2C)")]
    scl_channel: ChannelNumber
    sda_channel: ChannelNumber
    when: Annotated[str, Field(description="Trigger condition")]
    address: Annotated[Optional[int], Field(description="I2C address (for ADDRESS/ADDRESS_DATA modes)")]
    data_value: Annotated[Optional[int], Field(description="Data byte (for DATA/ADDRESS_DATA modes)")]
    address_width: Annotated[str, Field(description="Address width (7 or 10 bits)")]
    direction: Annotated[str, Field(description="Transfer direction")]
    clock_level: ClockThresholdField
    data_level: DataThresholdField


class SPITriggerResult(TypedDict):
    """Result for SPI trigger configuration."""

    trigger_mode: Annotated[Literal["SPI"], Field(description="Trigger mode (SPI)")]
    sclk_channel: ChannelNumber
    miso_channel: Annotated[Optional[int], Field(description="MISO channel")]
    cs_channel: Annotated[Optional[int], Field(description="Chip select channel")]
    clock_slope: Annotated[str, Field(description="Clock edge")]
    when: Annotated[str, Field(description="Trigger condition")]
    timeout: Annotated[Optional[float], Field(description="Timeout duration")]
    data_width: SPIDataWidthField
    data_value: DataValueField
    clock_level: ClockThresholdField
    miso_level: Annotated[Optional[float], Field(description="MISO threshold voltage")]
    cs_level: Annotated[Optional[float], Field(description="CS threshold voltage")]


class CANTriggerResult(TypedDict):
    """Result for CAN trigger configuration."""

    trigger_mode: Annotated[Literal["CAN"], Field(description="Trigger mode (CAN)")]
    channel: ChannelNumber
    baud_rate: BaudRateField
    signal_type: Annotated[str, Field(description="Signal type")]
    when: Annotated[str, Field(description="Trigger condition")]
    sample_point: CANSamplePointField
    frame_type: Annotated[str, Field(description="Frame type")]
    id_type: Annotated[str, Field(description="Identifier type")]
    identifier: Annotated[Optional[int], Field(description="CAN identifier")]
    data_bytes: Annotated[Optional[str], Field(description="Data pattern")]
    level: TriggerLevelField


class LINTriggerResult(TypedDict):
    """Result for LIN trigger configuration."""

    trigger_mode: Annotated[Literal["LIN"], Field(description="Trigger mode (LIN)")]
    channel: ChannelNumber
    standard: Annotated[str, Field(description="LIN version")]
    baud_rate: BaudRateField
    when: Annotated[str, Field(description="Trigger condition")]
    error_type: Annotated[Optional[str], Field(description="Error type (for ERROR mode)")]
    identifier: Annotated[Optional[int], Field(description="LIN identifier")]
    data_bytes: Annotated[Optional[str], Field(description="Data pattern")]
    level: TriggerLevelField


# Bus Decode Results


class ParallelBusResult(TypedDict):
    """Result for parallel bus decode configuration."""

    bus_number: BusNumberField
    bus_mode: Annotated[Literal["PARALLEL"], Field(description="Bus mode (PARALLEL)")]
    bit_assignments: Annotated[dict[int, int], Field(description="Bit position to channel mapping")]
    clock_channel: Annotated[Optional[int], Field(description="Clock channel")]
    width: Annotated[int, Field(description="Bus width in bits")]
    clock_polarity: Annotated[str, Field(description="Clock edge")]
    bit_order: Annotated[str, Field(description="Bit endianness")]


class RS232BusResult(TypedDict):
    """Result for RS232 bus decode configuration."""

    bus_number: BusNumberField
    bus_mode: Annotated[Literal["RS232"], Field(description="Bus mode (RS232)")]
    tx_channel: Annotated[Optional[int], Field(description="TX channel")]
    rx_channel: Annotated[Optional[int], Field(description="RX channel")]
    polarity: Annotated[str, Field(description="Signal polarity")]
    parity: Annotated[str, Field(description="Parity setting")]
    bit_order: Annotated[str, Field(description="Bit endianness")]
    baud_rate: BaudRateField
    data_bits: DataBitsField
    stop_bits: Annotated[str, Field(description="Stop bits")]


class I2CBusResult(TypedDict):
    """Result for I2C bus decode configuration."""

    bus_number: BusNumberField
    bus_mode: Annotated[Literal["I2C"], Field(description="Bus mode (I2C)")]
    scl_channel: ChannelNumber
    sda_channel: ChannelNumber
    address_width: Annotated[str, Field(description="Address width")]


class SPIBusResult(TypedDict):
    """Result for SPI bus decode configuration."""

    bus_number: BusNumberField
    bus_mode: Annotated[Literal["SPI"], Field(description="Bus mode (SPI)")]
    sclk_channel: ChannelNumber
    miso_channel: Annotated[Optional[int], Field(description="MISO channel")]
    mosi_channel: Annotated[Optional[int], Field(description="MOSI channel")]
    ss_channel: Annotated[Optional[int], Field(description="Slave select channel")]
    clock_polarity: Annotated[str, Field(description="Clock polarity")]
    data_bits: DataBitsField
    bit_order: Annotated[str, Field(description="Bit endianness")]
    spi_mode: Annotated[str, Field(description="SPI mode")]
    timeout: Annotated[float, Field(description="Frame timeout")]


class CANBusResult(TypedDict):
    """Result for CAN bus decode configuration."""

    bus_number: BusNumberField
    bus_mode: Annotated[Literal["CAN"], Field(description="Bus mode (CAN)")]
    source_channel: ChannelNumber
    signal_type: Annotated[str, Field(description="Signal type")]
    baud_rate: BaudRateField
    sample_point: CANSamplePointField


class LINBusResult(TypedDict):
    """Result for LIN bus decode configuration."""

    bus_number: BusNumberField
    bus_mode: Annotated[Literal["LIN"], Field(description="Bus mode (LIN)")]
    source_channel: ChannelNumber
    parity: Annotated[str, Field(description="Parity mode")]
    standard: Annotated[str, Field(description="LIN version")]


class BusDisplayResult(TypedDict):
    """Result for bus display settings."""

    bus_number: BusNumberField
    enabled: Annotated[bool, Field(description="Whether bus decode display is enabled")]


class BusFormatResult(TypedDict):
    """Result for bus format settings."""

    bus_number: BusNumberField
    format: Annotated[str, Field(description="Display format")]


class BusDataResult(TypedDict):
    """Result for bus decoded data."""

    bus_number: BusNumberField
    decoded_data: Annotated[str, Field(description="Decoded bus data string")]


class BusExportResult(TypedDict):
    """Result for bus data export operation."""

    bus_number: BusNumberField
    file_path: Annotated[str, Field(description="Local file path where CSV was saved")]
    bytes_downloaded: Annotated[int, Field(description="Number of bytes downloaded")]


# === OSCILLOSCOPE CONNECTION CLASS ===


class RigolDHO824:
    """Class to manage communication with Rigol DHO824 oscilloscope."""

    def __init__(self, resource_string: str, timeout: int = 5000):
        """
        Initialize the oscilloscope connection.

        Args:
            resource_string: VISA resource string for the oscilloscope
            timeout: Communication timeout in milliseconds
        """
        self.rm = pyvisa.ResourceManager()
        self.instrument: Optional[pyvisa.resources.MessageBasedResource] = None
        self.resource_string = resource_string
        self.timeout = timeout
        self._identity = None
        self.lock = asyncio.Lock()
        self.last_connection_error: Optional[str] = None

    @property
    def _instr(self) -> pyvisa.resources.MessageBasedResource:
        """
        Get the instrument resource, asserting it is connected.

        This property allows type-safe access to the instrument without
        needing type: ignore comments everywhere.

        Raises:
            AssertionError: If instrument is not connected
        """
        assert self.instrument is not None, "Instrument not connected"
        return self.instrument

    def _write_checked(self, command: str, raise_on_error: bool = True) -> Optional[str]:
        """
        Write SCPI command and check for errors immediately.

        Sends the command, then queries the error queue. If an error is detected,
        either raises an exception or returns the error string based on raise_on_error.

        Args:
            command: SCPI command to send
            raise_on_error: If True, raise exception on error. If False, return error string.

        Returns:
            None if no error, or error string if raise_on_error=False and error occurred

        Raises:
            Exception: If SCPI error is detected and raise_on_error is True
        """
        self._instr.write(command)
        error_response = self._instr.query(":SYSTem:ERRor?").strip()
        if error_response != '0,"No error"':
            if raise_on_error:
                raise Exception(f"SCPI error after '{command}': {error_response}")
            else:
                return error_response
        return None

    def _query_checked(self, command: str) -> str:
        """
        Query SCPI command and check for errors immediately.

        Sends the query, gets the response, then checks the error queue. If an error
        is detected, raises an exception with the error details.

        Args:
            command: SCPI query command to send

        Returns:
            Response string from the oscilloscope

        Raises:
            Exception: If SCPI error is detected after command execution
        """
        response = self._instr.query(command)
        error_response = self._instr.query(":SYSTem:ERRor?").strip()
        if error_response != '0,"No error"':
            raise Exception(f"SCPI error after '{command}': {error_response}")
        return response

    def _query_binary_values_checked(
        self, command: str, **kwargs
    ) -> Union[Sequence[Union[int, float]], bytes]:
        """
        Query binary values and check for errors immediately.

        Sends the binary query, gets the data, then checks the error queue. If an error
        is detected, raises an exception with the error details.

        Args:
            command: SCPI binary query command to send
            **kwargs: Additional arguments passed to query_binary_values (datatype, container, etc.)

        Returns:
            Binary data from the oscilloscope (sequence of numbers or bytes depending on container)

        Raises:
            Exception: If SCPI error is detected after command execution
        """
        response = self._instr.query_binary_values(command, **kwargs)
        error_response = self._instr.query(":SYSTem:ERRor?").strip()
        if error_response != '0,"No error"':
            raise Exception(f"SCPI error after '{command}': {error_response}")
        return response  # type: ignore[return-value]

    def _disable_ultra_conflicting_features(self) -> None:
        """
        Disable features that conflict with Ultra Acquisition mode.

        Ultra Acquisition requires these features to be disabled:
        - Cursor measurement
        - Protocol decoding (all buses)
        - Search function
        - Zoom (delayed sweep)
        - Pass/Fail test
        - Waveform recording
        - Roll/XY timebase modes (must be MAIN)

        Note: Uses best-effort approach - errors are ignored if features are
        already disabled or unavailable.
        """
        # Disable cursor
        self._write_checked(":CURSor:MODE OFF", raise_on_error=False)

        # Disable all decoding buses (BUS1-4)
        for bus in range(1, 5):
            self._write_checked(f":BUS{bus}:DISPlay 0", raise_on_error=False)

        # Disable search
        self._write_checked(":SEARch:STATe 0", raise_on_error=False)

        # Disable zoom (delayed sweep)
        self._write_checked(":TIMebase:DELay:ENABle 0", raise_on_error=False)

        # Disable pass/fail test
        self._write_checked(":MASK:ENABle 0", raise_on_error=False)

        # Disable waveform recording
        self._write_checked(":RECord:WRECord:ENABle 0", raise_on_error=False)

        # Set timebase to MAIN (not ROLL or XY)
        self._write_checked(":TIMebase:MODE MAIN", raise_on_error=False)

    def connect(self) -> bool:
        """
        Connect to the oscilloscope.

        Returns:
            True if connection successful, False otherwise
        """
        # Clear any previous error
        self.last_connection_error = None

        # If already connected, test if connection is still alive
        if self.instrument is not None:
            try:
                # Test if connection is still alive with a simple query
                self._instr.query("*OPC?")
                # self._instr.write('*OPC')
                return True
            except Exception as e:
                # Connection is dead, proceed to reconnect
                print("Connection dead")
                self.disconnect()

        print("Opening up new connection")
        try:
            # Use provided resource string
            try:
                self.instrument = cast(
                    pyvisa.resources.MessageBasedResource,
                    self.rm.open_resource(
                        self.resource_string,
                        access_mode=pyvisa.constants.AccessModes.exclusive_lock,  # type: ignore[reportAttributeAccessIssue]
                    ),
                )
            except Exception as e:
                self.last_connection_error = f"Failed to open resource '{self.resource_string}': {str(e)}"
                return False

            self._instr.timeout = self.timeout

            # Set proper termination characters for SCPI communication
            self._instr.read_termination = "\n"
            self._instr.write_termination = "\n"

            # Clear the instrument's input and output buffers
            # self._instr.clear()

            # Ensure synchronization - wait for all operations to complete
            self._instr.write("*OPC")

            # Test connection and cache identity
            try:
                self._identity = self._instr.query("*IDN?").strip()
            except Exception as e:
                self.last_connection_error = f"Connected to device but failed to query identity: {str(e)}"
                self.disconnect()
                return False

            return True

        except Exception as e:
            # Catch-all for any unexpected errors
            self.last_connection_error = f"Unexpected error during connection: {str(e)}"
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
                self._identity = self._instr.query("*IDN?").strip()
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
        parts = identity.split(",")
        if len(parts) >= 4:
            return {
                "manufacturer": parts[0],
                "model": parts[1],
                "serial": parts[2],
                "version": parts[3],
            }
        return None

    def extract_ip_from_resource(self) -> Optional[str]:
        """
        Extract IP address from VISA resource string.

        Returns:
            IP address string or None if not a TCPIP resource
        """
        if self.resource_string and "TCPIP" in self.resource_string:
            # Format: TCPIP0::192.168.44.37::inst0::INSTR
            parts = self.resource_string.split("::")
            if len(parts) >= 2:
                return parts[1]
        return None

    def download_file_via_ftp(
        self, ip_address: str, scope_filename: str, local_filepath: str
    ) -> bool:
        """
        Download file from oscilloscope via FTP with hash verification.

        Downloads the file twice to memory buffers and verifies MD5 hashes match
        before writing to disk. This ensures data integrity during transfer.

        Args:
            ip_address: IP address of oscilloscope
            scope_filename: Filename on the scope (without path, assumes C:/)
            local_filepath: Local file path to save downloaded file

        Returns:
            True if download successful and hashes match, False otherwise
        """
        try:
            # Connect to FTP server
            ftp = FTP()
            ftp.connect(ip_address, 21, timeout=30)
            ftp.login("anonymous", "")

            # List files to verify
            files = ftp.nlst()

            if scope_filename not in files:
                ftp.quit()
                return False

            # First download to memory
            buffer1 = io.BytesIO()
            ftp.retrbinary(f"RETR {scope_filename}", buffer1.write)
            buffer1.seek(0)
            hash1 = hashlib.md5(buffer1.read()).hexdigest()
            buffer1.seek(0)

            # Second download to memory
            buffer2 = io.BytesIO()
            ftp.retrbinary(f"RETR {scope_filename}", buffer2.write)
            buffer2.seek(0)
            hash2 = hashlib.md5(buffer2.read()).hexdigest()
            buffer2.seek(0)

            # Verify hashes match
            if hash1 != hash2:
                # Hashes don't match - corruption detected, don't delete from scope
                ftp.quit()
                return False

            # Hashes match - write to disk
            with open(local_filepath, "wb") as f:
                f.write(buffer1.read())

            # Delete file from scope after successful download and verification
            try:
                ftp.delete(scope_filename)
            except:
                pass  # Some configurations don't allow deletion

            ftp.quit()
            return True

        except Exception:
            # FTP failed (not on network, USB connection, etc.) - fail gracefully
            return False

    def dvm_enable(self, enabled: bool) -> None:
        """Enable or disable the Digital Voltmeter."""
        cmd = f":DVM:ENABle {'ON' if enabled else 'OFF'}"
        self._instr.write(cmd)

    def dvm_is_enabled(self) -> bool:
        """Query if DVM is enabled."""
        response = self._instr.query(":DVM:ENABle?")
        return response.strip() == "1"

    def dvm_set_source(self, channel: int) -> None:
        """Set DVM source channel (1-4)."""
        if channel not in [1, 2, 3, 4]:
            raise ValueError(f"Channel must be 1-4, got {channel}")
        cmd = f":DVM:SOURce CHANnel{channel}"
        self._instr.write(cmd)

    def dvm_get_source(self) -> str:
        """Query DVM source channel.

        Returns:
            SCPI channel name (e.g., 'CHAN1', 'CHAN2')
        """
        response = self._instr.query(":DVM:SOURce?")
        return response.strip()

    def dvm_set_mode(self, mode: DVMMode) -> None:
        """Set DVM measurement mode."""
        cmd = f":DVM:MODE {mode.value}"
        self._instr.write(cmd)

    def dvm_get_mode(self) -> DVMMode:
        """Query DVM measurement mode."""
        response = self._instr.query(":DVM:MODE?")
        mode_str = response.strip()
        return DVMMode(mode_str)

    def dvm_get_current_reading(self) -> float:
        """Get current DVM voltage reading.

        Returns:
            Voltage reading in volts
        """
        response = self._instr.query(":DVM:CURRent?")
        return float(response.strip())


def create_server(temp_dir: str, client_temp_dir: Optional[str] = None) -> FastMCP:
    """Create the FastMCP server with oscilloscope tools.

    Args:
        temp_dir: Path to temporary directory for storing waveforms and screenshots (internal)
        client_temp_dir: Optional path prefix for translating returned file paths to client-facing paths.
                        Used in container mode to translate container paths to host paths.
    """

    # Load environment variables
    load_dotenv()

    # Get configuration from environment
    resource_string = os.getenv("RIGOL_RESOURCE")
    if not resource_string:
        raise ValueError(
            "RIGOL_RESOURCE environment variable is required. "
            "Set it to your oscilloscope's VISA resource string (e.g., 'TCPIP::192.168.1.100::INSTR')"
        )

    timeout = int(os.getenv("VISA_TIMEOUT", "30000"))
    beeper_enabled = os.getenv("RIGOL_BEEPER_ENABLED", "false").lower() in ("true", "1", "yes")

    # Create MCP server
    mcp = FastMCP("rigol-dho824", stateless_http=True)

    # Create oscilloscope instance
    scope = RigolDHO824(resource_string, timeout)

    # === PATH TRANSLATION FOR CONTAINER MODE ===

    # Normalize temp_dir and client_temp_dir to absolute paths
    temp_dir_abs = os.path.abspath(temp_dir)
    client_temp_dir_abs = os.path.abspath(client_temp_dir) if client_temp_dir else None

    def to_client_path(path: Optional[str]) -> Optional[str]:
        """Translate internal file paths to client-facing paths.

        If client_temp_dir is configured and the path is under temp_dir,
        replace the temp_dir prefix with client_temp_dir.

        Args:
            path: File path to translate (or None)

        Returns:
            Translated path, or original path if translation not applicable
        """
        if path is None:
            return None

        if client_temp_dir_abs is None:
            return path

        # Normalize the input path to absolute
        abs_path = os.path.abspath(path)

        # Check if the path is under temp_dir
        if abs_path.startswith(temp_dir_abs + os.sep) or abs_path == temp_dir_abs:
            # Get the relative path from temp_dir
            rel_path = os.path.relpath(abs_path, temp_dir_abs)

            # Build the client-facing path
            return os.path.join(client_temp_dir_abs, rel_path)

        # Path is not under temp_dir, return unchanged
        return path

    # === DECORATOR FOR SCOPE CONNECTION AND LOCKING ===

    def with_scope_connection(func):
        """
        Decorator that handles scope connection, locking, and cleanup for tool functions.

        This decorator:
        1. Acquires the asyncio lock to ensure single-threaded access to the scope
        2. Connects to the oscilloscope (raises exception if connection fails)
        3. Locks the front panel and optionally enables beeper for remote operation (if RIGOL_BEEPER_ENABLED=true)
        4. Executes the tool function
        5. Restores panel control and optionally disables beeper
        6. Disconnects and releases the lock in the finally block
        """

        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            async with scope.lock:
                if not scope.connect():
                    error_detail = scope.last_connection_error or "Unknown error"
                    raise Exception(
                        f"Failed to connect to oscilloscope at '{scope.resource_string}'. "
                        f"Details: {error_detail}"
                    )
                # Clear any leftover errors from previous operations
                scope._write_checked("*CLS")

                # Lock panel and optionally enable beeper during remote operation
                scope._write_checked(":SYSTem:LOCKed ON")
                if beeper_enabled:
                    scope._write_checked(":SYSTem:BEEPer ON")

                try:
                    result = await func(*args, **kwargs)
                    return result
                finally:
                    # Restore panel control and disable beeper before disconnect
                    # Use _instr directly to avoid masking errors from the main function
                    if beeper_enabled:
                        try:
                            scope._instr.write(":SYSTem:BEEPer OFF")
                        except Exception:
                            pass  # Best effort cleanup
                    try:
                        scope._instr.write(":SYSTem:LOCKed OFF")
                    except Exception:
                        pass  # Best effort cleanup
                    scope.disconnect()

        return wrapper

    # === HELPER FUNCTIONS FOR ENUM MAPPING ===

    def map_trigger_status(raw_status: str) -> TriggerStatus:
        """Map raw trigger status to enum."""
        status_map = {
            "TD": TriggerStatus.TRIGGERED,
            "WAIT": TriggerStatus.WAITING,
            "RUN": TriggerStatus.RUNNING,
            "AUTO": TriggerStatus.AUTO,
            "STOP": TriggerStatus.STOPPED,
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

    def map_coupling_mode(raw_coupling: str) -> ChannelCoupling:
        """Map raw coupling mode to user-facing string (AC/DC/GND)."""
        coupling = raw_coupling.upper()
        if coupling in ["AC", "DC", "GND"]:
            return coupling  # type: ignore[return-value]
        return "GND"

    def map_acquisition_type(raw_type: str) -> AcquisitionType:
        """Map raw acquisition type to enum."""
        type_map = {
            "NORM": AcquisitionType.NORMAL,
            "AVER": AcquisitionType.AVERAGE,
            "PEAK": AcquisitionType.PEAK,
            "ULTR": AcquisitionType.ULTRA,
        }
        return type_map.get(raw_type, AcquisitionType.NORMAL)

    def map_trigger_mode(raw_mode: str) -> TriggerMode:
        """Map SCPI trigger mode response to TriggerMode enum."""
        for tm in TriggerMode:
            if raw_mode == tm.value or raw_mode == tm.value[:4].upper():
                return tm
        return TriggerMode.EDGE

    def _parse_channel_from_scpi(scpi_source: str) -> int:
        """Convert SCPI source (e.g., 'CHAN1') to channel number (1)."""
        channel_map = {
            "CHAN1": 1,
            "CHAN2": 2,
            "CHAN3": 3,
            "CHAN4": 4,
        }
        return channel_map.get(scpi_source, 1)

    # === IDENTITY TOOLS ===

    @mcp.tool
    @with_scope_connection
    async def get_model_number() -> ModelNumberResult:
        """
        Get the model number of the connected Rigol oscilloscope.

        Returns the model identifier (e.g., 'DHO824') from the oscilloscope's
        identity string.
        """
        identity_parts = scope.parse_identity()
        if not identity_parts:
            raise Exception("Failed to parse oscilloscope identity")

        return ModelNumberResult(model=identity_parts["model"])

    @mcp.tool
    @with_scope_connection
    async def get_software_version() -> SoftwareVersionResult:
        """
        Get the software/firmware version of the connected Rigol oscilloscope.

        Returns the software version string from the oscilloscope's
        identity information.
        """
        identity_parts = scope.parse_identity()
        if not identity_parts:
            raise Exception("Failed to parse oscilloscope identity")

        return SoftwareVersionResult(version=identity_parts["version"])

    @mcp.tool
    @with_scope_connection
    async def get_serial_number() -> SerialNumberResult:
        """
        Get the serial number of the connected Rigol oscilloscope.

        Returns the unique serial number identifier from the oscilloscope's
        identity string.
        """
        identity_parts = scope.parse_identity()
        if not identity_parts:
            raise Exception("Failed to parse oscilloscope identity")

        return SerialNumberResult(serial=identity_parts["serial"])

    # === WAVEFORM CAPTURE TOOLS ===

    @mcp.tool
    @with_scope_connection
    async def capture_waveform(
        ctx: Context,
        channels: Annotated[
            List[ChannelNumber],
            Field(
                description="List of channels to capture (1-4)", examples=[[1], [1, 2]]
            ),
        ] = [1],
    ) -> WaveformCaptureResult:
        """
        Capture raw waveform data from specified channels.

        Captures data in RAW mode with WORD format (16-bit) for maximum accuracy.
        Reads all available points from oscilloscope memory (up to 50M points depending on settings).
        Uses chunked reading with progress reporting for large data transfers.
        Saves waveform data to temporary JSON files and returns file paths along with all parameters needed for voltage conversion.
        Also attempts to capture WFM file (contains all channels) via FTP if network connection is available.
        The 'truncated' field indicates if any ADC values reached saturation (65535),
        which suggests the signal may be clipped and vertical scale adjustment may be needed.

        The WFM file is captured for long-term archival and serves as immutable ground truth
        for scientific reproducibility. Use the channel JSON files for analysis and processing,
        as they include parsed data and conversion parameters. Preserve the WFM file for future
        verification, auditing, or reprocessing with different tools.

        Voltage conversion formula: voltage = (raw_value - y_origin - y_reference) * y_increment
        Time calculation formula: time = sample_index * x_increment + x_origin
        """
        # Generate unique capture ID based on timestamp
        capture_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[
            :-3
        ]  # Include milliseconds

        # Create subdirectory for this capture
        capture_dir = tempfile.mkdtemp(prefix=f"waveform_capture_{capture_id}_", dir=temp_dir)

        results = []

        # Stop acquisition once for all channels
        scope._write_checked(":STOP")
        scope._query_checked("*OPC?")  # Wait for stop to complete

        for channel_idx, channel in enumerate(channels):
            # Check if channel is enabled
            channel_enabled = int(scope._query_checked(f":CHAN{channel}:DISP?"))
            if not channel_enabled:
                await ctx.report_progress(
                    progress=(channel_idx + 1) / len(channels),
                    message=f"Channel {channel} is disabled, skipping",
                )
                continue

            try:
                # Set source channel
                scope._write_checked(f":WAV:SOUR CHAN{channel}")

                # Configure for RAW mode with WORD format (16-bit)
                scope._write_checked(":WAV:MODE RAW")
                scope._write_checked(":WAV:FORM WORD")

                # Query memory depth to determine available points
                memory_depth = float(scope._query_checked(":ACQ:MDEP?"))
                max_points = int(memory_depth)

                # Adjust timeout based on memory depth
                # Estimate: 100ms per 100k points + 10s buffer
                if memory_depth > 1000000:  # >1M points
                    new_timeout = int((memory_depth / 100000) * 100 + 10000)
                    scope._instr.timeout = new_timeout

                # Query waveform parameters for conversion (before data transfer)
                y_increment = float(scope._query_checked(":WAV:YINC?"))
                y_origin = float(scope._query_checked(":WAV:YOR?"))
                y_reference = float(scope._query_checked(":WAV:YREF?"))
                x_increment = float(scope._query_checked(":WAV:XINC?"))
                x_origin = float(scope._query_checked(":WAV:XOR?"))

                # Query channel settings
                vertical_scale = float(scope._query_checked(f":CHAN{channel}:SCAL?"))
                vertical_offset = float(scope._query_checked(f":CHAN{channel}:OFFS?"))
                probe_ratio = float(scope._query_checked(f":CHAN{channel}:PROB?"))

                # Query sample rate
                sample_rate = float(scope._query_checked(":ACQ:SRAT?"))

                # Chunked reading for large data
                chunk_size = 10000  # 10k points per chunk
                raw_data = []

                if max_points > chunk_size:
                    # Use chunked reading with progress reporting
                    num_chunks = (max_points + chunk_size - 1) // chunk_size

                    for chunk_idx in range(num_chunks):
                        start = chunk_idx * chunk_size + 1
                        end = min(start + chunk_size - 1, max_points)

                        # Report progress
                        base_progress = channel_idx / len(channels)
                        chunk_progress = (chunk_idx / num_chunks) / len(channels)
                        await ctx.report_progress(
                            progress=base_progress + chunk_progress,
                            message=f"Channel {channel}: Reading points {start:,} to {end:,} of {max_points:,}",
                        )

                        # Set chunk range
                        scope._write_checked(f":WAV:STAR {start}")
                        scope._write_checked(f":WAV:STOP {end}")

                        # Read chunk
                        chunk_data = scope._query_binary_values_checked(
                            ":WAV:DATA?",
                            datatype="H",  # Unsigned 16-bit
                            is_big_endian=False,
                        )
                        raw_data.extend(chunk_data)
                else:
                    # Small data, read all at once
                    await ctx.report_progress(
                        progress=(channel_idx + 0.5) / len(channels),
                        message=f"Channel {channel}: Reading {max_points:,} points",
                    )

                    scope._write_checked(":WAV:STAR 1")
                    scope._write_checked(f":WAV:STOP {max_points}")

                    raw_data = scope._query_binary_values_checked(
                        ":WAV:DATA?",
                        datatype="H",  # Unsigned 16-bit
                        is_big_endian=False,
                    )

                # Check for ADC saturation (65535 is max value for 16-bit unsigned)
                truncated = bool(np.max(raw_data) == 65535) if raw_data else False

                await ctx.report_progress(
                    progress=(channel_idx + 1) / len(channels),
                    message=f"Channel {channel}: Completed ({len(raw_data):,} points)",
                )

                # Create waveform data structure
                # Fields ordered logically: identification, status, acquisition metadata,
                # Y-axis scaling, X-axis scaling, data size and content (raw_data always last)
                waveform_data = {
                    "channel": channel,
                    "truncated": truncated,
                    "sample_rate": sample_rate,
                    "y_increment": y_increment,
                    "y_origin": y_origin,
                    "y_reference": y_reference,
                    "vertical_scale": vertical_scale,
                    "vertical_offset": vertical_offset,
                    "probe_ratio": probe_ratio,
                    "x_increment": x_increment,
                    "x_origin": x_origin,
                    "points": len(raw_data),
                }
                # Always put raw_data last so tools like 'head' show metadata first
                waveform_data["raw_data"] = raw_data  # List of raw ADC values

                # Save waveform data to JSON file in capture directory
                file_path = os.path.join(capture_dir, f"ch{channel}.json")

                with open(file_path, 'w') as f:
                    json.dump(waveform_data, f, indent=2)

                # Return metadata with file path
                # Fields ordered to match waveform_data structure
                result_data: WaveformChannelData = {
                    "channel": channel,
                    "truncated": truncated,
                    "sample_rate": sample_rate,
                    "y_increment": y_increment,
                    "y_origin": y_origin,
                    "y_reference": y_reference,
                    "vertical_scale": vertical_scale,
                    "vertical_offset": vertical_offset,
                    "probe_ratio": probe_ratio,
                    "x_increment": x_increment,
                    "x_origin": x_origin,
                    "points": len(raw_data),
                    "file_path": to_client_path(file_path) or file_path,
                }

                results.append(result_data)

            except Exception as e:
                await ctx.report_progress(
                    progress=(channel_idx + 1) / len(channels),
                    message=f"Channel {channel}: Error - {str(e)}",
                )
                continue

        # Capture WFM file for future-proofing and scientific accuracy
        # WFM contains all enabled channels in a single file
        wfm_saved_path: Optional[str] = None

        # Generate random 8-char lowercase hex filename to avoid overwriting
        wfm_filename = f"{os.urandom(4).hex()}.wfm"
        wfm_scope_path = f"C:/{wfm_filename}"
        wfm_local_path = os.path.join(capture_dir, "data.wfm")

        # Try to save and download WFM via FTP (gracefully skip if FTP unavailable)
        try:
            await ctx.report_progress(
                progress=1.0, message="Saving WFM file on scope..."
            )

            # Enable file overwriting
            scope._write_checked(":SAVE:OVER ON")

            # Save memory waveform to scope
            scope._write_checked(f":SAVE:MEMory:WAVeform {wfm_scope_path}")
            await asyncio.sleep(5)  # Wait for save to complete

            # Check save status
            scope._query_checked(":SAVE:STATus?")

            # Try to download via FTP
            ip_address = scope.extract_ip_from_resource()
            if ip_address:
                await ctx.report_progress(
                    progress=1.0, message="Downloading WFM file via FTP..."
                )
                if scope.download_file_via_ftp(ip_address, wfm_filename, wfm_local_path):
                    wfm_saved_path = wfm_local_path
                    await ctx.report_progress(
                        progress=1.0, message=f"WFM file saved: {to_client_path(wfm_local_path)}"
                    )
                else:
                    await ctx.report_progress(
                        progress=1.0,
                        message="WFM download failed (FTP unavailable) - skipping",
                    )
            else:
                await ctx.report_progress(
                    progress=1.0,
                    message="WFM download skipped (not a network connection)",
                )

        except Exception as e:
            # WFM capture failed - report but don't fail the whole operation
            await ctx.report_progress(
                progress=1.0, message=f"WFM capture skipped: {str(e)}"
            )

        return WaveformCaptureResult(channels=results, wfm_file_path=to_client_path(wfm_saved_path))

    # === CHANNEL CONTROL TOOLS ===

    @mcp.tool
    @with_scope_connection
    async def set_channel_enable(
        channel: ChannelNumber,
        enabled: Annotated[bool, Field(description="True to enable, False to disable")],
    ) -> ChannelEnableResult:
        """
        Enable or disable a channel display.
        """
        state = "ON" if enabled else "OFF"
        scope._write_checked(f":CHAN{channel}:DISP {state}")

        # Verify the setting
        actual_state = int(scope._query_checked(f":CHAN{channel}:DISP?"))

        return ChannelEnableResult(channel=channel, enabled=bool(actual_state))

    @mcp.tool
    @with_scope_connection
    async def set_channel_coupling(
        channel: ChannelNumber,
        coupling: Annotated[
            ChannelCoupling, Field(description="Coupling mode: AC, DC, or GND")
        ],
    ) -> ChannelCouplingResult:
        """
        Set channel coupling mode.
        """
        # Use enum value directly
        scope._write_checked(f":CHAN{channel}:COUP {coupling}")

        # Verify the setting
        actual_coupling = scope._query_checked(f":CHAN{channel}:COUP?").strip()

        return ChannelCouplingResult(
            channel=channel, coupling=map_coupling_mode(actual_coupling)
        )

    @mcp.tool
    @with_scope_connection
    async def set_channel_probe(
        channel: ChannelNumber, probe_ratio: ProbeRatioField
    ) -> ChannelProbeResult:
        """
        Set channel probe attenuation ratio.
        """
        # Format as integer if it's a whole number, otherwise as float
        probe_value = (
            int(probe_ratio) if float(probe_ratio).is_integer() else float(probe_ratio)
        )
        scope._write_checked(f":CHAN{channel}:PROB {probe_value}")

        # Verify the setting
        actual_ratio = float(scope._query_checked(f":CHAN{channel}:PROB?"))

        return ChannelProbeResult(channel=channel, probe_ratio=actual_ratio)

    @mcp.tool
    @with_scope_connection
    async def set_channel_bandwidth(
        channel: ChannelNumber,
        bandwidth_limit: Annotated[
            Optional[Literal["OFF", "20MHz"]],
            Field(description="Bandwidth limit: OFF or 20MHz. Default is OFF"),
        ] = None,
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
        """
        if bandwidth_limit is None:
            bandwidth_limit = "OFF"

        # Map user-friendly value to SCPI
        bw_value = "20M" if bandwidth_limit == "20MHz" else "OFF"
        scope._write_checked(f":CHAN{channel}:BWL {bw_value}")

        # Verify the setting
        actual_bw = scope._query_checked(f":CHAN{channel}:BWL?").strip()

        # Map response to enum
        result_bw = "20MHz" if actual_bw == "20M" else "OFF"

        return ChannelBandwidthResult(channel=channel, bandwidth_limit=result_bw)

    @mcp.tool
    @with_scope_connection
    async def get_channel_status(channel: ChannelNumber) -> ChannelStatusResult:
        """
        Get comprehensive channel status and settings.
        """
        # Query all channel settings
        enabled = bool(int(scope._query_checked(f":CHAN{channel}:DISP?")))
        coupling = scope._query_checked(f":CHAN{channel}:COUP?").strip()
        probe_ratio = float(scope._query_checked(f":CHAN{channel}:PROB?"))
        bw_limit = scope._query_checked(f":CHAN{channel}:BWL?").strip()
        vertical_scale = float(scope._query_checked(f":CHAN{channel}:SCAL?"))
        vertical_offset = float(scope._query_checked(f":CHAN{channel}:OFFS?"))
        invert = bool(int(scope._query_checked(f":CHAN{channel}:INV?")))
        units = scope._query_checked(f":CHAN{channel}:UNIT?").strip()

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
            units=units,
        )

    # === PRIORITY 1: CHANNEL SETTINGS ===

    @mcp.tool
    @with_scope_connection
    async def set_channel_invert(
        channel: ChannelNumber,
        inverted: Annotated[bool, Field(description="Boolean to invert")]
    ) -> ChannelInvertResult:
        """
        Invert channel waveform display (multiply by -1).
        """
        scope._write_checked(f":CHAN{channel}:INV {'ON' if inverted else 'OFF'}")

        # Verify the setting
        actual_invert = bool(int(scope._query_checked(f":CHAN{channel}:INV?")))

        return ChannelInvertResult(channel=channel, inverted=actual_invert)

    @mcp.tool
    @with_scope_connection
    async def set_channel_label(
        channel: ChannelNumber,
        label: ChannelLabelField
    ) -> ChannelLabelResult:
        """
        Set custom channel label text.
        """
        scope._write_checked(f':CHAN{channel}:LAB:CONT "{label}"')

        # Verify the setting
        actual_label = scope._query_checked(f":CHAN{channel}:LAB:CONT?").strip().strip('"')

        return ChannelLabelResult(channel=channel, label=actual_label)

    @mcp.tool
    @with_scope_connection
    async def set_channel_label_visible(
        channel: ChannelNumber,
        visible: Annotated[bool, Field(description="Boolean to show/hide")]
    ) -> ChannelLabelVisibilityResult:
        """
        Show or hide custom channel label.
        """
        scope._write_checked(f":CHAN{channel}:LAB:SHOW {'ON' if visible else 'OFF'}")

        # Verify the setting
        actual_visible = bool(int(scope._query_checked(f":CHAN{channel}:LAB:SHOW?")))

        return ChannelLabelVisibilityResult(channel=channel, visible=actual_visible)

    @mcp.tool
    @with_scope_connection
    async def set_channel_units(
        channel: ChannelNumber,
        units: Annotated[ChannelUnits, Field(description='Unit type ("VOLT", "WATT", "AMPERE", "UNKNOWN")')]
    ) -> ChannelUnitsResult:
        """
        Set voltage display units for channel.
        """
        scope._write_checked(f":CHAN{channel}:UNIT {units.value}")

        # Verify the setting
        actual_units_str = scope._query_checked(f":CHAN{channel}:UNIT?").strip()

        # Map SCPI response to enum
        units_map = {
            "VOLT": ChannelUnits.VOLT,
            "WATT": ChannelUnits.WATT,
            "AMP": ChannelUnits.AMPERE,
            "UNKN": ChannelUnits.UNKNOWN,
        }
        actual_units = units_map.get(actual_units_str[:4], ChannelUnits.VOLT)

        return ChannelUnitsResult(channel=channel, units=actual_units)

    # === SCALE ADJUSTMENT TOOLS ===

    @mcp.tool
    @with_scope_connection
    async def set_vertical_scale(
        channel: ChannelNumber, vertical_scale: VerticalScaleField
    ) -> VerticalScaleResult:
        """
        Set channel vertical scale (V/div).
        """
        scope._write_checked(f":CHAN{channel}:SCAL {vertical_scale}")

        # Verify the setting
        actual_scale = float(scope._query_checked(f":CHAN{channel}:SCAL?"))

        return VerticalScaleResult(
            channel=channel, vertical_scale=actual_scale, units="V/div"
        )

    @mcp.tool
    @with_scope_connection
    async def set_vertical_offset(
        channel: ChannelNumber, vertical_offset: VerticalOffsetField
    ) -> VerticalOffsetResult:
        """
        Set channel vertical offset.
        """
        scope._write_checked(f":CHAN{channel}:OFFS {vertical_offset}")

        # Verify the setting
        actual_offset = float(scope._query_checked(f":CHAN{channel}:OFFS?"))

        return VerticalOffsetResult(
            channel=channel, vertical_offset=actual_offset, units="V"
        )

    @mcp.tool
    @with_scope_connection
    async def set_timebase_scale(
        time_per_div: Annotated[
            float, Field(description="Time per division in seconds")
        ]
    ) -> TimebaseScaleResult:
        """
        Set horizontal timebase scale.
        """
        scope._write_checked(f":TIM:MAIN:SCAL {time_per_div}")

        # Verify the setting
        actual_scale = float(scope._query_checked(":TIM:MAIN:SCAL?"))

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
            time_per_div=actual_scale, time_per_div_str=scale_str
        )

    @mcp.tool
    @with_scope_connection
    async def set_timebase_offset(time_offset: TimeOffsetField) -> TimebaseOffsetResult:
        """
        Set horizontal timebase offset.
        """
        scope._write_checked(f":TIM:MAIN:OFFS {time_offset}")

        # Verify the setting
        actual_offset = float(scope._query_checked(":TIM:MAIN:OFFS?"))

        return TimebaseOffsetResult(time_offset=actual_offset, units="s")

    # === PRIORITY 1: TIMEBASE SETTINGS ===

    @mcp.tool
    @with_scope_connection
    async def set_timebase_mode(
        mode: Annotated[TimebaseMode, Field(description='Timebase mode ("MAIN", "XY", "ROLL")')]
    ) -> TimebaseModeResult:
        """
        Set timebase display mode.

        - **MAIN**: Normal YT mode
        - **XY**: Lissajous/XY mode (Ch1 = X axis, Ch2 = Y axis)
        - **ROLL**: Slow sweep roll mode (for low frequencies)
        """
        scope._write_checked(f":TIM:MODE {mode.value}")

        # Verify the setting
        actual_mode_str = scope._query_checked(":TIM:MODE?").strip()

        # Map SCPI response to enum
        mode_map = {
            "MAIN": TimebaseMode.MAIN,
            "XY": TimebaseMode.XY,
            "ROLL": TimebaseMode.ROLL,
        }
        actual_mode = mode_map.get(actual_mode_str, TimebaseMode.MAIN)

        return TimebaseModeResult(mode=actual_mode)

    @mcp.tool
    @with_scope_connection
    async def enable_delayed_timebase(
        enabled: Annotated[bool, Field(description="Boolean to enable zoom window")]
    ) -> DelayedTimebaseEnableResult:
        """
        Enable or disable delayed/zoom timebase (zoomed window).
        """
        scope._write_checked(f":TIM:DEL:ENAB {'ON' if enabled else 'OFF'}")

        # Verify the setting
        actual_enabled = bool(int(scope._query_checked(":TIM:DEL:ENAB?")))

        return DelayedTimebaseEnableResult(enabled=actual_enabled)

    @mcp.tool
    @with_scope_connection
    async def set_delayed_timebase_scale(
        time_per_div: DelayedTimeScaleField
    ) -> DelayedTimebaseScaleResult:
        """
        Set zoom window horizontal scale (time/div).

        Must enable delayed timebase first with enable_delayed_timebase(True).
        """
        scope._write_checked(f":TIM:DEL:SCAL {time_per_div}")

        # Verify the setting
        actual_scale = float(scope._query_checked(":TIM:DEL:SCAL?"))

        # Convert to human-readable format
        if actual_scale >= 1:
            scale_str = f"{actual_scale:.2f} s/div"
        elif actual_scale >= 1e-3:
            scale_str = f"{actual_scale*1e3:.2f} ms/div"
        elif actual_scale >= 1e-6:
            scale_str = f"{actual_scale*1e6:.2f} μs/div"
        else:
            scale_str = f"{actual_scale*1e9:.2f} ns/div"

        return DelayedTimebaseScaleResult(
            time_per_div=actual_scale,
            time_per_div_str=scale_str
        )

    @mcp.tool
    @with_scope_connection
    async def set_delayed_timebase_offset(
        time_offset: DelayedTimeOffsetField
    ) -> DelayedTimebaseOffsetResult:
        """
        Set zoom window horizontal position.

        Must enable delayed timebase first with enable_delayed_timebase(True).
        """
        scope._write_checked(f":TIM:DEL:OFFS {time_offset}")

        # Verify the setting
        actual_offset = float(scope._query_checked(":TIM:DEL:OFFS?"))

        return DelayedTimebaseOffsetResult(time_offset=actual_offset, units="s")

    # === ACQUISITION CONTROL TOOLS ===

    @mcp.tool
    @with_scope_connection
    async def run_acquisition() -> AcquisitionStatusResult:
        """
        Start continuous acquisition (RUN mode).
        """
        scope._write_checked(":RUN")

        # Give it a moment to start
        await asyncio.sleep(0.1)

        # Check trigger status
        status = scope._query_checked(":TRIG:STAT?").strip()

        return AcquisitionStatusResult(
            action=AcquisitionAction.RUN, trigger_status=map_trigger_status(status)
        )

    @mcp.tool
    @with_scope_connection
    async def stop_acquisition() -> AcquisitionStatusResult:
        """
        Stop acquisition (STOP mode).
        """
        scope._write_checked(":STOP")

        # Give it a moment to stop
        await asyncio.sleep(0.1)

        # Check trigger status
        status = scope._query_checked(":TRIG:STAT?").strip()

        return AcquisitionStatusResult(
            action=AcquisitionAction.STOP, trigger_status=map_trigger_status(status)
        )

    @mcp.tool
    @with_scope_connection
    async def single_acquisition() -> AcquisitionStatusResult:
        """
        Perform single acquisition (SINGLE mode).
        """
        scope._write_checked(":SING")

        # Give it a moment to arm
        await asyncio.sleep(0.1)

        # Check trigger status
        status = scope._query_checked(":TRIG:STAT?").strip()

        return AcquisitionStatusResult(
            action=AcquisitionAction.SINGLE, trigger_status=map_trigger_status(status)
        )

    @mcp.tool
    @with_scope_connection
    async def force_trigger() -> ActionResult:
        """
        Force a trigger event.
        """
        scope._write_checked(":TFOR")

        return ActionResult(action=SystemAction.FORCE_TRIGGER)

    @mcp.tool
    @with_scope_connection
    async def get_trigger_status() -> TriggerStatusResult:
        """
        Get current trigger status.
        """
        # Query trigger status
        status = scope._query_checked(":TRIG:STAT?").strip()

        # Get additional trigger info
        mode = scope._query_checked(":TRIG:MODE?").strip()

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
            actual_source = scope._query_checked(":TRIG:EDGE:SOUR?").strip()
            if actual_source.startswith("CHAN") or actual_source.startswith("CH"):
                # Last character is channel number
                result["channel"] = int(actual_source[-1])
            result["trigger_level"] = float(scope._query_checked(":TRIG:EDGE:LEV?"))
            raw_slope = scope._query_checked(":TRIG:EDGE:SLOP?").strip()
            result["trigger_slope"] = map_trigger_slope_response(raw_slope)

        return result

    # === WAVEFORM RECORDING TOOLS ===

    @mcp.tool
    @with_scope_connection
    async def start_waveform_recording(
        frames: FrameCountField | None = None,
        frame_interval: FrameIntervalField = 10e-9,
    ) -> WaveformRecordingResult:
        """
        Start recording waveforms to segmented memory.

        Configures and starts waveform recording mode, which captures multiple
        waveform frames at specified intervals. Useful for capturing signal events
        over time.
        """
        # Enable waveform recording
        scope._write_checked(":RECord:WRECord:ENABle ON")

        # Set number of frames (None = use MAX)
        if frames is None:
            scope._write_checked(":RECord:WRECord:FRAMes:MAX")
        else:
            scope._write_checked(f":RECord:WRECord:FRAMes {frames}")

        # Set frame interval
        scope._write_checked(f":RECord:WRECord:FINTerval {frame_interval}")

        # Start recording
        scope._write_checked(":RECord:WRECord:OPERate RUN")

        # Brief pause for settings to take effect
        await asyncio.sleep(0.1)

        # Query current state to confirm
        enabled = bool(int(scope._query_checked(":RECord:WRECord:ENABle?")))
        operation_str = scope._query_checked(":RECord:WRECord:OPERate?").strip()
        actual_frames = int(scope._query_checked(":RECord:WRECord:FRAMes?"))
        actual_interval = float(scope._query_checked(":RECord:WRECord:FINTerval?"))
        max_frames = int(scope._query_checked(":RECord:WRECord:FMAX?"))

        return WaveformRecordingResult(
            enabled=enabled,
            operation=RecordingOperation(operation_str),
            frames=actual_frames,
            frame_interval=actual_interval,
            max_frames=max_frames,
        )

    @mcp.tool
    @with_scope_connection
    async def stop_waveform_recording() -> WaveformRecordingResult:
        """
        Stop waveform recording.

        Stops the current recording operation and returns the final recording state.
        """
        # Stop recording
        scope._write_checked(":RECord:WRECord:OPERate STOP")

        # Brief pause
        await asyncio.sleep(0.1)

        # Query current state
        enabled = bool(int(scope._query_checked(":RECord:WRECord:ENABle?")))
        operation_str = scope._query_checked(":RECord:WRECord:OPERate?").strip()
        actual_frames = int(scope._query_checked(":RECord:WRECord:FRAMes?"))
        actual_interval = float(scope._query_checked(":RECord:WRECord:FINTerval?"))
        max_frames = int(scope._query_checked(":RECord:WRECord:FMAX?"))

        return WaveformRecordingResult(
            enabled=enabled,
            operation=RecordingOperation(operation_str),
            frames=actual_frames,
            frame_interval=actual_interval,
            max_frames=max_frames,
        )

    @mcp.tool
    @with_scope_connection
    async def get_recording_status() -> WaveformRecordingResult:
        """
        Query current recording status and configuration.
        """
        # Query current state
        enabled = bool(int(scope._query_checked(":RECord:WRECord:ENABle?")))
        operation_str = scope._query_checked(":RECord:WRECord:OPERate?").strip()
        actual_frames = int(scope._query_checked(":RECord:WRECord:FRAMes?"))
        actual_interval = float(scope._query_checked(":RECord:WRECord:FINTerval?"))
        max_frames = int(scope._query_checked(":RECord:WRECord:FMAX?"))

        return WaveformRecordingResult(
            enabled=enabled,
            operation=RecordingOperation(operation_str),
            frames=actual_frames,
            frame_interval=actual_interval,
            max_frames=max_frames,
        )

    # === TRIGGER CONFIGURATION TOOLS ===

    @mcp.tool
    @with_scope_connection
    async def set_trigger_mode(
        trigger_mode: Annotated[TriggerMode, Field(description="Trigger mode")]
    ) -> TriggerModeResult:
        """
        Set trigger mode.
        """
        scope._write_checked(f":TRIG:MODE {trigger_mode.value}")

        # Verify the setting
        actual_mode = scope._query_checked(":TRIG:MODE?").strip()

        # Map to enum - handle abbreviated responses
        for tm in TriggerMode:
            if actual_mode == tm.value or actual_mode == tm.value[:4]:
                return TriggerModeResult(trigger_mode=tm)

        # Default to EDGE if unknown
        return TriggerModeResult(trigger_mode=TriggerMode.EDGE)

    @mcp.tool
    @with_scope_connection
    async def set_trigger_source(channel: ChannelNumber) -> TriggerSourceResult:
        """
        Set trigger source for edge trigger.
        """
        # Ensure we're in edge trigger mode
        current_mode = scope._query_checked(":TRIG:MODE?").strip()
        if current_mode not in ["EDGE", "EDG"]:
            scope._write_checked(":TRIG:MODE EDGE")

        # Use the channel's SCPI format
        scope._write_checked(f":TRIG:EDGE:SOUR CHAN{channel}")

        # Verify the setting
        actual_source = scope._query_checked(":TRIG:EDGE:SOUR?").strip()

        # Map back to channel number
        if actual_source.startswith("CHAN") or actual_source.startswith("CH"):
            channel_num = int(actual_source[-1])
        else:
            channel_num = 1

        return TriggerSourceResult(channel=channel_num)

    @mcp.tool
    @with_scope_connection
    async def set_trigger_level(
        trigger_level: TriggerLevelField,
        channel: Annotated[
            Optional[ChannelNumber],
            Field(description="Optional trigger source channel (1-4)"),
        ] = None,
    ) -> TriggerLevelResult:
        """
        Set trigger level voltage.
        """
        # If source specified, set it first
        if channel:
            # Ensure we're in edge trigger mode
            current_mode = scope._query_checked(":TRIG:MODE?").strip()
            if current_mode not in ["EDGE", "EDG"]:
                scope._write_checked(":TRIG:MODE EDGE")

            # Set the source
            scope._write_checked(f":TRIG:EDGE:SOUR CHAN{channel}")

        scope._write_checked(f":TRIG:EDGE:LEV {trigger_level}")

        # Verify the setting
        actual_level = float(scope._query_checked(":TRIG:EDGE:LEV?"))

        return TriggerLevelResult(trigger_level=actual_level, units="V")

    @mcp.tool
    @with_scope_connection
    async def set_trigger_slope(
        trigger_slope: Annotated[
            TriggerSlope, Field(description="Edge slope: POSITIVE, NEGATIVE, or EITHER")
        ]
    ) -> TriggerSlopeResult:
        """
        Set trigger edge slope.
        """
        # Map user-facing slope to SCPI value
        slope_map = {
            TriggerSlope.POSITIVE: "POS",
            TriggerSlope.NEGATIVE: "NEG",
            TriggerSlope.EITHER: "RFAL",
        }
        scope._write_checked(f":TRIG:EDGE:SLOP {slope_map[trigger_slope]}")

        # Verify the setting
        actual_slope = scope._query_checked(":TRIG:EDGE:SLOP?").strip()

        # Map back to friendly names
        result_slope = map_trigger_slope_response(actual_slope)

        return TriggerSlopeResult(trigger_slope=result_slope)

    @mcp.tool
    @with_scope_connection
    async def configure_trigger_coupling(
        coupling: Annotated[
            TriggerCouplingType,
            Field(description="Trigger coupling mode: AC, DC, LFReject, or HFReject"),
        ]
    ) -> TriggerCouplingResult:
        """
        Configure trigger coupling mode to filter signal components before triggering.

        Trigger coupling determines what signal components are passed to the trigger circuit:
        - **AC**: Blocks DC component, triggers only on AC signal
        - **DC**: Includes both AC and DC components (full signal)
        - **LFReject**: Low frequency rejection - blocks signals <8 kHz
        - **HFReject**: High frequency rejection - blocks signals >150 kHz
        """
        # Map user-friendly coupling to SCPI format
        scope._write_checked(f":TRIG:COUP {coupling}")

        # Verify the setting
        actual_coupling = scope._query_checked(":TRIG:COUP?").strip()

        # Map SCPI response back to user-friendly format
        # DHO800 may return abbreviated forms
        coupling_map = {
            "AC": "AC",
            "DC": "DC",
            "LFREJ": "LFReject",
            "LFR": "LFReject",
            "HFREJ": "HFReject",
            "HFR": "HFReject",
        }
        result_coupling = coupling_map.get(actual_coupling.upper(), coupling)

        return TriggerCouplingResult(trigger_coupling=result_coupling)  # type: ignore[typeddict-item]

    @mcp.tool
    @with_scope_connection
    async def configure_trigger_sweep(
        sweep_mode: Annotated[
            TriggerSweep,
            Field(description="Trigger sweep mode: AUTO, NORMAL, or SINGLE"),
        ]
    ) -> TriggerSweepResult:
        """
        Configure trigger sweep mode to control acquisition behavior.

        Trigger sweep mode controls how the oscilloscope responds to trigger events:
        - **AUTO**: Triggers automatically even without valid trigger event (for always-on display)
        - **NORMAL**: Only triggers on valid trigger events (for stable triggering)
        - **SINGLE**: Captures one trigger event then stops (for single-shot capture)

        Note: This is different from :RUN/:STOP/:SING commands which control acquisition state.
        Sweep mode controls *how* the scope responds to triggers, while RUN/STOP/SINGLE
        control *whether* the scope is acquiring.
        """
        # TriggerSweep enum values map directly to SCPI format
        scope._write_checked(f":TRIG:SWE {sweep_mode.value}")

        # Verify the setting
        actual_sweep = scope._query_checked(":TRIG:SWE?").strip()

        # Map response back to enum
        sweep_map = {
            "AUTO": TriggerSweep.AUTO,
            "NORM": TriggerSweep.NORMAL,
            "NORMAL": TriggerSweep.NORMAL,
            "SING": TriggerSweep.SINGLE,
            "SINGLE": TriggerSweep.SINGLE,
        }
        result_sweep = sweep_map.get(actual_sweep.upper(), sweep_mode)

        return TriggerSweepResult(trigger_sweep=result_sweep)

    @mcp.tool
    @with_scope_connection
    async def configure_trigger_holdoff(
        holdoff_time: Annotated[
            float,
            Field(description="Trigger holdoff time in seconds (16ns to 10s)"),
        ]
    ) -> TriggerHoldoffResult:
        """
        Set trigger holdoff time to prevent re-triggering on same event.

        Holdoff creates a "dead time" after each trigger where the scope ignores new trigger
        events. This is essential for:
        - Ignoring ringing or oscillations after trigger point
        - Triggering on first pulse in a burst (ignore subsequent pulses)
        - Stable triggering on complex waveforms with multiple edges
        """
        # Validate range
        if holdoff_time < 16e-9 or holdoff_time > 10:
            raise ValueError(
                f"Holdoff time must be between 16ns and 10s, got {holdoff_time}s"
            )

        scope._write_checked(f":TRIG:HOLD {holdoff_time}")

        # Verify the setting
        actual_holdoff = float(scope._query_checked(":TRIG:HOLD?"))

        # Convert to human-readable format
        if actual_holdoff >= 1:
            holdoff_str = f"{actual_holdoff:.3f} s"
        elif actual_holdoff >= 1e-3:
            holdoff_str = f"{actual_holdoff*1e3:.3f} ms"
        elif actual_holdoff >= 1e-6:
            holdoff_str = f"{actual_holdoff*1e6:.3f} μs"
        else:
            holdoff_str = f"{actual_holdoff*1e9:.3f} ns"

        return TriggerHoldoffResult(
            holdoff_time=actual_holdoff, holdoff_time_str=holdoff_str
        )

    @mcp.tool
    @with_scope_connection
    async def configure_trigger_noise_reject(
        enabled: Annotated[
            bool, Field(description="Enable/disable trigger noise rejection")
        ]
    ) -> TriggerNoiseRejectResult:
        """
        Enable/disable trigger noise rejection filter.

        When enabled, adds hysteresis to the trigger level to prevent false triggers from
        noise. This increases trigger stability but may reduce sensitivity to small signals.

        Noise rejection is useful when:
        - Triggering on noisy signals
        - Experiencing false triggers due to signal noise
        - Needing more stable trigger behavior

        Trade-off: Improved stability vs. reduced sensitivity to genuine small signals.
        """
        state = "ON" if enabled else "OFF"
        scope._write_checked(f":TRIG:NREJ {state}")

        # Verify the setting
        actual_state = int(scope._query_checked(":TRIG:NREJ?"))

        return TriggerNoiseRejectResult(noise_reject_enabled=bool(actual_state))

    # === ADVANCED TRIGGER TYPES ===

    @mcp.tool
    @with_scope_connection
    async def configure_pulse_trigger(
        channel: ChannelNumber,
        polarity: Annotated[
            Literal["POSITIVE", "NEGATIVE"],
            Field(description="Pulse polarity: POSITIVE or NEGATIVE"),
        ],
        when: Annotated[
            Literal["GREATER", "LESS", "WITHIN"],
            Field(description="Width condition: GREATER, LESS, or WITHIN"),
        ],
        upper_width: UpperWidthLimitField,
        level: TriggerLevelField,
        lower_width: Annotated[
            Optional[float],
            Field(description="Lower width limit in seconds (required for WITHIN)"),
        ] = None,
    ) -> PulseTriggerResult:
        """
        Configure pulse width trigger to detect pulses that meet width conditions.

        Detects pulses narrower/wider than specified limits or within a range.
        Essential for finding glitches, detecting timeouts, and validating pulse widths.

        Use cases:
        - Finding glitches (LESS than expected width)
        - Detecting timeouts (GREATER than expected)
        - Validating pulse width range (WITHIN limits)
        """
        # Validate WITHIN requires lower_width
        if when == "WITHIN" and lower_width is None:
            raise ValueError("lower_width is required when when='WITHIN'")

        # Set trigger mode to PULSE
        scope._write_checked(":TRIG:MODE PULS")

        # Set source channel
        scope._write_checked(f":TRIG:PULS:SOUR CHAN{channel}")

        # Map when condition to SCPI format
        when_map = {
            "GREATER": "GRE",
            "LESS": "LESS",
            "WITHIN": "GLES",
        }
        scope._write_checked(f":TRIG:PULS:WHEN {when_map[when]}")

        # Set upper width
        scope._write_checked(f":TRIG:PULS:UWID {upper_width}")

        # Set lower width if WITHIN
        if when == "WITHIN" and lower_width is not None:
            scope._write_checked(f":TRIG:PULS:LWID {lower_width}")

        # Map polarity to SCPI format
        polarity_map = {
            "POSITIVE": "POS",
            "NEGATIVE": "NEG",
        }
        scope._write_checked(f":TRIG:PULS:POL {polarity_map[polarity]}")

        # Set trigger level
        scope._write_checked(f":TRIG:PULS:LEV {level}")

        # Verify configuration by reading back
        actual_source = scope._query_checked(":TRIG:PULS:SOUR?").strip()
        actual_when = scope._query_checked(":TRIG:PULS:WHEN?").strip()
        actual_upper = float(scope._query_checked(":TRIG:PULS:UWID?"))
        actual_polarity = scope._query_checked(":TRIG:PULS:POL?").strip()
        actual_level = float(scope._query_checked(":TRIG:PULS:LEV?"))

        # Parse channel from source
        actual_channel = _parse_channel_from_scpi(actual_source)

        # Read lower width if applicable
        actual_lower: Optional[float] = None
        if when == "WITHIN":
            actual_lower = float(scope._query_checked(":TRIG:PULS:LWID?"))

        # Map responses back to user-friendly format
        when_reverse = {"GRE": "GREATER", "GREA": "GREATER", "LESS": "LESS", "GLES": "WITHIN"}
        polarity_reverse = {"POS": "POSITIVE", "NEG": "NEGATIVE"}

        return PulseTriggerResult(
            trigger_mode="PULSE",
            channel=actual_channel,
            polarity=polarity_reverse.get(actual_polarity, polarity),
            when=when_reverse.get(actual_when, when),
            upper_width=actual_upper,
            lower_width=actual_lower,
            level=actual_level,
        )

    @mcp.tool
    @with_scope_connection
    async def configure_slope_trigger(
        channel: ChannelNumber,
        polarity: Annotated[
            Literal["POSITIVE", "NEGATIVE"],
            Field(description="Slope direction: POSITIVE (rising) or NEGATIVE (falling)"),
        ],
        when: Annotated[
            Literal["GREATER", "LESS", "WITHIN"],
            Field(description="Time condition: GREATER, LESS, or WITHIN"),
        ],
        upper_time: UpperTimeLimitField,
        level_a: StartVoltageLevelField,
        level_b: EndVoltageLevelField,
        window: Annotated[
            Literal["TA", "TB", "TAB"],
            Field(description="Time measurement window: TA, TB, or TAB"),
        ],
        lower_time: Annotated[
            Optional[float],
            Field(description="Lower time limit in seconds (required for WITHIN)"),
        ] = None,
    ) -> SlopeTriggerResult:
        """
        Configure slope/rise time trigger to detect edges with specific timing characteristics.

        Detects edges that are too fast, too slow, or within timing range.
        Essential for signal integrity analysis and validating rise/fall time specifications.

        Use cases:
        - Detecting slow edges (signal integrity issues)
        - Finding fast transients
        - Validating rise/fall time specifications
        """
        # Validate WITHIN requires lower_time
        if when == "WITHIN" and lower_time is None:
            raise ValueError("lower_time is required when when='WITHIN'")

        # Set trigger mode to SLOPE
        scope._write_checked(":TRIG:MODE SLOP")

        # Set source channel
        scope._write_checked(f":TRIG:SLOP:SOUR CHAN{channel}")

        # Map when condition to SCPI format
        when_map = {
            "GREATER": "GRE",
            "LESS": "LESS",
            "WITHIN": "GLES",
        }
        scope._write_checked(f":TRIG:SLOP:WHEN {when_map[when]}")

        # Set upper time
        scope._write_checked(f":TRIG:SLOP:TUPP {upper_time}")

        # Set lower time if WITHIN
        if when == "WITHIN" and lower_time is not None:
            scope._write_checked(f":TRIG:SLOP:TLOW {lower_time}")

        # Map polarity to SCPI format
        polarity_map = {
            "POSITIVE": "POS",
            "NEGATIVE": "NEG",
        }
        scope._write_checked(f":TRIG:SLOP:POL {polarity_map[polarity]}")

        # Set voltage levels
        scope._write_checked(f":TRIG:SLOP:ALEV {level_a}")
        scope._write_checked(f":TRIG:SLOP:BLEV {level_b}")

        # Set window
        scope._write_checked(f":TRIG:SLOP:WIND {window}")

        # Verify configuration by reading back
        actual_source = scope._query_checked(":TRIG:SLOP:SOUR?").strip()
        actual_when = scope._query_checked(":TRIG:SLOP:WHEN?").strip()
        actual_upper = float(scope._query_checked(":TRIG:SLOP:TUPP?"))
        actual_polarity = scope._query_checked(":TRIG:SLOP:POL?").strip()
        actual_level_a = float(scope._query_checked(":TRIG:SLOP:ALEV?"))
        actual_level_b = float(scope._query_checked(":TRIG:SLOP:BLEV?"))
        actual_window = scope._query_checked(":TRIG:SLOP:WIND?").strip()

        # Parse channel from source
        actual_channel = _parse_channel_from_scpi(actual_source)

        # Read lower time if applicable
        actual_lower: Optional[float] = None
        if when == "WITHIN":
            actual_lower = float(scope._query_checked(":TRIG:SLOP:TLOW?"))

        # Map responses back to user-friendly format
        when_reverse = {"GRE": "GREATER", "GREA": "GREATER", "LESS": "LESS", "GLES": "WITHIN"}
        polarity_reverse = {"POS": "POSITIVE", "NEG": "NEGATIVE"}

        return SlopeTriggerResult(
            trigger_mode="SLOPE",
            channel=actual_channel,
            polarity=polarity_reverse.get(actual_polarity, polarity),
            when=when_reverse.get(actual_when, when),
            upper_time=actual_upper,
            lower_time=actual_lower,
            level_a=actual_level_a,
            level_b=actual_level_b,
            window=actual_window,
        )

    @mcp.tool
    @with_scope_connection
    async def configure_video_trigger(
        channel: ChannelNumber,
        polarity: Annotated[
            Literal["POSITIVE", "NEGATIVE"],
            Field(description="Sync polarity: POSITIVE or NEGATIVE"),
        ],
        mode: Annotated[
            Literal["ODD_FIELD", "EVEN_FIELD", "LINE", "ALL_LINES"],
            Field(description="Trigger mode: ODD_FIELD, EVEN_FIELD, LINE, or ALL_LINES"),
        ],
        standard: Annotated[
            Literal["PAL_SECAM", "NTSC", "480P", "576P"],
            Field(description="Video standard: PAL_SECAM, NTSC, 480P, or 576P"),
        ],
        level: TriggerLevelField,
        line_number: Annotated[
            Optional[int],
            Field(description="Line number (1-625 for PAL, 1-525 for NTSC, required for LINE mode)"),
        ] = None,
    ) -> VideoTriggerResult:
        """
        Configure video trigger to detect video sync signals (NTSC, PAL, SECAM).

        Triggers on video synchronization pulses for analyzing video signals.
        """
        # Validate LINE mode requires line_number
        if mode == "LINE" and line_number is None:
            raise ValueError("line_number is required when mode='LINE'")

        # Set trigger mode to VIDEO
        scope._write_checked(":TRIG:MODE VID")

        # Set source channel
        scope._write_checked(f":TRIG:VID:SOUR CHAN{channel}")

        # Map polarity to SCPI format
        polarity_map = {
            "POSITIVE": "POS",
            "NEGATIVE": "NEG",
        }
        scope._write_checked(f":TRIG:VID:POL {polarity_map[polarity]}")

        # Map mode to SCPI format
        mode_map = {
            "ODD_FIELD": "ODDF",
            "EVEN_FIELD": "EVENF",
            "LINE": "LINE",
            "ALL_LINES": "ALIN",
        }
        scope._write_checked(f":TRIG:VID:MODE {mode_map[mode]}")

        # Set line number if LINE mode
        if mode == "LINE" and line_number is not None:
            scope._write_checked(f":TRIG:VID:LINE {line_number}")

        # Map standard to SCPI format
        standard_map = {
            "PAL_SECAM": "PALS",
            "NTSC": "NTSC",
            "480P": "480P",
            "576P": "576P",
        }
        scope._write_checked(f":TRIG:VID:STAN {standard_map[standard]}")

        # Set trigger level
        scope._write_checked(f":TRIG:VID:LEV {level}")

        # Verify configuration
        actual_source = scope._query_checked(":TRIG:VID:SOUR?").strip()
        actual_polarity = scope._query_checked(":TRIG:VID:POL?").strip()
        actual_mode = scope._query_checked(":TRIG:VID:MODE?").strip()
        actual_standard = scope._query_checked(":TRIG:VID:STAN?").strip()
        actual_level = float(scope._query_checked(":TRIG:VID:LEV?"))

        # Parse channel from source
        actual_channel = _parse_channel_from_scpi(actual_source)

        # Read line number if LINE mode
        actual_line: Optional[int] = None
        if mode == "LINE":
            actual_line = int(scope._query_checked(":TRIG:VID:LINE?"))

        # Map responses back
        polarity_reverse = {"POS": "POSITIVE", "NEG": "NEGATIVE"}
        mode_reverse = {"ODDF": "ODD_FIELD", "EVENF": "EVEN_FIELD", "LINE": "LINE", "ALIN": "ALL_LINES"}
        standard_reverse = {"PALS": "PAL_SECAM", "NTSC": "NTSC", "480P": "480P", "576P": "576P"}

        return VideoTriggerResult(
            trigger_mode="VIDEO",
            channel=actual_channel,
            polarity=polarity_reverse.get(actual_polarity, polarity),
            mode=mode_reverse.get(actual_mode, mode),
            line_number=actual_line,
            standard=standard_reverse.get(actual_standard, standard),
            level=actual_level,
        )

    @mcp.tool
    @with_scope_connection
    async def configure_pattern_trigger(
        pattern: Annotated[
            List[str],
            Field(description="4-element pattern list with values: H (high), L (low), X (don't care), R (rising), F (falling)"),
        ],
        levels: Annotated[
            dict[int, float],
            Field(description="Dictionary mapping channel numbers (1-4) to trigger levels in volts, e.g., {1: 1.5, 2: 2.0}"),
        ],
    ) -> PatternTriggerResult:
        """
        Configure pattern trigger to detect multi-channel logic patterns.

        Triggers when multi-channel logic pattern is met. Combines up to 4 channels with AND logic.

        Pattern values per channel:
        - H: High (above threshold)
        - L: Low (below threshold)
        - X: Don't care
        - R: Rising edge
        - F: Falling edge

        Use cases:
        - Multi-signal qualification
        - State machine debugging
        - Bus protocol analysis
        """
        # Validate pattern length
        if len(pattern) != 4:
            raise ValueError(f"Pattern must have exactly 4 elements, got {len(pattern)}")

        # Validate pattern values
        valid_values = {"H", "L", "X", "R", "F"}
        for val in pattern:
            if val not in valid_values:
                raise ValueError(f"Invalid pattern value '{val}'. Must be one of: {valid_values}")

        # Set trigger mode to PATTERN
        scope._write_checked(":TRIG:MODE PATT")

        # Set pattern (comma-separated)
        pattern_str = ",".join(pattern)
        scope._write_checked(f":TRIG:PATT:PATT {pattern_str}")

        # Set trigger levels for specified channels
        for channel, level in levels.items():
            if channel < 1 or channel > 4:
                raise ValueError(f"Channel must be 1-4, got {channel}")
            scope._write_checked(f":TRIG:PATT:LEV{channel} {level}")

        # Verify configuration
        actual_pattern_str = scope._query_checked(":TRIG:PATT:PATT?").strip()
        actual_pattern = actual_pattern_str.split(",")

        # Read back levels for all channels
        actual_levels = {}
        for channel in range(1, 5):
            try:
                level = float(scope._query_checked(f":TRIG:PATT:LEV{channel}?"))
                actual_levels[channel] = level
            except:
                pass  # Channel level may not be set

        return PatternTriggerResult(
            trigger_mode="PATTERN",
            pattern=actual_pattern,
            levels=actual_levels,
        )

    @mcp.tool
    @with_scope_connection
    async def configure_runt_trigger(
        channel: ChannelNumber,
        polarity: Annotated[
            Literal["POSITIVE", "NEGATIVE"],
            Field(description="Runt pulse direction: POSITIVE or NEGATIVE"),
        ],
        when: Annotated[
            Literal["GREATER", "LESS", "WITHIN"],
            Field(description="Width qualification: GREATER, LESS, or WITHIN"),
        ],
        upper_width: UpperWidthLimitField,
        lower_width: LowerWidthLimitField,
        level_a: UpperVoltageLevelField,
        level_b: LowerVoltageLevelField,
    ) -> RuntTriggerResult:
        """
        Configure runt pulse trigger to detect incomplete transitions.

        Triggers on runt pulses - pulses that cross one threshold but fail to reach
        the other threshold before returning. Essential for signal integrity analysis.

        Use cases:
        - Signal integrity analysis
        - Detecting incomplete transitions
        - Power supply glitches
        """
        # Set trigger mode to RUNT
        scope._write_checked(":TRIG:MODE RUNT")

        # Set source channel
        scope._write_checked(f":TRIG:RUNT:SOUR CHAN{channel}")

        # Map polarity to SCPI format
        polarity_map = {
            "POSITIVE": "POS",
            "NEGATIVE": "NEG",
        }
        scope._write_checked(f":TRIG:RUNT:POL {polarity_map[polarity]}")

        # Map when condition to SCPI format
        when_map = {
            "GREATER": "GRE",
            "LESS": "LESS",
            "WITHIN": "GLES",
        }
        scope._write_checked(f":TRIG:RUNT:WHEN {when_map[when]}")

        # Set width limits
        scope._write_checked(f":TRIG:RUNT:UWID {upper_width}")
        scope._write_checked(f":TRIG:RUNT:LWID {lower_width}")

        # Set voltage thresholds
        scope._write_checked(f":TRIG:RUNT:ALEV {level_a}")
        scope._write_checked(f":TRIG:RUNT:BLEV {level_b}")

        # Verify configuration
        actual_source = scope._query_checked(":TRIG:RUNT:SOUR?").strip()
        actual_polarity = scope._query_checked(":TRIG:RUNT:POL?").strip()
        actual_when = scope._query_checked(":TRIG:RUNT:WHEN?").strip()
        actual_upper = float(scope._query_checked(":TRIG:RUNT:UWID?"))
        actual_lower = float(scope._query_checked(":TRIG:RUNT:LWID?"))
        actual_level_a = float(scope._query_checked(":TRIG:RUNT:ALEV?"))
        actual_level_b = float(scope._query_checked(":TRIG:RUNT:BLEV?"))

        # Parse channel from source
        actual_channel = _parse_channel_from_scpi(actual_source)

        # Map responses back
        polarity_reverse = {"POS": "POSITIVE", "NEG": "NEGATIVE"}
        when_reverse = {"GRE": "GREATER", "GREA": "GREATER", "LESS": "LESS", "GLES": "WITHIN"}

        return RuntTriggerResult(
            trigger_mode="RUNT",
            channel=actual_channel,
            polarity=polarity_reverse.get(actual_polarity, polarity),
            when=when_reverse.get(actual_when, when),
            upper_width=actual_upper,
            lower_width=actual_lower,
            level_a=actual_level_a,
            level_b=actual_level_b,
        )

    @mcp.tool
    @with_scope_connection
    async def configure_timeout_trigger(
        channel: ChannelNumber,
        slope: Annotated[
            Literal["POSITIVE", "NEGATIVE"],
            Field(description="Edge to start timeout counter: POSITIVE or NEGATIVE"),
        ],
        timeout: TimeoutDurationField,
        level: TriggerLevelField,
    ) -> TimeoutTriggerResult:
        """
        Configure timeout/idle trigger to detect when signal remains idle.

        Triggers when signal remains idle (no edge) for specified duration.
        Essential for detecting bus stalls and protocol timeouts.

        Use cases:
        - Detecting bus stalls
        - Finding protocol timeouts
        - Analyzing idle periods
        """
        # Set trigger mode to TIMEOUT
        scope._write_checked(":TRIG:MODE TIM")

        # Set source channel
        scope._write_checked(f":TRIG:TIM:SOUR CHAN{channel}")

        # Map slope to SCPI format
        slope_map = {
            "POSITIVE": "POS",
            "NEGATIVE": "NEG",
        }
        scope._write_checked(f":TRIG:TIM:SLOP {slope_map[slope]}")

        # Set timeout duration
        scope._write_checked(f":TRIG:TIM:TIM {timeout}")

        # Set trigger level
        scope._write_checked(f":TRIG:TIM:LEV {level}")

        # Verify configuration
        actual_source = scope._query_checked(":TRIG:TIM:SOUR?").strip()
        actual_slope = scope._query_checked(":TRIG:TIM:SLOP?").strip()
        actual_timeout = float(scope._query_checked(":TRIG:TIM:TIM?"))
        actual_level = float(scope._query_checked(":TRIG:TIM:LEV?"))

        # Parse channel from source
        actual_channel = _parse_channel_from_scpi(actual_source)

        # Map responses back
        slope_reverse = {"POS": "POSITIVE", "NEG": "NEGATIVE"}

        return TimeoutTriggerResult(
            trigger_mode="TIMEOUT",
            channel=actual_channel,
            slope=slope_reverse.get(actual_slope, slope),
            timeout=actual_timeout,
            level=actual_level,
        )

    @mcp.tool
    @with_scope_connection
    async def configure_duration_trigger(
        channel: ChannelNumber,
        pattern_type: Annotated[
            Literal["GREATER", "LESS", "WITHIN", "OUTSIDE"],
            Field(description="Pattern qualifier: GREATER, LESS, WITHIN, or OUTSIDE"),
        ],
        when: Annotated[
            Literal["GREATER", "LESS", "WITHIN", "OUTSIDE"],
            Field(description="Duration condition: GREATER, LESS, WITHIN, or OUTSIDE"),
        ],
        upper_width: UpperTimeLimitField,
        lower_width: LowerTimeLimitField,
        level: TriggerLevelField,
    ) -> DurationTriggerResult:
        """
        Configure duration trigger for pattern that persists for specific duration.

        Triggers on pattern that persists for specific duration.
        """
        # Set trigger mode to DURATION
        scope._write_checked(":TRIG:MODE DUR")

        # Set source channel
        scope._write_checked(f":TRIG:DUR:SOUR CHAN{channel}")

        # Map conditions to SCPI format
        condition_map = {
            "GREATER": "GRE",
            "LESS": "LESS",
            "WITHIN": "GLES",
            "OUTSIDE": "UNGL",
        }
        scope._write_checked(f":TRIG:DUR:TYPE {condition_map[pattern_type]}")
        scope._write_checked(f":TRIG:DUR:WHEN {condition_map[when]}")

        # Set time limits
        scope._write_checked(f":TRIG:DUR:UWID {upper_width}")
        scope._write_checked(f":TRIG:DUR:LWID {lower_width}")

        # Set trigger level
        scope._write_checked(f":TRIG:DUR:LEV {level}")

        # Verify configuration
        actual_source = scope._query_checked(":TRIG:DUR:SOUR?").strip()
        actual_type = scope._query_checked(":TRIG:DUR:TYPE?").strip()
        actual_when = scope._query_checked(":TRIG:DUR:WHEN?").strip()
        actual_upper = float(scope._query_checked(":TRIG:DUR:UWID?"))
        actual_lower = float(scope._query_checked(":TRIG:DUR:LWID?"))
        actual_level = float(scope._query_checked(":TRIG:DUR:LEV?"))

        # Parse channel from source
        actual_channel = _parse_channel_from_scpi(actual_source)

        # Map responses back
        condition_reverse = {"GRE": "GREATER", "GREA": "GREATER", "LESS": "LESS", "GLES": "WITHIN", "UNGL": "OUTSIDE"}

        return DurationTriggerResult(
            trigger_mode="DURATION",
            channel=actual_channel,
            pattern_type=condition_reverse.get(actual_type, pattern_type),
            when=condition_reverse.get(actual_when, when),
            upper_width=actual_upper,
            lower_width=actual_lower,
            level=actual_level,
        )

    @mcp.tool
    @with_scope_connection
    async def configure_setup_hold_trigger(
        data_channel: ChannelNumber,
        clock_channel: ChannelNumber,
        clock_slope: Annotated[
            Literal["POSITIVE", "NEGATIVE"],
            Field(description="Clock edge to check: POSITIVE or NEGATIVE"),
        ],
        data_pattern: Annotated[
            Literal["H", "L"],
            Field(description="Expected data value: H (high) or L (low)"),
        ],
        setup_time: SetupTimeField,
        hold_time: HoldTimeField,
        data_level: DataThresholdField,
        clock_level: ClockThresholdField,
    ) -> SetupHoldTriggerResult:
        """
        Configure setup/hold trigger for timing violations.

        Triggers on setup/hold time violations between data and clock signals.
        Essential for verifying timing relationships in synchronous interfaces.

        Use cases:
        - Verifying timing relationships
        - Debugging synchronous interfaces
        - Validating memory timing
        """
        # Set trigger mode to SETUP/HOLD
        scope._write_checked(":TRIG:MODE SHOL")

        # Set data and clock sources
        scope._write_checked(f":TRIG:SHOL:DSRC CHAN{data_channel}")
        scope._write_checked(f":TRIG:SHOL:CSRC CHAN{clock_channel}")

        # Map clock slope to SCPI format
        slope_map = {
            "POSITIVE": "POS",
            "NEGATIVE": "NEG",
        }
        scope._write_checked(f":TRIG:SHOL:SLOP {slope_map[clock_slope]}")

        # Set data pattern
        scope._write_checked(f":TRIG:SHOL:PATT {data_pattern}")

        # Set setup and hold times
        scope._write_checked(f":TRIG:SHOL:STIM {setup_time}")
        scope._write_checked(f":TRIG:SHOL:HTIM {hold_time}")

        # Set voltage levels
        scope._write_checked(f":TRIG:SHOL:DLEV {data_level}")
        scope._write_checked(f":TRIG:SHOL:CLEV {clock_level}")

        # Verify configuration
        actual_dsrc = scope._query_checked(":TRIG:SHOL:DSRC?").strip()
        actual_csrc = scope._query_checked(":TRIG:SHOL:CSRC?").strip()
        actual_slope = scope._query_checked(":TRIG:SHOL:SLOP?").strip()
        actual_pattern = scope._query_checked(":TRIG:SHOL:PATT?").strip()
        actual_setup = float(scope._query_checked(":TRIG:SHOL:STIM?"))
        actual_hold = float(scope._query_checked(":TRIG:SHOL:HTIM?"))
        actual_dlev = float(scope._query_checked(":TRIG:SHOL:DLEV?"))
        actual_clev = float(scope._query_checked(":TRIG:SHOL:CLEV?"))

        # Parse channels from source
        actual_data_channel = _parse_channel_from_scpi(actual_dsrc)
        actual_clock_channel = _parse_channel_from_scpi(actual_csrc)

        # Map responses back
        slope_reverse = {"POS": "POSITIVE", "NEG": "NEGATIVE"}

        return SetupHoldTriggerResult(
            trigger_mode="SETUP_HOLD",
            data_channel=actual_data_channel,
            clock_channel=actual_clock_channel,
            clock_slope=slope_reverse.get(actual_slope, clock_slope),
            data_pattern=actual_pattern,
            setup_time=actual_setup,
            hold_time=actual_hold,
            data_level=actual_dlev,
            clock_level=actual_clev,
        )

    @mcp.tool
    @with_scope_connection
    async def configure_nth_edge_trigger(
        channel: ChannelNumber,
        slope: Annotated[
            Literal["POSITIVE", "NEGATIVE"],
            Field(description="Edge direction to count: POSITIVE or NEGATIVE"),
        ],
        idle_time: IdleTimeField,
        edge_count: EdgeCountField,
        level: TriggerLevelField,
    ) -> NthEdgeTriggerResult:
        """
        Configure Nth edge trigger for burst signals.

        Triggers on the Nth edge after an idle period. Useful for triggering
        inside burst transmissions and skipping preamble/sync edges.

        Use cases:
        - Triggering inside burst transmissions
        - Skipping preamble/sync edges
        - Analyzing periodic burst signals
        """
        # Validate edge count range
        if edge_count < 1 or edge_count > 65535:
            raise ValueError(f"edge_count must be 1-65535, got {edge_count}")

        # Set trigger mode to NTH EDGE
        scope._write_checked(":TRIG:MODE NEDG")

        # Set source channel
        scope._write_checked(f":TRIG:NEDG:SOUR CHAN{channel}")

        # Map slope to SCPI format
        slope_map = {
            "POSITIVE": "POS",
            "NEGATIVE": "NEG",
        }
        scope._write_checked(f":TRIG:NEDG:SLOP {slope_map[slope]}")

        # Set idle time and edge count
        scope._write_checked(f":TRIG:NEDG:IDLE {idle_time}")
        scope._write_checked(f":TRIG:NEDG:EDGE {edge_count}")

        # Set trigger level
        scope._write_checked(f":TRIG:NEDG:LEV {level}")

        # Verify configuration
        actual_source = scope._query_checked(":TRIG:NEDG:SOUR?").strip()
        actual_slope = scope._query_checked(":TRIG:NEDG:SLOP?").strip()
        actual_idle = float(scope._query_checked(":TRIG:NEDG:IDLE?"))
        actual_count = int(scope._query_checked(":TRIG:NEDG:EDGE?"))
        actual_level = float(scope._query_checked(":TRIG:NEDG:LEV?"))

        # Parse channel from source
        actual_channel = _parse_channel_from_scpi(actual_source)

        # Map responses back
        slope_reverse = {"POS": "POSITIVE", "NEG": "NEGATIVE"}

        return NthEdgeTriggerResult(
            trigger_mode="NTH_EDGE",
            channel=actual_channel,
            slope=slope_reverse.get(actual_slope, slope),
            idle_time=actual_idle,
            edge_count=actual_count,
            level=actual_level,
        )

    @mcp.tool
    @with_scope_connection
    async def configure_window_trigger(
        channel: ChannelNumber,
        slope: Annotated[
            Literal["POSITIVE", "NEGATIVE"],
            Field(description="Edge direction: POSITIVE or NEGATIVE"),
        ],
        position: Annotated[
            Literal["EXIT", "ENTER", "TIME"],
            Field(description="Trigger position: EXIT, ENTER, or TIME"),
        ],
        level_a: UpperVoltageLevelField,
        level_b: LowerVoltageLevelField,
        time: Annotated[
            Optional[float],
            Field(description="Duration for TIME position mode (seconds, required for TIME)"),
        ] = None,
    ) -> WindowTriggerResult:
        """
        Configure window trigger for voltage window entry/exit detection.

        Triggers when signal enters or exits voltage window between two thresholds.
        Essential for power supply regulation analysis and detecting over/under voltage.

        Use cases:
        - Power supply regulation analysis
        - Detecting over/under voltage
        - Tracking signal excursions
        """
        # Validate TIME position requires time
        if position == "TIME" and time is None:
            raise ValueError("time is required when position='TIME'")

        # Set trigger mode to WINDOW
        scope._write_checked(":TRIG:MODE WIND")

        # Set source channel
        scope._write_checked(f":TRIG:WIND:SOUR CHAN{channel}")

        # Map slope to SCPI format
        slope_map = {
            "POSITIVE": "POS",
            "NEGATIVE": "NEG",
        }
        scope._write_checked(f":TRIG:WIND:SLOP {slope_map[slope]}")

        # Set position
        scope._write_checked(f":TRIG:WIND:POS {position}")

        # Set time if TIME position
        if position == "TIME" and time is not None:
            scope._write_checked(f":TRIG:WIND:TIME {time}")

        # Set voltage thresholds
        scope._write_checked(f":TRIG:WIND:ALEV {level_a}")
        scope._write_checked(f":TRIG:WIND:BLEV {level_b}")

        # Verify configuration
        actual_source = scope._query_checked(":TRIG:WIND:SOUR?").strip()
        actual_slope = scope._query_checked(":TRIG:WIND:SLOP?").strip()
        actual_position = scope._query_checked(":TRIG:WIND:POS?").strip()
        actual_level_a = float(scope._query_checked(":TRIG:WIND:ALEV?"))
        actual_level_b = float(scope._query_checked(":TRIG:WIND:BLEV?"))

        # Parse channel from source
        actual_channel = _parse_channel_from_scpi(actual_source)

        # Read time if TIME position
        actual_time: Optional[float] = None
        if position == "TIME":
            actual_time = float(scope._query_checked(":TRIG:WIND:TIME?"))

        # Map responses back
        slope_reverse = {"POS": "POSITIVE", "NEG": "NEGATIVE"}

        return WindowTriggerResult(
            trigger_mode="WINDOW",
            channel=actual_channel,
            slope=slope_reverse.get(actual_slope, slope),
            position=actual_position,
            time=actual_time,
            level_a=actual_level_a,
            level_b=actual_level_b,
        )

    @mcp.tool
    @with_scope_connection
    async def configure_delay_trigger(
        source_a_channel: ChannelNumber,
        source_b_channel: ChannelNumber,
        slope_a: Annotated[
            Literal["POSITIVE", "NEGATIVE"],
            Field(description="Source A edge direction: POSITIVE or NEGATIVE"),
        ],
        slope_b: Annotated[
            Literal["POSITIVE", "NEGATIVE"],
            Field(description="Source B edge direction: POSITIVE or NEGATIVE"),
        ],
        delay_type: Annotated[
            Literal["GREATER", "LESS", "WITHIN"],
            Field(description="Delay condition: GREATER, LESS, or WITHIN"),
        ],
        upper_time: UpperTimeLimitField,
        level_a: SourceAThresholdField,
        level_b: SourceBThresholdField,
        lower_time: Annotated[
            Optional[float],
            Field(description="Lower time limit in seconds (required for WITHIN)"),
        ] = None,
    ) -> DelayTriggerResult:
        """
        Configure delay trigger for time delay between two signal edges.

        Triggers on time delay between two signal edges. Essential for measuring
        propagation delays, detecting timing skew, and verifying signal sequencing.

        Use cases:
        - Measuring propagation delays
        - Detecting timing skew
        - Verifying signal sequencing
        """
        # Validate WITHIN requires lower_time
        if delay_type == "WITHIN" and lower_time is None:
            raise ValueError("lower_time is required when delay_type='WITHIN'")

        # Set trigger mode to DELAY
        scope._write_checked(":TRIG:MODE DEL")

        # Set source channels
        scope._write_checked(f":TRIG:DEL:SA CHAN{source_a_channel}")
        scope._write_checked(f":TRIG:DEL:SB CHAN{source_b_channel}")

        # Map slopes to SCPI format
        slope_map = {
            "POSITIVE": "POS",
            "NEGATIVE": "NEG",
        }
        scope._write_checked(f":TRIG:DEL:ASLOP {slope_map[slope_a]}")
        scope._write_checked(f":TRIG:DEL:BSLOP {slope_map[slope_b]}")

        # Map delay type to SCPI format
        type_map = {
            "GREATER": "GRE",
            "LESS": "LESS",
            "WITHIN": "GLES",
        }
        scope._write_checked(f":TRIG:DEL:TYPE {type_map[delay_type]}")

        # Set time limits
        scope._write_checked(f":TRIG:DEL:TUPP {upper_time}")
        if delay_type == "WITHIN" and lower_time is not None:
            scope._write_checked(f":TRIG:DEL:TLOW {lower_time}")

        # Set voltage levels
        scope._write_checked(f":TRIG:DEL:LEVA {level_a}")
        scope._write_checked(f":TRIG:DEL:LEVB {level_b}")

        # Verify configuration
        actual_sa = scope._query_checked(":TRIG:DEL:SA?").strip()
        actual_sb = scope._query_checked(":TRIG:DEL:SB?").strip()
        actual_slope_a = scope._query_checked(":TRIG:DEL:ASLOP?").strip()
        actual_slope_b = scope._query_checked(":TRIG:DEL:BSLOP?").strip()
        actual_type = scope._query_checked(":TRIG:DEL:TYPE?").strip()
        actual_upper = float(scope._query_checked(":TRIG:DEL:TUPP?"))
        actual_level_a = float(scope._query_checked(":TRIG:DEL:LEVA?"))
        actual_level_b = float(scope._query_checked(":TRIG:DEL:LEVB?"))

        # Parse channels from source
        actual_source_a = _parse_channel_from_scpi(actual_sa)
        actual_source_b = _parse_channel_from_scpi(actual_sb)

        # Read lower time if WITHIN
        actual_lower: Optional[float] = None
        if delay_type == "WITHIN":
            actual_lower = float(scope._query_checked(":TRIG:DEL:TLOW?"))

        # Map responses back
        slope_reverse = {"POS": "POSITIVE", "NEG": "NEGATIVE"}
        type_reverse = {"GRE": "GREATER", "GREA": "GREATER", "LESS": "LESS", "GLES": "WITHIN"}

        return DelayTriggerResult(
            trigger_mode="DELAY",
            source_a_channel=actual_source_a,
            source_b_channel=actual_source_b,
            slope_a=slope_reverse.get(actual_slope_a, slope_a),
            slope_b=slope_reverse.get(actual_slope_b, slope_b),
            delay_type=type_reverse.get(actual_type, delay_type),
            upper_time=actual_upper,
            lower_time=actual_lower,
            level_a=actual_level_a,
            level_b=actual_level_b,
        )

    # === PROTOCOL TRIGGERS ===

    @mcp.tool
    @with_scope_connection
    async def configure_rs232_trigger(
        channel: ChannelNumber,
        when: Annotated[
            Literal["START", "ERROR", "PARITY_ERROR", "DATA"],
            Field(description="Trigger condition"),
        ],
        baud_rate: BaudRateField,
        parity: Annotated[
            Literal["NONE", "EVEN", "ODD", "MARK", "SPACE"],
            Field(description="Parity setting"),
        ],
        stop_bits: Annotated[
            Literal["1", "1.5", "2"],
            Field(description="Stop bit count"),
        ],
        polarity: Annotated[
            Literal["POSITIVE", "NEGATIVE"],
            Field(description="Signal polarity"),
        ],
        level: TriggerLevelField,
        data_value: Annotated[
            Optional[int],
            Field(ge=0, le=255, description="Data byte to match (0-255, required for DATA mode)"),
        ] = None,
        data_bits: Annotated[
            Literal[5, 6, 7, 8],
            Field(description="Number of data bits"),
        ] = 8,
    ) -> RS232TriggerResult:
        """
        Trigger on UART/RS232 serial data patterns.

        Detects start frames, error frames, parity errors, or specific data bytes
        on RS232/UART serial communication lines.

        Use cases:
        - Triggering on frame start for synchronization
        - Detecting communication errors
        - Capturing specific data patterns
        """
        # Validate DATA mode requires data_value
        if when == "DATA" and data_value is None:
            raise ValueError("data_value is required when when='DATA'")

        # Set trigger mode to RS232
        scope._write_checked(":TRIG:MODE RS232")

        # Set source channel
        scope._write_checked(f":TRIG:RS232:SOUR CHAN{channel}")

        # Map when condition to SCPI format
        when_map = {
            "START": "STAR",
            "ERROR": "ERR",
            "PARITY_ERROR": "CERR",
            "DATA": "DATA",
        }
        scope._write_checked(f":TRIG:RS232:WHEN {when_map[when]}")

        # Set data value if DATA mode
        if when == "DATA" and data_value is not None:
            scope._write_checked(f":TRIG:RS232:DATA {data_value}")

        # Set baud rate
        scope._write_checked(f":TRIG:RS232:BAUD {baud_rate}")

        # Set data width
        scope._write_checked(f":TRIG:RS232:WIDT {data_bits}")

        # Set stop bits
        scope._write_checked(f":TRIG:RS232:STOP {stop_bits}")

        # Map parity to SCPI format
        parity_scpi = SerialParity[parity].value
        scope._write_checked(f":TRIG:RS232:PAR {parity_scpi}")

        # Map polarity to SCPI format
        polarity_map = {"POSITIVE": "POS", "NEGATIVE": "NEG"}
        scope._write_checked(f":TRIG:RS232:POL {polarity_map[polarity]}")

        # Set trigger level
        scope._write_checked(f":TRIG:RS232:LEV {level}")

        # Verify configuration by reading back
        actual_source = scope._query_checked(":TRIG:RS232:SOUR?").strip()
        actual_when = scope._query_checked(":TRIG:RS232:WHEN?").strip()
        actual_baud = int(scope._query_checked(":TRIG:RS232:BAUD?"))
        actual_width = int(scope._query_checked(":TRIG:RS232:WIDT?"))
        actual_stop = scope._query_checked(":TRIG:RS232:STOP?").strip()
        actual_parity = scope._query_checked(":TRIG:RS232:PAR?").strip()
        actual_polarity = scope._query_checked(":TRIG:RS232:POL?").strip()
        actual_level = float(scope._query_checked(":TRIG:RS232:LEV?"))

        # Parse channel from source
        actual_channel = _parse_channel_from_scpi(actual_source)

        # Read data value if DATA mode
        actual_data: Optional[int] = None
        if when == "DATA":
            actual_data = int(scope._query_checked(":TRIG:RS232:DATA?"))

        # Map responses back to user-friendly format
        when_reverse = {"STAR": "START", "ERR": "ERROR", "CERR": "PARITY_ERROR", "DATA": "DATA"}
        parity_reverse = {"NONE": "NONE", "EVEN": "EVEN", "ODD": "ODD", "MARK": "MARK", "SPAC": "SPACE"}
        polarity_reverse = {"POS": "POSITIVE", "NEG": "NEGATIVE"}

        return RS232TriggerResult(
            trigger_mode="RS232",
            channel=actual_channel,
            when=when_reverse.get(actual_when, when),
            data_value=actual_data,
            baud_rate=actual_baud,
            parity=parity_reverse.get(actual_parity, parity),
            stop_bits=actual_stop,
            data_bits=actual_width,
            polarity=polarity_reverse.get(actual_polarity, polarity),
            level=actual_level,
        )

    @mcp.tool
    @with_scope_connection
    async def configure_i2c_trigger(
        scl_channel: ChannelNumber,
        sda_channel: ChannelNumber,
        when: Annotated[
            Literal["START", "RESTART", "STOP", "NACK", "ADDRESS", "DATA", "ADDRESS_DATA"],
            Field(description="Trigger condition"),
        ],
        clock_level: ClockThresholdField,
        data_level: DataThresholdField,
        address: Annotated[
            Optional[int],
            Field(description="I2C address (required for ADDRESS/ADDRESS_DATA modes)"),
        ] = None,
        data_value: Annotated[
            Optional[int],
            Field(ge=0, le=255, description="Data byte (required for DATA/ADDRESS_DATA modes)"),
        ] = None,
        address_width: Annotated[
            Literal["7", "10"],
            Field(description="Address width (7 or 10 bits)"),
        ] = "7",
        direction: Annotated[
            Literal["READ", "WRITE", "READ_WRITE"],
            Field(description="Transfer direction"),
        ] = "READ_WRITE",
    ) -> I2CTriggerResult:
        """
        Trigger on I2C bus events (start, stop, address, data).

        Detects I2C protocol events including start conditions, stop conditions,
        address matches, data patterns, and acknowledgment errors.

        Use cases:
        - Triggering on specific device addresses
        - Detecting protocol errors (NACK)
        - Capturing specific data patterns
        """
        # Validate modes that require address or data
        if when in ["ADDRESS", "ADDRESS_DATA"] and address is None:
            raise ValueError(f"address is required when when='{when}'")
        if when in ["DATA", "ADDRESS_DATA"] and data_value is None:
            raise ValueError(f"data_value is required when when='{when}'")

        # Set trigger mode to I2C
        scope._write_checked(":TRIG:MODE IIC")

        # Set SCL and SDA channels
        scope._write_checked(f":TRIG:IIC:SCL CHAN{scl_channel}")
        scope._write_checked(f":TRIG:IIC:SDA CHAN{sda_channel}")

        # Map when condition to SCPI format
        when_map = {
            "START": "STAR",
            "RESTART": "REST",
            "STOP": "STOP",
            "NACK": "NACK",
            "ADDRESS": "ADDR",
            "DATA": "DATA",
            "ADDRESS_DATA": "ADAT",
        }
        scope._write_checked(f":TRIG:IIC:WHEN {when_map[when]}")

        # Set address width
        scope._write_checked(f":TRIG:IIC:AWID {address_width}")

        # Set address if needed
        if when in ["ADDRESS", "ADDRESS_DATA"] and address is not None:
            scope._write_checked(f":TRIG:IIC:ADDR {address}")

        # Set data if needed
        if when in ["DATA", "ADDRESS_DATA"] and data_value is not None:
            scope._write_checked(f":TRIG:IIC:DATA {data_value}")

        # Map direction to SCPI format
        direction_scpi = I2CDirection[direction].value
        scope._write_checked(f":TRIG:IIC:DIR {direction_scpi}")

        # Set voltage levels
        scope._write_checked(f":TRIG:IIC:CLEV {clock_level}")
        scope._write_checked(f":TRIG:IIC:DLEV {data_level}")

        # Verify configuration
        actual_scl = scope._query_checked(":TRIG:IIC:SCL?").strip()
        actual_sda = scope._query_checked(":TRIG:IIC:SDA?").strip()
        actual_when = scope._query_checked(":TRIG:IIC:WHEN?").strip()
        actual_width = scope._query_checked(":TRIG:IIC:AWID?").strip()
        actual_direction = scope._query_checked(":TRIG:IIC:DIR?").strip()
        actual_clevel = float(scope._query_checked(":TRIG:IIC:CLEV?"))
        actual_dlevel = float(scope._query_checked(":TRIG:IIC:DLEV?"))

        actual_scl_channel = _parse_channel_from_scpi(actual_scl)
        actual_sda_channel = _parse_channel_from_scpi(actual_sda)

        # Read address and data if applicable
        actual_address: Optional[int] = None
        actual_data: Optional[int] = None
        if when in ["ADDRESS", "ADDRESS_DATA"]:
            actual_address = int(scope._query_checked(":TRIG:IIC:ADDR?"))
        if when in ["DATA", "ADDRESS_DATA"]:
            actual_data = int(scope._query_checked(":TRIG:IIC:DATA?"))

        # Map responses back
        when_reverse = {
            "STAR": "START",
            "REST": "RESTART",
            "STOP": "STOP",
            "NACK": "NACK",
            "ADDR": "ADDRESS",
            "DATA": "DATA",
            "ADAT": "ADDRESS_DATA",
        }
        direction_reverse = {"READ": "READ", "WRIT": "WRITE", "RWRI": "READ_WRITE"}

        return I2CTriggerResult(
            trigger_mode="I2C",
            scl_channel=actual_scl_channel,
            sda_channel=actual_sda_channel,
            when=when_reverse.get(actual_when, when),
            address=actual_address,
            data_value=actual_data,
            address_width=actual_width,
            direction=direction_reverse.get(actual_direction, direction),
            clock_level=actual_clevel,
            data_level=actual_dlevel,
        )

    @mcp.tool
    @with_scope_connection
    async def configure_spi_trigger(
        sclk_channel: ChannelNumber,
        clock_slope: Annotated[
            Literal["POSITIVE", "NEGATIVE"],
            Field(description="Clock edge"),
        ],
        when: Annotated[
            Literal["TIMEOUT"],
            Field(description="Trigger condition"),
        ],
        timeout: Annotated[float, Field(description="Timeout duration in seconds")],
        data_width: Annotated[
            Literal[8, 16, 24, 32],
            Field(description="Data width in bits"),
        ],
        data_value: DataValueField,
        clock_level: ClockThresholdField,
        miso_channel: Annotated[
            Optional[int],
            Field(ge=1, le=4, description="MISO channel (1-4, optional)"),
        ] = None,
        cs_channel: Annotated[
            Optional[int],
            Field(ge=1, le=4, description="Chip select channel (1-4, optional)"),
        ] = None,
        miso_level: Annotated[
            Optional[float],
            Field(description="MISO threshold voltage (required if miso_channel set)"),
        ] = None,
        cs_level: Annotated[
            Optional[float],
            Field(description="CS threshold voltage (required if cs_channel set)"),
        ] = None,
    ) -> SPITriggerResult:
        """
        Trigger on SPI bus data patterns.

        Detects SPI timeout conditions when no clock edges occur for the
        specified duration.

        Use cases:
        - Detecting bus idle/timeout conditions
        - Capturing specific data patterns
        """
        # Validate MISO/CS levels if channels are specified
        if miso_channel is not None and miso_level is None:
            raise ValueError("miso_level is required when miso_channel is set")
        if cs_channel is not None and cs_level is None:
            raise ValueError("cs_level is required when cs_channel is set")

        # Set trigger mode to SPI
        scope._write_checked(":TRIG:MODE SPI")

        # Set SCLK channel
        scope._write_checked(f":TRIG:SPI:CLK CHAN{sclk_channel}")

        # Set MISO channel if provided
        if miso_channel is not None:
            scope._write_checked(f":TRIG:SPI:MISO CHAN{miso_channel}")

        # Set CS channel if provided
        if cs_channel is not None:
            scope._write_checked(f":TRIG:SPI:CS CHAN{cs_channel}")

        # Set clock slope
        slope_map = {"POSITIVE": "POS", "NEGATIVE": "NEG"}
        scope._write_checked(f":TRIG:SPI:SLOP {slope_map[clock_slope]}")

        # Set when condition
        scope._write_checked(":TRIG:SPI:WHEN TOUT")

        # Set timeout
        scope._write_checked(f":TRIG:SPI:TIMeout {timeout}")

        # Set data width
        scope._write_checked(f":TRIG:SPI:WIDT {data_width}")

        # Set data value
        scope._write_checked(f":TRIG:SPI:DATA {data_value}")

        # Set voltage levels
        scope._write_checked(f":TRIG:SPI:CLEV {clock_level}")
        if miso_level is not None:
            scope._write_checked(f":TRIG:SPI:DLEV {miso_level}")
        if cs_level is not None:
            scope._write_checked(f":TRIG:SPI:SLEV {cs_level}")

        # Verify configuration
        actual_sclk = scope._query_checked(":TRIG:SPI:CLK?").strip()
        actual_slope = scope._query_checked(":TRIG:SPI:SLOP?").strip()
        actual_when = scope._query_checked(":TRIG:SPI:WHEN?").strip()
        actual_timeout = float(scope._query_checked(":TRIG:SPI:TIMeout?"))
        actual_width = int(scope._query_checked(":TRIG:SPI:WIDT?"))
        actual_data = int(scope._query_checked(":TRIG:SPI:DATA?"))
        actual_clevel = float(scope._query_checked(":TRIG:SPI:CLEV?"))

        actual_sclk_channel = _parse_channel_from_scpi(actual_sclk)

        # Read optional channels
        actual_miso: Optional[int] = None
        actual_cs: Optional[int] = None
        actual_miso_level: Optional[float] = None
        actual_cs_level: Optional[float] = None

        if miso_channel is not None:
            miso_source = scope._query_checked(":TRIG:SPI:MISO?").strip()
            actual_miso = _parse_channel_from_scpi(miso_source)
            actual_miso_level = float(scope._query_checked(":TRIG:SPI:DLEV?"))

        if cs_channel is not None:
            cs_source = scope._query_checked(":TRIG:SPI:CS?").strip()
            actual_cs = _parse_channel_from_scpi(cs_source)
            actual_cs_level = float(scope._query_checked(":TRIG:SPI:SLEV?"))

        slope_reverse = {"POS": "POSITIVE", "NEG": "NEGATIVE"}

        return SPITriggerResult(
            trigger_mode="SPI",
            sclk_channel=actual_sclk_channel,
            miso_channel=actual_miso,
            cs_channel=actual_cs,
            clock_slope=slope_reverse.get(actual_slope, clock_slope),
            when="TIMEOUT",
            timeout=actual_timeout,
            data_width=actual_width,
            data_value=actual_data,
            clock_level=actual_clevel,
            miso_level=actual_miso_level,
            cs_level=actual_cs_level,
        )

    @mcp.tool
    @with_scope_connection
    async def configure_can_trigger(
        channel: ChannelNumber,
        baud_rate: BaudRateField,
        signal_type: Annotated[
            Literal["RX", "TX", "DIFF"],
            Field(description="Signal type"),
        ],
        when: Annotated[
            Literal["START", "FRAME", "IDENTIFIER", "DATA", "ID_DATA", "ERROR", "END", "ACK"],
            Field(description="Trigger condition"),
        ],
        level: TriggerLevelField,
        sample_point: Annotated[
            int,
            Field(ge=5, le=95, description="Sample point percentage (5-95%)"),
        ] = 50,
        frame_type: Annotated[
            Literal["DATA", "REMOTE"],
            Field(description="Frame type"),
        ] = "DATA",
        id_type: Annotated[
            Literal["STANDARD", "EXTENDED"],
            Field(description="Identifier type"),
        ] = "STANDARD",
        identifier: Annotated[
            Optional[int],
            Field(description="CAN identifier (required for IDENTIFIER/ID_DATA modes)"),
        ] = None,
        data_bytes: Annotated[
            Optional[str],
            Field(description="Data pattern (hex string, required for DATA/ID_DATA modes)"),
        ] = None,
    ) -> CANTriggerResult:
        """
        Trigger on CAN bus frames and errors.

        Detects CAN protocol events including start of frame, specific identifiers,
        data patterns, errors, and acknowledgments.

        Use cases:
        - Triggering on specific CAN IDs
        - Detecting CAN errors
        - Capturing specific data frames
        """
        # Validate modes that require identifier or data
        if when in ["IDENTIFIER", "ID_DATA"] and identifier is None:
            raise ValueError(f"identifier is required when when='{when}'")
        if when in ["DATA", "ID_DATA"] and data_bytes is None:
            raise ValueError(f"data_bytes is required when when='{when}'")

        # Set trigger mode to CAN
        scope._write_checked(":TRIG:MODE CAN")

        # Set source channel
        scope._write_checked(f":TRIG:CAN:SOUR CHAN{channel}")

        # Set baud rate
        scope._write_checked(f":TRIG:CAN:BAUD {baud_rate}")

        # Map signal type to SCPI format (trigger uses different values than decode)
        signal_trigger_map = {
            "RX": "H",
            "TX": "L",
            "DIFF": "DIFF",
        }
        signal_scpi = signal_trigger_map.get(signal_type, signal_type)
        scope._write_checked(f":TRIG:CAN:STYPE {signal_scpi}")

        # Map when condition to SCPI format
        when_map = {
            "START": "SOF",
            "FRAME": "IDFR",
            "IDENTIFIER": "ID",
            "DATA": "DATA",
            "ID_DATA": "IDD",
            "ERROR": "ERR",
            "END": "EOF",
            "ACK": "ACK",
        }
        scope._write_checked(f":TRIG:CAN:WHEN {when_map[when]}")

        # Set sample point
        scope._write_checked(f":TRIG:CAN:SPOint {sample_point}")

        # Set frame type
        frame_scpi = CANFrameType[frame_type].value
        scope._write_checked(f":TRIG:CAN:DEFine {frame_scpi}")

        # Set ID type
        id_scpi = CANIDType[id_type].value
        scope._write_checked(f":TRIG:CAN:EXTended {id_scpi}")

        # Set identifier if needed
        if when in ["IDENTIFIER", "ID_DATA"] and identifier is not None:
            scope._write_checked(f":TRIG:CAN:ID {identifier}")

        # Set data if needed
        if when in ["DATA", "ID_DATA"] and data_bytes is not None:
            scope._write_checked(f":TRIG:CAN:DATA {data_bytes}")

        # Set trigger level
        scope._write_checked(f":TRIG:CAN:LEV {level}")

        # Verify configuration
        actual_source = scope._query_checked(":TRIG:CAN:SOUR?").strip()
        actual_baud = int(scope._query_checked(":TRIG:CAN:BAUD?"))
        actual_signal = scope._query_checked(":TRIG:CAN:STYPE?").strip()
        actual_when = scope._query_checked(":TRIG:CAN:WHEN?").strip()
        actual_sample = int(scope._query_checked(":TRIG:CAN:SPOint?"))
        actual_frame = scope._query_checked(":TRIG:CAN:DEFine?").strip()
        actual_id_type = scope._query_checked(":TRIG:CAN:EXTended?").strip()
        actual_level = float(scope._query_checked(":TRIG:CAN:LEV?"))

        actual_channel = _parse_channel_from_scpi(actual_source)

        # Read identifier and data if applicable
        actual_id: Optional[int] = None
        actual_data: Optional[str] = None
        if when in ["IDENTIFIER", "ID_DATA"]:
            actual_id = int(scope._query_checked(":TRIG:CAN:ID?"))
        if when in ["DATA", "ID_DATA"]:
            actual_data = scope._query_checked(":TRIG:CAN:DATA?").strip()

        # Map responses back
        when_reverse = {
            "SOF": "START",
            "IDFR": "FRAME",
            "ID": "IDENTIFIER",
            "DATA": "DATA",
            "IDD": "ID_DATA",
            "ERR": "ERROR",
            "EOF": "END",
            "ACK": "ACK",
        }
        signal_reverse = {"H": "RX", "L": "TX", "DIFF": "DIFF", "RXTX": "DIFF"}
        frame_reverse = {"DATA": "DATA", "REM": "REMOTE"}
        id_type_reverse = {"STAN": "STANDARD", "EXT": "EXTENDED"}

        return CANTriggerResult(
            trigger_mode="CAN",
            channel=actual_channel,
            baud_rate=actual_baud,
            signal_type=signal_reverse.get(actual_signal, signal_type),
            when=when_reverse.get(actual_when, when),
            sample_point=actual_sample,
            frame_type=frame_reverse.get(actual_frame, frame_type),
            id_type=id_type_reverse.get(actual_id_type, id_type),
            identifier=actual_id,
            data_bytes=actual_data,
            level=actual_level,
        )

    @mcp.tool
    @with_scope_connection
    async def configure_lin_trigger(
        channel: ChannelNumber,
        standard: Annotated[
            Literal["V1_0", "V2_0", "V2_1", "V2_2"],
            Field(description="LIN version"),
        ],
        baud_rate: BaudRateField,
        when: Annotated[
            Literal["SYNC", "IDENTIFIER", "DATA", "ID_DATA", "ERROR", "WAKEUP"],
            Field(description="Trigger condition"),
        ],
        level: TriggerLevelField,
        error_type: Annotated[
            Optional[Literal["SYNC_ERROR", "PARITY_ERROR", "CHECKSUM_ERROR", "TIMEOUT_ERROR"]],
            Field(description="Error type (required for ERROR mode)"),
        ] = None,
        identifier: Annotated[
            Optional[int],
            Field(ge=0, le=63, description="LIN identifier (0-63, required for IDENTIFIER/ID_DATA modes)"),
        ] = None,
        data_bytes: Annotated[
            Optional[str],
            Field(description="Data pattern (hex string, required for DATA/ID_DATA modes)"),
        ] = None,
    ) -> LINTriggerResult:
        """
        Trigger on LIN bus frames and errors.

        Detects LIN protocol events including sync fields, identifiers,
        data patterns, errors, and wakeup signals.

        Use cases:
        - Triggering on specific LIN IDs
        - Detecting LIN protocol errors
        - Capturing wakeup signals
        """
        # Validate modes that require specific parameters
        if when == "ERROR" and error_type is None:
            raise ValueError("error_type is required when when='ERROR'")
        if when in ["IDENTIFIER", "ID_DATA"] and identifier is None:
            raise ValueError(f"identifier is required when when='{when}'")
        if when in ["DATA", "ID_DATA"] and data_bytes is None:
            raise ValueError(f"data_bytes is required when when='{when}'")

        # Set trigger mode to LIN
        scope._write_checked(":TRIG:MODE LIN")

        # Set source channel
        scope._write_checked(f":TRIG:LIN:SOUR CHAN{channel}")

        # Map standard to SCPI format (trigger uses different values than decode)
        standard_trigger_map = {
            "V1_X": "1X",
            "V2_X": "2X",
            "MIXED": "BOTH",
        }
        standard_scpi = standard_trigger_map.get(standard, standard)
        scope._write_checked(f":TRIG:LIN:STAN {standard_scpi}")

        # Set baud rate
        scope._write_checked(f":TRIG:LIN:BAUD {baud_rate}")

        # Map when condition to SCPI format
        when_map = {
            "SYNC": "SYNCbreak",
            "IDENTIFIER": "ID",
            "DATA": "DATA",
            "ID_DATA": "IDData",
            "ERROR": "ERR",
            "WAKEUP": "AWAK",
        }
        scope._write_checked(f":TRIG:LIN:WHEN {when_map[when]}")

        # Set error type if ERROR mode
        if when == "ERROR" and error_type is not None:
            error_scpi = LINErrorType[error_type].value
            scope._write_checked(f":TRIG:LIN:ERRor {error_scpi}")

        # Set identifier if needed
        if when in ["IDENTIFIER", "ID_DATA"] and identifier is not None:
            scope._write_checked(f":TRIG:LIN:ID {identifier}")

        # Set data if needed
        if when in ["DATA", "ID_DATA"] and data_bytes is not None:
            scope._write_checked(f":TRIG:LIN:DATA {data_bytes}")

        # Set trigger level
        scope._write_checked(f":TRIG:LIN:LEV {level}")

        # Verify configuration
        actual_source = scope._query_checked(":TRIG:LIN:SOUR?").strip()
        actual_standard = scope._query_checked(":TRIG:LIN:STAN?").strip()
        actual_baud = int(scope._query_checked(":TRIG:LIN:BAUD?"))
        actual_when = scope._query_checked(":TRIG:LIN:WHEN?").strip()
        actual_level = float(scope._query_checked(":TRIG:LIN:LEV?"))

        actual_channel = _parse_channel_from_scpi(actual_source)

        # Read optional fields
        actual_error: Optional[str] = None
        actual_id: Optional[int] = None
        actual_data: Optional[str] = None

        if when == "ERROR":
            err_type = scope._query_checked(":TRIG:LIN:ERRor?").strip()
            error_reverse = {
                "SYNC": "SYNC_ERROR",
                "ID": "PARITY_ERROR",
                "CHECk": "CHECKSUM_ERROR",
            }
            actual_error = error_reverse.get(err_type)

        if when in ["IDENTIFIER", "ID_DATA"]:
            actual_id = int(scope._query_checked(":TRIG:LIN:ID?"))

        if when in ["DATA", "ID_DATA"]:
            actual_data = scope._query_checked(":TRIG:LIN:DATA?").strip()

        # Map responses back
        when_reverse = {
            "SYNC": "SYNC",
            "SYNCbreak": "SYNC",
            "ID": "IDENTIFIER",
            "DATA": "DATA",
            "IDD": "ID_DATA",
            "IDData": "ID_DATA",
            "ERR": "ERROR",
            "AWAK": "WAKEUP",
        }
        standard_reverse = {"1X": "V1_X", "2X": "V2_X", "BOTH": "MIXED"}

        return LINTriggerResult(
            trigger_mode="LIN",
            channel=actual_channel,
            standard=standard_reverse.get(actual_standard, standard),
            baud_rate=actual_baud,
            when=when_reverse.get(actual_when, when),
            error_type=actual_error,
            identifier=actual_id,
            data_bytes=actual_data,
            level=actual_level,
        )

    # === BUS DECODE CONFIGURATION ===

    @mcp.tool
    @with_scope_connection
    async def configure_parallel_bus(
        bus_number: BusNumberField,
        bit_assignments: Annotated[
            dict[int, int],
            Field(description="Dictionary mapping bit positions (0-7) to channels (1-4)"),
        ],
        width: Annotated[
            int,
            Field(ge=1, le=8, description="Bus width in bits (1-8)"),
        ],
        clock_channel: Annotated[
            Optional[int],
            Field(ge=1, le=4, description="Clock channel (1-4, optional)"),
        ] = None,
        clock_polarity: Annotated[
            Literal["POSITIVE", "NEGATIVE"],
            Field(description="Clock edge"),
        ] = "POSITIVE",
        bit_order: Annotated[
            Literal["LSB", "MSB"],
            Field(description="Bit endianness"),
        ] = "LSB",
    ) -> ParallelBusResult:
        """
        Configure parallel bus decode (up to 8 bits).

        Sets up parallel bus decoding with configurable bit assignments,
        optional clock, and bit ordering.

        Use cases:
        - Decoding parallel data buses
        - Analyzing microprocessor buses
        """
        # Set bus mode to PARALLEL
        scope._write_checked(f":BUS{bus_number}:MODE PAR")

        # Set bus width
        scope._write_checked(f":BUS{bus_number}:PAR:WIDT {width}")

        # Set bit assignments
        for bit_pos, chan in bit_assignments.items():
            if bit_pos < 0 or bit_pos >= width:
                raise ValueError(f"Bit position {bit_pos} out of range for width {width}")
            # Use two-step sequence: first select the bit, then set its source
            scope._write_checked(f":BUS{bus_number}:PAR:BITX {bit_pos}")
            scope._write_checked(f":BUS{bus_number}:PAR:SOUR CHAN{chan}")

        # Set clock channel if provided
        if clock_channel is not None:
            scope._write_checked(f":BUS{bus_number}:PAR:CLK CHAN{clock_channel}")

        # Set clock polarity
        polarity_scpi = "POS" if clock_polarity == "POSITIVE" else "NEG"
        scope._write_checked(f":BUS{bus_number}:PAR:SLOP {polarity_scpi}")

        # Set bit order
        bit_order_scpi = BitOrder[bit_order].value
        scope._write_checked(f":BUS{bus_number}:PAR:END {bit_order_scpi}")

        # Verify configuration
        actual_width = int(scope._query_checked(f":BUS{bus_number}:PAR:WIDT?"))
        actual_polarity = scope._query_checked(f":BUS{bus_number}:PAR:SLOP?").strip()
        actual_bit_order = scope._query_checked(f":BUS{bus_number}:PAR:END?").strip()

        # Read back bit assignments (using two-step sequence)
        verified_assignments = {}
        for bit_pos in range(actual_width):
            scope._write_checked(f":BUS{bus_number}:PAR:BITX {bit_pos}")
            bit_source = scope._query_checked(f":BUS{bus_number}:PAR:SOUR?").strip()
            verified_assignments[bit_pos] = _parse_channel_from_scpi(bit_source)

        # Read clock channel if configured
        actual_clock: Optional[int] = None
        if clock_channel is not None:
            clock_source = scope._query_checked(f":BUS{bus_number}:PAR:CLK?").strip()
            actual_clock = _parse_channel_from_scpi(clock_source)

        polarity_reverse = {"POS": "POSITIVE", "NEG": "NEGATIVE"}
        bit_order_reverse = {"LSB": "LSB", "MSB": "MSB"}

        return ParallelBusResult(
            bus_number=bus_number,
            bus_mode="PARALLEL",
            bit_assignments=verified_assignments,
            clock_channel=actual_clock,
            width=actual_width,
            clock_polarity=polarity_reverse.get(actual_polarity, clock_polarity),
            bit_order=bit_order_reverse.get(actual_bit_order, bit_order),
        )

    @mcp.tool
    @with_scope_connection
    async def configure_rs232_bus(
        bus_number: BusNumberField,
        baud_rate: BaudRateField,
        parity: Annotated[
            Literal["NONE", "EVEN", "ODD", "MARK", "SPACE"],
            Field(description="Parity setting"),
        ],
        stop_bits: Annotated[
            Literal["1", "1.5", "2"],
            Field(description="Stop bits"),
        ],
        polarity: Annotated[
            Literal["POSITIVE", "NEGATIVE"],
            Field(description="Signal polarity"),
        ],
        bit_order: Annotated[
            Literal["LSB", "MSB"],
            Field(description="Bit endianness"),
        ],
        tx_channel: Annotated[
            Optional[int],
            Field(ge=1, le=4, description="TX channel (optional)"),
        ] = None,
        rx_channel: Annotated[
            Optional[int],
            Field(ge=1, le=4, description="RX channel (optional)"),
        ] = None,
        data_bits: Annotated[
            Literal[5, 6, 7, 8, 9],
            Field(description="Number of data bits"),
        ] = 8,
    ) -> RS232BusResult:
        """
        Configure UART/RS232 bus decode.

        Sets up RS232/UART bus decoding with configurable TX/RX channels,
        baud rate, parity, and data format.

        Use cases:
        - Decoding UART communication
        - Analyzing serial protocols
        """
        # Set bus mode to RS232
        scope._write_checked(f":BUS{bus_number}:MODE RS232")

        # Set TX channel if provided
        if tx_channel is not None:
            scope._write_checked(f":BUS{bus_number}:RS232:TX CHAN{tx_channel}")

        # Set RX channel if provided
        if rx_channel is not None:
            scope._write_checked(f":BUS{bus_number}:RS232:RX CHAN{rx_channel}")

        # Set polarity
        polarity_scpi = "POS" if polarity == "POSITIVE" else "NEG"
        scope._write_checked(f":BUS{bus_number}:RS232:POL {polarity_scpi}")

        # Set parity
        parity_scpi = SerialParity[parity].value
        scope._write_checked(f":BUS{bus_number}:RS232:PAR {parity_scpi}")

        # Set bit order
        bit_order_scpi = BitOrder[bit_order].value
        scope._write_checked(f":BUS{bus_number}:RS232:END {bit_order_scpi}")

        # Set baud rate
        scope._write_checked(f":BUS{bus_number}:RS232:BAUD {baud_rate}")

        # Set data bits
        scope._write_checked(f":BUS{bus_number}:RS232:DBIT {data_bits}")

        # Set stop bits
        scope._write_checked(f":BUS{bus_number}:RS232:SBIT {stop_bits}")

        # Verify configuration
        actual_polarity = scope._query_checked(f":BUS{bus_number}:RS232:POL?").strip()
        actual_parity = scope._query_checked(f":BUS{bus_number}:RS232:PAR?").strip()
        actual_bit_order = scope._query_checked(f":BUS{bus_number}:RS232:END?").strip()
        actual_baud = int(scope._query_checked(f":BUS{bus_number}:RS232:BAUD?"))
        actual_data_bits = int(scope._query_checked(f":BUS{bus_number}:RS232:DBIT?"))
        actual_stop_bits = scope._query_checked(f":BUS{bus_number}:RS232:SBIT?").strip()

        # Read TX/RX channels if configured
        actual_tx: Optional[int] = None
        actual_rx: Optional[int] = None
        if tx_channel is not None:
            tx_source = scope._query_checked(f":BUS{bus_number}:RS232:TX?").strip()
            actual_tx = _parse_channel_from_scpi(tx_source)
        if rx_channel is not None:
            rx_source = scope._query_checked(f":BUS{bus_number}:RS232:RX?").strip()
            actual_rx = _parse_channel_from_scpi(rx_source)

        polarity_reverse = {"POS": "POSITIVE", "NEG": "NEGATIVE"}
        parity_reverse = {"NONE": "NONE", "EVEN": "EVEN", "ODD": "ODD", "MARK": "MARK", "SPAC": "SPACE"}
        bit_order_reverse = {"LSB": "LSB", "MSB": "MSB"}

        return RS232BusResult(
            bus_number=bus_number,
            bus_mode="RS232",
            tx_channel=actual_tx,
            rx_channel=actual_rx,
            polarity=polarity_reverse.get(actual_polarity, polarity),
            parity=parity_reverse.get(actual_parity, parity),
            bit_order=bit_order_reverse.get(actual_bit_order, bit_order),
            baud_rate=actual_baud,
            data_bits=actual_data_bits,
            stop_bits=actual_stop_bits,
        )

    @mcp.tool
    @with_scope_connection
    async def configure_i2c_bus(
        bus_number: BusNumberField,
        scl_channel: ChannelNumber,
        sda_channel: ChannelNumber,
        address_width: Annotated[
            Literal["7", "10"],
            Field(description="Address width (7 or 10 bits)"),
        ] = "7",
    ) -> I2CBusResult:
        """
        Configure I2C bus decode.

        Sets up I2C bus decoding with SCL/SDA channels and address width.

        Use cases:
        - Decoding I2C communication
        - Analyzing I2C devices
        """
        # Set bus mode to I2C
        scope._write_checked(f":BUS{bus_number}:MODE IIC")

        # Set SCL and SDA channels
        scope._write_checked(f":BUS{bus_number}:IIC:SCLK:SOUR CHAN{scl_channel}")
        scope._write_checked(f":BUS{bus_number}:IIC:SDA:SOUR CHAN{sda_channel}")

        # Set address width (translate numeric to SCPI format)
        addr_map = {"7": "NORM", "10": "RW"}
        addr_scpi = addr_map.get(str(address_width), "NORM")
        scope._write_checked(f":BUS{bus_number}:IIC:ADDR {addr_scpi}")

        # Verify configuration
        actual_scl = scope._query_checked(f":BUS{bus_number}:IIC:SCLK:SOUR?").strip()
        actual_sda = scope._query_checked(f":BUS{bus_number}:IIC:SDA:SOUR?").strip()
        actual_width_scpi = scope._query_checked(f":BUS{bus_number}:IIC:ADDR?").strip()

        actual_scl_channel = _parse_channel_from_scpi(actual_scl)
        actual_sda_channel = _parse_channel_from_scpi(actual_sda)

        # Translate SCPI address width back to numeric
        addr_reverse = {"NORM": "7", "RW": "10"}
        actual_width = addr_reverse.get(actual_width_scpi, address_width)

        return I2CBusResult(
            bus_number=bus_number,
            bus_mode="I2C",
            scl_channel=actual_scl_channel,
            sda_channel=actual_sda_channel,
            address_width=actual_width,
        )

    @mcp.tool
    @with_scope_connection
    async def configure_spi_bus(
        bus_number: BusNumberField,
        sclk_channel: ChannelNumber,
        clock_polarity: Annotated[
            Literal["POSITIVE", "NEGATIVE"],
            Field(description="Clock polarity"),
        ],
        data_bits: Annotated[
            Literal[4, 8, 16, 24, 32],
            Field(description="Data width in bits"),
        ],
        bit_order: Annotated[
            Literal["LSB", "MSB"],
            Field(description="Bit endianness"),
        ],
        spi_mode: Annotated[
            Literal["MODE_0", "MODE_1", "MODE_2", "MODE_3"],
            Field(description="SPI mode (CPOL/CPHA combination)"),
        ],
        timeout: Annotated[float, Field(description="Frame timeout in seconds")],
        miso_channel: Annotated[
            Optional[int],
            Field(ge=1, le=4, description="MISO channel (optional)"),
        ] = None,
        mosi_channel: Annotated[
            Optional[int],
            Field(ge=1, le=4, description="MOSI channel (optional)"),
        ] = None,
        ss_channel: Annotated[
            Optional[int],
            Field(ge=1, le=4, description="Slave select channel (optional)"),
        ] = None,
    ) -> SPIBusResult:
        """
        Configure SPI bus decode.

        Sets up SPI bus decoding with clock, data lines, and protocol parameters.

        Use cases:
        - Decoding SPI communication
        - Analyzing SPI devices
        """
        # Set bus mode to SPI
        scope._write_checked(f":BUS{bus_number}:MODE SPI")

        # Set SCLK channel
        scope._write_checked(f":BUS{bus_number}:SPI:SCLK:SOUR CHAN{sclk_channel}")

        # Set optional channels
        if miso_channel is not None:
            scope._write_checked(f":BUS{bus_number}:SPI:MISO:SOUR CHAN{miso_channel}")
        if mosi_channel is not None:
            scope._write_checked(f":BUS{bus_number}:SPI:MOSI:SOUR CHAN{mosi_channel}")
        if ss_channel is not None:
            scope._write_checked(f":BUS{bus_number}:SPI:SS:SOUR CHAN{ss_channel}")

        # Set clock slope/polarity
        polarity_scpi = "POS" if clock_polarity == "POSITIVE" else "NEG"
        scope._write_checked(f":BUS{bus_number}:SPI:SCLK:SLOP {polarity_scpi}")

        # Set data bits
        scope._write_checked(f":BUS{bus_number}:SPI:DBIT {data_bits}")

        # Set bit order
        bit_order_scpi = BitOrder[bit_order].value
        scope._write_checked(f":BUS{bus_number}:SPI:END {bit_order_scpi}")

        # Set SPI mode
        spi_mode_scpi = SPIMode[spi_mode].value
        scope._write_checked(f":BUS{bus_number}:SPI:MODE {spi_mode_scpi}")

        # Set timeout
        scope._write_checked(f":BUS{bus_number}:SPI:TIMeout:TIME {timeout}")

        # Verify configuration
        actual_sclk = scope._query_checked(f":BUS{bus_number}:SPI:SCLK:SOUR?").strip()
        actual_polarity = scope._query_checked(f":BUS{bus_number}:SPI:SCLK:SLOP?").strip()
        actual_data_bits = int(scope._query_checked(f":BUS{bus_number}:SPI:DBIT?"))
        actual_bit_order = scope._query_checked(f":BUS{bus_number}:SPI:END?").strip()
        actual_spi_mode = scope._query_checked(f":BUS{bus_number}:SPI:MODE?").strip()
        actual_timeout = float(scope._query_checked(f":BUS{bus_number}:SPI:TIMeout:TIME?"))

        actual_sclk_channel = _parse_channel_from_scpi(actual_sclk)

        # Read optional channels
        actual_miso: Optional[int] = None
        actual_mosi: Optional[int] = None
        actual_ss: Optional[int] = None
        if miso_channel is not None:
            miso_source = scope._query_checked(f":BUS{bus_number}:SPI:MISO:SOUR?").strip()
            actual_miso = _parse_channel_from_scpi(miso_source)
        if mosi_channel is not None:
            mosi_source = scope._query_checked(f":BUS{bus_number}:SPI:MOSI:SOUR?").strip()
            actual_mosi = _parse_channel_from_scpi(mosi_source)
        if ss_channel is not None:
            ss_source = scope._query_checked(f":BUS{bus_number}:SPI:SS:SOUR?").strip()
            actual_ss = _parse_channel_from_scpi(ss_source)

        polarity_reverse = {"POS": "POSITIVE", "NEG": "NEGATIVE"}
        bit_order_reverse = {"LSB": "LSB", "MSB": "MSB"}
        # Map SCPI mode back to user-friendly enum
        mode_reverse = {
            "CPOL0CPHA0": "MODE_0",
            "CPOL0CPHA1": "MODE_1",
            "CPOL1CPHA0": "MODE_2",
            "CPOL1CPHA1": "MODE_3",
        }

        return SPIBusResult(
            bus_number=bus_number,
            bus_mode="SPI",
            sclk_channel=actual_sclk_channel,
            miso_channel=actual_miso,
            mosi_channel=actual_mosi,
            ss_channel=actual_ss,
            clock_polarity=polarity_reverse.get(actual_polarity, clock_polarity),
            data_bits=actual_data_bits,
            bit_order=bit_order_reverse.get(actual_bit_order, bit_order),
            spi_mode=mode_reverse.get(actual_spi_mode, spi_mode),
            timeout=actual_timeout,
        )

    @mcp.tool
    @with_scope_connection
    async def configure_can_bus(
        bus_number: BusNumberField,
        source_channel: ChannelNumber,
        signal_type: Annotated[
            Literal["RX", "TX", "DIFF"],
            Field(description="Signal type"),
        ],
        baud_rate: BaudRateField,
        sample_point: Annotated[
            int,
            Field(ge=5, le=95, description="Sample point percentage (5-95%)"),
        ] = 50,
    ) -> CANBusResult:
        """
        Configure CAN bus decode.

        Sets up CAN bus decoding with signal source, baud rate, and sample point.

        Use cases:
        - Decoding CAN communication
        - Analyzing automotive networks
        """
        # Set bus mode to CAN
        scope._write_checked(f":BUS{bus_number}:MODE CAN")

        # Set source channel
        scope._write_checked(f":BUS{bus_number}:CAN:SOUR CHAN{source_channel}")

        # Set signal type
        signal_scpi = CANSignalType[signal_type].value
        scope._write_checked(f":BUS{bus_number}:CAN:STYPE {signal_scpi}")

        # Set baud rate
        scope._write_checked(f":BUS{bus_number}:CAN:BAUD {baud_rate}")

        # Set sample point
        scope._write_checked(f":BUS{bus_number}:CAN:SPOint {sample_point}")

        # Verify configuration
        actual_source = scope._query_checked(f":BUS{bus_number}:CAN:SOUR?").strip()
        actual_signal = scope._query_checked(f":BUS{bus_number}:CAN:STYPE?").strip()
        actual_baud = int(scope._query_checked(f":BUS{bus_number}:CAN:BAUD?"))
        actual_sample = int(scope._query_checked(f":BUS{bus_number}:CAN:SPOint?"))

        actual_source_channel = _parse_channel_from_scpi(actual_source)

        signal_reverse = {"RX": "RX", "TX": "TX", "DIFF": "DIFF"}

        return CANBusResult(
            bus_number=bus_number,
            bus_mode="CAN",
            source_channel=actual_source_channel,
            signal_type=signal_reverse.get(actual_signal, signal_type),
            baud_rate=actual_baud,
            sample_point=actual_sample,
        )

    @mcp.tool
    @with_scope_connection
    async def configure_lin_bus(
        bus_number: BusNumberField,
        source_channel: ChannelNumber,
        parity: Annotated[
            Literal["ENHANCED", "CLASSIC"],
            Field(description="Parity mode"),
        ],
        standard: Annotated[
            Literal["V1_X", "V2_X", "MIXED"],
            Field(description="LIN version"),
        ],
    ) -> LINBusResult:
        """
        Configure LIN bus decode.

        Sets up LIN bus decoding with source channel, parity mode, and LIN version.

        Use cases:
        - Decoding LIN communication
        - Analyzing automotive LIN networks
        """
        # Set bus mode to LIN
        scope._write_checked(f":BUS{bus_number}:MODE LIN")

        # Set source channel
        scope._write_checked(f":BUS{bus_number}:LIN:SOUR CHAN{source_channel}")

        # Set parity
        parity_scpi = "ON" if parity == "ENHANCED" else "OFF"
        scope._write_checked(f":BUS{bus_number}:LIN:PAR {parity_scpi}")

        # Set standard
        standard_scpi = LINStandard[standard].value
        scope._write_checked(f":BUS{bus_number}:LIN:STAN {standard_scpi}")

        # Verify configuration
        actual_source = scope._query_checked(f":BUS{bus_number}:LIN:SOUR?").strip()
        actual_parity = scope._query_checked(f":BUS{bus_number}:LIN:PAR?").strip()
        actual_standard = scope._query_checked(f":BUS{bus_number}:LIN:STAN?").strip()

        actual_source_channel = _parse_channel_from_scpi(actual_source)

        parity_reverse = {"ON": "ENHANCED", "OFF": "CLASSIC"}
        standard_reverse = {"V1X": "V1_X", "V2X": "V2_X", "MIX": "MIXED"}

        return LINBusResult(
            bus_number=bus_number,
            bus_mode="LIN",
            source_channel=actual_source_channel,
            parity=parity_reverse.get(actual_parity, parity),
            standard=standard_reverse.get(actual_standard, standard),
        )

    # === BUS UTILITY TOOLS ===

    @mcp.tool
    @with_scope_connection
    async def set_bus_display(
        bus_number: BusNumberField,
        enabled: Annotated[bool, Field(description="Enable/disable bus decode display")],
    ) -> BusDisplayResult:
        """
        Enable or disable bus decode display on screen.

        Controls whether the decoded bus data is displayed on the oscilloscope screen.
        """
        # Set bus display
        display_cmd = "ON" if enabled else "OFF"
        scope._write_checked(f":BUS{bus_number}:DISP {display_cmd}")

        # Verify
        actual_display = scope._query_checked(f":BUS{bus_number}:DISP?").strip()
        actual_enabled = actual_display == "1" or actual_display.upper() == "ON"

        return BusDisplayResult(
            bus_number=bus_number,
            enabled=actual_enabled,
        )

    @mcp.tool
    @with_scope_connection
    async def set_bus_format(
        bus_number: BusNumberField,
        format: Annotated[
            Literal["HEX", "DEC", "BIN", "ASCII"],
            Field(description="Display format"),
        ],
    ) -> BusFormatResult:
        """
        Set bus decode display format.

        Controls how decoded bus data is formatted on the screen (hexadecimal,
        decimal, binary, or ASCII).
        """
        # Set bus format
        format_scpi = BusFormat[format].value
        scope._write_checked(f":BUS{bus_number}:FORM {format_scpi}")

        # Verify
        actual_format = scope._query_checked(f":BUS{bus_number}:FORM?").strip()

        format_reverse = {"HEX": "HEX", "DEC": "DEC", "BIN": "BIN", "ASC": "ASCII"}

        return BusFormatResult(
            bus_number=bus_number,
            format=format_reverse.get(actual_format, format),
        )

    @mcp.tool
    @with_scope_connection
    async def get_bus_decoded_data(
        bus_number: BusNumberField,
    ) -> BusDataResult:
        """
        Retrieve decoded bus data from screen.

        Returns the currently decoded bus data as displayed on the oscilloscope.
        """
        # Query decoded bus data
        decoded_data = scope._query_checked(f":BUS{bus_number}:DATA?").strip()

        return BusDataResult(
            bus_number=bus_number,
            decoded_data=decoded_data,
        )

    @mcp.tool
    @with_scope_connection
    async def export_bus_data(
        ctx: Context,
        bus_number: BusNumberField,
        local_filepath: Annotated[str, Field(description="Local path to save CSV file")],
    ) -> BusExportResult:
        """
        Export decoded bus data to CSV file.

        Exports the decoded data from the protocol analyzer to a CSV file containing
        timestamps, decoded values, and protocol-specific fields.

        Note:
        - CSV contains timestamp, decoded values, and protocol-specific fields
        """
        # Generate random 8-char lowercase hex filename to avoid overwriting
        csv_filename = f"{os.urandom(4).hex()}.csv"
        csv_scope_path = f"C:/{csv_filename}"

        await ctx.report_progress(
            progress=0.3, message=f"Exporting bus {bus_number} data on scope..."
        )

        # Export bus data to CSV on scope
        scope._write_checked(f":BUS{bus_number}:EEXP '{csv_scope_path}'")

        # Wait for export to complete
        await asyncio.sleep(0.5)

        await ctx.report_progress(progress=0.6, message="Downloading CSV file...")

        # Download via FTP
        scope_ip = scope.extract_ip_from_resource()
        if not scope_ip:
            raise Exception("Could not extract IP address - network connection required")

        if not scope.download_file_via_ftp(scope_ip, csv_filename, local_filepath):
            raise Exception("Failed to download CSV file via FTP")

        bytes_downloaded = os.path.getsize(local_filepath)

        await ctx.report_progress(
            progress=1.0, message=f"Export complete: {to_client_path(local_filepath)}"
        )

        return BusExportResult(
            bus_number=bus_number,
            file_path=to_client_path(local_filepath) or local_filepath,
            bytes_downloaded=bytes_downloaded,
        )

    # === MEMORY & ACQUISITION SETTINGS ===

    @mcp.tool
    @with_scope_connection
    async def set_memory_depth(
        memory_depth: Annotated[MemoryDepth, Field(description="Memory depth setting")]
    ) -> MemoryDepthResult:
        """
        Set acquisition memory depth.
        """
        scope._write_checked(f":ACQ:MDEP {memory_depth.value}")

        # Verify the setting
        actual_depth = float(scope._query_checked(":ACQ:MDEP?"))

        # Convert to human-readable format
        if actual_depth >= 1e6:
            depth_str = f"{actual_depth/1e6:.0f}M"
        elif actual_depth >= 1e3:
            depth_str = f"{actual_depth/1e3:.0f}K"
        else:
            depth_str = f"{actual_depth:.0f}"

        return MemoryDepthResult(memory_depth=actual_depth, memory_depth_str=depth_str)

    @mcp.tool
    @with_scope_connection
    async def set_acquisition_type(
        acquisition_type: Annotated[
            AcquisitionType, Field(description="Acquisition type")
        ]
    ) -> AcquisitionTypeResult:
        """
        Set acquisition type.
        """
        # Map enum to SCPI format
        type_map = {
            AcquisitionType.NORMAL: "NORMal",
            AcquisitionType.AVERAGE: "AVERages",
            AcquisitionType.PEAK: "PEAK",
            AcquisitionType.ULTRA: "ULTRa",
        }

        scpi_type = type_map[acquisition_type]
        scope._write_checked(f":ACQ:TYPE {scpi_type}")

        # Verify the setting
        actual_type = scope._query_checked(":ACQ:TYPE?").strip()

        return AcquisitionTypeResult(acquisition_type=map_acquisition_type(actual_type))

    # === PRIORITY 1: ACQUISITION SETTINGS ===

    @mcp.tool
    @with_scope_connection
    async def set_acquisition_averages(averages: AveragesCountField) -> AcquisitionAveragesResult:
        """
        Set number of averages when acquisition type is AVERAGE.

        Note: Only applies when acquisition type is set to AVERAGE. Use with set_acquisition_type("AVERAGE").
        """
        scope._write_checked(f":ACQ:AVER {averages}")

        # Verify the setting
        actual_averages = int(scope._query_checked(":ACQ:AVER?"))

        return AcquisitionAveragesResult(
            averages=actual_averages,
            message=f"Averages set to {actual_averages}"
        )

    @mcp.tool
    @with_scope_connection
    async def configure_ultra_acquisition(
        display_mode: Annotated[UltraDisplayMode, Field(description="Display mode for waveform segments")],
        timeout: UltraTimeoutField,
        max_frames: MaxFramesField
    ) -> UltraAcquisitionResult:
        """
        Configure Ultra Acquisition mode for high-speed waveform capture.

        Ultra Acquisition mode captures waveforms at maximum speed for anomaly detection.
        Automatically disables conflicting features (cursor, search, zoom, etc.) before enabling.
        """
        # Disable conflicting features first
        scope._disable_ultra_conflicting_features()

        # Set acquisition type to Ultra
        scope._write_checked(":ACQ:TYPE ULTRa")

        # Set Ultra display mode
        scope._write_checked(f":ACQ:ULTR:MODE {display_mode.value}")

        # Set timeout
        scope._write_checked(f":ACQ:ULTR:TIMeout {timeout}")

        # Set max frames
        scope._write_checked(f":ACQ:ULTR:MAXFrame {max_frames}")

        # Verify settings
        actual_mode_str = scope._query_checked(":ACQ:ULTR:MODE?").strip()
        actual_timeout = float(scope._query_checked(":ACQ:ULTR:TIMeout?"))
        actual_max_frames = int(float(scope._query_checked(":ACQ:ULTR:MAXFrame?")))

        # Map SCPI response to enum
        mode_map = {
            "ADJ": UltraDisplayMode.ADJACENT,
            "OVER": UltraDisplayMode.OVERLAY,
            "WAT": UltraDisplayMode.WATERFALL,
            "PERS": UltraDisplayMode.PERSPECTIVE,
            "MOS": UltraDisplayMode.MOSAIC,
        }
        actual_mode = mode_map.get(actual_mode_str, display_mode)

        return UltraAcquisitionResult(
            display_mode=actual_mode,
            timeout=actual_timeout,
            max_frames=actual_max_frames,
            message=f"Ultra Acquisition configured: {actual_mode.value} display, {actual_timeout}s timeout, {actual_max_frames} max frames"
        )

    @mcp.tool
    @with_scope_connection
    async def get_sample_rate() -> SampleRateResult:
        """
        Get current sample rate.
        """
        sample_rate = float(scope._query_checked(":ACQ:SRAT?"))

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
            sample_rate=sample_rate, sample_rate_str=rate_str, units="Sa/s"
        )

    # === UTILITY TOOLS ===

    @mcp.tool
    @with_scope_connection
    async def auto_setup() -> ActionResult:
        """
        Perform automatic setup of the oscilloscope.

        Automatically configures vertical scale, horizontal scale, and trigger
        settings for optimal display of the input signal.
        """
        scope._write_checked(":AUT")

        # Auto setup takes a moment
        await asyncio.sleep(2)

        return ActionResult(action=SystemAction.AUTO_SETUP)

    @mcp.tool
    @with_scope_connection
    async def clear_display() -> ActionResult:
        """
        Clear the oscilloscope display.
        """
        scope._write_checked(":CLE")

        return ActionResult(action=SystemAction.CLEAR_DISPLAY)

    @mcp.tool
    @with_scope_connection
    async def reset_instrument() -> ActionResult:
        """
        Reset the oscilloscope to factory default settings.

        Restores all settings to their factory defaults, including
        channel configurations, timebase, trigger settings, and
        display options.
        """
        scope._write_checked("*RST")

        # Reset takes a moment to complete
        await asyncio.sleep(2)

        return ActionResult(action=SystemAction.RESET)

    @mcp.tool
    @with_scope_connection
    async def get_screenshot() -> ScreenshotResult:
        """
        Capture a screenshot of the oscilloscope display.

        Saves a PNG image of the current oscilloscope screen display to a temporary file,
        including waveforms, measurements, and all visible UI elements.
        """
        # Set image format to PNG
        scope._write_checked(":SAVE:IMAGe:FORMat PNG")

        # Wait for operations to complete and on-screen messages to clear
        scope._query_checked("*OPC?")
        await asyncio.sleep(3.5)

        # Query the image data
        # Response format: TMC header + binary PNG data + terminator
        png_data = cast(
            bytes,
            scope._query_binary_values_checked(
                ":SAVE:IMAGe:DATA?",
                datatype="B",  # Read as bytes
                is_big_endian=False,
                container=bytes,  # Return as bytes object
            ),
        )

        # Save screenshot to temporary PNG file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
        fd, file_path = tempfile.mkstemp(
            suffix=".png",
            prefix=f"screenshot_{timestamp}_",
            dir=temp_dir,
        )
        try:
            # Write PNG data to file
            os.write(fd, png_data)
        finally:
            os.close(fd)

        return ScreenshotResult(file_path=to_client_path(file_path) or file_path)

    # === DVM TOOLS ===

    @mcp.tool
    @with_scope_connection
    async def configure_dvm(
        channel: Annotated[Optional[ChannelNumber], Field(description="Channel number (1-4), optional")] = None,
        mode: Annotated[
            Optional[str],
            Field(
                description="Measurement mode, optional. One of: 'AC_RMS' (RMS value with DC component removed), 'DC' (Average/DC value), 'AC+DC_RMS' (True RMS including both AC and DC components)"
            ),
        ] = None,
        enabled: Annotated[Optional[bool], Field(description="Enable/disable DVM, optional")] = None,
    ) -> DVMConfigureResult:
        """
        Configure Digital Voltmeter settings.

        Change any combination of DVM settings in a single call. Omitted parameters
        remain unchanged.

        The DVM provides 4-digit voltage measurements asynchronously from the
        main acquisition system. Once enabled, it continuously measures even
        when the scope is stopped. Measurements work even if the channel is
        not enabled on the display.
        """
        # Apply changes in order: channel, mode, enabled
        if channel is not None:
            scope.dvm_set_source(channel)

        if mode is not None:
            # Convert user-friendly mode to DVMMode enum
            dvm_mode = DVMMode.from_user_input(mode)
            scope.dvm_set_mode(dvm_mode)

        if enabled is not None:
            scope.dvm_enable(enabled)

        # Query all settings to get final state
        is_enabled = scope.dvm_is_enabled()
        scpi_source = scope.dvm_get_source()
        channel_num = _parse_channel_from_scpi(scpi_source)
        dvm_mode = scope.dvm_get_mode()

        # Query current reading if enabled
        current_reading: Optional[float] = None
        if is_enabled:
            current_reading = scope.dvm_get_current_reading()

        # Build status message
        status_parts = []
        if channel is not None:
            status_parts.append(f"Channel {channel_num}")
        if mode is not None:
            status_parts.append(f"{dvm_mode.to_user_name()} mode")
        if enabled is not None:
            status_parts.append("enabled" if enabled else "disabled")

        message = "DVM configured"
        if status_parts:
            message += ": " + ", ".join(status_parts)

        return DVMConfigureResult(
            enabled=is_enabled,
            source=scpi_source,
            channel=channel_num,
            mode=dvm_mode.to_user_name(),
            mode_description=dvm_mode.description(),
            current_reading=current_reading,
            unit="V",
            message=message,
        )

    @mcp.tool
    @with_scope_connection
    async def get_dvm_status() -> DVMStatusResult:
        """
        Get comprehensive Digital Voltmeter status and current reading.

        Returns all DVM settings including enable status, source channel,
        measurement mode, mode description, and current voltage reading
        (if DVM is enabled).
        """
        # Query all DVM settings
        is_enabled = scope.dvm_is_enabled()
        scpi_source = scope.dvm_get_source()
        channel_num = _parse_channel_from_scpi(scpi_source)
        dvm_mode = scope.dvm_get_mode()

        # Query current reading if enabled
        current_reading: Optional[float] = None
        if is_enabled:
            current_reading = scope.dvm_get_current_reading()

        return DVMStatusResult(
            enabled=is_enabled,
            source=scpi_source,
            channel=channel_num,
            mode=dvm_mode.to_user_name(),
            mode_description=dvm_mode.description(),
            current_reading=current_reading,
            unit="V",
        )

    # === PRIORITY 1: HARDWARE COUNTER ===

    @mcp.tool
    @with_scope_connection
    async def configure_hardware_counter(
        enabled: Annotated[bool, Field(description="Boolean to enable counter")],
        channel: ChannelNumber,
        mode: Annotated[HardwareCounterMode, Field(description='Measurement mode ("FREQUENCY", "PERIOD", "TOTALIZE")')],
        digits: CounterDigitsField,
        totalize_enabled: Annotated[bool, Field(description="Enable statistics (only for FREQUENCY/PERIOD modes)")],
    ) -> HardwareCounterConfigResult:
        """
        Configure hardware frequency counter in a single call.

        Modes:
        - **FREQUENCY**: Measures signal frequency (Hz)
        - **PERIOD**: Measures signal period (seconds)
        - **TOTALIZE**: Counts total rising/falling edges

        Use cases:
        - High-accuracy frequency measurement (6-digit precision)
        - Period measurement for low-frequency signals
        - Edge counting for event totalization

        Note: Counter must be enabled first. Units depend on mode (Hz for frequency, seconds for period, count for totalize).
        """
        # Enable/disable counter
        scope._write_checked(f":COUN:ENAB {'ON' if enabled else 'OFF'}")

        # Set source channel
        scope._write_checked(f":COUN:SOUR CHAN{channel}")

        # Set mode
        scope._write_checked(f":COUN:MODE {mode.value}")

        # Set digit resolution
        scope._write_checked(f":COUN:NDIG {digits}")

        # Set totalize enable (statistics)
        scope._write_checked(f":COUN:TOT:ENAB {'ON' if totalize_enabled else 'OFF'}")

        # Verify settings
        actual_enabled = bool(int(scope._query_checked(":COUN:ENAB?")))
        actual_source = scope._query_checked(":COUN:SOUR?").strip()
        actual_channel = _parse_channel_from_scpi(actual_source)
        actual_mode_str = scope._query_checked(":COUN:MODE?").strip()
        actual_digits = int(scope._query_checked(":COUN:NDIG?"))
        actual_totalize = bool(int(scope._query_checked(":COUN:TOT:ENAB?")))

        # Map SCPI response to enum
        mode_map = {
            "FREQ": HardwareCounterMode.FREQUENCY,
            "PER": HardwareCounterMode.PERIOD,
            "TOT": HardwareCounterMode.TOTALIZE,
        }
        actual_mode = mode_map.get(actual_mode_str[:3], HardwareCounterMode.FREQUENCY)

        # Get current value if enabled
        current_value: Optional[float] = None
        unit = "Hz"  # Default unit
        if actual_enabled:
            try:
                current_value = float(scope._query_checked(":COUN:CURR?"))
                # Determine unit based on mode
                if actual_mode == HardwareCounterMode.FREQUENCY:
                    unit = "Hz"
                elif actual_mode == HardwareCounterMode.PERIOD:
                    unit = "s"
                else:  # TOTALIZE
                    unit = "count"
            except:
                current_value = None

        return HardwareCounterConfigResult(
            enabled=actual_enabled,
            channel=actual_channel,
            mode=actual_mode,
            digits=actual_digits,
            totalize_enabled=actual_totalize,
            current_value=current_value,
            unit=unit,
            message=f"Hardware counter configured: {'enabled' if actual_enabled else 'disabled'}, CH{actual_channel}, {actual_mode.value} mode, {actual_digits} digits"
        )

    @mcp.tool
    @with_scope_connection
    async def get_hardware_counter_value() -> HardwareCounterValueResult:
        """
        Get current hardware counter reading.

        Note: Counter must be enabled first. Units depend on mode (Hz for frequency, seconds for period, count for totalize).
        """
        # Get current mode to determine unit
        mode_str = scope._query_checked(":COUN:MODE?").strip()
        mode_map = {
            "FREQ": ("Hz", HardwareCounterMode.FREQUENCY),
            "PER": ("s", HardwareCounterMode.PERIOD),
            "TOT": ("count", HardwareCounterMode.TOTALIZE),
        }
        unit, _ = mode_map.get(mode_str[:3], ("Hz", HardwareCounterMode.FREQUENCY))

        # Get current reading
        value = float(scope._query_checked(":COUN:CURR?"))

        return HardwareCounterValueResult(value=value, unit=unit)

    @mcp.tool
    @with_scope_connection
    async def reset_counter_totalize() -> CounterTotalizeResetResult:
        """
        Clear/reset the totalize counter and statistics.

        Note: Only applies when counter is in statistics mode (totalize enabled).
        """
        scope._write_checked(":COUN:TOT:CLE")

        return CounterTotalizeResetResult(message="Counter totalize reset")

    return mcp


def _validate_temp_directory(temp_dir: str) -> None:
    """Validate that the temp directory exists and is writable.

    Args:
        temp_dir: Path to the temporary directory to validate

    Raises:
        SystemExit: If directory doesn't exist or is not writable
    """
    import sys

    # Check if directory exists
    if not os.path.exists(temp_dir):
        print(f"ERROR: RIGOL_TEMP_DIR directory does not exist: {temp_dir}", file=sys.stderr)
        print("Please create the directory or unset RIGOL_TEMP_DIR to use system default.", file=sys.stderr)
        sys.exit(1)

    # Check if it's actually a directory
    if not os.path.isdir(temp_dir):
        print(f"ERROR: RIGOL_TEMP_DIR is not a directory: {temp_dir}", file=sys.stderr)
        sys.exit(1)

    # Check if directory is writable
    test_file = None
    try:
        import tempfile as tf
        fd, test_file = tf.mkstemp(dir=temp_dir, prefix="write_test_")
        os.close(fd)
        os.unlink(test_file)
    except (OSError, PermissionError) as e:
        print(f"ERROR: RIGOL_TEMP_DIR is not writable: {temp_dir}", file=sys.stderr)
        print(f"Permission error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Failed to validate RIGOL_TEMP_DIR: {temp_dir}", file=sys.stderr)
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Run the MCP server."""
    import argparse

    parser = argparse.ArgumentParser(description="Rigol DHO824 MCP Server")
    parser.add_argument(
        "--http", action="store_true", help="Use HTTP transport instead of stdio"
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host for HTTP transport (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--port", type=int, default=8000, help="Port for HTTP transport (default: 8000)"
    )
    parser.add_argument(
        "--path", default="/mcp", help="Path for HTTP transport (default: /mcp)"
    )

    args = parser.parse_args()

    # Check if container path translation is enabled
    container_mode = os.getenv("RIGOL_CONTAINER_PATH_TRANSLATION", "false").lower() in ("true", "1", "yes")

    if container_mode:
        # === CONTAINER MODE ===
        # Always use /tmp/rigol as internal temp dir in containers
        internal_temp_dir = "/tmp/rigol"
        _validate_temp_directory(internal_temp_dir)

        # Get the host-side path from RIGOL_TEMP_DIR (required in container mode)
        client_temp_dir = os.getenv("RIGOL_TEMP_DIR")
        if not client_temp_dir:
            import sys
            print("ERROR: RIGOL_TEMP_DIR is required when RIGOL_CONTAINER_PATH_TRANSLATION is enabled", file=sys.stderr)
            print("Set RIGOL_TEMP_DIR to the host-side path (e.g., /Users/dave/rigol-data)", file=sys.stderr)
            sys.exit(1)

        # Create the server with path translation
        mcp = create_server(internal_temp_dir, client_temp_dir=client_temp_dir)

        if args.http:
            mcp.run(transport="http", host=args.host, port=args.port, path=args.path)
        else:
            mcp.run()
    else:
        # === NORMAL MODE ===
        # Check if user specified a custom temp directory
        custom_temp_dir = os.getenv("RIGOL_TEMP_DIR")

        if custom_temp_dir:
            # User specified temp directory - validate and use it (no auto-cleanup)
            _validate_temp_directory(custom_temp_dir)
            temp_dir = custom_temp_dir

            # Create the server (no path translation)
            mcp = create_server(temp_dir)

            if args.http:
                mcp.run(transport="http", host=args.host, port=args.port, path=args.path)
            else:
                mcp.run()
        else:
            # Use system default temp directory with automatic cleanup on exit
            with tempfile.TemporaryDirectory(prefix="rigol_dho824_") as temp_dir:
                # Create the server
                mcp = create_server(temp_dir)

                if args.http:
                    mcp.run(transport="http", host=args.host, port=args.port, path=args.path)
                else:
                    mcp.run()


if __name__ == "__main__":
    main()
