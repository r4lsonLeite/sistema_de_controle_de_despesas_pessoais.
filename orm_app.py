from sqlalchemy import create_engine, Column, Integer, String, Numeric, Date, ForeignKey, func, desc
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import date

# ==============================================================================
# PARTE 1 - CONFIGURAÇÃO DO PROJETO E CONEXÃO
# ==============================================================================
# Sua conexão exata inserida aqui!
DATABASE_URI = r'postgresql://postgres:99306561r@127.0.0.1:5432/postgres'

# Motor de conexão
engine = create_engine(DATABASE_URI, echo=False)
Base = declarative_base()

# ==============================================================================
# PARTE 2 - MAPEAMENTO ORM (Classes ↔ Tabelas)
# ==============================================================================
class Usuario(Base):
    __tablename__ = 'usuarios'
    
    id_usuario = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)
    
    contas = relationship("Conta", back_populates="usuario", cascade="all, delete-orphan")

class Categoria(Base):
    __tablename__ = 'categorias'
    
    id_categoria = Column(Integer, primary_key=True)
    nome_categoria = Column(String(50), nullable=False, unique=True)
    icone = Column(String(50))
    limite_mensal = Column(Numeric(10, 2), default=0.00)
    
    transacoes = relationship("Transacao", back_populates="categoria")

class Conta(Base):
    __tablename__ = 'contas'
    
    id_conta = Column(Integer, primary_key=True)
    nome_conta = Column(String(50), nullable=False)
    tipo_conta = Column(String(30))
    saldo_atual = Column(Numeric(10, 2), default=0.00)
    id_usuario_fk = Column(Integer, ForeignKey('usuarios.id_usuario', ondelete="CASCADE"), nullable=False)
    
    usuario = relationship("Usuario", back_populates="contas")
    transacoes = relationship("Transacao", back_populates="conta", cascade="all, delete-orphan")

class Transacao(Base):
    __tablename__ = 'transacoes'
    
    id_transacao = Column(Integer, primary_key=True)
    data_transacao = Column(Date, nullable=False, default=date.today)
    valor = Column(Numeric(10, 2), nullable=False)
    descricao = Column(String)
    tipo_transacao = Column(String(10)) 
    id_conta_fk = Column(Integer, ForeignKey('contas.id_conta', ondelete="CASCADE"), nullable=False)
    id_categoria_fk = Column(Integer, ForeignKey('categorias.id_categoria', ondelete="RESTRICT"), nullable=False)
    
    conta = relationship("Conta", back_populates="transacoes")
    categoria = relationship("Categoria", back_populates="transacoes")


Session = sessionmaker(bind=engine)
session = Session()

def executar_crud_e_consultas():
    print("\n--- INICIANDO CRUD VIA ORM ---")
    
    # ==============================================================================
    # PARTE 3 - OPERAÇÕES CRUD VIA ORM
    # ==============================================================================
    
    # 3.1 CREATE: Verifica se a Juliana já existe antes de inserir
    novo_usuario = session.query(Usuario).filter_by(email="juliana@email.com").first()
    if not novo_usuario:
        novo_usuario = Usuario(nome="Juliana Paes", email="juliana@email.com", senha="123")
        session.add(novo_usuario)
        print("CREATE: Usuário Juliana inserido com sucesso!")
    else:
        print("CREATE: Usuário Juliana já existia no banco. Pulando inserção.")

    # CREATE: Categoria
    nova_categoria = session.query(Categoria).filter_by(nome_categoria="Educação").first()
    if not nova_categoria:
        nova_categoria = Categoria(nome_categoria="Educação", icone="fa-book")
        session.add(nova_categoria)
    
    # CREATE: Conta
    nova_conta = session.query(Conta).filter_by(nome_conta="C6 Bank").first()
    if not nova_conta:
        nova_conta = Conta(nome_conta="C6 Bank", tipo_conta="Corrente", usuario=novo_usuario)
        session.add(nova_conta)

    # CREATE: Transações
    t1_existe = session.query(Transacao).filter_by(descricao="Livro Python").first()
    if not t1_existe:
        t1 = Transacao(valor=150.00, descricao="Livro Python", tipo_transacao="DESPESA", conta=nova_conta, categoria=nova_categoria)
        t2 = Transacao(valor=2500.00, descricao="Bolsa de Estágio", tipo_transacao="RECEITA", conta=nova_conta, categoria=nova_categoria)
        t3 = Transacao(valor=50.00, descricao="Cadernos", tipo_transacao="DESPESA", conta=nova_conta, categoria=nova_categoria)
        session.add_all([t1, t2, t3])
        print("CREATE: 3 Transações inseridas com sucesso!")
    
    session.commit()

    # 3.2 READ (Listagem com Ordenação)
    print("\nREAD: Listando as 3 maiores transações registradas no sistema:")
    transacoes_ord = session.query(Transacao).order_by(desc(Transacao.valor)).limit(3).all()
    for t in transacoes_ord:
        print(f"-> R$ {t.valor} - {t.descricao}")

    # 3.3 UPDATE (Atualização)
    conta_atualizar = session.query(Conta).filter_by(nome_conta="C6 Bank").first()
    if conta_atualizar:
        conta_atualizar.tipo_conta = "Conta Salário" 
        session.commit()                             
        print("\nUPDATE: Tipo de conta 'C6 Bank' atualizado para 'Conta Salário'!")

    # 3.4 DELETE (Remoção)
    transacao_remover = session.query(Transacao).filter_by(descricao="Cadernos").first()
    if transacao_remover:
        session.delete(transacao_remover)
        session.commit()
        print("\nDELETE: Transação 'Cadernos' removida com sucesso!")


    # ==============================================================================
    # PARTE 4 - CONSULTAS COM RELACIONAMENTO
    # ==============================================================================
    print("\n--- INICIANDO CONSULTAS AVANÇADAS ORM ---")

    print("\n1. Extrato Detalhado (JOIN Transacao + Conta + Categoria):")
    extrato = session.query(Transacao, Conta, Categoria)\
        .join(Conta, Transacao.id_conta_fk == Conta.id_conta)\
        .join(Categoria, Transacao.id_categoria_fk == Categoria.id_categoria)\
        .limit(3).all()
    
    for t, c, cat in extrato:
        print(f"[{c.nome_conta}] {cat.nome_categoria} -> {t.descricao}: R$ {t.valor}")

    print("\n2. Total Gasto por Categoria (Agregação + JOIN):")
    gastos_por_cat = session.query(
            Categoria.nome_categoria, 
            func.sum(Transacao.valor).label('Total')
        )\
        .join(Transacao)\
        .filter(Transacao.tipo_transacao == 'DESPESA')\
        .group_by(Categoria.nome_categoria).all()
    
    for nome_cat, total in gastos_por_cat:
        print(f"Categoria: {nome_cat} | Total Gasto: R$ {total:.2f}")

    print("\n3. Top 3 Maiores Despesas (Filtro + Ordenação LIMIT):")
    top_despesas = session.query(Transacao)\
        .filter(Transacao.tipo_transacao == 'DESPESA')\
        .order_by(desc(Transacao.valor))\
        .limit(3).all()
    
    for desp in top_despesas:
        print(f"Data: {desp.data_transacao} | Valor: R$ {desp.valor} | Ref: {desp.descricao}")


if __name__ == '__main__':
    try:
        executar_crud_e_consultas()
    except Exception as e:
        session.rollback()
        print(f"\n[!] O banco de dados recusou a operação. O erro real escondido é:")
        print(repr(e))
    finally:
        session.close()