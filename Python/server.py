from http.server import BaseHTTPRequestHandler, HTTPServer
import time

hostName = "localhost"  # Server address
serverPort = 8080       # Server port

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        self.send_response(200)  # HTTP status code (200 = OK)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
        # HTML content to send
        html_content = f"""
        <html>
        <head>
            <title>My Simple Server</title>
        </head>
        <body>
            <h1>Welcome to my simple server!</h1>
            <p>Current time: {time.ctime()}</p>
            <p>You accessed path: {self.path}</p>
        </body>
        </html>
        """
        
        self.wfile.write(bytes(html_content, "utf-8"))

if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print(f"Server started at http://{hostName}:{serverPort}")
    
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    
    webServer.server_close()
    print("Server stopped.")