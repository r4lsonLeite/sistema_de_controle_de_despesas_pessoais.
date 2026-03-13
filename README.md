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
No arquivo orm_app.py, altere a DATABASE_URI (linha 10) com as suas credenciais locais:

Python
DATABASE_URI = r'postgresql://usuario:senha@127.0.0.1:5432/nome_do_banco'
Passo 3: Rodar o CRUD
No terminal, execute o script:

Bash
python orm_app.py
O console exibirá o log de inserções, atualizações, exclusões e os relatórios financeiros avançados.

Esse README.md resume perfeitamente todo o esforço e a técnica aplicada nessas últimas etapas do projeto, que simples mas que atende as demandas de estudo poposta.
