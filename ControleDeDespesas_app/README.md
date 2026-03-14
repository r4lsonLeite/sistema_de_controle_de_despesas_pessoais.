Disciplina: Banco de dados – Projeto final  – modelo logico
Professor: JAYR ALENCAR PEREIRA
Curso: Análise e Desenvolvimento de Sistemas
Aluno: jose railson leite da silva 2025019392

--projeto usando banco de dados postgres.
--Usando a linguagem python.

Sistema de Controle de Despesas Pessoais
Um sistema de gerenciamento financeiro focado na modelagem avançada de banco de dados relacional PostgreSQL e integração utilizando mapeamento objeto-relacional SQLAlchemy.

>>>>>Sobre o Projeto
Este projeto foi desenvolvido como avaliação de Banco de Dados. O objetivo é garantir a integridade de transações financeiras aplicando regras de negócio diretamente no banco de dados (constraints, triggers e procedures), além de realizar a comunicação com a aplicação via ORM em Python.

>>>>>Tecnologias Utilizadas
Banco de Dados: PostgreSQL 

Linguagem: Python 3.10

ORM: SQLAlchemy

Extensões DB: pg_trgm para otimização de buscas textuais

>>>>>Arquitetura do Banco de Dados
O modelo relacional foi desenhado para simular o comportamento de um banco real, garantindo consistência e performance.

Tabelas Principais:
USUARIOS: Titulares das contas.

CONTAS: Carteiras, contas correntes ou cartões associados a um usuário.

CATEGORIAS: Classificação de gastos (Alimentação, Lazer, etc.) com limites mensais.

TRANSACOES: Registros financeiros (Receitas e Despesas).

ORCAMENTOS e ALERTAS: Tabelas auxiliares para metas de economia e avisos de sistema.

Mecanismos Avançados (DBA):
Integridade Referencial: Uso de ON DELETE CASCADE para contas dependentes e ON DELETE RESTRICT para proteger categorias com histórico.

Stored Procedures: sp_transferir_fundos que garante a criação de duas transações (saída e entrada) de forma atômica durante transferências entre contas.

Triggers:

BEFORE: trg_before_padroniza_descricao intercepta e padroniza as descrições dos gastos para maiúsculo.

AFTER: trg_after_atualiza_saldo atualiza automaticamente o saldo das contas envolvidas assim que uma nova transação é registrada.

Views:

vw_extrato_detalhado: Facilita a leitura de extratos complexos unindo 4 tabelas.

vw_mat_resumo_mensal_categorias: View Materializada para relatórios gerenciais pesados, otimizando o carregamento de dashboards.

Query Tuning (Otimização):
Implementação de Índices B-Tree compostos (idx_transacao_conta_tipo) para acelerar agregações frequentes.

Uso de Índice GIN com Trigramas (idx_transacao_desc_gin) para reduzir o custo de buscas textuais parciais (ILIKE).

Refatoração de consultas via técnica de SARGability (isolamento de colunas com datas).

>>>>>Integração Python (ORM)
A camada de aplicação foi construída com SQLAlchemy, abstraindo a complexidade do SQL e tratando o banco de forma orientada a objetos.

Mapeamento: Classes bidirecionais utilizando relationship() e ForeignKey.

CRUD: Inserção inteligente prevenindo duplicatas (UNIQUE constraint), atualização de registros e exclusão (DELETE) respeitando a integridade.

Consultas Avançadas: Uso de func.sum(), .join(), .group_by() e .order_by(desc()) para gerar relatórios diretamente via Python.

>>>>>Como Executar o Projeto
Pré-requisitos
PostgreSQL instalado e rodando localmente (porta 5432).

Python instalado.

Passo 1: Configuração do Banco de Dados
Abra o DBeaver ou pgAdmin.

Crie um banco de dados vazio (ex: postgres ou projeto_finall).

Execute todo o conteúdo do arquivo projeto_finall.sql para criar as tabelas, funções, views e popular os dados iniciais.

Passo 2: Configuração da Aplicação
Clone este repositório.

Crie e ative um ambiente virtual (.venv).

Instale as dependências:

