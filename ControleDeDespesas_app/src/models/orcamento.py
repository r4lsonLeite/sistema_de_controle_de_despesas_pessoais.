from src.models.lancamento import Receita, Despesa

class OrcamentoMensal:
    def __init__(self, mes, config):
        self.mes = mes
        self.lancamentos = []
        self.config = config

    def adicionar_lancamento(self, lancamento):
        self.lancamentos.append(lancamento)
        self.verificar_alertas(lancamento)

    def calcular_saldo_atual(self):
        receitas = sum(l.valor for l in self.lancamentos if isinstance(l, Receita))
        despesas = sum(l.valor for l in self.lancamentos if isinstance(l, Despesa))
        return receitas - despesas

    def verificar_alertas(self, lancamento):
        # 1. Alerta de Alto Valor (Dinâmico via JSON)
        limite_alto = self.config.get("alerta_alto_valor", 500.0)
        if lancamento.valor > limite_alto:
            print(f"⚠️ [ALERTA ALTO VALOR] {lancamento.descricao}: R$ {lancamento.valor}")

        # 2. Alerta de Limite da Categoria (Despesas)
        if isinstance(lancamento, Despesa) and hasattr(lancamento.categoria, 'limite_mensal'):
            if lancamento.categoria.limite_mensal > 0:
                total_cat = sum(l.valor for l in self.lancamentos if l.categoria == lancamento.categoria)
                if total_cat > lancamento.categoria.limite_mensal:
                    print(f"🚨 [LIMITE EXCEDIDO] Categoria: {lancamento.categoria.nome}!")

        # 3. Alerta de Saldo Negativo
        if self.calcular_saldo_atual() < 0:
            print(f"📉 [DÉFICIT] Saldo do mês {self.mes} ficou negativo!")

    def relatorio_meta_economia(self):
        receitas = sum(l.valor for l in self.lancamentos if isinstance(l, Receita))
        if receitas == 0: return "Sem receitas registradas."
        
        saldo = self.calcular_saldo_atual()
        percentual_economizado = (saldo / receitas) * 100
        meta = self.config.get("meta_economia_percentual", 10.0)
        
        if percentual_economizado >= meta:
            return f"✅ Meta batida! Economia de {percentual_economizado:.1f}% (Meta: {meta}%)"
        else:
            return f"❌ Abaixo da meta. Economia de {percentual_economizado:.1f}% (Meta: {meta}%)"

    def __add__(self, lancamento):
        """Permite usar 'orcamento + lancamento'."""
        if isinstance(lancamento, (Receita, Despesa)):
            self.adicionar_lancamento(lancamento)
            return self
        raise TypeError("Só é possível adicionar Receitas ou Despesas ao orçamento.")
    
    # No arquivo src/models/orcamento.py
from src.models.alerta import Alerta

class OrcamentoMensal:
    def __init__(self, mes, config):
        self.mes = mes
        self.lancamentos = []
        self.alertas = [] # Lista de objetos Alerta
        self.config = config

    def registrar_alerta(self, tipo, mensagem):
        novo_alerta = Alerta(tipo, mensagem)
        self.alertas.append(novo_alerta)
        print(novo_alerta) # Exibe na CLI também

    def relatorio_estatistico(self):
        """Atende ao requisito: Percentual de cada categoria."""
        total_despesas = sum(l.valor for l in self.lancamentos if isinstance(l, Despesa))
        if total_despesas == 0: return "Nenhuma despesa para analisar."

        gastos_por_cat = {}
        for l in self.lancamentos:
            if isinstance(l, Despesa):
                gastos_por_cat[l.categoria.nome] = gastos_por_cat.get(l.categoria.nome, 0) + l.valor

        print(f"\n--- Estatísticas de {self.mes} ---")
        for cat, valor in gastos_por_cat.items():
            percentual = (valor / total_despesas) * 100
            print(f"{cat}: R$ {valor:.2f} ({percentual:.1f}%)")