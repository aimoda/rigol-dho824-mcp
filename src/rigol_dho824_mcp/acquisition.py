"""Acquisition control for Rigol DHO824."""

from typing import Dict, Any
import time


class AcquisitionControl:
    """Handle acquisition control and settings."""
    
    @staticmethod
    def run_acquisition(instrument) -> Dict[str, Any]:
        """
        Start continuous acquisition (RUN mode).
        
        Args:
            instrument: PyVISA instrument instance
            
        Returns:
            Status dictionary
        """
        instrument.write(':RUN')
        
        # Give it a moment to start
        time.sleep(0.1)
        
        # Check trigger status
        status = instrument.query(':TRIG:STAT?').strip()
        
        return {
            "action": "run",
            "trigger_status": status,
            "success": True
        }
    
    @staticmethod
    def stop_acquisition(instrument) -> Dict[str, Any]:
        """
        Stop acquisition (STOP mode).
        
        Args:
            instrument: PyVISA instrument instance
            
        Returns:
            Status dictionary
        """
        instrument.write(':STOP')
        
        # Give it a moment to stop
        time.sleep(0.1)
        
        # Check trigger status
        status = instrument.query(':TRIG:STAT?').strip()
        
        return {
            "action": "stop",
            "trigger_status": status,
            "success": status == "STOP"
        }
    
    @staticmethod
    def single_acquisition(instrument) -> Dict[str, Any]:
        """
        Perform single acquisition (SINGLE mode).
        
        Args:
            instrument: PyVISA instrument instance
            
        Returns:
            Status dictionary
        """
        instrument.write(':SING')
        
        # Give it a moment to arm
        time.sleep(0.1)
        
        # Check trigger status
        status = instrument.query(':TRIG:STAT?').strip()
        
        return {
            "action": "single",
            "trigger_status": status,
            "success": True
        }
    
    @staticmethod
    def set_memory_depth(instrument, depth: str) -> Dict[str, Any]:
        """
        Set acquisition memory depth.
        
        Args:
            instrument: PyVISA instrument instance
            depth: Memory depth ("AUTO", "1K", "10K", "100K", "1M", "10M", "25M", "50M")
            
        Returns:
            Status dictionary
        """
        valid_depths = ["AUTO", "1K", "10K", "100K", "1M", "10M", "25M", "50M"]
        
        depth = depth.upper()
        if depth not in valid_depths:
            raise ValueError(f"Invalid memory depth. Must be one of {valid_depths}")
        
        instrument.write(f':ACQ:MDEP {depth}')
        
        # Verify the setting
        actual_depth = float(instrument.query(':ACQ:MDEP?'))
        
        # Convert to human-readable format
        if actual_depth >= 1e6:
            depth_str = f"{actual_depth/1e6:.0f}M"
        elif actual_depth >= 1e3:
            depth_str = f"{actual_depth/1e3:.0f}K"
        else:
            depth_str = f"{actual_depth:.0f}"
        
        return {
            "memory_depth": actual_depth,
            "memory_depth_str": depth_str,
            "success": True
        }
    
    @staticmethod
    def set_acquisition_type(instrument, acq_type: str) -> Dict[str, Any]:
        """
        Set acquisition type.
        
        Args:
            instrument: PyVISA instrument instance
            acq_type: Acquisition type ("NORMAL", "AVERAGE", "PEAK", "HIGHRES")
            
        Returns:
            Status dictionary
        """
        # Map friendly names to SCPI format
        type_map = {
            "NORMAL": "NORM",
            "NORM": "NORM",
            "AVERAGE": "AVER",
            "AVER": "AVER",
            "PEAK": "PEAK",
            "HIGHRES": "HRES",
            "HRES": "HRES"
        }
        
        acq_type = acq_type.upper()
        if acq_type not in type_map:
            raise ValueError(f"Invalid acquisition type. Must be one of {list(type_map.keys())}")
        
        scpi_type = type_map[acq_type]
        instrument.write(f':ACQ:TYPE {scpi_type}')
        
        # Verify the setting
        actual_type = instrument.query(':ACQ:TYPE?').strip()
        
        return {
            "acquisition_type": actual_type,
            "success": actual_type == scpi_type
        }
    
    @staticmethod
    def set_average_count(instrument, count: int) -> Dict[str, Any]:
        """
        Set number of averages for average acquisition mode.
        
        Args:
            instrument: PyVISA instrument instance
            count: Number of averages (2 to 8192, powers of 2)
            
        Returns:
            Status dictionary
        """
        # Valid average counts are powers of 2
        valid_counts = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192]
        
        if count not in valid_counts:
            # Find closest valid count
            import numpy as np
            count = valid_counts[np.argmin(np.abs(np.array(valid_counts) - count))]
        
        instrument.write(f':ACQ:AVER {count}')
        
        # Verify the setting
        actual_count = int(instrument.query(':ACQ:AVER?'))
        
        return {
            "average_count": actual_count,
            "success": actual_count == count
        }
    
    @staticmethod
    def get_sample_rate(instrument) -> Dict[str, Any]:
        """
        Get current sample rate.
        
        Args:
            instrument: PyVISA instrument instance
            
        Returns:
            Dictionary with sample rate information
        """
        sample_rate = float(instrument.query(':ACQ:SRAT?'))
        
        # Convert to human-readable format
        if sample_rate >= 1e9:
            rate_str = f"{sample_rate/1e9:.2f} GSa/s"
        elif sample_rate >= 1e6:
            rate_str = f"{sample_rate/1e6:.2f} MSa/s"
        elif sample_rate >= 1e3:
            rate_str = f"{sample_rate/1e3:.2f} kSa/s"
        else:
            rate_str = f"{sample_rate:.2f} Sa/s"
        
        return {
            "sample_rate": sample_rate,
            "sample_rate_str": rate_str,
            "units": "Sa/s"
        }
    
    @staticmethod
    def set_timebase_scale(instrument, scale: float) -> Dict[str, Any]:
        """
        Set horizontal timebase scale.
        
        Args:
            instrument: PyVISA instrument instance
            scale: Time per division in seconds
            
        Returns:
            Status dictionary
        """
        instrument.write(f':TIM:MAIN:SCAL {scale}')
        
        # Verify the setting
        actual_scale = float(instrument.query(':TIM:MAIN:SCAL?'))
        
        # Convert to human-readable format
        if actual_scale >= 1:
            scale_str = f"{actual_scale:.2f} s/div"
        elif actual_scale >= 1e-3:
            scale_str = f"{actual_scale*1e3:.2f} ms/div"
        elif actual_scale >= 1e-6:
            scale_str = f"{actual_scale*1e6:.2f} μs/div"
        else:
            scale_str = f"{actual_scale*1e9:.2f} ns/div"
        
        return {
            "timebase_scale": actual_scale,
            "timebase_scale_str": scale_str,
            "success": abs(actual_scale - scale) < 1e-12
        }
    
    @staticmethod
    def set_timebase_offset(instrument, offset: float) -> Dict[str, Any]:
        """
        Set horizontal timebase offset.
        
        Args:
            instrument: PyVISA instrument instance
            offset: Time offset in seconds
            
        Returns:
            Status dictionary
        """
        instrument.write(f':TIM:MAIN:OFFS {offset}')
        
        # Verify the setting
        actual_offset = float(instrument.query(':TIM:MAIN:OFFS?'))
        
        return {
            "timebase_offset": actual_offset,
            "units": "s",
            "success": abs(actual_offset - offset) < 1e-12
        }
    
    @staticmethod
    def auto_setup(instrument) -> Dict[str, Any]:
        """
        Perform automatic setup of the oscilloscope.
        
        Args:
            instrument: PyVISA instrument instance
            
        Returns:
            Status dictionary
        """
        instrument.write(':AUT')
        
        # Auto setup takes a moment
        time.sleep(2)
        
        return {
            "action": "auto_setup",
            "success": True
        }
    
    @staticmethod
    def clear_display(instrument) -> Dict[str, Any]:
        """
        Clear the display.
        
        Args:
            instrument: PyVISA instrument instance
            
        Returns:
            Status dictionary
        """
        instrument.write(':CLE')
        
        return {
            "action": "clear_display",
            "success": True
        }