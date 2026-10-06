#!/usr/bin/env python3
"""
Servidor local do site.

O http.server padrão do Python responde HTTP/1.0 e ignora cabeçalho Range,
e sem Range o Chrome não toca os MP4 do site. Este aqui entende Range, então
o vídeo roda igual rodaria em qualquer hospedagem estática de verdade.

    python3 servidor.py [porta]
"""
import http.server, os, re, socketserver, sys

PORTA = int(sys.argv[1]) if len(sys.argv) > 1 else 4179
RAIZ = os.path.dirname(os.path.abspath(__file__))


class Handler(http.server.SimpleHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def __init__(self, *a, **kw):
        super().__init__(*a, directory=RAIZ, **kw)

    def end_headers(self):
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def send_head(self):
        faixa = self.headers.get("Range")
        if not faixa:
            return super().send_head()

        caminho = self.translate_path(self.path)
        if os.path.isdir(caminho) or not os.path.isfile(caminho):
            return super().send_head()

        m = re.match(r"bytes=(\d*)-(\d*)$", faixa.strip())
        if not m:
            return super().send_head()

        tamanho = os.path.getsize(caminho)
        ini, fim = m.group(1), m.group(2)
        if ini == "":                      # sufixo: últimos N bytes
            n = int(fim or 0)
            ini, fim = max(0, tamanho - n), tamanho - 1
        else:
            ini = int(ini)
            fim = int(fim) if fim else tamanho - 1
        fim = min(fim, tamanho - 1)
        if ini > fim:
            self.send_response(416)
            self.send_header("Content-Range", "bytes */%d" % tamanho)
            self.end_headers()
            return None

        f = open(caminho, "rb")
        f.seek(ini)
        self.send_response(206)
        self.send_header("Content-Type", self.guess_type(caminho))
        self.send_header("Content-Range", "bytes %d-%d/%d" % (ini, fim, tamanho))
        self.send_header("Content-Length", str(fim - ini + 1))
        self.end_headers()
        return _Pedaco(f, fim - ini + 1)

    def log_message(self, *a):
        pass


class _Pedaco:
    """Entrega só o trecho pedido para o copyfile do SimpleHTTPRequestHandler."""
    def __init__(self, f, restam):
        self.f, self.restam = f, restam

    def read(self, n=-1):
        if self.restam <= 0:
            return b""
        if n < 0 or n > self.restam:
            n = self.restam
        d = self.f.read(n)
        self.restam -= len(d)
        return d

    def close(self):
        self.f.close()


class Servidor(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


if __name__ == "__main__":
    print("Old Man rodando em http://localhost:%d" % PORTA)
    Servidor(("", PORTA), Handler).serve_forever()
