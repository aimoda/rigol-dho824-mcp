#!/usr/bin/env python3
"""
Test script to determine if changing the vertical scale affects raw waveform data
from the Rigol DHO824 oscilloscope.
"""

import pyvisa
import numpy as np
import time

def capture_waveform_data(inst, mode='RAW'):
    """Capture waveform data in specified mode."""
    inst.write(':WAV:MODE ' + mode)
    inst.write(':WAV:FORM BYTE')
    
    if mode == 'RAW':
        inst.write(':WAV:STAR 1')
        inst.write(':WAV:STOP 10000')
    
    data = inst.query_binary_values(':WAV:DATA?', datatype='B')
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
    
    raw_data = {}
    normal_data = {}
    
    for scale in scales:
        print(f"\n{'='*60}")
        print(f"Testing scale: {scale} V/div")
        
        inst.write(f':CHAN1:SCAL {scale}')
        time.sleep(0.5)
        
        actual_scale = float(inst.query(':CHAN1:SCAL?'))
        print(f"Actual scale set: {actual_scale} V/div")
        
        print("Capturing RAW mode data...")
        raw_data[scale] = capture_waveform_data(inst, 'RAW')
        
        print("Capturing NORMAL mode data...")
        normal_data[scale] = capture_waveform_data(inst, 'NORMal')
        
        print(f"RAW data - Min: {raw_data[scale].min()}, Max: {raw_data[scale].max()}, "
              f"Mean: {raw_data[scale].mean():.2f}, Std: {raw_data[scale].std():.2f}")
        print(f"NORMAL data - Min: {normal_data[scale].min()}, Max: {normal_data[scale].max()}, "
              f"Mean: {normal_data[scale].mean():.2f}, Std: {normal_data[scale].std():.2f}")
    
    print("\n" + "="*60)
    print("ANALYSIS: Comparing RAW data across different scales")
    print("="*60)
    
    reference_scale = scales[0]
    ref_data = raw_data[reference_scale]
    
    for scale in scales[1:]:
        current_data = raw_data[scale]
        
        min_len = min(len(ref_data), len(current_data))
        
        if np.array_equal(ref_data[:min_len], current_data[:min_len]):
            print(f"Scale {reference_scale} vs {scale}: RAW data is IDENTICAL")
        else:
            diff = np.abs(ref_data[:min_len].astype(float) - current_data[:min_len].astype(float))
            print(f"Scale {reference_scale} vs {scale}: RAW data DIFFERS")
            print(f"  Max difference: {diff.max()}")
            print(f"  Mean difference: {diff.mean():.2f}")
            print(f"  % of points different: {(diff > 0).sum() / len(diff) * 100:.1f}%")
    
    print("\n" + "="*60)
    print("ANALYSIS: Comparing NORMAL data across different scales")
    print("="*60)
    
    ref_data = normal_data[reference_scale]
    
    for scale in scales[1:]:
        current_data = normal_data[scale]
        
        min_len = min(len(ref_data), len(current_data))
        
        if np.array_equal(ref_data[:min_len], current_data[:min_len]):
            print(f"Scale {reference_scale} vs {scale}: NORMAL data is IDENTICAL")
        else:
            diff = np.abs(ref_data[:min_len].astype(float) - current_data[:min_len].astype(float))
            print(f"Scale {reference_scale} vs {scale}: NORMAL data DIFFERS")
            print(f"  Max difference: {diff.max()}")
            print(f"  Mean difference: {diff.mean():.2f}")
            print(f"  % of points different: {(diff > 0).sum() / len(diff) * 100:.1f}%")
    
    print("\n" + "="*60)
    print("CONCLUSION:")
    print("="*60)
    print("RAW mode: Should return the same raw ADC data regardless of scale")
    print("NORMAL mode: Returns screen display data, likely affected by scale")
    
    inst.close()

if __name__ == "__main__":
    main()