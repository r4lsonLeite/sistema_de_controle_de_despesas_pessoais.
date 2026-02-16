import pytest
from datetime import date
from src.models.lancamento import Receita, Despesa
from src.models.categorias import Categoria
from src.models.orcamento import OrcamentoMensal

# --- Testes de Validação (Encapsulamento) ---

def test_impedir_valor_negativo_ou_zero():
    """RT: Não é permitido cadastrar despesas com valor <= 0."""
    with pytest.raises(ValueError, match="maior que zero"):
        Receita(-100, date.today(), "Teste", "Bonus")
    
    with pytest.raises(ValueError, match="maior que zero"):
        Despesa(0, date.today(), "Teste", "Lanche", "PIX")

# --- Testes de POO e Métodos Especiais ---

def test_soma_orcamento_com_metodo_add():
    """RT: __add__ deve somar lançamentos ao orçamento."""
    config = {"alerta_alto_valor": 500, "meta_economia_percentual": 10}
    orcamento = OrcamentoMensal("02/2026", config)
    
    r1 = Receita(1000.0, date.today(), "Salário", "Trabalho")
    d1 = Despesa(200.0, date.today(), "Internet", "Contas", "Boleto")
    
    # Testa o método __add__
    orcamento + r1
    orcamento + d1
    
    assert len(orcamento.lancamentos) == 2
    assert orcamento.calcular_saldo_atual() == 800.0

def test_comparacao_lancamentos_eq():
    """RT: __eq__ deve comparar por dados e descrição."""
    cat = Categoria("Lazer", "DESPESA")
    d1 = Despesa(50.0, date(2026, 2, 15), "Cinema", cat, "Crédito")
    d2 = Despesa(50.0, date(2026, 2, 15), "Cinema", cat, "Crédito")
    
    assert d1 == d2

# --- Testes de Regras de Negócio (Alertas) ---

def test_alerta_limite_categoria(capsys):
    """RT: Se o valor ultrapassar o limite da categoria, registrar alerta."""
    cat_alimentacao = Categoria("Alimentação", "DESPESA", limite_mensal=100.0)
    config = {"alerta_alto_valor": 1000}
    orcamento = OrcamentoMensal("02/2026", config)
    
    d1 = Despesa(150.0, date.today(), "Jantar Fora", cat_alimentacao, "Cartão")
    orcamento + d1 # Ultrapassa o limite de 100.0
    
    captured = capsys.readouterr()
    assert "LIMITE EXCEDIDO" in captured.out