#!/usr/bin/env python3
"""
Test script for the MCP tools implementation.
This script directly tests the core functionality without going through MCP.
"""

import pyvisa
from src.rigol_dho824_mcp.waveform import WaveformCapture
from src.rigol_dho824_mcp.channel import ChannelControl
from src.rigol_dho824_mcp.trigger import TriggerControl
from src.rigol_dho824_mcp.acquisition import AcquisitionControl


def test_connection():
    """Test basic connection to the oscilloscope."""
    print("Testing connection...")
    rm = pyvisa.ResourceManager()
    
    try:
        inst = rm.open_resource('TCPIP::192.168.44.37::INSTR')
        inst.timeout = 5000
        
        identity = inst.query('*IDN?').strip()
        print(f"✓ Connected to: {identity}")
        
        inst.close()
        return True
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return False


def test_channel_status():
    """Test getting channel status."""
    print("\nTesting channel status...")
    rm = pyvisa.ResourceManager()
    
    try:
        inst = rm.open_resource('TCPIP::192.168.44.37::INSTR')
        inst.timeout = 5000
        
        status = ChannelControl.get_channel_status(inst, 1)
        print(f"✓ Channel 1 status:")
        for key, value in status.items():
            print(f"  {key}: {value}")
        
        inst.close()
        return True
    except Exception as e:
        print(f"✗ Failed to get channel status: {e}")
        return False


def test_trigger_status():
    """Test getting trigger status."""
    print("\nTesting trigger status...")
    rm = pyvisa.ResourceManager()
    
    try:
        inst = rm.open_resource('TCPIP::192.168.44.37::INSTR')
        inst.timeout = 5000
        
        status = TriggerControl.get_trigger_status(inst)
        print(f"✓ Trigger status:")
        for key, value in status.items():
            print(f"  {key}: {value}")
        
        inst.close()
        return True
    except Exception as e:
        print(f"✗ Failed to get trigger status: {e}")
        return False


def test_sample_rate():
    """Test getting sample rate."""
    print("\nTesting sample rate query...")
    rm = pyvisa.ResourceManager()
    
    try:
        inst = rm.open_resource('TCPIP::192.168.44.37::INSTR')
        inst.timeout = 5000
        
        result = AcquisitionControl.get_sample_rate(inst)
        print(f"✓ Sample rate: {result['sample_rate_str']}")
        
        inst.close()
        return True
    except Exception as e:
        print(f"✗ Failed to get sample rate: {e}")
        return False


def test_waveform_capture():
    """Test waveform capture (if scope is stopped)."""
    print("\nTesting waveform capture...")
    rm = pyvisa.ResourceManager()
    
    try:
        inst = rm.open_resource('TCPIP::192.168.44.37::INSTR')
        inst.timeout = 10000
        
        # Check if scope is stopped
        trigger_status = inst.query(':TRIG:STAT?').strip()
        if trigger_status != "STOP":
            print(f"✓ Scope is running (status: {trigger_status}), skipping capture test")
            inst.close()
            return True
        
        # Try to capture data
        print("  Capturing data from channel 1...")
        data = WaveformCapture.capture_channel_data(inst, 1)
        
        print(f"✓ Captured {data['points']} points")
        print(f"  Units: {data['units']}")
        print(f"  Sample rate: {data['sample_rate']:.2e} Sa/s")
        print(f"  Statistics:")
        for key, value in data['statistics'].items():
            print(f"    {key}: {value:.4f} {data['units']}")
        
        inst.close()
        return True
    except Exception as e:
        print(f"✗ Failed to capture waveform: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("MCP Tools Implementation Test")
    print("=" * 60)
    
    tests = [
        test_connection,
        test_channel_status,
        test_trigger_status,
        test_sample_rate,
        test_waveform_capture
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print(f"Tests passed: {sum(results)}/{len(results)}")
    
    if all(results):
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed")


if __name__ == "__main__":
    main()