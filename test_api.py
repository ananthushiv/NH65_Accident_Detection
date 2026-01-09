#!/usr/bin/env python
import socket
import time

def make_request(path):
    """Make HTTP request to localhost:5000"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', 5000))
        sock.send(f'GET {path} HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n'.encode())
        
        response = b''
        while True:
            try:
                data = sock.recv(4096)
                if not data:
                    break
                response += data
            except:
                break
        sock.close()
        
        # Extract body from HTTP response
        body_start = response.find(b'\r\n\r\n')
        if body_start != -1:
            body = response[body_start+4:].decode('utf-8')
            return body
        return str(response)
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    print("Testing /api/live-data:")
    print(make_request('/api/live-data'))
    print("\n" + "="*50 + "\n")
    
    print("Testing /api/traffic-status:")
    print(make_request('/api/traffic-status'))
    print("\n" + "="*50 + "\n")
    
    print("Testing /api/all-records:")
    result = make_request('/api/all-records')
    # Only print first 500 chars
    if len(result) > 500:
        print(result[:500] + "...")
    else:
        print(result)
