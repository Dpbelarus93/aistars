#!/usr/bin/env python3
import json
import sys

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    request = json.loads(line)
    method = request.get("method", "")
    request_id = request.get("id")
    
    if method == "initialize":
        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "simple-mcp", "version": "1.0.0"}
            }
        }
    elif method == "tools/list":
        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "tools": [{
                    "name": "test_tool",
                    "description": "Simple test tool",
                    "inputSchema": {
                        "type": "object",
                        "properties": {"message": {"type": "string"}},
                        "required": ["message"]
                    }
                }]
            }
        }
    elif method == "tools/call":
        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "content": [{
                    "type": "text", 
                    "text": "Simple MCP server is working!"
                }]
            }
        }
    else:
        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"status": "OK"}
        }
    
    print(json.dumps(response), flush=True) 