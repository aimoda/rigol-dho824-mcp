"""MCP server for Rigol DHO824 oscilloscope with proper type definitions."""

import asyncio
import functools
import os
import tempfile
import time
import json
from datetime import datetime
from enum import Enum
from ftplib import FTP
from typing import Optional, TypedDict, Annotated, List, Literal
import numpy as np
from pydantic import Field
from fastmcp import FastMCP, Context
from dotenv import load_dotenv
import pyvisa


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
        self.lock = asyncio.Lock()

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
                self.instrument.query("*OPC?")  # type: ignore[reportOptionalMemberAccess, reportAttributeAccessIssue]
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
                self.instrument = self.rm.open_resource(
                    self.resource_string,
                    access_mode=pyvisa.constants.AccessModes.exclusive_lock,  # type: ignore[reportAttributeAccessIssue]
                )
            else:
                # Auto-discover Rigol oscilloscope
                resources = self.rm.list_resources()
                rigol_resources = [
                    r for r in resources if "RIGOL" in r.upper() or "0x1AB1" in r
                ]

                if not rigol_resources:
                    return False

                # Try to connect to first Rigol device found
                self.instrument = self.rm.open_resource(
                    rigol_resources[0],
                    access_mode=pyvisa.constants.AccessModes.exclusive_lock,  # type: ignore[reportAttributeAccessIssue]
                )

            self.instrument.timeout = self.timeout  # type: ignore[reportAttributeAccessIssue]

            # Set proper termination characters for SCPI communication
            self.instrument.read_termination = "\n"  # type: ignore[reportAttributeAccessIssue]
            self.instrument.write_termination = "\n"  # type: ignore[reportAttributeAccessIssue]

            # Clear the instrument's input and output buffers
            # self.instrument.clear()

            # Ensure synchronization - wait for all operations to complete
            self.instrument.write("*OPC")  # type: ignore[reportAttributeAccessIssue]

            # Test connection and cache identity
            self._identity = self.instrument.query("*IDN?").strip()  # type: ignore[reportAttributeAccessIssue]

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
                self._identity = self.instrument.query("*IDN?").strip()  # type: ignore[reportOptionalMemberAccess, reportAttributeAccessIssue]
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

    def download_wfm_via_ftp(
        self, ip_address: str, scope_filename: str, local_filepath: str
    ) -> bool:
        """
        Download WFM file from oscilloscope via FTP.

        Args:
            ip_address: IP address of oscilloscope
            scope_filename: Filename on the scope (without path, assumes C:/)
            local_filepath: Local file path to save downloaded file

        Returns:
            True if download successful, False otherwise
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

            # Download file
            with open(local_filepath, "wb") as f:
                ftp.retrbinary(f"RETR {scope_filename}", f.write)

            # Delete file from scope after successful download
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
        self.instrument.write(cmd)  # type: ignore[reportOptionalMemberAccess, reportAttributeAccessIssue]

    def dvm_is_enabled(self) -> bool:
        """Query if DVM is enabled."""
        response = self.instrument.query(":DVM:ENABle?")  # type: ignore[reportOptionalMemberAccess, reportAttributeAccessIssue]
        return response.strip() == "1"

    def dvm_set_source(self, channel: int) -> None:
        """Set DVM source channel (1-4)."""
        if channel not in [1, 2, 3, 4]:
            raise ValueError(f"Channel must be 1-4, got {channel}")
        cmd = f":DVM:SOURce CHANnel{channel}"
        self.instrument.write(cmd)  # type: ignore[reportOptionalMemberAccess, reportAttributeAccessIssue]

    def dvm_get_source(self) -> str:
        """Query DVM source channel.

        Returns:
            SCPI channel name (e.g., 'CHAN1', 'CHAN2')
        """
        response = self.instrument.query(":DVM:SOURce?")  # type: ignore[reportOptionalMemberAccess, reportAttributeAccessIssue]
        return response.strip()

    def dvm_set_mode(self, mode: DVMMode) -> None:
        """Set DVM measurement mode."""
        cmd = f":DVM:MODE {mode.value}"
        self.instrument.write(cmd)  # type: ignore[reportOptionalMemberAccess, reportAttributeAccessIssue]

    def dvm_get_mode(self) -> DVMMode:
        """Query DVM measurement mode."""
        response = self.instrument.query(":DVM:MODE?")  # type: ignore[reportOptionalMemberAccess, reportAttributeAccessIssue]
        mode_str = response.strip()
        return DVMMode(mode_str)

    def dvm_get_current_reading(self) -> float:
        """Get current DVM voltage reading.

        Returns:
            Voltage reading in volts
        """
        response = self.instrument.query(":DVM:CURRent?")  # type: ignore[reportOptionalMemberAccess, reportAttributeAccessIssue]
        return float(response.strip())


def create_server(temp_dir: str) -> FastMCP:
    """Create the FastMCP server with oscilloscope tools.

    Args:
        temp_dir: Path to temporary directory for storing waveforms and screenshots
    """

    # Load environment variables
    load_dotenv()

    # Get configuration from environment
    resource_string = os.getenv("RIGOL_RESOURCE", "")
    timeout = int(os.getenv("VISA_TIMEOUT", "5000"))

    # Create MCP server
    mcp = FastMCP("rigol-dho824", stateless_http=True)

    # Create oscilloscope instance
    scope = RigolDHO824(resource_string if resource_string else None, timeout)

    # === DECORATOR FOR SCOPE CONNECTION AND LOCKING ===

    def with_scope_connection(func):
        """
        Decorator that handles scope connection, locking, and cleanup for tool functions.

        This decorator:
        1. Acquires the asyncio lock to ensure single-threaded access to the scope
        2. Connects to the oscilloscope (raises exception if connection fails)
        3. Locks the front panel and enables beeper for remote operation
        4. Executes the tool function
        5. Restores panel control and disables beeper
        6. Disconnects and releases the lock in the finally block
        """

        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            async with scope.lock:
                if not scope.connect():
                    raise Exception(
                        "Failed to connect to oscilloscope. Check connection and RIGOL_RESOURCE environment variable."
                    )
                # Lock panel and enable beeper during remote operation
                scope.instrument.write(":SYSTem:LOCKed ON")  # type: ignore[reportAttributeAccessIssue]
                scope.instrument.write(":SYSTem:BEEPer ON")  # type: ignore[reportAttributeAccessIssue]
                try:
                    return await func(*args, **kwargs)
                finally:
                    # Restore panel control and disable beeper before disconnect
                    scope.instrument.write(":SYSTem:BEEPer OFF")  # type: ignore[reportAttributeAccessIssue]
                    scope.instrument.write(":SYSTem:LOCKed OFF")  # type: ignore[reportAttributeAccessIssue]
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

        Args:
            channels: List of channel numbers to capture (1-4), defaults to [1]

        Returns:
            Dictionary containing list of channel data with conversion parameters and optional WFM file path
        """
        # Generate unique capture ID based on timestamp
        capture_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[
            :-3
        ]  # Include milliseconds

        # Create subdirectory for this capture
        capture_dir = tempfile.mkdtemp(prefix=f"waveform_capture_{capture_id}_", dir=temp_dir)

        results = []

        # Stop acquisition once for all channels
        scope.instrument.write(":STOP")  # type: ignore[reportAttributeAccessIssue]
        scope.instrument.query("*OPC?")  # type: ignore[reportAttributeAccessIssue]  # Wait for stop to complete

        for channel_idx, channel in enumerate(channels):
            # Check if channel is enabled
            channel_enabled = int(scope.instrument.query(f":CHAN{channel}:DISP?"))  # type: ignore[reportAttributeAccessIssue]
            if not channel_enabled:
                await ctx.report_progress(
                    progress=(channel_idx + 1) / len(channels),
                    message=f"Channel {channel} is disabled, skipping",
                )
                continue

            try:
                # Set source channel
                scope.instrument.write(f":WAV:SOUR CHAN{channel}")  # type: ignore[reportAttributeAccessIssue]

                # Configure for RAW mode with WORD format (16-bit)
                scope.instrument.write(":WAV:MODE RAW")  # type: ignore[reportAttributeAccessIssue]
                scope.instrument.write(":WAV:FORM WORD")  # type: ignore[reportAttributeAccessIssue]

                # Query memory depth to determine available points
                memory_depth = float(scope.instrument.query(":ACQ:MDEP?"))  # type: ignore[reportAttributeAccessIssue]
                max_points = int(memory_depth)

                # Adjust timeout based on memory depth
                # Estimate: 100ms per 100k points + 10s buffer
                if memory_depth > 1000000:  # >1M points
                    new_timeout = int((memory_depth / 100000) * 100 + 10000)
                    scope.instrument.timeout = new_timeout  # type: ignore[reportAttributeAccessIssue]

                # Query waveform parameters for conversion (before data transfer)
                y_increment = float(scope.instrument.query(":WAV:YINC?"))  # type: ignore[reportAttributeAccessIssue]
                y_origin = float(scope.instrument.query(":WAV:YOR?"))  # type: ignore[reportAttributeAccessIssue]
                y_reference = float(scope.instrument.query(":WAV:YREF?"))  # type: ignore[reportAttributeAccessIssue]
                x_increment = float(scope.instrument.query(":WAV:XINC?"))  # type: ignore[reportAttributeAccessIssue]
                x_origin = float(scope.instrument.query(":WAV:XOR?"))  # type: ignore[reportAttributeAccessIssue]

                # Query channel settings
                vertical_scale = float(scope.instrument.query(f":CHAN{channel}:SCAL?"))  # type: ignore[reportAttributeAccessIssue]
                vertical_offset = float(scope.instrument.query(f":CHAN{channel}:OFFS?"))  # type: ignore[reportAttributeAccessIssue]
                probe_ratio = float(scope.instrument.query(f":CHAN{channel}:PROB?"))  # type: ignore[reportAttributeAccessIssue]

                # Query sample rate
                sample_rate = float(scope.instrument.query(":ACQ:SRAT?"))  # type: ignore[reportAttributeAccessIssue]

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
                        scope.instrument.write(f":WAV:STAR {start}")  # type: ignore[reportAttributeAccessIssue]
                        scope.instrument.write(f":WAV:STOP {end}")  # type: ignore[reportAttributeAccessIssue]

                        # Read chunk
                        chunk_data = scope.instrument.query_binary_values(  # type: ignore[reportAttributeAccessIssue]
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

                    scope.instrument.write(":WAV:STAR 1")  # type: ignore[reportAttributeAccessIssue]
                    scope.instrument.write(f":WAV:STOP {max_points}")  # type: ignore[reportAttributeAccessIssue]

                    raw_data = scope.instrument.query_binary_values(  # type: ignore[reportAttributeAccessIssue]
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
                waveform_data = {
                    "channel": channel,
                    "truncated": truncated,
                    "y_increment": y_increment,
                    "y_origin": y_origin,
                    "y_reference": y_reference,
                    "x_increment": x_increment,
                    "x_origin": x_origin,
                    "vertical_scale": vertical_scale,
                    "vertical_offset": vertical_offset,
                    "probe_ratio": probe_ratio,
                    "sample_rate": sample_rate,
                    "points": len(raw_data),
                    "raw_data": raw_data,  # List of raw ADC values
                }

                # Save waveform data to JSON file in capture directory
                file_path = os.path.join(capture_dir, f"ch{channel}.json")
                with open(file_path, 'w') as f:
                    json.dump(waveform_data, f, indent=2)

                # Return metadata with file path
                results.append(
                    WaveformChannelData(
                        channel=channel,
                        truncated=truncated,
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
                        file_path=file_path,
                    )
                )
            except Exception as e:
                await ctx.report_progress(
                    progress=(channel_idx + 1) / len(channels),
                    message=f"Channel {channel}: Error - {str(e)}",
                )
                continue

        # Capture WFM file for future-proofing and scientific accuracy
        # WFM contains all enabled channels in a single file
        # Generate random 8-char lowercase hex filename to avoid overwriting
        wfm_filename = f"{os.urandom(4).hex()}.wfm"
        wfm_scope_path = f"C:/{wfm_filename}"
        wfm_local_path = os.path.join(capture_dir, "data.wfm")
        wfm_saved_path: Optional[str] = None

        # Try to save and download WFM via FTP (gracefully skip if FTP unavailable)
        try:
            await ctx.report_progress(
                progress=1.0, message="Saving WFM file on scope..."
            )

            # Enable file overwriting
            scope.instrument.write(":SAVE:OVER ON")  # type: ignore[reportAttributeAccessIssue]

            # Save memory waveform to scope
            scope.instrument.write(f":SAVE:MEMory:WAVeform {wfm_scope_path}")  # type: ignore[reportAttributeAccessIssue]
            time.sleep(5)  # Wait for save to complete

            # Check save status
            scope.instrument.query(":SAVE:STATus?")  # type: ignore[reportAttributeAccessIssue]

            # Try to download via FTP
            ip_address = scope.extract_ip_from_resource()
            if ip_address:
                await ctx.report_progress(
                    progress=1.0, message="Downloading WFM file via FTP..."
                )
                if scope.download_wfm_via_ftp(ip_address, wfm_filename, wfm_local_path):
                    wfm_saved_path = wfm_local_path
                    await ctx.report_progress(
                        progress=1.0, message=f"WFM file saved: {wfm_local_path}"
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

        return WaveformCaptureResult(channels=results, wfm_file_path=wfm_saved_path)

    # === CHANNEL CONTROL TOOLS ===

    @mcp.tool
    @with_scope_connection
    async def set_channel_enable(
        channel: ChannelNumber,
        enabled: Annotated[bool, Field(description="True to enable, False to disable")],
    ) -> ChannelEnableResult:
        """
        Enable or disable a channel display.

        Args:
            channel: Channel number (1-4)
            enabled: True to enable, False to disable

        Returns:
            Channel enable status
        """
        state = "ON" if enabled else "OFF"
        scope.instrument.write(f":CHAN{channel}:DISP {state}")  # type: ignore[reportAttributeAccessIssue]

        # Verify the setting
        actual_state = int(scope.instrument.query(f":CHAN{channel}:DISP?"))  # type: ignore[reportAttributeAccessIssue]

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

        Args:
            channel: Channel number (1-4)
            coupling: Coupling mode (AC, DC, or GND)

        Returns:
            Channel coupling setting
        """
        # Use enum value directly
        scope.instrument.write(f":CHAN{channel}:COUP {coupling}")  # type: ignore[reportAttributeAccessIssue]

        # Verify the setting
        actual_coupling = scope.instrument.query(f":CHAN{channel}:COUP?").strip()  # type: ignore[reportAttributeAccessIssue]

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

        Args:
            channel: Channel number (1-4)
            probe_ratio: Probe ratio (e.g., 1, 10, 100, 1000)

        Returns:
            Channel probe setting
        """
        # Format as integer if it's a whole number, otherwise as float
        probe_value = (
            int(probe_ratio) if float(probe_ratio).is_integer() else float(probe_ratio)
        )
        scope.instrument.write(f":CHAN{channel}:PROB {probe_value}")  # type: ignore[reportAttributeAccessIssue]

        # Verify the setting
        actual_ratio = float(scope.instrument.query(f":CHAN{channel}:PROB?"))  # type: ignore[reportAttributeAccessIssue]

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

        Args:
            channel: Channel number (1-4)
            bandwidth_limit: Bandwidth limit setting (OFF or 20MHz). Defaults to OFF

        Returns:
            Channel bandwidth setting
        """
        if bandwidth_limit is None:
            bandwidth_limit = "OFF"

        # Map user-friendly value to SCPI
        bw_value = "20M" if bandwidth_limit == "20MHz" else "OFF"
        scope.instrument.write(f":CHAN{channel}:BWL {bw_value}")  # type: ignore[reportAttributeAccessIssue]

        # Verify the setting
        actual_bw = scope.instrument.query(f":CHAN{channel}:BWL?").strip()  # type: ignore[reportAttributeAccessIssue]

        # Map response to enum
        result_bw = "20MHz" if actual_bw == "20M" else "OFF"

        return ChannelBandwidthResult(channel=channel, bandwidth_limit=result_bw)

    @mcp.tool
    @with_scope_connection
    async def get_channel_status(channel: ChannelNumber) -> ChannelStatusResult:
        """
        Get comprehensive channel status and settings.

        Args:
            channel: Channel number (1-4)

        Returns:
            All channel settings
        """
        # Query all channel settings
        enabled = bool(int(scope.instrument.query(f":CHAN{channel}:DISP?")))  # type: ignore[reportAttributeAccessIssue]
        coupling = scope.instrument.query(f":CHAN{channel}:COUP?").strip()  # type: ignore[reportAttributeAccessIssue]
        probe_ratio = float(scope.instrument.query(f":CHAN{channel}:PROB?"))  # type: ignore[reportAttributeAccessIssue]
        bw_limit = scope.instrument.query(f":CHAN{channel}:BWL?").strip()  # type: ignore[reportAttributeAccessIssue]
        vertical_scale = float(scope.instrument.query(f":CHAN{channel}:SCAL?"))  # type: ignore[reportAttributeAccessIssue]
        vertical_offset = float(scope.instrument.query(f":CHAN{channel}:OFFS?"))  # type: ignore[reportAttributeAccessIssue]
        invert = bool(int(scope.instrument.query(f":CHAN{channel}:INV?")))  # type: ignore[reportAttributeAccessIssue]
        units = scope.instrument.query(f":CHAN{channel}:UNIT?").strip()  # type: ignore[reportAttributeAccessIssue]

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

    # === SCALE ADJUSTMENT TOOLS ===

    @mcp.tool
    @with_scope_connection
    async def set_vertical_scale(
        channel: ChannelNumber, vertical_scale: VerticalScaleField
    ) -> VerticalScaleResult:
        """
        Set channel vertical scale (V/div).

        Args:
            channel: Channel number (1-4)
            vertical_scale: Vertical scale in V/div

        Returns:
            Vertical scale setting
        """
        # Valid scales follow 1-2-5 sequence
        valid_scales = [
            1e-3,
            2e-3,
            5e-3,  # mV range
            1e-2,
            2e-2,
            5e-2,
            1e-1,
            2e-1,
            5e-1,
            1,
            2,
            5,  # V range
            10,
            20,
            50,
            100,
        ]

        # Find closest valid scale
        scale = vertical_scale
        if scale not in valid_scales:
            scale = valid_scales[np.argmin(np.abs(np.array(valid_scales) - scale))]

        scope.instrument.write(f":CHAN{channel}:SCAL {scale}")  # type: ignore[reportAttributeAccessIssue]

        # Verify the setting
        actual_scale = float(scope.instrument.query(f":CHAN{channel}:SCAL?"))  # type: ignore[reportAttributeAccessIssue]

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

        Args:
            channel: Channel number (1-4)
            vertical_offset: Vertical offset in volts

        Returns:
            Vertical offset setting
        """
        scope.instrument.write(f":CHAN{channel}:OFFS {vertical_offset}")  # type: ignore[reportAttributeAccessIssue]

        # Verify the setting
        actual_offset = float(scope.instrument.query(f":CHAN{channel}:OFFS?"))  # type: ignore[reportAttributeAccessIssue]

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

        Args:
            time_per_div: Time per division in seconds

        Returns:
            Timebase scale setting
        """
        scope.instrument.write(f":TIM:MAIN:SCAL {time_per_div}")  # type: ignore[reportAttributeAccessIssue]

        # Verify the setting
        actual_scale = float(scope.instrument.query(":TIM:MAIN:SCAL?"))  # type: ignore[reportAttributeAccessIssue]

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

        Args:
            time_offset: Time offset in seconds

        Returns:
            Timebase offset setting
        """
        scope.instrument.write(f":TIM:MAIN:OFFS {time_offset}")  # type: ignore[reportAttributeAccessIssue]

        # Verify the setting
        actual_offset = float(scope.instrument.query(":TIM:MAIN:OFFS?"))  # type: ignore[reportAttributeAccessIssue]

        return TimebaseOffsetResult(time_offset=actual_offset, units="s")

    # === ACQUISITION CONTROL TOOLS ===

    @mcp.tool
    @with_scope_connection
    async def run_acquisition() -> AcquisitionStatusResult:
        """
        Start continuous acquisition (RUN mode).

        Returns:
            Acquisition status
        """
        scope.instrument.write(":RUN")  # type: ignore[reportAttributeAccessIssue]

        # Give it a moment to start
        time.sleep(0.1)

        # Check trigger status
        status = scope.instrument.query(":TRIG:STAT?").strip()  # type: ignore[reportAttributeAccessIssue]

        return AcquisitionStatusResult(
            action=AcquisitionAction.RUN, trigger_status=map_trigger_status(status)
        )

    @mcp.tool
    @with_scope_connection
    async def stop_acquisition() -> AcquisitionStatusResult:
        """
        Stop acquisition (STOP mode).

        Returns:
            Acquisition status
        """
        scope.instrument.write(":STOP")  # type: ignore[reportAttributeAccessIssue]

        # Give it a moment to stop
        time.sleep(0.1)

        # Check trigger status
        status = scope.instrument.query(":TRIG:STAT?").strip()  # type: ignore[reportAttributeAccessIssue]

        return AcquisitionStatusResult(
            action=AcquisitionAction.STOP, trigger_status=map_trigger_status(status)
        )

    @mcp.tool
    @with_scope_connection
    async def single_acquisition() -> AcquisitionStatusResult:
        """
        Perform single acquisition (SINGLE mode).

        Returns:
            Acquisition status
        """
        scope.instrument.write(":SING")  # type: ignore[reportAttributeAccessIssue]

        # Give it a moment to arm
        time.sleep(0.1)

        # Check trigger status
        status = scope.instrument.query(":TRIG:STAT?").strip()  # type: ignore[reportAttributeAccessIssue]

        return AcquisitionStatusResult(
            action=AcquisitionAction.SINGLE, trigger_status=map_trigger_status(status)
        )

    @mcp.tool
    @with_scope_connection
    async def force_trigger() -> ActionResult:
        """
        Force a trigger event.

        Returns:
            Action confirmation
        """
        scope.instrument.write(":TFOR")  # type: ignore[reportAttributeAccessIssue]

        return ActionResult(action=SystemAction.FORCE_TRIGGER)

    @mcp.tool
    @with_scope_connection
    async def get_trigger_status() -> TriggerStatusResult:
        """
        Get current trigger status.

        Returns:
            Trigger status and settings
        """
        # Query trigger status
        status = scope.instrument.query(":TRIG:STAT?").strip()  # type: ignore[reportAttributeAccessIssue]

        # Get additional trigger info
        mode = scope.instrument.query(":TRIG:MODE?").strip()  # type: ignore[reportAttributeAccessIssue]

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
            actual_source = scope.instrument.query(":TRIG:EDGE:SOUR?").strip()  # type: ignore[reportAttributeAccessIssue]
            if actual_source.startswith("CHAN") or actual_source.startswith("CH"):
                # Last character is channel number
                result["channel"] = int(actual_source[-1])
            result["trigger_level"] = float(scope.instrument.query(":TRIG:EDGE:LEV?"))  # type: ignore[reportAttributeAccessIssue]
            raw_slope = scope.instrument.query(":TRIG:EDGE:SLOP?").strip()  # type: ignore[reportAttributeAccessIssue]
            result["trigger_slope"] = map_trigger_slope_response(raw_slope)

        return result

    # === TRIGGER CONFIGURATION TOOLS ===

    @mcp.tool
    @with_scope_connection
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
        scope.instrument.write(f":TRIG:MODE {trigger_mode.value}")  # type: ignore[reportAttributeAccessIssue]

        # Verify the setting
        actual_mode = scope.instrument.query(":TRIG:MODE?").strip()  # type: ignore[reportAttributeAccessIssue]

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

        Args:
            channel: Trigger source channel (1-4)

        Returns:
            Trigger source setting
        """
        # Ensure we're in edge trigger mode
        current_mode = scope.instrument.query(":TRIG:MODE?").strip()  # type: ignore[reportAttributeAccessIssue]
        if current_mode not in ["EDGE", "EDG"]:
            scope.instrument.write(":TRIG:MODE EDGE")  # type: ignore[reportAttributeAccessIssue]

        # Use the channel's SCPI format
        scope.instrument.write(f":TRIG:EDGE:SOUR CHAN{channel}")  # type: ignore[reportAttributeAccessIssue]

        # Verify the setting
        actual_source = scope.instrument.query(":TRIG:EDGE:SOUR?").strip()  # type: ignore[reportAttributeAccessIssue]

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

        Args:
            trigger_level: Trigger level in volts
            channel: Optional channel to set level for (defaults to current source)

        Returns:
            Trigger level setting
        """
        # If source specified, set it first
        if channel:
            # Ensure we're in edge trigger mode
            current_mode = scope.instrument.query(":TRIG:MODE?").strip()  # type: ignore[reportAttributeAccessIssue]
            if current_mode not in ["EDGE", "EDG"]:
                scope.instrument.write(":TRIG:MODE EDGE")  # type: ignore[reportAttributeAccessIssue]

            # Set the source
            scope.instrument.write(f":TRIG:EDGE:SOUR CHAN{channel}")  # type: ignore[reportAttributeAccessIssue]

        scope.instrument.write(f":TRIG:EDGE:LEV {trigger_level}")  # type: ignore[reportAttributeAccessIssue]

        # Verify the setting
        actual_level = float(scope.instrument.query(":TRIG:EDGE:LEV?"))  # type: ignore[reportAttributeAccessIssue]

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

        Args:
            trigger_slope: Edge slope (POSITIVE, NEGATIVE, or EITHER)

        Returns:
            Trigger slope setting
        """
        # Map user-facing slope to SCPI value
        slope_map = {
            TriggerSlope.POSITIVE: "POS",
            TriggerSlope.NEGATIVE: "NEG",
            TriggerSlope.EITHER: "RFAL",
        }
        scope.instrument.write(f":TRIG:EDGE:SLOP {slope_map[trigger_slope]}")  # type: ignore[reportAttributeAccessIssue]

        # Verify the setting
        actual_slope = scope.instrument.query(":TRIG:EDGE:SLOP?").strip()  # type: ignore[reportAttributeAccessIssue]

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

        Args:
            coupling: Trigger coupling mode (AC, DC, LFReject, or HFReject)

        Returns:
            Current trigger coupling setting
        """
        # Map user-friendly coupling to SCPI format
        scope.instrument.write(f":TRIG:COUP {coupling}")  # type: ignore[reportAttributeAccessIssue]

        # Verify the setting
        actual_coupling = scope.instrument.query(":TRIG:COUP?").strip()  # type: ignore[reportAttributeAccessIssue]

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

        Args:
            sweep_mode: Trigger sweep mode (AUTO, NORMAL, or SINGLE)

        Returns:
            Current sweep mode setting
        """
        # TriggerSweep enum values map directly to SCPI format
        scope.instrument.write(f":TRIG:SWE {sweep_mode.value}")  # type: ignore[reportAttributeAccessIssue]

        # Verify the setting
        actual_sweep = scope.instrument.query(":TRIG:SWE?").strip()  # type: ignore[reportAttributeAccessIssue]

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

        Args:
            holdoff_time: Holdoff duration in seconds (minimum: 16ns, maximum: 10s)

        Returns:
            Current holdoff time in seconds with human-readable format
        """
        # Validate range
        if holdoff_time < 16e-9 or holdoff_time > 10:
            raise ValueError(
                f"Holdoff time must be between 16ns and 10s, got {holdoff_time}s"
            )

        scope.instrument.write(f":TRIG:HOLD {holdoff_time}")  # type: ignore[reportAttributeAccessIssue]

        # Verify the setting
        actual_holdoff = float(scope.instrument.query(":TRIG:HOLD?"))  # type: ignore[reportAttributeAccessIssue]

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

        Args:
            enabled: True to enable noise rejection, False to disable

        Returns:
            Current noise reject status
        """
        state = "ON" if enabled else "OFF"
        scope.instrument.write(f":TRIG:NREJ {state}")  # type: ignore[reportAttributeAccessIssue]

        # Verify the setting
        actual_state = int(scope.instrument.query(":TRIG:NREJ?"))  # type: ignore[reportAttributeAccessIssue]

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

        Args:
            channel: Source channel (1-4)
            polarity: Pulse polarity - "POSITIVE" or "NEGATIVE"
            when: Width condition - "GREATER", "LESS", or "WITHIN"
            upper_width: Upper width limit in seconds
            level: Trigger level in volts
            lower_width: Lower width limit in seconds (required for WITHIN)

        Returns:
            Complete pulse trigger configuration

        Use cases:
        - Finding glitches (LESS than expected width)
        - Detecting timeouts (GREATER than expected)
        - Validating pulse width range (WITHIN limits)
        """
        # Validate WITHIN requires lower_width
        if when == "WITHIN" and lower_width is None:
            raise ValueError("lower_width is required when when='WITHIN'")

        # Set trigger mode to PULSE
        scope.instrument.write(":TRIG:MODE PULS")  # type: ignore[reportAttributeAccessIssue]

        # Set source channel
        scope.instrument.write(f":TRIG:PULS:SOUR CHAN{channel}")  # type: ignore[reportAttributeAccessIssue]

        # Map when condition to SCPI format
        when_map = {
            "GREATER": "GRE",
            "LESS": "LESS",
            "WITHIN": "WITH",
        }
        scope.instrument.write(f":TRIG:PULS:WHEN {when_map[when]}")  # type: ignore[reportAttributeAccessIssue]

        # Set upper width
        scope.instrument.write(f":TRIG:PULS:UWID {upper_width}")  # type: ignore[reportAttributeAccessIssue]

        # Set lower width if WITHIN
        if when == "WITHIN" and lower_width is not None:
            scope.instrument.write(f":TRIG:PULS:LWID {lower_width}")  # type: ignore[reportAttributeAccessIssue]

        # Map polarity to SCPI format
        polarity_map = {
            "POSITIVE": "POS",
            "NEGATIVE": "NEG",
        }
        scope.instrument.write(f":TRIG:PULS:POL {polarity_map[polarity]}")  # type: ignore[reportAttributeAccessIssue]

        # Set trigger level
        scope.instrument.write(f":TRIG:PULS:LEV {level}")  # type: ignore[reportAttributeAccessIssue]

        # Verify configuration by reading back
        actual_source = scope.instrument.query(":TRIG:PULS:SOUR?").strip()  # type: ignore[reportAttributeAccessIssue]
        actual_when = scope.instrument.query(":TRIG:PULS:WHEN?").strip()  # type: ignore[reportAttributeAccessIssue]
        actual_upper = float(scope.instrument.query(":TRIG:PULS:UWID?"))  # type: ignore[reportAttributeAccessIssue]
        actual_polarity = scope.instrument.query(":TRIG:PULS:POL?").strip()  # type: ignore[reportAttributeAccessIssue]
        actual_level = float(scope.instrument.query(":TRIG:PULS:LEV?"))  # type: ignore[reportAttributeAccessIssue]

        # Parse channel from source
        actual_channel = _parse_channel_from_scpi(actual_source)

        # Read lower width if applicable
        actual_lower: Optional[float] = None
        if when == "WITHIN":
            actual_lower = float(scope.instrument.query(":TRIG:PULS:LWID?"))  # type: ignore[reportAttributeAccessIssue]

        # Map responses back to user-friendly format
        when_reverse = {"GRE": "GREATER", "GREA": "GREATER", "LESS": "LESS", "WITH": "WITHIN"}
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

        Args:
            channel: Source channel (1-4)
            polarity: Slope direction - "POSITIVE" (rising) or "NEGATIVE" (falling)
            when: Time condition - "GREATER", "LESS", or "WITHIN"
            upper_time: Upper time limit in seconds
            level_a: Start voltage level
            level_b: End voltage level
            window: Time measurement window - "TA", "TB", or "TAB"
            lower_time: Lower time limit in seconds (required for WITHIN)

        Returns:
            Complete slope trigger configuration

        Use cases:
        - Detecting slow edges (signal integrity issues)
        - Finding fast transients
        - Validating rise/fall time specifications
        """
        # Validate WITHIN requires lower_time
        if when == "WITHIN" and lower_time is None:
            raise ValueError("lower_time is required when when='WITHIN'")

        # Set trigger mode to SLOPE
        scope.instrument.write(":TRIG:MODE SLOP")  # type: ignore[reportAttributeAccessIssue]

        # Set source channel
        scope.instrument.write(f":TRIG:SLOP:SOUR CHAN{channel}")  # type: ignore[reportAttributeAccessIssue]

        # Map when condition to SCPI format
        when_map = {
            "GREATER": "GRE",
            "LESS": "LESS",
            "WITHIN": "WITH",
        }
        scope.instrument.write(f":TRIG:SLOP:WHEN {when_map[when]}")  # type: ignore[reportAttributeAccessIssue]

        # Set upper time
        scope.instrument.write(f":TRIG:SLOP:TUPP {upper_time}")  # type: ignore[reportAttributeAccessIssue]

        # Set lower time if WITHIN
        if when == "WITHIN" and lower_time is not None:
            scope.instrument.write(f":TRIG:SLOP:TLOW {lower_time}")  # type: ignore[reportAttributeAccessIssue]

        # Map polarity to SCPI format
        polarity_map = {
            "POSITIVE": "POS",
            "NEGATIVE": "NEG",
        }
        scope.instrument.write(f":TRIG:SLOP:POL {polarity_map[polarity]}")  # type: ignore[reportAttributeAccessIssue]

        # Set voltage levels
        scope.instrument.write(f":TRIG:SLOP:ALEV {level_a}")  # type: ignore[reportAttributeAccessIssue]
        scope.instrument.write(f":TRIG:SLOP:BLEV {level_b}")  # type: ignore[reportAttributeAccessIssue]

        # Set window
        scope.instrument.write(f":TRIG:SLOP:WIND {window}")  # type: ignore[reportAttributeAccessIssue]

        # Verify configuration by reading back
        actual_source = scope.instrument.query(":TRIG:SLOP:SOUR?").strip()  # type: ignore[reportAttributeAccessIssue]
        actual_when = scope.instrument.query(":TRIG:SLOP:WHEN?").strip()  # type: ignore[reportAttributeAccessIssue]
        actual_upper = float(scope.instrument.query(":TRIG:SLOP:TUPP?"))  # type: ignore[reportAttributeAccessIssue]
        actual_polarity = scope.instrument.query(":TRIG:SLOP:POL?").strip()  # type: ignore[reportAttributeAccessIssue]
        actual_level_a = float(scope.instrument.query(":TRIG:SLOP:ALEV?"))  # type: ignore[reportAttributeAccessIssue]
        actual_level_b = float(scope.instrument.query(":TRIG:SLOP:BLEV?"))  # type: ignore[reportAttributeAccessIssue]
        actual_window = scope.instrument.query(":TRIG:SLOP:WIND?").strip()  # type: ignore[reportAttributeAccessIssue]

        # Parse channel from source
        actual_channel = _parse_channel_from_scpi(actual_source)

        # Read lower time if applicable
        actual_lower: Optional[float] = None
        if when == "WITHIN":
            actual_lower = float(scope.instrument.query(":TRIG:SLOP:TLOW?"))  # type: ignore[reportAttributeAccessIssue]

        # Map responses back to user-friendly format
        when_reverse = {"GRE": "GREATER", "GREA": "GREATER", "LESS": "LESS", "WITH": "WITHIN"}
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

        Args:
            channel: Source channel (1-4)
            polarity: Sync polarity - "POSITIVE" or "NEGATIVE"
            mode: Trigger mode - "ODD_FIELD", "EVEN_FIELD", "LINE", or "ALL_LINES"
            standard: Video standard - "PAL_SECAM", "NTSC", "480P", or "576P"
            level: Trigger level in volts
            line_number: Line number for LINE mode (1-625 for PAL, 1-525 for NTSC)

        Returns:
            Complete video trigger configuration
        """
        # Validate LINE mode requires line_number
        if mode == "LINE" and line_number is None:
            raise ValueError("line_number is required when mode='LINE'")

        # Set trigger mode to VIDEO
        scope.instrument.write(":TRIG:MODE VID")  # type: ignore[reportAttributeAccessIssue]

        # Set source channel
        scope.instrument.write(f":TRIG:VID:SOUR CHAN{channel}")  # type: ignore[reportAttributeAccessIssue]

        # Map polarity to SCPI format
        polarity_map = {
            "POSITIVE": "POS",
            "NEGATIVE": "NEG",
        }
        scope.instrument.write(f":TRIG:VID:POL {polarity_map[polarity]}")  # type: ignore[reportAttributeAccessIssue]

        # Map mode to SCPI format
        mode_map = {
            "ODD_FIELD": "ODDF",
            "EVEN_FIELD": "EVENF",
            "LINE": "LINE",
            "ALL_LINES": "ALIN",
        }
        scope.instrument.write(f":TRIG:VID:MODE {mode_map[mode]}")  # type: ignore[reportAttributeAccessIssue]

        # Set line number if LINE mode
        if mode == "LINE" and line_number is not None:
            scope.instrument.write(f":TRIG:VID:LINE {line_number}")  # type: ignore[reportAttributeAccessIssue]

        # Map standard to SCPI format
        standard_map = {
            "PAL_SECAM": "PALS",
            "NTSC": "NTSC",
            "480P": "480P",
            "576P": "576P",
        }
        scope.instrument.write(f":TRIG:VID:STAN {standard_map[standard]}")  # type: ignore[reportAttributeAccessIssue]

        # Set trigger level
        scope.instrument.write(f":TRIG:VID:LEV {level}")  # type: ignore[reportAttributeAccessIssue]

        # Verify configuration
        actual_source = scope.instrument.query(":TRIG:VID:SOUR?").strip()  # type: ignore[reportAttributeAccessIssue]
        actual_polarity = scope.instrument.query(":TRIG:VID:POL?").strip()  # type: ignore[reportAttributeAccessIssue]
        actual_mode = scope.instrument.query(":TRIG:VID:MODE?").strip()  # type: ignore[reportAttributeAccessIssue]
        actual_standard = scope.instrument.query(":TRIG:VID:STAN?").strip()  # type: ignore[reportAttributeAccessIssue]
        actual_level = float(scope.instrument.query(":TRIG:VID:LEV?"))  # type: ignore[reportAttributeAccessIssue]

        # Parse channel from source
        actual_channel = _parse_channel_from_scpi(actual_source)

        # Read line number if LINE mode
        actual_line: Optional[int] = None
        if mode == "LINE":
            actual_line = int(scope.instrument.query(":TRIG:VID:LINE?"))  # type: ignore[reportAttributeAccessIssue]

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

        Args:
            pattern: 4-element list of pattern values, e.g., ["H", "L", "X", "R"]
            levels: Dictionary of trigger levels per channel, e.g., {1: 1.5, 2: 2.0, 4: 1.8}

        Returns:
            Complete pattern trigger configuration

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
        scope.instrument.write(":TRIG:MODE PATT")  # type: ignore[reportAttributeAccessIssue]

        # Set pattern (comma-separated)
        pattern_str = ",".join(pattern)
        scope.instrument.write(f":TRIG:PATT:PATT {pattern_str}")  # type: ignore[reportAttributeAccessIssue]

        # Set trigger levels for specified channels
        for channel, level in levels.items():
            if channel < 1 or channel > 4:
                raise ValueError(f"Channel must be 1-4, got {channel}")
            scope.instrument.write(f":TRIG:PATT:LEV{channel} {level}")  # type: ignore[reportAttributeAccessIssue]

        # Verify configuration
        actual_pattern_str = scope.instrument.query(":TRIG:PATT:PATT?").strip()  # type: ignore[reportAttributeAccessIssue]
        actual_pattern = actual_pattern_str.split(",")

        # Read back levels for all channels
        actual_levels = {}
        for channel in range(1, 5):
            try:
                level = float(scope.instrument.query(f":TRIG:PATT:LEV{channel}?"))  # type: ignore[reportAttributeAccessIssue]
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

        Args:
            channel: Source channel (1-4)
            polarity: Runt pulse direction - "POSITIVE" or "NEGATIVE"
            when: Width qualification - "GREATER", "LESS", or "WITHIN"
            upper_width: Upper width limit in seconds
            lower_width: Lower width limit in seconds
            level_a: Upper voltage threshold
            level_b: Lower voltage threshold

        Returns:
            Complete runt trigger configuration

        Use cases:
        - Signal integrity analysis
        - Detecting incomplete transitions
        - Power supply glitches
        """
        # Set trigger mode to RUNT
        scope.instrument.write(":TRIG:MODE RUNT")  # type: ignore[reportAttributeAccessIssue]

        # Set source channel
        scope.instrument.write(f":TRIG:RUNT:SOUR CHAN{channel}")  # type: ignore[reportAttributeAccessIssue]

        # Map polarity to SCPI format
        polarity_map = {
            "POSITIVE": "POS",
            "NEGATIVE": "NEG",
        }
        scope.instrument.write(f":TRIG:RUNT:POL {polarity_map[polarity]}")  # type: ignore[reportAttributeAccessIssue]

        # Map when condition to SCPI format
        when_map = {
            "GREATER": "GRE",
            "LESS": "LESS",
            "WITHIN": "WITH",
        }
        scope.instrument.write(f":TRIG:RUNT:WHEN {when_map[when]}")  # type: ignore[reportAttributeAccessIssue]

        # Set width limits
        scope.instrument.write(f":TRIG:RUNT:UWID {upper_width}")  # type: ignore[reportAttributeAccessIssue]
        scope.instrument.write(f":TRIG:RUNT:LWID {lower_width}")  # type: ignore[reportAttributeAccessIssue]

        # Set voltage thresholds
        scope.instrument.write(f":TRIG:RUNT:ALEV {level_a}")  # type: ignore[reportAttributeAccessIssue]
        scope.instrument.write(f":TRIG:RUNT:BLEV {level_b}")  # type: ignore[reportAttributeAccessIssue]

        # Verify configuration
        actual_source = scope.instrument.query(":TRIG:RUNT:SOUR?").strip()  # type: ignore[reportAttributeAccessIssue]
        actual_polarity = scope.instrument.query(":TRIG:RUNT:POL?").strip()  # type: ignore[reportAttributeAccessIssue]
        actual_when = scope.instrument.query(":TRIG:RUNT:WHEN?").strip()  # type: ignore[reportAttributeAccessIssue]
        actual_upper = float(scope.instrument.query(":TRIG:RUNT:UWID?"))  # type: ignore[reportAttributeAccessIssue]
        actual_lower = float(scope.instrument.query(":TRIG:RUNT:LWID?"))  # type: ignore[reportAttributeAccessIssue]
        actual_level_a = float(scope.instrument.query(":TRIG:RUNT:ALEV?"))  # type: ignore[reportAttributeAccessIssue]
        actual_level_b = float(scope.instrument.query(":TRIG:RUNT:BLEV?"))  # type: ignore[reportAttributeAccessIssue]

        # Parse channel from source
        actual_channel = _parse_channel_from_scpi(actual_source)

        # Map responses back
        polarity_reverse = {"POS": "POSITIVE", "NEG": "NEGATIVE"}
        when_reverse = {"GRE": "GREATER", "GREA": "GREATER", "LESS": "LESS", "WITH": "WITHIN"}

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

        Args:
            channel: Source channel (1-4)
            slope: Edge to start timeout counter - "POSITIVE" or "NEGATIVE"
            timeout: Idle time in seconds before trigger
            level: Trigger level in volts

        Returns:
            Complete timeout trigger configuration

        Use cases:
        - Detecting bus stalls
        - Finding protocol timeouts
        - Analyzing idle periods
        """
        # Set trigger mode to TIMEOUT
        scope.instrument.write(":TRIG:MODE TIM")  # type: ignore[reportAttributeAccessIssue]

        # Set source channel
        scope.instrument.write(f":TRIG:TIM:SOUR CHAN{channel}")  # type: ignore[reportAttributeAccessIssue]

        # Map slope to SCPI format
        slope_map = {
            "POSITIVE": "POS",
            "NEGATIVE": "NEG",
        }
        scope.instrument.write(f":TRIG:TIM:SLOP {slope_map[slope]}")  # type: ignore[reportAttributeAccessIssue]

        # Set timeout duration
        scope.instrument.write(f":TRIG:TIM:TIM {timeout}")  # type: ignore[reportAttributeAccessIssue]

        # Set trigger level
        scope.instrument.write(f":TRIG:TIM:LEV {level}")  # type: ignore[reportAttributeAccessIssue]

        # Verify configuration
        actual_source = scope.instrument.query(":TRIG:TIM:SOUR?").strip()  # type: ignore[reportAttributeAccessIssue]
        actual_slope = scope.instrument.query(":TRIG:TIM:SLOP?").strip()  # type: ignore[reportAttributeAccessIssue]
        actual_timeout = float(scope.instrument.query(":TRIG:TIM:TIM?"))  # type: ignore[reportAttributeAccessIssue]
        actual_level = float(scope.instrument.query(":TRIG:TIM:LEV?"))  # type: ignore[reportAttributeAccessIssue]

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
            Literal["GREATER", "LESS", "WITHIN"],
            Field(description="Pattern qualifier: GREATER, LESS, or WITHIN"),
        ],
        when: Annotated[
            Literal["GREATER", "LESS", "WITHIN"],
            Field(description="Duration condition: GREATER, LESS, or WITHIN"),
        ],
        upper_width: UpperTimeLimitField,
        lower_width: LowerTimeLimitField,
        level: TriggerLevelField,
    ) -> DurationTriggerResult:
        """
        Configure duration trigger for pattern that persists for specific duration.

        Triggers on pattern that persists for specific duration.

        Args:
            channel: Source channel (1-4)
            pattern_type: Pattern qualifier - "GREATER", "LESS", or "WITHIN"
            when: Duration condition - "GREATER", "LESS", or "WITHIN"
            upper_width: Upper time limit in seconds
            lower_width: Lower time limit in seconds
            level: Trigger level in volts

        Returns:
            Complete duration trigger configuration
        """
        # Set trigger mode to DURATION
        scope.instrument.write(":TRIG:MODE DUR")  # type: ignore[reportAttributeAccessIssue]

        # Set source channel
        scope.instrument.write(f":TRIG:DUR:SOUR CHAN{channel}")  # type: ignore[reportAttributeAccessIssue]

        # Map conditions to SCPI format
        condition_map = {
            "GREATER": "GRE",
            "LESS": "LESS",
            "WITHIN": "WITH",
        }
        scope.instrument.write(f":TRIG:DUR:TYPE {condition_map[pattern_type]}")  # type: ignore[reportAttributeAccessIssue]
        scope.instrument.write(f":TRIG:DUR:WHEN {condition_map[when]}")  # type: ignore[reportAttributeAccessIssue]

        # Set time limits
        scope.instrument.write(f":TRIG:DUR:UWID {upper_width}")  # type: ignore[reportAttributeAccessIssue]
        scope.instrument.write(f":TRIG:DUR:LWID {lower_width}")  # type: ignore[reportAttributeAccessIssue]

        # Set trigger level
        scope.instrument.write(f":TRIG:DUR:LEV {level}")  # type: ignore[reportAttributeAccessIssue]

        # Verify configuration
        actual_source = scope.instrument.query(":TRIG:DUR:SOUR?").strip()  # type: ignore[reportAttributeAccessIssue]
        actual_type = scope.instrument.query(":TRIG:DUR:TYPE?").strip()  # type: ignore[reportAttributeAccessIssue]
        actual_when = scope.instrument.query(":TRIG:DUR:WHEN?").strip()  # type: ignore[reportAttributeAccessIssue]
        actual_upper = float(scope.instrument.query(":TRIG:DUR:UWID?"))  # type: ignore[reportAttributeAccessIssue]
        actual_lower = float(scope.instrument.query(":TRIG:DUR:LWID?"))  # type: ignore[reportAttributeAccessIssue]
        actual_level = float(scope.instrument.query(":TRIG:DUR:LEV?"))  # type: ignore[reportAttributeAccessIssue]

        # Parse channel from source
        actual_channel = _parse_channel_from_scpi(actual_source)

        # Map responses back
        condition_reverse = {"GRE": "GREATER", "GREA": "GREATER", "LESS": "LESS", "WITH": "WITHIN"}

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

        Args:
            data_channel: Data signal channel (1-4)
            clock_channel: Clock signal channel (1-4)
            clock_slope: Clock edge to check - "POSITIVE" or "NEGATIVE"
            data_pattern: Expected data value - "H" or "L"
            setup_time: Minimum setup time in seconds
            hold_time: Minimum hold time in seconds
            data_level: Data threshold voltage
            clock_level: Clock threshold voltage

        Returns:
            Complete setup/hold trigger configuration

        Use cases:
        - Verifying timing relationships
        - Debugging synchronous interfaces
        - Validating memory timing
        """
        # Set trigger mode to SETUP/HOLD
        scope.instrument.write(":TRIG:MODE SHOL")  # type: ignore[reportAttributeAccessIssue]

        # Set data and clock sources
        scope.instrument.write(f":TRIG:SHOL:DSRC CHAN{data_channel}")  # type: ignore[reportAttributeAccessIssue]
        scope.instrument.write(f":TRIG:SHOL:CSRC CHAN{clock_channel}")  # type: ignore[reportAttributeAccessIssue]

        # Map clock slope to SCPI format
        slope_map = {
            "POSITIVE": "POS",
            "NEGATIVE": "NEG",
        }
        scope.instrument.write(f":TRIG:SHOL:SLOP {slope_map[clock_slope]}")  # type: ignore[reportAttributeAccessIssue]

        # Set data pattern
        scope.instrument.write(f":TRIG:SHOL:PATT {data_pattern}")  # type: ignore[reportAttributeAccessIssue]

        # Set setup and hold times
        scope.instrument.write(f":TRIG:SHOL:STIM {setup_time}")  # type: ignore[reportAttributeAccessIssue]
        scope.instrument.write(f":TRIG:SHOL:HTIM {hold_time}")  # type: ignore[reportAttributeAccessIssue]

        # Set voltage levels
        scope.instrument.write(f":TRIG:SHOL:DLEV {data_level}")  # type: ignore[reportAttributeAccessIssue]
        scope.instrument.write(f":TRIG:SHOL:CLEV {clock_level}")  # type: ignore[reportAttributeAccessIssue]

        # Verify configuration
        actual_dsrc = scope.instrument.query(":TRIG:SHOL:DSRC?").strip()  # type: ignore[reportAttributeAccessIssue]
        actual_csrc = scope.instrument.query(":TRIG:SHOL:CSRC?").strip()  # type: ignore[reportAttributeAccessIssue]
        actual_slope = scope.instrument.query(":TRIG:SHOL:SLOP?").strip()  # type: ignore[reportAttributeAccessIssue]
        actual_pattern = scope.instrument.query(":TRIG:SHOL:PATT?").strip()  # type: ignore[reportAttributeAccessIssue]
        actual_setup = float(scope.instrument.query(":TRIG:SHOL:STIM?"))  # type: ignore[reportAttributeAccessIssue]
        actual_hold = float(scope.instrument.query(":TRIG:SHOL:HTIM?"))  # type: ignore[reportAttributeAccessIssue]
        actual_dlev = float(scope.instrument.query(":TRIG:SHOL:DLEV?"))  # type: ignore[reportAttributeAccessIssue]
        actual_clev = float(scope.instrument.query(":TRIG:SHOL:CLEV?"))  # type: ignore[reportAttributeAccessIssue]

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

        Args:
            channel: Source channel (1-4)
            slope: Edge direction to count - "POSITIVE" or "NEGATIVE"
            idle_time: Minimum idle time in seconds before starting count
            edge_count: Which edge number to trigger on (1-65535)
            level: Trigger level in volts

        Returns:
            Complete Nth edge trigger configuration

        Use cases:
        - Triggering inside burst transmissions
        - Skipping preamble/sync edges
        - Analyzing periodic burst signals
        """
        # Validate edge count range
        if edge_count < 1 or edge_count > 65535:
            raise ValueError(f"edge_count must be 1-65535, got {edge_count}")

        # Set trigger mode to NTH EDGE
        scope.instrument.write(":TRIG:MODE NEDG")  # type: ignore[reportAttributeAccessIssue]

        # Set source channel
        scope.instrument.write(f":TRIG:NEDG:SOUR CHAN{channel}")  # type: ignore[reportAttributeAccessIssue]

        # Map slope to SCPI format
        slope_map = {
            "POSITIVE": "POS",
            "NEGATIVE": "NEG",
        }
        scope.instrument.write(f":TRIG:NEDG:SLOP {slope_map[slope]}")  # type: ignore[reportAttributeAccessIssue]

        # Set idle time and edge count
        scope.instrument.write(f":TRIG:NEDG:IDLE {idle_time}")  # type: ignore[reportAttributeAccessIssue]
        scope.instrument.write(f":TRIG:NEDG:EDGE {edge_count}")  # type: ignore[reportAttributeAccessIssue]

        # Set trigger level
        scope.instrument.write(f":TRIG:NEDG:LEV {level}")  # type: ignore[reportAttributeAccessIssue]

        # Verify configuration
        actual_source = scope.instrument.query(":TRIG:NEDG:SOUR?").strip()  # type: ignore[reportAttributeAccessIssue]
        actual_slope = scope.instrument.query(":TRIG:NEDG:SLOP?").strip()  # type: ignore[reportAttributeAccessIssue]
        actual_idle = float(scope.instrument.query(":TRIG:NEDG:IDLE?"))  # type: ignore[reportAttributeAccessIssue]
        actual_count = int(scope.instrument.query(":TRIG:NEDG:EDGE?"))  # type: ignore[reportAttributeAccessIssue]
        actual_level = float(scope.instrument.query(":TRIG:NEDG:LEV?"))  # type: ignore[reportAttributeAccessIssue]

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

        Args:
            channel: Source channel (1-4)
            slope: Edge direction - "POSITIVE" or "NEGATIVE"
            position: Trigger position - "EXIT", "ENTER", or "TIME"
            level_a: Upper voltage threshold
            level_b: Lower voltage threshold
            time: Duration for TIME position mode (seconds, required for TIME)

        Returns:
            Complete window trigger configuration

        Use cases:
        - Power supply regulation analysis
        - Detecting over/under voltage
        - Tracking signal excursions
        """
        # Validate TIME position requires time
        if position == "TIME" and time is None:
            raise ValueError("time is required when position='TIME'")

        # Set trigger mode to WINDOW
        scope.instrument.write(":TRIG:MODE WIND")  # type: ignore[reportAttributeAccessIssue]

        # Set source channel
        scope.instrument.write(f":TRIG:WIND:SOUR CHAN{channel}")  # type: ignore[reportAttributeAccessIssue]

        # Map slope to SCPI format
        slope_map = {
            "POSITIVE": "POS",
            "NEGATIVE": "NEG",
        }
        scope.instrument.write(f":TRIG:WIND:SLOP {slope_map[slope]}")  # type: ignore[reportAttributeAccessIssue]

        # Set position
        scope.instrument.write(f":TRIG:WIND:POS {position}")  # type: ignore[reportAttributeAccessIssue]

        # Set time if TIME position
        if position == "TIME" and time is not None:
            scope.instrument.write(f":TRIG:WIND:TIME {time}")  # type: ignore[reportAttributeAccessIssue]

        # Set voltage thresholds
        scope.instrument.write(f":TRIG:WIND:ALEV {level_a}")  # type: ignore[reportAttributeAccessIssue]
        scope.instrument.write(f":TRIG:WIND:BLEV {level_b}")  # type: ignore[reportAttributeAccessIssue]

        # Verify configuration
        actual_source = scope.instrument.query(":TRIG:WIND:SOUR?").strip()  # type: ignore[reportAttributeAccessIssue]
        actual_slope = scope.instrument.query(":TRIG:WIND:SLOP?").strip()  # type: ignore[reportAttributeAccessIssue]
        actual_position = scope.instrument.query(":TRIG:WIND:POS?").strip()  # type: ignore[reportAttributeAccessIssue]
        actual_level_a = float(scope.instrument.query(":TRIG:WIND:ALEV?"))  # type: ignore[reportAttributeAccessIssue]
        actual_level_b = float(scope.instrument.query(":TRIG:WIND:BLEV?"))  # type: ignore[reportAttributeAccessIssue]

        # Parse channel from source
        actual_channel = _parse_channel_from_scpi(actual_source)

        # Read time if TIME position
        actual_time: Optional[float] = None
        if position == "TIME":
            actual_time = float(scope.instrument.query(":TRIG:WIND:TIME?"))  # type: ignore[reportAttributeAccessIssue]

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

        Args:
            source_a_channel: First signal channel (1-4)
            source_b_channel: Second signal channel (1-4)
            slope_a: Source A edge direction - "POSITIVE" or "NEGATIVE"
            slope_b: Source B edge direction - "POSITIVE" or "NEGATIVE"
            delay_type: Delay condition - "GREATER", "LESS", or "WITHIN"
            upper_time: Upper time limit in seconds
            level_a: Source A threshold voltage
            level_b: Source B threshold voltage
            lower_time: Lower time limit in seconds (required for WITHIN)

        Returns:
            Complete delay trigger configuration

        Use cases:
        - Measuring propagation delays
        - Detecting timing skew
        - Verifying signal sequencing
        """
        # Validate WITHIN requires lower_time
        if delay_type == "WITHIN" and lower_time is None:
            raise ValueError("lower_time is required when delay_type='WITHIN'")

        # Set trigger mode to DELAY
        scope.instrument.write(":TRIG:MODE DEL")  # type: ignore[reportAttributeAccessIssue]

        # Set source channels
        scope.instrument.write(f":TRIG:DEL:SA CHAN{source_a_channel}")  # type: ignore[reportAttributeAccessIssue]
        scope.instrument.write(f":TRIG:DEL:SB CHAN{source_b_channel}")  # type: ignore[reportAttributeAccessIssue]

        # Map slopes to SCPI format
        slope_map = {
            "POSITIVE": "POS",
            "NEGATIVE": "NEG",
        }
        scope.instrument.write(f":TRIG:DEL:SLOPA {slope_map[slope_a]}")  # type: ignore[reportAttributeAccessIssue]
        scope.instrument.write(f":TRIG:DEL:SLOPB {slope_map[slope_b]}")  # type: ignore[reportAttributeAccessIssue]

        # Map delay type to SCPI format
        type_map = {
            "GREATER": "GRE",
            "LESS": "LESS",
            "WITHIN": "WITH",
        }
        scope.instrument.write(f":TRIG:DEL:TYPE {type_map[delay_type]}")  # type: ignore[reportAttributeAccessIssue]

        # Set time limits
        scope.instrument.write(f":TRIG:DEL:TUPP {upper_time}")  # type: ignore[reportAttributeAccessIssue]
        if delay_type == "WITHIN" and lower_time is not None:
            scope.instrument.write(f":TRIG:DEL:TLOW {lower_time}")  # type: ignore[reportAttributeAccessIssue]

        # Set voltage levels
        scope.instrument.write(f":TRIG:DEL:LEVA {level_a}")  # type: ignore[reportAttributeAccessIssue]
        scope.instrument.write(f":TRIG:DEL:LEVB {level_b}")  # type: ignore[reportAttributeAccessIssue]

        # Verify configuration
        actual_sa = scope.instrument.query(":TRIG:DEL:SA?").strip()  # type: ignore[reportAttributeAccessIssue]
        actual_sb = scope.instrument.query(":TRIG:DEL:SB?").strip()  # type: ignore[reportAttributeAccessIssue]
        actual_slope_a = scope.instrument.query(":TRIG:DEL:SLOPA?").strip()  # type: ignore[reportAttributeAccessIssue]
        actual_slope_b = scope.instrument.query(":TRIG:DEL:SLOPB?").strip()  # type: ignore[reportAttributeAccessIssue]
        actual_type = scope.instrument.query(":TRIG:DEL:TYPE?").strip()  # type: ignore[reportAttributeAccessIssue]
        actual_upper = float(scope.instrument.query(":TRIG:DEL:TUPP?"))  # type: ignore[reportAttributeAccessIssue]
        actual_level_a = float(scope.instrument.query(":TRIG:DEL:LEVA?"))  # type: ignore[reportAttributeAccessIssue]
        actual_level_b = float(scope.instrument.query(":TRIG:DEL:LEVB?"))  # type: ignore[reportAttributeAccessIssue]

        # Parse channels from source
        actual_source_a = _parse_channel_from_scpi(actual_sa)
        actual_source_b = _parse_channel_from_scpi(actual_sb)

        # Read lower time if WITHIN
        actual_lower: Optional[float] = None
        if delay_type == "WITHIN":
            actual_lower = float(scope.instrument.query(":TRIG:DEL:TLOW?"))  # type: ignore[reportAttributeAccessIssue]

        # Map responses back
        slope_reverse = {"POS": "POSITIVE", "NEG": "NEGATIVE"}
        type_reverse = {"GRE": "GREATER", "GREA": "GREATER", "LESS": "LESS", "WITH": "WITHIN"}

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

    # === MEMORY & ACQUISITION SETTINGS ===

    @mcp.tool
    @with_scope_connection
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
        scope.instrument.write(f":ACQ:MDEP {memory_depth.value}")  # type: ignore[reportAttributeAccessIssue]

        # Verify the setting
        actual_depth = float(scope.instrument.query(":ACQ:MDEP?"))  # type: ignore[reportAttributeAccessIssue]

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

        Args:
            acquisition_type: Acquisition type

        Returns:
            Acquisition type setting
        """
        # Map enum to SCPI format
        type_map = {
            AcquisitionType.NORMAL: "NORMal",
            AcquisitionType.AVERAGE: "AVERages",
            AcquisitionType.PEAK: "PEAK",
            AcquisitionType.ULTRA: "ULTRa",
        }

        scpi_type = type_map[acquisition_type]
        scope.instrument.write(f":ACQ:TYPE {scpi_type}")  # type: ignore[reportAttributeAccessIssue]

        # Verify the setting
        actual_type = scope.instrument.query(":ACQ:TYPE?").strip()  # type: ignore[reportAttributeAccessIssue]

        return AcquisitionTypeResult(acquisition_type=map_acquisition_type(actual_type))

    @mcp.tool
    @with_scope_connection
    async def get_sample_rate() -> SampleRateResult:
        """
        Get current sample rate.

        Returns:
            Sample rate information
        """
        sample_rate = float(scope.instrument.query(":ACQ:SRAT?"))  # type: ignore[reportAttributeAccessIssue]

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

        Returns:
            Action confirmation
        """
        scope.instrument.write(":AUT")  # type: ignore[reportAttributeAccessIssue]

        # Auto setup takes a moment
        time.sleep(2)

        return ActionResult(action=SystemAction.AUTO_SETUP)

    @mcp.tool
    @with_scope_connection
    async def clear_display() -> ActionResult:
        """
        Clear the oscilloscope display.

        Returns:
            Action confirmation
        """
        scope.instrument.write(":CLE")  # type: ignore[reportAttributeAccessIssue]

        return ActionResult(action=SystemAction.CLEAR_DISPLAY)

    @mcp.tool
    @with_scope_connection
    async def get_screenshot() -> ScreenshotResult:
        """
        Capture a screenshot of the oscilloscope display.

        Saves a PNG image of the current oscilloscope screen display to a temporary file,
        including waveforms, measurements, and all visible UI elements.

        Returns:
            Screenshot file path
        """
        # Set image format to PNG
        scope.instrument.write(":SAVE:IMAGe:FORMat PNG")  # type: ignore[reportAttributeAccessIssue]

        # Query the image data
        # Response format: TMC header + binary PNG data + terminator
        png_data = scope.instrument.query_binary_values(  # type: ignore[reportAttributeAccessIssue]
            ":SAVE:IMAGe:DATA?",
            datatype="B",  # Read as bytes
            is_big_endian=False,
            container=bytes,  # Return as bytes object
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

        return ScreenshotResult(file_path=file_path)

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

        Args:
            channel: Channel number (1-4), optional
            mode: Measurement mode, optional. One of:
                - 'AC_RMS': RMS value with DC component removed
                - 'DC': Average (DC) value
                - 'AC+DC_RMS': True RMS including both AC and DC components
            enabled: Enable/disable DVM, optional

        Returns:
            Dictionary with complete DVM status after applying changes
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

        Returns:
            Dictionary with complete DVM status and current reading
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

    return mcp


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

    # Create temporary directory with automatic cleanup on exit
    with tempfile.TemporaryDirectory(prefix="rigol_dho824_") as temp_dir:
        # Create the server
        mcp = create_server(temp_dir)

        if args.http:
            # Run with HTTP transport
            mcp.run(transport="http", host=args.host, port=args.port, path=args.path)
        else:
            # Default to stdio transport
            mcp.run()


if __name__ == "__main__":
    main()
