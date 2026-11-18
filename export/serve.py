import http.server,json,sys,os,functools
D=os.path.abspath(sys.argv[1])
class R(http.server.SimpleHTTPRequestHandler):
    def __init__(self,*a,**k): super().__init__(*a,directory=D,**k)
    def end_headers(self):
        for h in json.load(open(D+'/vercel.json'))['headers'][0]['headers']: self.send_header(h['key'],h['value'])
        super().end_headers()
    def do_GET(self):
        if self.path=='/privacidad': self.path='/privacidad.html'
        super().do_GET()
    def log_message(self,*a): pass
http.server.ThreadingHTTPServer(('127.0.0.1',8765),R).serve_forever()
