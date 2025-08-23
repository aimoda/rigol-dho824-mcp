"""Waveform capture and data processing for Rigol DHO824."""

import numpy as np
from typing import Dict, List, Optional, Any
from datetime import datetime


class WaveformCapture:
    """Handle waveform data capture and conversion."""
    
    @staticmethod
    def capture_channel_data(instrument, channel: int) -> Dict[str, Any]:
        """
        Capture waveform data from a single channel.
        
        Args:
            instrument: PyVISA instrument instance
            channel: Channel number (1-4)
            
        Returns:
            Dictionary with waveform data and metadata
        """
        # Stop acquisition to read from internal memory
        instrument.write(':STOP')
        
        # Set source channel
        instrument.write(f':WAV:SOUR CHAN{channel}')
        
        # Configure for RAW mode with WORD format (16-bit)
        instrument.write(':WAV:MODE RAW')
        instrument.write(':WAV:FORM WORD')
        
        # Query memory depth to determine available points
        memory_depth = float(instrument.query(':ACQ:MDEP?'))
        
        # Set read range (adjust if memory depth is large)
        max_points = min(int(memory_depth), 1000000)  # Cap at 1M points
        instrument.write(':WAV:STAR 1')
        instrument.write(f':WAV:STOP {max_points}')
        
        # Query waveform parameters for conversion
        y_increment = float(instrument.query(':WAV:YINC?'))
        y_origin = float(instrument.query(':WAV:YOR?'))
        y_reference = float(instrument.query(':WAV:YREF?'))
        x_increment = float(instrument.query(':WAV:XINC?'))
        x_origin = float(instrument.query(':WAV:XOR?'))
        
        # Query channel settings
        vertical_scale = float(instrument.query(f':CHAN{channel}:SCAL?'))
        vertical_offset = float(instrument.query(f':CHAN{channel}:OFFS?'))
        probe_ratio = float(instrument.query(f':CHAN{channel}:PROB?'))
        
        # Query sample rate
        sample_rate = float(instrument.query(':ACQ:SRAT?'))
        
        # Capture the waveform data (16-bit unsigned integers)
        raw_data = instrument.query_binary_values(
            ':WAV:DATA?', 
            datatype='H',  # Unsigned 16-bit
            is_big_endian=False
        )
        
        # Convert to numpy array
        raw_array = np.array(raw_data, dtype=np.float64)
        
        # Convert raw data to voltage values
        voltage_data = (raw_array - y_origin - y_reference) * y_increment
        
        # Apply probe ratio correction
        voltage_data = voltage_data * probe_ratio
        
        # Determine appropriate units
        max_voltage = np.max(np.abs(voltage_data))
        if max_voltage < 1e-6:
            units = "nV"
            scale_factor = 1e9
        elif max_voltage < 1e-3:
            units = "μV"
            scale_factor = 1e6
        elif max_voltage < 1:
            units = "mV"
            scale_factor = 1e3
        else:
            units = "V"
            scale_factor = 1
        
        # Scale the data to appropriate units
        scaled_data = voltage_data * scale_factor
        
        # Generate time array
        time_points = np.arange(len(voltage_data)) * x_increment + x_origin
        
        return {
            "channel": f"CH{channel}",
            "data": scaled_data.tolist(),  # Convert to list for JSON serialization
            "time": time_points.tolist(),
            "units": units,
            "sample_rate": sample_rate,
            "time_increment": x_increment,
            "time_offset": x_origin,
            "vertical_scale": vertical_scale,
            "vertical_offset": vertical_offset,
            "probe_ratio": probe_ratio,
            "points": len(voltage_data),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "statistics": {
                "min": float(np.min(scaled_data)),
                "max": float(np.max(scaled_data)),
                "mean": float(np.mean(scaled_data)),
                "std": float(np.std(scaled_data)),
                "rms": float(np.sqrt(np.mean(scaled_data**2)))
            }
        }
    
    @staticmethod
    def capture_multiple_channels(instrument, channels: List[int]) -> List[Dict[str, Any]]:
        """
        Capture waveform data from multiple channels.
        
        Args:
            instrument: PyVISA instrument instance
            channels: List of channel numbers (1-4)
            
        Returns:
            List of dictionaries with waveform data for each channel
        """
        results = []
        
        # Stop acquisition once for all channels
        instrument.write(':STOP')
        
        for channel in channels:
            # Check if channel is enabled
            channel_enabled = int(instrument.query(f':CHAN{channel}:DISP?'))
            if not channel_enabled:
                continue
                
            try:
                data = WaveformCapture.capture_channel_data(instrument, channel)
                results.append(data)
            except Exception as e:
                # Log error but continue with other channels
                results.append({
                    "channel": f"CH{channel}",
                    "error": str(e)
                })
        
        return results