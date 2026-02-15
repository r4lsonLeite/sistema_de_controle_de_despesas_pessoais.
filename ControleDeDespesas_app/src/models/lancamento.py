class Lancamento:
    def __init__(self, valor, data, descricao, categoria):
        self._valor = valor
        self.data = data
        self.descricao = descricao
        self.categoria = categoria

    @property
    def valor(self):
        return self._valor

    @valor.setter
    def valor(self, novo_valor):
        if novo_valor <= 0:
            raise ValueError("O valor do lançamento deve ser maior que zero.")
        self._valor = novo_valor

    def __repr__(self):
        return f"{self.__class__.__name__}(valor={self.valor}, data='{self.data}')"

class Receita(Lancamento):
    def __str__(self):
        return f"[+] Receita: {self.descricao} - R$ {self.valor:.2f}"

class Despesa(Lancamento):
    def __init__(self, valor, data, descricao, categoria, forma_pagto):
        super().__init__(valor, data, descricao, categoria)
        self.forma_pagto = forma_pagto

    def __str__(self):
        return f"[-] Despesa: {self.descricao} ({self.forma_pagto}) - R$ {self.valor:.2f}"