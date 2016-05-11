#!/usr/bin/env python

# Test server for Shardnado testing

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer

PORT_NUMBER = 9200

class testServer(BaseHTTPRequestHandler):
    # This class handles test requests for the test_shardado.py script
    
    # Handler for the GET requests
    def do_GET(self):
        if self.path=="/_cat/shards":
            self.send_response(200)
            self.send_header('Content-type','text/plain')
            self.end_headers()
            # Send the html message
            self.wfile.write("test_index 1 r UNASSIGNED 52679412 4.6gb 127.0.0.1  elasticsearch-node")

        if self.path=="/_cat/nodes?h=host":
            self.send_response(200)
            self.send_header('Content-type','text/plain')
            self.end_headers()
            # Send the html message
            self.wfile.write("  127.0.0.1 ")
        
        return

    # Simple server doesn't do POST well
    def do_POST(self):
        if self.path=="/_cluster/reroute":
            self.send_response(200)
            self.end_headers()

        return

try:
    # Create a web server and define the handler to manage the
    # incoming requests
    server = HTTPServer(('', PORT_NUMBER), testServer)
    print 'Started test server on port %s' % str(PORT_NUMBER)
    
    # Wait forever for incoming http requests
    server.serve_forever()

except KeyboardInterrupt:
    print '^C received, shutting down the test server'
    server.socket.close()
    
