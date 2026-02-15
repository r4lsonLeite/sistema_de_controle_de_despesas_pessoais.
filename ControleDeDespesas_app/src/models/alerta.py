from datetime import datetime

class Alerta:
    def __init__(self, tipo, mensagem):
        self.tipo = tipo # 'ALTO VALOR', 'LIMITE EXCEDIDO', 'DÉFICIT'
        self.mensagem = mensagem
        self.timestamp = datetime.now()

    def __str__(self):
        return f"[{self.timestamp.strftime('%d/%m %H:%M')}] {self.tipo}: {self.mensagem}"