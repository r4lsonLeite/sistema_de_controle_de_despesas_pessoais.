from src.models.lancamento import Receita, Despesa
from src.models.orcamento import OrcamentoMensal
from src.services.config_service import carregar_configuracoes

def rodar_app():
    # 1. Carrega configs do JSON
    config = carregar_configuracoes()
    
    # 2. Inicia o orçamento
    orcamento = OrcamentoMensal("Fevereiro/2026", config)
    
    # 3. Teste rápido
    try:
        salario = Receita(5500.0, "2026-02-01", "Pro-labore", "Salário")
        internet = Despesa(150.0, "2026-02-10", "Fibra Óptica", "Contas", "Boleto")
        compra_luxo = Despesa(1200.0, "2026-02-12", "Relógio", "Lazer", "Crédito")
        
        orcamento + salario
        orcamento + internet
        orcamento + compra_luxo # Isso deve disparar o alerta de alto valor
        
        print(f"\nResumo de {orcamento.mes}:")
        print(f"Saldo: R$ {orcamento.calcular_saldo_atual():.2f}")
        print(orcamento.relatorio_meta_economia())
        
    except ValueError as e:
        print(f"Erro de validação: {e}")

if __name__ == "__main__":
    rodar_app()