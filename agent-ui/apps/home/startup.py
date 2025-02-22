import http.server
import socketserver
import threading
import json

from apps.home.models import Event, Pod

# Define the port on which the server will listen
PORT = 4321

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):

        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        post_data = post_data.decode('utf-8')

        try:
            payload = json.loads(post_data)
        except Exception as e: 
            print(e)
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<p>Bad Request</p>")
            return

        event_id = payload.event_id
        pod_name = payload.pod_name
        kind = payload.kind

        if self.path == "/event/create":
            status = Event.PENDING
        elif self.path ==  "/event/finish":
            reply = payload.reply
            status = Event.FINISHED
        elif self.path = "/event/fail":
            status = Event.FAIL

        results = Pod.objects.filter(name=pod_name)
        if len(results) == 0:
            # TODO update from kubernetes
            return

        if reply != None:
            event = Event(status=status, pod=results[0], event_id=event_id, kind=kind, reply=reply)
            event.save()
        else:
            event = Event(status=status, pod=results[0], event_id=event_id, kind=kind)
            event.save()

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"<p>OK</p>")

def run_server():
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"Serving on port {PORT}...")
        httpd.serve_forever()

def event_listener():
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.daemon = True
    server_thread.start()
    print("Server is running in a background thread.")
