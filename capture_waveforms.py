#!/usr/bin/env python3
"""
Capture waveforms from Rigol DHO824 oscilloscope in multiple formats.

This script captures waveforms in three channel configurations and saves them
in CSV, BIN, WFM, PNG, and JSON formats, then transfers them via FTP.
"""

import os
import time
import json
from ftplib import FTP
from pathlib import Path
from typing import List, Dict, Any
import pyvisa
import numpy as np


class RigolWaveformCapture:
    """Handle waveform capture and file transfer from Rigol oscilloscope."""
    
    def __init__(self, resource_string: str = None, ftp_host: str = None):
        """
        Initialize the capture tool.
        
        Args:
            resource_string: VISA resource string for oscilloscope
            ftp_host: IP address of oscilloscope for FTP transfer
        """
        self.rm = pyvisa.ResourceManager()
        self.instrument = None
        self.resource_string = resource_string or os.getenv('RIGOL_RESOURCE')
        self.ftp_host = ftp_host or self.extract_ip_from_resource()
        self.output_dir = Path('captured_waveforms')
        self.output_dir.mkdir(exist_ok=True)
        
    def extract_ip_from_resource(self) -> str:
        """Extract IP address from VISA resource string."""
        if self.resource_string and 'TCPIP' in self.resource_string:
            # Format: TCPIP0::192.168.44.37::inst0::INSTR
            parts = self.resource_string.split('::')
            if len(parts) >= 2:
                return parts[1]
        return '192.168.44.37'  # Default IP
    
    def connect(self) -> bool:
        """Connect to the oscilloscope."""
        try:
            if self.resource_string:
                self.instrument = self.rm.open_resource(self.resource_string)
            else:
                # Auto-discover
                resources = self.rm.list_resources()
                rigol_resources = [r for r in resources if 'RIGOL' in r.upper()]
                if not rigol_resources:
                    raise Exception("No Rigol oscilloscope found")
                self.instrument = self.rm.open_resource(rigol_resources[0])
            
            self.instrument.timeout = 30000  # 30 seconds for large transfers
            identity = self.instrument.query('*IDN?')
            print(f"Connected to: {identity.strip()}")
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from the oscilloscope."""
        if self.instrument:
            self.instrument.close()
            self.instrument = None
    
    def setup_channels(self, channels: List[int]):
        """
        Enable specified channels and disable others, then auto setup.
        
        Args:
            channels: List of channel numbers to enable (1-4)
        """
        print(f"Setting up channels: {channels}")
        
        # First, perform auto setup to get good vertical/horizontal settings
        print("  Performing auto setup...")
        self.instrument.write(':AUToset')
        time.sleep(3)  # Wait for auto setup to complete
        
        # Now explicitly enable/disable channels as needed
        # Auto setup may have enabled all channels, so we set them explicitly
        print("  Setting channel states after auto setup:")
        for ch in range(1, 5):
            if ch in channels:
                self.instrument.write(f':CHANnel{ch}:DISPlay ON')
                print(f"    Channel {ch}: ON")
            else:
                self.instrument.write(f':CHANnel{ch}:DISPlay OFF')
                print(f"    Channel {ch}: OFF")
        
        time.sleep(1)  # Give time for channel settings to take effect
        
        # Set memory depth to 10k points
        self.instrument.write(':ACQuire:MDEPth 10000')
        print("  Memory depth set to 10k points")
        
        # Ensure we're in a good trigger state
        self.instrument.write(':TRIG:MODE EDGE')
        self.instrument.write(':RUN')
        time.sleep(1)
        
        print("  Channel setup complete")
    
    def save_waveform_on_scope(self, base_filename: str, formats: List[str]) -> List[str]:
        """
        Save waveforms on oscilloscope in specified formats (without stopping/starting acquisition).
        
        Args:
            base_filename: Base filename without extension
            formats: List of formats to save ('csv', 'bin', 'wfm', 'png')
            
        Returns:
            List of filenames saved on scope
        """
        saved_files = []
        
        # Enable file overwriting
        self.instrument.write(':SAVE:OVER ON')
        
        for fmt in formats:
            filename = f"{base_filename}.{fmt}"
            scope_path = f"C:/{filename}"
            
            try:
                if fmt == 'png':
                    # Save screenshot
                    self.instrument.write(f':SAVE:IMAGe:FORMat PNG')
                    self.instrument.write(f':SAVE:IMAGe {scope_path}')
                    print(f"    Saved screenshot: {filename}")
                elif fmt == 'csv':
                    # Save screen waveform as CSV
                    self.instrument.write(f':SAVE:WAVeform {scope_path}')
                    print(f"    Saved waveform CSV: {filename}")
                elif fmt in ['bin', 'wfm']:
                    # Save memory waveform
                    self.instrument.write(f':SAVE:MEMory:WAVeform {scope_path}')
                    print(f"    Saved memory waveform: {filename}")
                
                # Wait for save to complete
                time.sleep(5)  # Longer delay for safety
                # Check if save is complete
                self.instrument.query(':SAVE:STATus?')
                
                saved_files.append(filename)
                
            except Exception as e:
                print(f"    Error saving {filename}: {e}")
        
        return saved_files
    
    
    def capture_raw_waveform(self, channels: List[int]) -> Dict[str, Any]:
        """
        Capture raw waveform data for JSON format (without stopping/starting acquisition).
        
        Args:
            channels: List of channel numbers to capture
            
        Returns:
            Dictionary with waveform data for all channels
        """
        waveform_data = {
            'channels': [],
            'capture_time': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        for channel in channels:
            # Check if channel is enabled
            channel_enabled = int(self.instrument.query(f':CHAN{channel}:DISP?'))
            if not channel_enabled:
                continue
            
            print(f"    Capturing raw data from channel {channel}...")
            
            # Set source channel and configure for RAW mode
            self.instrument.write(f':WAV:SOUR CHAN{channel}')
            self.instrument.write(':WAV:MODE RAW')
            self.instrument.write(':WAV:FORM WORD')  # 16-bit format
            
            # Set to read 10k points
            self.instrument.write(':WAV:STAR 1')
            self.instrument.write(':WAV:STOP 10000')
            
            # Query waveform parameters
            y_increment = float(self.instrument.query(':WAV:YINC?'))
            y_origin = float(self.instrument.query(':WAV:YOR?'))
            y_reference = float(self.instrument.query(':WAV:YREF?'))
            x_increment = float(self.instrument.query(':WAV:XINC?'))
            x_origin = float(self.instrument.query(':WAV:XOR?'))
            
            # Query channel settings
            vertical_scale = float(self.instrument.query(f':CHAN{channel}:SCAL?'))
            vertical_offset = float(self.instrument.query(f':CHAN{channel}:OFFS?'))
            probe_ratio = float(self.instrument.query(f':CHAN{channel}:PROB?'))
            
            # Query sample rate
            sample_rate = float(self.instrument.query(':ACQ:SRAT?'))
            
            # Read waveform data
            raw_data = self.instrument.query_binary_values(
                ':WAV:DATA?',
                datatype='H',  # Unsigned 16-bit
                is_big_endian=False
            )
            
            # Check for ADC saturation
            truncated = bool(np.max(raw_data) == 65535) if raw_data else False
            
            channel_data = {
                'channel': channel,
                'raw_data': raw_data[:10000],  # Limit to 10k points
                'truncated': truncated,
                'y_increment': y_increment,
                'y_origin': y_origin,
                'y_reference': y_reference,
                'x_increment': x_increment,
                'x_origin': x_origin,
                'vertical_scale': vertical_scale,
                'vertical_offset': vertical_offset,
                'probe_ratio': probe_ratio,
                'sample_rate': sample_rate,
                'points': len(raw_data[:10000])
            }
            
            waveform_data['channels'].append(channel_data)
        
        return waveform_data
    
    
    def save_json_file(self, data: Dict[str, Any], subdir: str, filename: str):
        """Save waveform data as JSON file in subdirectory."""
        dirpath = self.output_dir / subdir
        dirpath.mkdir(parents=True, exist_ok=True)
        filepath = dirpath / filename
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"    Saved JSON: {subdir}/{filename}")
    
    def download_files_via_ftp(self, filenames: List[str], subdir: str):
        """
        Download files from oscilloscope via FTP to subdirectory.
        
        Args:
            filenames: List of filenames to download
            subdir: Subdirectory name for organizing files
        """
        try:
            # Create subdirectory
            dirpath = self.output_dir / subdir
            dirpath.mkdir(parents=True, exist_ok=True)
            
            print(f"  Connecting to FTP server at {self.ftp_host}...")
            ftp = FTP()
            ftp.connect(self.ftp_host, 21, timeout=30)
            ftp.login('anonymous', '')
            
            # List files to verify
            files = ftp.nlst()
            print(f"  Files on FTP server: {files}")
            
            for filename in filenames:
                if filename in files:
                    # Use simple meaningful names for each format
                    ext = filename.split('.')[-1]
                    if ext == 'png':
                        local_filename = 'screenshot.png'
                    elif ext == 'csv':
                        local_filename = 'data.csv'
                    elif ext == 'bin':
                        local_filename = 'data.bin'
                    elif ext == 'wfm':
                        local_filename = 'data.wfm'
                    else:
                        local_filename = f'data.{ext}'
                    local_path = dirpath / local_filename
                    
                    with open(local_path, 'wb') as f:
                        ftp.retrbinary(f'RETR {filename}', f.write)
                    print(f"    Downloaded: {filename} -> {subdir}/{local_filename}")
                    
                    # Delete file from scope after download
                    try:
                        ftp.delete(filename)
                        print(f"    Deleted from scope: {filename}")
                    except:
                        pass  # Some FTP servers don't allow deletion
                else:
                    print(f"    File not found on FTP: {filename}")
            
            ftp.quit()
            
        except Exception as e:
            print(f"  FTP error: {e}")
    
    def capture_configuration(self, channels: List[int], name: str):
        """
        Capture waveforms for a specific channel configuration.
        
        Args:
            channels: List of channels to capture
            name: Name for this configuration
        """
        print(f"\n{'='*60}")
        print(f"Capturing configuration: {name}")
        print(f"{'='*60}")
        
        # Setup channels and auto trigger
        self.setup_channels(channels)
        
        # Stop acquisition once for all captures to ensure same data
        print("  Stopping acquisition for capture...")
        self.instrument.write(':STOP')
        time.sleep(0.5)
        
        # Generate base filename
        base_filename = f"wfm_{name}"
        
        # Save screenshot first to avoid capturing file dialogs
        print("  Saving screenshot first...")
        saved_files = self.save_waveform_on_scope(base_filename, ['png'])
        
        # Wait longer to ensure any dialogs are cleared
        time.sleep(5)
        
        # Save other files on oscilloscope (CSV, BIN, WFM)
        print("  Saving waveform files...")
        saved_files.extend(self.save_waveform_on_scope(base_filename, ['csv', 'bin', 'wfm']))
        
        # Capture raw data for JSON - without stopping/starting
        print("  Capturing raw waveform data...")
        json_data = self.capture_raw_waveform(channels)
        self.save_json_file(json_data, name, "raw.json")
        
        # Resume acquisition after all captures
        print("  Resuming acquisition...")
        self.instrument.write(':RUN')
        
        # Download files via FTP
        print("  Downloading files via FTP...")
        self.download_files_via_ftp(saved_files, name)
        
        print(f"  Configuration {name} complete!")
    
    def run(self):
        """Run the complete capture process."""
        if not self.connect():
            print("Failed to connect to oscilloscope")
            return
        
        try:
            # Configuration 1: Channel 1 only
            self.capture_configuration([1], "ch1")
            
            # Configuration 2: Channels 1-4
            self.capture_configuration([1, 2, 3, 4], "ch1234")
            
            # Configuration 3: Channels 1-2
            self.capture_configuration([1, 2], "ch12")
            
            print(f"\n{'='*60}")
            print(f"All captures complete!")
            print(f"Files saved to: {self.output_dir.absolute()}")
            print(f"{'='*60}")
            
        finally:
            self.disconnect()


def main():
    """Main entry point."""
    # Get RIGOL_RESOURCE from environment or use default
    resource = os.getenv('RIGOL_RESOURCE')
    
    if not resource:
        print("RIGOL_RESOURCE environment variable not set")
        print("Attempting auto-discovery...")
    
    # Create and run capture tool
    capture = RigolWaveformCapture(resource_string=resource)
    capture.run()


if __name__ == "__main__":
    main()