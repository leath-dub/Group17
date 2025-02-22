# SAMPLE PYTHON HTTP SERVER STUBBING FOR HELM SETUP
from http.server import BaseHTTPRequestHandler, HTTPServer

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Hello from my minimal Python HTTP server!")

server_address = ("0.0.0.0", 8080)
httpd = HTTPServer(server_address, MyHandler)
print("Serving on port 8080...")
httpd.serve_forever()
