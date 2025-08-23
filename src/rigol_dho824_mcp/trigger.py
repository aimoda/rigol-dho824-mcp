"""Trigger configuration for Rigol DHO824."""

from typing import Dict, Any


class TriggerControl:
    """Handle trigger configuration and control."""
    
    @staticmethod
    def set_trigger_mode(instrument, mode: str) -> Dict[str, Any]:
        """
        Set trigger mode.
        
        Args:
            instrument: PyVISA instrument instance
            mode: Trigger mode ("EDGE", "PULSE", "SLOPE", "VIDEO", "PATTERN", 
                  "RS232", "I2C", "SPI", "CAN", "LIN", "FLEXRAY", "CANFD")
            
        Returns:
            Status dictionary
        """
        valid_modes = ["EDGE", "PULSE", "SLOPE", "VIDEO", "PATTERN", 
                      "RS232", "I2C", "SPI", "CAN", "LIN", "FLEXRAY", "CANFD"]
        
        mode = mode.upper()
        if mode not in valid_modes:
            raise ValueError(f"Invalid trigger mode. Must be one of {valid_modes}")
        
        instrument.write(f':TRIG:MODE {mode}')
        
        # Verify the setting
        actual_mode = instrument.query(':TRIG:MODE?').strip()
        
        return {
            "trigger_mode": actual_mode,
            "success": actual_mode == mode or actual_mode == mode[:4]
        }
    
    @staticmethod
    def set_trigger_source(instrument, source: str) -> Dict[str, Any]:
        """
        Set trigger source for edge trigger.
        
        Args:
            instrument: PyVISA instrument instance
            source: Trigger source ("CH1", "CH2", "CH3", "CH4", "EXT", "AC")
            
        Returns:
            Status dictionary
        """
        # Ensure we're in edge trigger mode
        current_mode = instrument.query(':TRIG:MODE?').strip()
        if current_mode not in ["EDGE", "EDG"]:
            instrument.write(':TRIG:MODE EDGE')
        
        # Map friendly names to SCPI format
        source_map = {
            "CH1": "CHAN1", "CH2": "CHAN2", "CH3": "CHAN3", "CH4": "CHAN4",
            "CHAN1": "CHAN1", "CHAN2": "CHAN2", "CHAN3": "CHAN3", "CHAN4": "CHAN4",
            "EXT": "EXT", "AC": "AC"
        }
        
        source = source.upper()
        if source not in source_map:
            raise ValueError(f"Invalid trigger source. Must be one of {list(source_map.keys())}")
        
        scpi_source = source_map[source]
        instrument.write(f':TRIG:EDGE:SOUR {scpi_source}')
        
        # Verify the setting
        actual_source = instrument.query(':TRIG:EDGE:SOUR?').strip()
        
        return {
            "trigger_source": actual_source,
            "success": actual_source == scpi_source or actual_source == scpi_source[:4]
        }
    
    @staticmethod
    def set_trigger_level(instrument, level: float, source: str = None) -> Dict[str, Any]:
        """
        Set trigger level voltage.
        
        Args:
            instrument: PyVISA instrument instance
            level: Trigger level in volts
            source: Optional source to set level for (defaults to current source)
            
        Returns:
            Status dictionary
        """
        # If source specified, set it first
        if source:
            TriggerControl.set_trigger_source(instrument, source)
        
        instrument.write(f':TRIG:EDGE:LEV {level}')
        
        # Verify the setting
        actual_level = float(instrument.query(':TRIG:EDGE:LEV?'))
        
        return {
            "trigger_level": actual_level,
            "units": "V",
            "success": abs(actual_level - level) < 1e-6
        }
    
    @staticmethod
    def set_trigger_slope(instrument, slope: str) -> Dict[str, Any]:
        """
        Set trigger edge slope.
        
        Args:
            instrument: PyVISA instrument instance
            slope: Edge slope ("RISING", "FALLING", "EITHER", "POSITIVE", "NEGATIVE")
            
        Returns:
            Status dictionary
        """
        # Map friendly names to SCPI format
        slope_map = {
            "RISING": "POS", "POSITIVE": "POS", "POS": "POS",
            "FALLING": "NEG", "NEGATIVE": "NEG", "NEG": "NEG",
            "EITHER": "EITH", "EITH": "EITH"
        }
        
        slope = slope.upper()
        if slope not in slope_map:
            raise ValueError(f"Invalid trigger slope. Must be one of {list(slope_map.keys())}")
        
        scpi_slope = slope_map[slope]
        instrument.write(f':TRIG:EDGE:SLOP {scpi_slope}')
        
        # Verify the setting
        actual_slope = instrument.query(':TRIG:EDGE:SLOP?').strip()
        
        return {
            "trigger_slope": actual_slope,
            "success": actual_slope == scpi_slope
        }
    
    @staticmethod
    def get_trigger_status(instrument) -> Dict[str, Any]:
        """
        Get current trigger status.
        
        Args:
            instrument: PyVISA instrument instance
            
        Returns:
            Dictionary with trigger status
        """
        # Query trigger status
        status = instrument.query(':TRIG:STAT?').strip()
        
        # Map status codes to friendly names
        status_map = {
            "TD": "triggered",
            "WAIT": "waiting",
            "RUN": "running",
            "AUTO": "auto",
            "STOP": "stopped"
        }
        
        friendly_status = status_map.get(status, status)
        
        # Get additional trigger info
        mode = instrument.query(':TRIG:MODE?').strip()
        
        result = {
            "status": friendly_status,
            "raw_status": status,
            "mode": mode
        }
        
        # If edge trigger, get edge-specific settings
        if mode in ["EDGE", "EDG"]:
            result.update({
                "source": instrument.query(':TRIG:EDGE:SOUR?').strip(),
                "level": float(instrument.query(':TRIG:EDGE:LEV?')),
                "slope": instrument.query(':TRIG:EDGE:SLOP?').strip()
            })
        
        return result
    
    @staticmethod
    def set_trigger_sweep(instrument, sweep: str) -> Dict[str, Any]:
        """
        Set trigger sweep mode.
        
        Args:
            instrument: PyVISA instrument instance
            sweep: Sweep mode ("AUTO", "NORMAL", "SINGLE")
            
        Returns:
            Status dictionary
        """
        valid_sweeps = ["AUTO", "NORMAL", "SINGLE", "NORM", "SING"]
        
        sweep = sweep.upper()
        if sweep not in valid_sweeps:
            raise ValueError(f"Invalid sweep mode. Must be one of {valid_sweeps}")
        
        # Map to SCPI format
        sweep_map = {
            "NORMAL": "NORM",
            "SINGLE": "SING",
            "AUTO": "AUTO",
            "NORM": "NORM",
            "SING": "SING"
        }
        
        scpi_sweep = sweep_map.get(sweep, sweep)
        instrument.write(f':TRIG:SWE {scpi_sweep}')
        
        # Verify the setting
        actual_sweep = instrument.query(':TRIG:SWE?').strip()
        
        return {
            "trigger_sweep": actual_sweep,
            "success": actual_sweep == scpi_sweep
        }
    
    @staticmethod
    def force_trigger(instrument) -> Dict[str, Any]:
        """
        Force a trigger event.
        
        Args:
            instrument: PyVISA instrument instance
            
        Returns:
            Status dictionary
        """
        instrument.write(':TFOR')
        
        return {
            "action": "force_trigger",
            "success": True
        }