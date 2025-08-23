"""Channel control functions for Rigol DHO824."""

from typing import Optional, Dict, Any
from enum import Enum


class BandwidthLimit(str, Enum):
    """Bandwidth limit options for DHO800 series oscilloscopes."""
    OFF = "OFF"  # Full bandwidth (no limiting)
    LIMIT_20M = "20M"  # 20 MHz bandwidth limit


class ChannelControl:
    """Handle channel configuration and control."""
    
    @staticmethod
    def set_channel_enable(instrument, channel: int, enable: bool) -> Dict[str, Any]:
        """
        Enable or disable a channel display.
        
        Args:
            instrument: PyVISA instrument instance
            channel: Channel number (1-4)
            enable: True to enable, False to disable
            
        Returns:
            Status dictionary
        """
        state = "ON" if enable else "OFF"
        instrument.write(f':CHAN{channel}:DISP {state}')
        
        # Verify the setting
        actual_state = int(instrument.query(f':CHAN{channel}:DISP?'))
        
        return {
            "channel": f"CH{channel}",
            "enabled": bool(actual_state),
            "success": bool(actual_state) == enable
        }
    
    @staticmethod
    def set_channel_coupling(instrument, channel: int, coupling: str) -> Dict[str, Any]:
        """
        Set channel coupling mode.
        
        Args:
            instrument: PyVISA instrument instance
            channel: Channel number (1-4)
            coupling: Coupling mode ("AC", "DC", "GND")
            
        Returns:
            Status dictionary
        """
        valid_couplings = ["AC", "DC", "GND"]
        coupling = coupling.upper()
        
        if coupling not in valid_couplings:
            raise ValueError(f"Invalid coupling mode. Must be one of {valid_couplings}")
        
        instrument.write(f':CHAN{channel}:COUP {coupling}')
        
        # Verify the setting
        actual_coupling = instrument.query(f':CHAN{channel}:COUP?').strip()
        
        return {
            "channel": f"CH{channel}",
            "coupling": actual_coupling,
            "success": actual_coupling == coupling or actual_coupling == coupling[:2]
        }
    
    @staticmethod
    def set_channel_probe(instrument, channel: int, ratio: float) -> Dict[str, Any]:
        """
        Set channel probe attenuation ratio.
        
        Args:
            instrument: PyVISA instrument instance
            channel: Channel number (1-4)
            ratio: Probe ratio (e.g., 1, 10, 100, 1000)
            
        Returns:
            Status dictionary
        """
        valid_ratios = [0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5,
                       1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000]
        
        if ratio not in valid_ratios:
            # Find closest valid ratio
            import numpy as np
            ratio = valid_ratios[np.argmin(np.abs(np.array(valid_ratios) - ratio))]
        
        instrument.write(f':CHAN{channel}:PROB {ratio}')
        
        # Verify the setting
        actual_ratio = float(instrument.query(f':CHAN{channel}:PROB?'))
        
        return {
            "channel": f"CH{channel}",
            "probe_ratio": actual_ratio,
            "success": abs(actual_ratio - ratio) < 0.01
        }
    
    @staticmethod
    def set_channel_bandwidth(instrument, channel: int, bandwidth: Optional[BandwidthLimit]) -> Dict[str, Any]:
        """
        Set channel bandwidth limit.
        
        Setting the bandwidth limit can reduce noise in displayed waveforms by
        attenuating high frequency components greater than the limit.
        
        Args:
            instrument: PyVISA instrument instance
            channel: Channel number (1-4)
            bandwidth: Bandwidth limit enum value, None defaults to OFF
            
        Returns:
            Status dictionary
        """
        if bandwidth is None:
            bandwidth = BandwidthLimit.OFF
        
        # Use the enum's value for the SCPI command
        bw_value = bandwidth.value
        
        instrument.write(f':CHAN{channel}:BWL {bw_value}')
        
        # Verify the setting
        actual_bw = instrument.query(f':CHAN{channel}:BWL?').strip()
        
        return {
            "channel": f"CH{channel}",
            "bandwidth_limit": actual_bw,
            "success": actual_bw == bw_value
        }
    
    @staticmethod
    def get_channel_status(instrument, channel: int) -> Dict[str, Any]:
        """
        Get comprehensive channel status.
        
        Args:
            instrument: PyVISA instrument instance
            channel: Channel number (1-4)
            
        Returns:
            Dictionary with all channel settings
        """
        status = {
            "channel": f"CH{channel}",
            "enabled": bool(int(instrument.query(f':CHAN{channel}:DISP?'))),
            "coupling": instrument.query(f':CHAN{channel}:COUP?').strip(),
            "probe_ratio": float(instrument.query(f':CHAN{channel}:PROB?')),
            "bandwidth_limit": instrument.query(f':CHAN{channel}:BWL?').strip(),
            "vertical_scale": float(instrument.query(f':CHAN{channel}:SCAL?')),
            "vertical_offset": float(instrument.query(f':CHAN{channel}:OFFS?')),
            "invert": bool(int(instrument.query(f':CHAN{channel}:INV?'))),
            "units": instrument.query(f':CHAN{channel}:UNIT?').strip()
        }
        
        return status
    
    @staticmethod
    def set_vertical_scale(instrument, channel: int, scale: float) -> Dict[str, Any]:
        """
        Set channel vertical scale (V/div).
        
        Args:
            instrument: PyVISA instrument instance
            channel: Channel number (1-4)
            scale: Vertical scale in V/div
            
        Returns:
            Status dictionary
        """
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
        if scale not in valid_scales:
            import numpy as np
            scale = valid_scales[np.argmin(np.abs(np.array(valid_scales) - scale))]
        
        instrument.write(f':CHAN{channel}:SCAL {scale}')
        
        # Verify the setting
        actual_scale = float(instrument.query(f':CHAN{channel}:SCAL?'))
        
        return {
            "channel": f"CH{channel}",
            "vertical_scale": actual_scale,
            "units": "V/div",
            "success": abs(actual_scale - scale) < 1e-6
        }
    
    @staticmethod
    def set_vertical_offset(instrument, channel: int, offset: float) -> Dict[str, Any]:
        """
        Set channel vertical offset.
        
        Args:
            instrument: PyVISA instrument instance
            channel: Channel number (1-4)
            offset: Vertical offset in volts
            
        Returns:
            Status dictionary
        """
        instrument.write(f':CHAN{channel}:OFFS {offset}')
        
        # Verify the setting
        actual_offset = float(instrument.query(f':CHAN{channel}:OFFS?'))
        
        return {
            "channel": f"CH{channel}",
            "vertical_offset": actual_offset,
            "units": "V",
            "success": abs(actual_offset - offset) < 1e-6
        }