"""MCP server for Rigol DHO824 oscilloscope."""

import os
from typing import Optional, TypedDict, Annotated, List, Dict, Any
from pydantic import Field
from fastmcp import FastMCP
from dotenv import load_dotenv
import pyvisa

# Import our modules
from .waveform import WaveformCapture
from .channel import ChannelControl, BandwidthLimit
from .trigger import TriggerControl
from .acquisition import AcquisitionControl


# Type definitions for results
class ModelNumberResult(TypedDict):
    """Result containing the oscilloscope model number."""
    model: Annotated[str, Field(description="The oscilloscope model number", examples=["DHO824", "DHO804", "DHO914", "DHO924"])]


class SoftwareVersionResult(TypedDict):
    """Result containing the oscilloscope software version."""
    version: Annotated[str, Field(description="The firmware/software version", examples=["00.02.01.SP2", "00.01.05", "00.02.00.SP1"])]


class SerialNumberResult(TypedDict):
    """Result containing the oscilloscope serial number."""
    serial: Annotated[str, Field(description="The unique serial number", examples=["DHO8240000001", "DHO8040000123", "DHO9140000456"])]


class WaveformDataResult(TypedDict):
    """Result containing captured waveform data."""
    channel: Annotated[str, Field(description="Channel identifier")]
    data: Annotated[List[float], Field(description="Voltage values in specified units")]
    time: Annotated[List[float], Field(description="Time values in seconds")]
    units: Annotated[str, Field(description="Voltage units (V, mV, μV, nV)")]
    sample_rate: Annotated[float, Field(description="Sample rate in Sa/s")]
    points: Annotated[int, Field(description="Number of data points")]
    timestamp: Annotated[str, Field(description="ISO format timestamp")]


