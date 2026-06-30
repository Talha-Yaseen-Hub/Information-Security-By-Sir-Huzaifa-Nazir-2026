import http.server, ssl, pathlib, os

PORT = 4443
WWW = pathlib.Path.cwd() / "www"
WWW.mkdir(exist_ok=True)
(WWW / "index.html").write_text("<html><body><h1>TLS Lab</h1><p>Hello! BSIT from a secured server, Can you read this?</p></body></html>")

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        # Corrected: fixed double underscores and super() call
        super().__init__(*a, directory=str(WWW), **kw)

if __name__ == "__main__":
    server_address = ('0.0.0.0', PORT)
    httpd = http.server.HTTPServer(server_address, Handler)
    
    # Initialize TLS Context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")

    try:
        # Corrected: Use |= for bitwise OR and fixed underscores
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        context.maximum_version = ssl.TLSVersion.TLSv1_2
        
        # This specific cipher allows Method B (RSA decryption) to work [cite: 39, 77]
        context.set_ciphers("AES128-SHA")
    except Exception as e:
        print("Cipher selection error:", e)

    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
    print(f"Serving on https://localhost:{PORT}")
    httpd.serve_forever()