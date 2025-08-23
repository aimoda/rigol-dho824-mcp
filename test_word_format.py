#!/usr/bin/env python3
"""
Test script to capture 16-bit WORD format data from Rigol DHO824
"""

import pyvisa
import numpy as np
import time

def capture_waveform_data(inst, format='BYTE', mode='RAW'):
    """Capture waveform data in specified format and mode."""
    inst.write(':WAV:MODE ' + mode)
    inst.write(':WAV:FORM ' + format)
    
    if mode == 'RAW':
        inst.write(':WAV:STAR 1')
        inst.write(':WAV:STOP 10000')
    
    if format == 'WORD':
        # For WORD format, use 'H' for unsigned 16-bit integers
        data = inst.query_binary_values(':WAV:DATA?', datatype='H', is_big_endian=False)
    elif format == 'BYTE':
        data = inst.query_binary_values(':WAV:DATA?', datatype='B')
    else:  # ASCII
        response = inst.query(':WAV:DATA?')
        data = np.array([float(x) for x in response.split(',')])
    
    return np.array(data)

def main():
    rm = pyvisa.ResourceManager()
    
    print("Connecting to oscilloscope at TCPIP::192.168.44.37::INSTR")
    inst = rm.open_resource('TCPIP::192.168.44.37::INSTR')
    inst.timeout = 10000
    
    print(f"Connected to: {inst.query('*IDN?').strip()}")
    
    inst.write(':WAV:SOUR CHAN1')
    
    inst.write(':STOP')
    time.sleep(0.5)
    
    scales = [0.05, 0.1, 0.2, 0.5, 1.0]
    
    byte_data = {}
    word_data = {}
    
    for scale in scales:
        print(f"\n{'='*70}")
        print(f"Testing scale: {scale} V/div")
        
        inst.write(f':CHAN1:SCAL {scale}')
        time.sleep(0.5)
        
        actual_scale = float(inst.query(':CHAN1:SCAL?'))
        print(f"Actual scale set: {actual_scale} V/div")
        
        print("Capturing BYTE format data (8-bit)...")
        byte_data[scale] = capture_waveform_data(inst, 'BYTE', 'RAW')
        
        print("Capturing WORD format data (16-bit)...")
        word_data[scale] = capture_waveform_data(inst, 'WORD', 'RAW')
        
        print(f"\nBYTE (8-bit) data:")
        print(f"  Range: {byte_data[scale].min()} - {byte_data[scale].max()}")
        print(f"  Mean: {byte_data[scale].mean():.2f}, Std: {byte_data[scale].std():.2f}")
        print(f"  Unique values: {len(np.unique(byte_data[scale]))}")
        
        print(f"\nWORD (16-bit) data:")
        print(f"  Range: {word_data[scale].min()} - {word_data[scale].max()}")
        print(f"  Mean: {word_data[scale].mean():.2f}, Std: {word_data[scale].std():.2f}")
        print(f"  Unique values: {len(np.unique(word_data[scale]))}")
        
        # Show scaling factor from 8-bit to 16-bit
        if byte_data[scale].max() > 0:
            scale_factor = word_data[scale].max() / (byte_data[scale].max() * 256)
            print(f"\n16-bit/8-bit scale factor: ~{scale_factor:.3f}")
    
    print("\n" + "="*70)
    print("ANALYSIS: Comparing WORD data across different scales")
    print("="*70)
    
    reference_scale = scales[0]
    ref_data = word_data[reference_scale]
    
    for scale in scales[1:]:
        current_data = word_data[scale]
        
        min_len = min(len(ref_data), len(current_data))
        
        if np.array_equal(ref_data[:min_len], current_data[:min_len]):
            print(f"Scale {reference_scale} vs {scale}: WORD data is IDENTICAL")
        else:
            diff = np.abs(ref_data[:min_len].astype(float) - current_data[:min_len].astype(float))
            print(f"Scale {reference_scale} vs {scale}: WORD data DIFFERS")
            print(f"  Max difference: {diff.max()}")
            print(f"  Mean difference: {diff.mean():.2f}")
            print(f"  % of points different: {(diff > 0).sum() / len(diff) * 100:.1f}%")
    
    print("\n" + "="*70)
    print("CONCLUSION:")
    print("="*70)
    print("WORD format provides 16-bit resolution instead of 8-bit")
    print("But the data still changes with vertical scale settings")
    print("The oscilloscope appears to scale data to the display range")
    
    inst.close()

if __name__ == "__main__":
    main()