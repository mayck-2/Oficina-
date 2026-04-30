from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

def layout(content):
    return f"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<title>Oficina Premium</title>

<style>
body {{
    margin:0;
    font-family: 'Segoe UI', sans-serif;
    background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);
    color:#333;
}}

.header {{
    background: #000;
    color: #fff;
    padding: 15px;
    text-align: center;
    font-size: 20px;
    letter-spacing: 1px;
}}

.container {{
    max-width: 400px;
    margin: 40px auto;
    background: white;
    padding: 25px;
    border-radius: 20px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.6);
    animation: fade 0.6s ease;
}}

input, textarea {{
    width:100%;
    padding:12px;
    margin:10px 0;
    border-radius:10px;
    border:1px solid #ddd;
}}

button {{
    width:100%;
    padding:12px;
    border:none;
    border-radius:10px;
    background: linear-gradient(135deg,#00c6ff,#0072ff);
    color:white;
    font-size:16px;
    cursor:pointer;
}}

.whatsapp {{
    background:#25D366;
    margin-top:10px;
}}

@keyframes fade {{
    from {{opacity:0; transform:translateY(20px);}}
    to {{opacity:1; transform:translateY(0);}}
}}
</style>

</head>

<body>

<div class="header">🔧 Oficina Premium</div>

{content}

</body>
</html>
"""

class Server(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path == "/admin":
            try:
                with open("pedidos.txt","r",encoding="utf-8") as f:
                    dados = f.readlines()
            except:
                dados = []

            lista = ""
            for d in dados:
                lista += f"<div style='background:#111;color:#fff;padding:10px;margin:10px;border-radius:10px'>{d}</div>"

            html = layout(f"<div class='container'><h2>Painel</h2>{lista}</div>")
            self.send(html)

        else:
            form = """
<div class="container">
<h2>Solicitar Conserto</h2>

<form method="POST">
<input name="nome" placeholder="Seu nome" required>
<input name="telefone" placeholder="WhatsApp" required>
<input name="aparelho" placeholder="Aparelho" required>
<textarea name="problema" placeholder="Problema"></textarea>

<button>Enviar Pedido</button>
</form>

<a href="https://wa.me/5581982393467">
<button class="whatsapp">Falar no WhatsApp</button>
</a>

</div>
"""
            self.send(layout(form))

    def do_POST(self):
        tamanho = int(self.headers['Content-Length'])
        dados = self.rfile.read(tamanho).decode()
        data = urllib.parse.parse_qs(dados)

        texto = f"{data.get('nome',[''])[0]} | {data.get('telefone',[''])[0]} | {data.get('aparelho',[''])[0]} | {data.get('problema',[''])[0]}"

        with open("pedidos.txt","a",encoding="utf-8") as f:
            f.write(texto+"\n")

        sucesso = """
<div class="container" style="text-align:center">
<h1>✔ Pedido Enviado</h1>
<p>Entraremos em contato em breve</p>
<a href="/"><button>Voltar</button></a>
</div>
"""
        self.send(layout(sucesso))

    def send(self, html):
        self.send_response(200)
        self.send_header('Content-type','text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

server = HTTPServer(('0.0.0.0',8080), Server)
print("🔥 Sistema profissional rodando")
server.serve_forever()
