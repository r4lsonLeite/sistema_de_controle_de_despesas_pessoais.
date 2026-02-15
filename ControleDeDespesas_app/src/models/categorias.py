class Categoria:
    def __init__(self, nome, tipo, limite_mensal=0.0):
        self.nome = nome
        self.tipo = tipo.upper() # 'RECEITA' ou 'DESPESA'
        # Regra de negócio: Receitas não têm limite
        self.limite_mensal = 0.0 if self.tipo == 'RECEITA' else limite_mensal

    def __repr__(self):
        return f"Categoria(nome='{self.nome}', tipo='{self.tipo}', limite={self.limite_mensal})"