Bash
pip install sqlalchemy psycopg2-binary
No arquivo orm_app.py, altere a DATABASE_URI  com as suas credenciais locais:

Python
DATABASE_URI = r'postgresql://usuario:senha@127.0.0.1:5432/nome_do_banco'
Passo 3: Rodar o CRUD
No terminal, execute o script:

Bash
python orm_app.py
O console exibirá o log de inserções, atualizações, exclusões e os relatórios financeiros avançados.

**Destaques Técnicos do Banco (DDL/DML):**
* Integridade Referencial (`CASCADE`, `RESTRICT`) e Constraints (`CHECK`).
* Triggers (`BEFORE` para padronização de texto e `AFTER` para recálculo automático de saldos).
* Stored Procedure (`sp_transferir_fundos`) para transações atômicas.
* Query Tuning com Índices GIN (trigramas) e B-Tree.
* Views e Materialized Views para relatórios otimizados.

**Destaques do ORM (Python):**
* Mapeamento declarativo completo das entidades (`Usuario`, `Conta`, `Categoria`, `Transacao`).
* Relacionamentos bidirecionais utilizando `relationship()` e `back_populates`.
* Operações CRUD 100% via ORM (`session.add`, `session.delete`, `session.commit`).
* Consultas avançadas envolvendo `JOIN`, Agregações (`func.sum()`), `GROUP BY`, filtros e ordenações (`order_by`).

---

## >>>>Como Configurar e Executar<<<<

### 1. Configuração do Banco de Dados
1. No DBeaver ou pgAdmin, crie um banco de dados chamado `postgres` (ou `projeto_finall`).
2. Abra e execute o arquivo script `projeto_finall.sql`. Ele recriará as tabelas, as lógicas de negócio e as cargas iniciais (DML).

### 2. Configuração da Aplicação (Variáveis de Conexão)
1. Certifique-se de ter o Python 3 instalado.
2. Instale as dependências do ORM e o driver do PostgreSQL:
   ```bash
   pip install sqlalchemy psycopg2-binary
Abra o arquivo orm_app.py. Na linha 10, localize a variável DATABASE_URI e configure com as credenciais do seu banco local:

Python
# Formato: postgresql://USUARIO:SENHA@HOST:PORTA/NOME_DO_BANCO
DATABASE_URI = r'postgresql://postgres:sua_senha_aqui@127.0.0.1:5432/postgres'
3. Comando de Execução
Com o banco configurado e as dependências instaladas, abra o terminal na pasta do projeto e execute:

Bash
python orm_app.py
>>>>Exemplos de Uso e Saída Esperada
Ao executar o script, a aplicação se conectará ao banco via ORM, validará a existência dos dados, executará o CRUD completo e fará as 3 consultas relacionais exigidas.

Exemplo da saída gerada no terminal (Evidência das Consultas Avançadas):

Plaintext
--- INICIANDO CONSULTAS AVANÇADAS ORM ---

1. Extrato Detalhado (JOIN Transacao + Conta + Categoria):
[C6 Bank] Educação -> Livro Python: R$ 150.00
[C6 Bank] Educação -> Bolsa de Estágio: R$ 2500.00
[Nubank] Salário -> Salário Mensal: R$ 4500.00

2. Total Gasto por Categoria (Agregação + JOIN):
Categoria: Alimentação | Total Gasto: R$ 385.90
Categoria: Educação | Total Gasto: R$ 150.00
Categoria: Lazer | Total Gasto: R$ 170.00
Categoria: Transporte | Total Gasto: R$ 15.50

3. Top 3 Maiores Despesas (Filtro + Ordenação LIMIT):
Data: 2026-03-10 | Valor: R$ 300.00 | Ref: Supermercado Semanal
Data: 2026-03-12 | Valor: R$ 150.00 | Ref: Livro Python
Data: 2026-03-11 | Valor: R$ 120.00 | Ref: Compra Jogo Steam
(Nota: Os prints completos do terminal provando o funcionamento real estão anexados na pasta raiz deste projeto).

Esse README.md resume perfeitamente todo o esforço e a técnica aplicada nessas últimas etapas do projeto, que simples mas que atende as demandas de estudo poposta.
