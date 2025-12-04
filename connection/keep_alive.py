from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import os
import time

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"I am alive!")
    
    def do_HEAD(self):
        # HEAD requests are like GET but without body (used by health checks)
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
    
    def do_POST(self):
        # Some health checks use POST
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"I am alive!")
    
    def log_message(self, format, *args):
        # Suppress default HTTP logs (too verbose)
        pass

def run_server():
    # Render assigns a port in the environment variable PORT
    port = int(os.environ.get('PORT', 10000))
    
    try:
        server = HTTPServer(('0.0.0.0', port), SimpleHandler)
        print(f"✅ Keep-alive server started successfully on port {port}")
        print(f"🌐 Server will respond to: http://0.0.0.0:{port}/")
        server.serve_forever()
    except Exception as e:
        print(f"❌ CRITICAL: Keep-alive server failed to start!")
        print(f"Error: {e}")
        print("Bot will go offline after 15 minutes of inactivity!")

def keep_alive():
    t = threading.Thread(target=run_server, daemon=True)
    t.start()
    
    # Give the server a moment to start
    time.sleep(0.5)
    print("Keep-alive thread started")
