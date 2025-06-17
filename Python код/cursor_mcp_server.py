#!/usr/bin/env python3
"""
Proper MCP Server for Cursor (stdio-based)
"""
import json
import sys
import logging
from typing import Any, Dict

# Setup logging to file (not to stdout!)
logging.basicConfig(
    filename='/tmp/cursor_mcp.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def handle_request():
    for line in sys.stdin:
        try:
            request = json.loads(line.strip())
            method = request.get("method")
            request_id = request.get("id")
            
            if method == "initialize":
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {"name": "comfyui-mcp", "version": "1.0.0"}
                    }
                }
            elif method == "tools/list":
                response = {
                    "jsonrpc": "2.0", 
                    "id": request_id,
                    "result": {
                        "tools": [
                            {
                                "name": "generate_image",
                                "description": "Generate image via ComfyUI",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "prompt": {
                                            "type": "string",
                                            "description": "Image description for generation"
                                        },
                                        "width": {
                                            "type": "integer",
                                            "description": "Image width",
                                            "default": 512
                                        },
                                        "height": {
                                            "type": "integer", 
                                            "description": "Image height",
                                            "default": 512
                                        }
                                    },
                                    "required": ["prompt"]
                                }
                            }
                        ]
                    }
                }
            elif method == "tools/call":
                params = request.get("params", {})
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                
                if tool_name == "generate_image":
                    prompt = arguments.get("prompt", "test image")
                    width = arguments.get("width", 512)
                    height = arguments.get("height", 512)
                    
                    mock_result = {
                        "image_url": f"http://localhost:8188/mock_image_{width}x{height}.png",
                        "prompt": prompt,
                        "dimensions": f"{width}x{height}",
                        "status": "success (mock)",
                        "message": "Mock image generated successfully"
                    }
                    
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": json.dumps(mock_result, ensure_ascii=True, indent=2)
                                }
                            ]
                        }
                    }
                else:
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"}
                    }
            else:
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {"status": "ok"}
                }
            
            print(json.dumps(response, ensure_ascii=True))
            sys.stdout.flush()
            
        except Exception as e:
            error_response = {
                "jsonrpc": "2.0",
                "id": request.get("id") if 'request' in locals() else None,
                "error": {"code": -32603, "message": str(e)}
            }
            print(json.dumps(error_response, ensure_ascii=True))
            sys.stdout.flush()

if __name__ == "__main__":
    handle_request() 