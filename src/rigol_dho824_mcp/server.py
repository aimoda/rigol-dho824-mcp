"""MCP server for Rigol DHO824 oscilloscope."""

import os
from typing import Optional, TypedDict, Annotated, Literal, Union
from pydantic import Field
from fastmcp import FastMCP
from dotenv import load_dotenv
import pyvisa


class ModelNumberResult(TypedDict):
    """Result containing the oscilloscope model number."""
    model: Annotated[str, Field(description="The oscilloscope model number", examples=["DHO824", "DHO804", "DHO914", "DHO924"])]


class SoftwareVersionResult(TypedDict):
    """Result containing the oscilloscope software version."""
    version: Annotated[str, Field(description="The firmware/software version", examples=["00.02.01.SP2", "00.01.05", "00.02.00.SP1"])]


class SerialNumberResult(TypedDict):
    """Result containing the oscilloscope serial number."""
    serial: Annotated[str, Field(description="The unique serial number", examples=["DHO8240000001", "DHO8040000123", "DHO9140000456"])]


class ScopeError(TypedDict):
    """Error response when oscilloscope operation fails."""
    success: Annotated[Literal[False], Field(description="Always False for error responses")]
    error: Annotated[str, Field(description="Descriptive error message", examples=["Failed to connect to oscilloscope. Check connection and RIGOL_RESOURCE environment variable.", "Failed to parse oscilloscope identity", "Connection timeout"])]


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
    
    @mcp.tool
    async def get_model_number() -> Union[ModelNumberResult, ScopeError]:
        """
        Get the model number of the connected Rigol oscilloscope.
        
        Returns the model identifier (e.g., 'DHO824') from the oscilloscope's
        identity string.
        """
        try:
            if not scope.connect():
                return ScopeError(
                    success=False,
                    error="Failed to connect to oscilloscope. Check connection and RIGOL_RESOURCE environment variable."
                )
            
            identity_parts = scope.parse_identity()
            if not identity_parts:
                return ScopeError(
                    success=False,
                    error="Failed to parse oscilloscope identity"
                )
            
            return ModelNumberResult(
                model=identity_parts['model']
            )
            
        except Exception as e:
            return ScopeError(
                success=False,
                error=f"Error getting model number: {str(e)}"
            )
        finally:
            scope.disconnect()
    
    @mcp.tool
    async def get_software_version() -> Union[SoftwareVersionResult, ScopeError]:
        """
        Get the software/firmware version of the connected Rigol oscilloscope.
        
        Returns the software version string from the oscilloscope's
        identity information.
        """
        try:
            if not scope.connect():
                return ScopeError(
                    success=False,
                    error="Failed to connect to oscilloscope. Check connection and RIGOL_RESOURCE environment variable."
                )
            
            identity_parts = scope.parse_identity()
            if not identity_parts:
                return ScopeError(
                    success=False,
                    error="Failed to parse oscilloscope identity"
                )
            
            return SoftwareVersionResult(
                version=identity_parts['version']
            )
            
        except Exception as e:
            return ScopeError(
                success=False,
                error=f"Error getting software version: {str(e)}"
            )
        finally:
            scope.disconnect()
    
    @mcp.tool
    async def get_serial_number() -> Union[SerialNumberResult, ScopeError]:
        """
        Get the serial number of the connected Rigol oscilloscope.
        
        Returns the unique serial number identifier from the oscilloscope's
        identity string.
        """
        try:
            if not scope.connect():
                return ScopeError(
                    success=False,
                    error="Failed to connect to oscilloscope. Check connection and RIGOL_RESOURCE environment variable."
                )
            
            identity_parts = scope.parse_identity()
            if not identity_parts:
                return ScopeError(
                    success=False,
                    error="Failed to parse oscilloscope identity"
                )
            
            return SerialNumberResult(
                serial=identity_parts['serial']
            )
            
        except Exception as e:
            return ScopeError(
                success=False,
                error=f"Error getting serial number: {str(e)}"
            )
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