class StatusResult(TypedDict):
    """Generic status result."""
    success: Annotated[bool, Field(description="Whether the operation succeeded")]
    message: Annotated[Optional[str], Field(description="Optional status message")]


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
            Tuple of (manufacturer, model, serial, version) or None if parsing fails
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
        channels: Annotated[List[int], Field(description="List of channel numbers to capture (1-4)")] = [1]
    ) -> List[Dict[str, Any]]:
        """
        Capture waveform data from specified channels.
        
        Captures data in RAW mode with WORD format (16-bit) for maximum accuracy.
        Automatically converts raw values to calibrated voltages with appropriate units.
        
        Args:
            channels: List of channel numbers to capture (1-4), defaults to [1]
            
        Returns:
            List of dictionaries containing waveform data, time arrays, units, and metadata
        """
        try:
            if not scope.connect():
                raise Exception("Failed to connect to oscilloscope")
            
            # Validate channel numbers
            for ch in channels:
                if ch not in [1, 2, 3, 4]:
                    raise ValueError(f"Invalid channel number: {ch}. Must be 1-4")
            
            # Capture data from all requested channels
            results = WaveformCapture.capture_multiple_channels(scope.instrument, channels)
            
            return results
            
        except Exception as e:
            raise Exception(f"Error capturing waveform: {str(e)}") from e
        finally:
            scope.disconnect()
    
    # === CHANNEL CONTROL TOOLS ===
    
    @mcp.tool
    async def set_channel_enable(
        channel: Annotated[int, Field(description="Channel number (1-4)")],
        enable: Annotated[bool, Field(description="True to enable, False to disable")]
    ) -> Dict[str, Any]:
        """
        Enable or disable a channel display.
        
        Args:
            channel: Channel number (1-4)
            enable: True to enable, False to disable
            
        Returns:
            Status dictionary with success indicator
        """
        try:
            if not scope.connect():
                raise Exception("Failed to connect to oscilloscope")
            
            result = ChannelControl.set_channel_enable(scope.instrument, channel, enable)
            return result
            
        except Exception as e:
            raise Exception(f"Error setting channel enable: {str(e)}") from e
        finally:
            scope.disconnect()
    
    @mcp.tool
    async def set_channel_coupling(
        channel: Annotated[int, Field(description="Channel number (1-4)")],
        coupling: Annotated[str, Field(description="Coupling mode: AC, DC, or GND")]
    ) -> Dict[str, Any]:
        """
        Set channel coupling mode.
        
        Args:
            channel: Channel number (1-4)
            coupling: Coupling mode ("AC", "DC", "GND")
            
        Returns:
            Status dictionary with actual coupling set
        """
        try:
            if not scope.connect():
                raise Exception("Failed to connect to oscilloscope")
            
            result = ChannelControl.set_channel_coupling(scope.instrument, channel, coupling)
            return result
            
        except Exception as e:
            raise Exception(f"Error setting channel coupling: {str(e)}") from e
        finally:
            scope.disconnect()
    
    @mcp.tool
    async def set_channel_probe(
        channel: Annotated[int, Field(description="Channel number (1-4)")],
        ratio: Annotated[float, Field(description="Probe ratio (e.g., 1, 10, 100, 1000)")]
    ) -> Dict[str, Any]:
        """
        Set channel probe attenuation ratio.
        
        Args:
            channel: Channel number (1-4)
            ratio: Probe ratio (e.g., 1, 10, 100, 1000)
            
        Returns:
            Status dictionary with actual probe ratio set
        """
        try:
            if not scope.connect():
                raise Exception("Failed to connect to oscilloscope")
            
            result = ChannelControl.set_channel_probe(scope.instrument, channel, ratio)
            return result
            
        except Exception as e:
            raise Exception(f"Error setting channel probe: {str(e)}") from e
        finally:
            scope.disconnect()
    
    @mcp.tool
    async def set_channel_bandwidth(
        channel: Annotated[int, Field(description="Channel number (1-4)", ge=1, le=4)],
        bandwidth: Annotated[Optional[BandwidthLimit], Field(description="Bandwidth limit: OFF (full bandwidth) or LIMIT_20M (20MHz limit). Default is OFF")] = None
    ) -> Dict[str, Any]:
        """
        Set channel bandwidth limit to reduce noise and filter high frequencies.
        
        The bandwidth limit attenuates high frequency components in the signal that
        are greater than the specified limit. This is useful for reducing noise in
        displayed waveforms while preserving the lower frequency components of interest.
        
        The DHO800 series supports:
        - BandwidthLimit.OFF: Full bandwidth (no limiting)
        - BandwidthLimit.LIMIT_20M: 20 MHz bandwidth limit
        
        Note: Bandwidth limiting not only reduces noise but also attenuates or eliminates
        the high frequency components of the signal.
        
        Args:
            channel: Channel number (1-4)
            bandwidth: Bandwidth limit enum value, None defaults to OFF
            
        Returns:
            Status dictionary with actual bandwidth limit set
        """
        try:
            if not scope.connect():
                raise Exception("Failed to connect to oscilloscope")
            
            result = ChannelControl.set_channel_bandwidth(scope.instrument, channel, bandwidth)
            return result
            
        except Exception as e:
            raise Exception(f"Error setting channel bandwidth: {str(e)}") from e
        finally:
            scope.disconnect()
    
    @mcp.tool
    async def get_channel_status(
        channel: Annotated[int, Field(description="Channel number (1-4)")]
    ) -> Dict[str, Any]:
        """
        Get comprehensive channel status and settings.
        
        Args:
            channel: Channel number (1-4)
            
        Returns:
            Dictionary with all channel settings
        """
        try:
            if not scope.connect():
                raise Exception("Failed to connect to oscilloscope")
            
            result = ChannelControl.get_channel_status(scope.instrument, channel)
            return result
            
        except Exception as e:
            raise Exception(f"Error getting channel status: {str(e)}") from e
        finally:
            scope.disconnect()
    
    # === SCALE ADJUSTMENT TOOLS ===
    
    @mcp.tool
    async def set_vertical_scale(
        channel: Annotated[int, Field(description="Channel number (1-4)")],
        scale: Annotated[float, Field(description="Vertical scale in V/div")]
    ) -> Dict[str, Any]:
        """
        Set channel vertical scale (V/div).
        
        Args:
            channel: Channel number (1-4)
            scale: Vertical scale in V/div
            
        Returns:
            Status dictionary with actual scale set
        """
        try:
            if not scope.connect():
                raise Exception("Failed to connect to oscilloscope")
            
            result = ChannelControl.set_vertical_scale(scope.instrument, channel, scale)
            return result
            
        except Exception as e:
            raise Exception(f"Error setting vertical scale: {str(e)}") from e
        finally:
            scope.disconnect()
    
    @mcp.tool
    async def set_vertical_offset(
        channel: Annotated[int, Field(description="Channel number (1-4)")],
        offset: Annotated[float, Field(description="Vertical offset in volts")]
    ) -> Dict[str, Any]:
        """
        Set channel vertical offset.
        
        Args:
            channel: Channel number (1-4)
            offset: Vertical offset in volts
            
        Returns:
            Status dictionary with actual offset set
        """
        try:
            if not scope.connect():
                raise Exception("Failed to connect to oscilloscope")
            
            result = ChannelControl.set_vertical_offset(scope.instrument, channel, offset)
            return result
            
        except Exception as e:
            raise Exception(f"Error setting vertical offset: {str(e)}") from e
        finally:
            scope.disconnect()
    
    @mcp.tool
    async def set_timebase_scale(
        scale: Annotated[float, Field(description="Time per division in seconds")]
    ) -> Dict[str, Any]:
        """
        Set horizontal timebase scale.
        
        Args:
            scale: Time per division in seconds
            
        Returns:
            Status dictionary with actual scale set
        """
        try:
            if not scope.connect():
                raise Exception("Failed to connect to oscilloscope")
            
            result = AcquisitionControl.set_timebase_scale(scope.instrument, scale)
            return result
            
        except Exception as e:
            raise Exception(f"Error setting timebase scale: {str(e)}") from e
        finally:
            scope.disconnect()
    
    @mcp.tool
    async def set_timebase_offset(
        offset: Annotated[float, Field(description="Time offset in seconds")]
    ) -> Dict[str, Any]:
        """
        Set horizontal timebase offset.
        
        Args:
            offset: Time offset in seconds
            
        Returns:
            Status dictionary with actual offset set
        """
        try:
            if not scope.connect():
                raise Exception("Failed to connect to oscilloscope")
            
            result = AcquisitionControl.set_timebase_offset(scope.instrument, offset)
            return result
            
        except Exception as e:
            raise Exception(f"Error setting timebase offset: {str(e)}") from e
        finally:
            scope.disconnect()
    
    # === ACQUISITION CONTROL TOOLS ===
    
    @mcp.tool
    async def run_acquisition() -> Dict[str, Any]:
        """
        Start continuous acquisition (RUN mode).
        
        Returns:
            Status dictionary with trigger status
        """
        try:
            if not scope.connect():
                raise Exception("Failed to connect to oscilloscope")
            
            result = AcquisitionControl.run_acquisition(scope.instrument)
            return result
            
        except Exception as e:
            raise Exception(f"Error starting acquisition: {str(e)}") from e
        finally:
            scope.disconnect()
    
    @mcp.tool
    async def stop_acquisition() -> Dict[str, Any]:
        """
        Stop acquisition (STOP mode).
        
        Returns:
            Status dictionary with trigger status
        """
        try:
            if not scope.connect():
                raise Exception("Failed to connect to oscilloscope")
            
            result = AcquisitionControl.stop_acquisition(scope.instrument)
            return result
            
        except Exception as e:
            raise Exception(f"Error stopping acquisition: {str(e)}") from e
        finally:
            scope.disconnect()
    
    @mcp.tool
    async def single_acquisition() -> Dict[str, Any]:
        """
        Perform single acquisition (SINGLE mode).
        
        Returns:
            Status dictionary with trigger status
        """
        try:
            if not scope.connect():
                raise Exception("Failed to connect to oscilloscope")
            
            result = AcquisitionControl.single_acquisition(scope.instrument)
            return result
            
        except Exception as e:
            raise Exception(f"Error performing single acquisition: {str(e)}") from e
        finally:
            scope.disconnect()
    
    @mcp.tool
    async def force_trigger() -> Dict[str, Any]:
        """
        Force a trigger event.
        
        Returns:
            Status dictionary
        """
        try:
            if not scope.connect():
                raise Exception("Failed to connect to oscilloscope")
            
            result = TriggerControl.force_trigger(scope.instrument)
            return result
            
        except Exception as e:
            raise Exception(f"Error forcing trigger: {str(e)}") from e
        finally:
            scope.disconnect()
    
    @mcp.tool
    async def get_trigger_status() -> Dict[str, Any]:
        """
        Get current trigger status.
        
        Returns:
            Dictionary with trigger status and settings
        """
        try:
            if not scope.connect():
                raise Exception("Failed to connect to oscilloscope")
            
            result = TriggerControl.get_trigger_status(scope.instrument)
            return result
            
        except Exception as e:
            raise Exception(f"Error getting trigger status: {str(e)}") from e
        finally:
            scope.disconnect()
    
    # === TRIGGER CONFIGURATION TOOLS ===
    
    @mcp.tool
    async def set_trigger_mode(
        mode: Annotated[str, Field(description="Trigger mode: EDGE, PULSE, SLOPE, etc.")]
    ) -> Dict[str, Any]:
        """
        Set trigger mode.
        
        Args:
            mode: Trigger mode ("EDGE", "PULSE", "SLOPE", "VIDEO", "PATTERN", 
                  "RS232", "I2C", "SPI", "CAN", "LIN", "FLEXRAY", "CANFD")
            
        Returns:
            Status dictionary with actual mode set
        """
        try:
            if not scope.connect():
                raise Exception("Failed to connect to oscilloscope")
            
            result = TriggerControl.set_trigger_mode(scope.instrument, mode)
            return result
            
        except Exception as e:
            raise Exception(f"Error setting trigger mode: {str(e)}") from e
        finally:
            scope.disconnect()
    
    @mcp.tool
    async def set_trigger_source(
        source: Annotated[str, Field(description="Trigger source: CH1, CH2, CH3, CH4, EXT, AC")]
    ) -> Dict[str, Any]:
        """
        Set trigger source for edge trigger.
        
        Args:
            source: Trigger source ("CH1", "CH2", "CH3", "CH4", "EXT", "AC")
            
        Returns:
            Status dictionary with actual source set
        """
        try:
            if not scope.connect():
                raise Exception("Failed to connect to oscilloscope")
            
            result = TriggerControl.set_trigger_source(scope.instrument, source)
            return result
            
        except Exception as e:
            raise Exception(f"Error setting trigger source: {str(e)}") from e
        finally:
            scope.disconnect()
    
    @mcp.tool
    async def set_trigger_level(
        level: Annotated[float, Field(description="Trigger level in volts")],
        source: Annotated[Optional[str], Field(description="Optional trigger source")] = None
    ) -> Dict[str, Any]:
        """
        Set trigger level voltage.
        
        Args:
            level: Trigger level in volts
            source: Optional source to set level for (defaults to current source)
            
        Returns:
            Status dictionary with actual level set
        """
        try:
            if not scope.connect():
                raise Exception("Failed to connect to oscilloscope")
            
            result = TriggerControl.set_trigger_level(scope.instrument, level, source)
            return result
            
        except Exception as e:
            raise Exception(f"Error setting trigger level: {str(e)}") from e
        finally:
            scope.disconnect()
    
    @mcp.tool
    async def set_trigger_slope(
        slope: Annotated[str, Field(description="Edge slope: RISING, FALLING, or EITHER")]
    ) -> Dict[str, Any]:
        """
        Set trigger edge slope.
        
        Args:
            slope: Edge slope ("RISING", "FALLING", "EITHER", "POSITIVE", "NEGATIVE")
            
        Returns:
            Status dictionary with actual slope set
        """
        try:
            if not scope.connect():
                raise Exception("Failed to connect to oscilloscope")
            
            result = TriggerControl.set_trigger_slope(scope.instrument, slope)
            return result
            
        except Exception as e:
            raise Exception(f"Error setting trigger slope: {str(e)}") from e
        finally:
            scope.disconnect()
    
    # === MEMORY & ACQUISITION SETTINGS ===
    
    @mcp.tool
    async def set_memory_depth(
        depth: Annotated[str, Field(description="Memory depth: AUTO, 1K, 10K, 100K, 1M, 10M, 25M, 50M")]
    ) -> Dict[str, Any]:
        """
        Set acquisition memory depth.
        
        Args:
            depth: Memory depth ("AUTO", "1K", "10K", "100K", "1M", "10M", "25M", "50M")
            
        Returns:
            Status dictionary with actual depth set
        """
        try:
            if not scope.connect():
                raise Exception("Failed to connect to oscilloscope")
            
            result = AcquisitionControl.set_memory_depth(scope.instrument, depth)
            return result
            
        except Exception as e:
            raise Exception(f"Error setting memory depth: {str(e)}") from e
        finally:
            scope.disconnect()
    
    @mcp.tool
    async def set_acquisition_type(
        acq_type: Annotated[str, Field(description="Acquisition type: NORMAL, AVERAGE, PEAK, or ULTRA")]
    ) -> Dict[str, Any]:
        """
        Set acquisition type.
        
        Args:
            acq_type: Acquisition type ("NORMAL", "AVERAGE", "PEAK", "ULTRA")
            
        Returns:
            Status dictionary with actual type set
        """
        try:
            if not scope.connect():
                raise Exception("Failed to connect to oscilloscope")
            
            result = AcquisitionControl.set_acquisition_type(scope.instrument, acq_type)
            return result
            
        except Exception as e:
            raise Exception(f"Error setting acquisition type: {str(e)}") from e
        finally:
            scope.disconnect()
    
    @mcp.tool
    async def get_sample_rate() -> Dict[str, Any]:
        """
        Get current sample rate.
        
        Returns:
            Dictionary with sample rate information
        """
        try:
            if not scope.connect():
                raise Exception("Failed to connect to oscilloscope")
            
            result = AcquisitionControl.get_sample_rate(scope.instrument)
            return result
            
        except Exception as e:
            raise Exception(f"Error getting sample rate: {str(e)}") from e
        finally:
            scope.disconnect()
    
    # === UTILITY TOOLS ===
    
    @mcp.tool
    async def auto_setup() -> Dict[str, Any]:
        """
        Perform automatic setup of the oscilloscope.
        
        Automatically configures vertical scale, horizontal scale, and trigger
        settings for optimal display of the input signal.
        
        Returns:
            Status dictionary
        """
        try:
            if not scope.connect():
                raise Exception("Failed to connect to oscilloscope")
            
            result = AcquisitionControl.auto_setup(scope.instrument)
            return result
            
        except Exception as e:
            raise Exception(f"Error performing auto setup: {str(e)}") from e
        finally:
            scope.disconnect()
    
    @mcp.tool
    async def clear_display() -> Dict[str, Any]:
        """
        Clear the oscilloscope display.
        
        Returns:
            Status dictionary
        """
        try:
            if not scope.connect():
                raise Exception("Failed to connect to oscilloscope")
            
            result = AcquisitionControl.clear_display(scope.instrument)
            return result
            
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