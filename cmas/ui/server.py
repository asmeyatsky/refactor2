import http.server
import socketserver
import json
import os
from urllib.parse import urlparse, parse_qs

PORT = 8000
WEB_DIR = os.path.join(os.path.dirname(__file__), "static")

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/logs":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            
            log_file = "system_logs.json"
            logs = []
            if os.path.exists(log_file):
                try:
                    with open(log_file, 'r') as f:
                        logs = json.load(f)
                except:
                    pass
            
            self.wfile.write(json.dumps(logs).encode())
        else:
            # Serve static files
            if self.path == "/":
                self.path = "/index.html"
            
            # Basic security check
            if ".." in self.path:
                self.send_error(403)
                return
                
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def translate_path(self, path):
        # Override to serve from specific directory
        path = path.split('?',1)[0]
        path = path.split('#',1)[0]
        path = os.path.normpath(path)
        words = path.split('/')
        words = filter(None, words)
        path = WEB_DIR
        for word in words:
            if os.path.dirname(word) or word in (os.curdir, os.pardir):
                continue
            path = os.path.join(path, word)
        return path

def run_server():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving UI at http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    run_server()
