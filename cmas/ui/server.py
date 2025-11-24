import http.server
import socketserver
import json
import os
from urllib.parse import urlparse, parse_qs

PORT = 8000
WEB_DIR = os.path.join(os.path.dirname(__file__), "static")

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/api/submit":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            
            code = data.get('code')
            if code:
                # Save to file
                input_dir = os.path.join(os.getcwd(), "cmas/demo_input")
                os.makedirs(input_dir, exist_ok=True)
                with open(os.path.join(input_dir, "user_code.py"), "w") as f:
                    f.write(code)
                
                # Trigger agents in background (simplified)
                import subprocess
                subprocess.Popen(["python3", "cmas/refactor_agent/src/main.py", "cmas/demo_input", "cmas/demo_output"])
                # We assume refactor agent triggers validation or we run it after? 
                # For now let's just run refactor. 
                # Ideally we'd chain them. Let's chain them in a shell command.
                cmd = "python3 cmas/refactor_agent/src/main.py cmas/demo_input cmas/demo_output && python3 cmas/validation_agent/src/main.py cmas/demo_input/user_code.py cmas/demo_output/user_code.py"
                subprocess.Popen(cmd, shell=True)

                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok", "message": "Agents started"}).encode())
            else:
                self.send_error(400)
        else:
            self.send_error(404)

    def do_GET(self):
        if self.path.startswith("/api/logs"):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            log_path = os.path.join(os.getcwd(), "system_logs.json")
            if os.path.exists(log_path):
                with open(log_path, 'r') as f:
                    self.wfile.write(f.read().encode())
            else:
                self.wfile.write(b"[]")
        elif self.path.startswith("/api/code"):
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            
            code_path = os.path.join(os.getcwd(), "cmas/demo_output/user_code.py")
            if os.path.exists(code_path):
                with open(code_path, 'r') as f:
                    self.wfile.write(f.read().encode())
            else:
                self.wfile.write(b"")
        elif self.path.startswith("/api/report"):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            report_path = os.path.join(os.getcwd(), "validation_report.json")
            if os.path.exists(report_path):
                with open(report_path, 'r') as f:
                    self.wfile.write(f.read().encode())
            else:
                self.wfile.write(b"{}")
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
