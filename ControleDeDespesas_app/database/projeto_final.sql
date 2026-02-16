
CREATE TABLE USUARIOS (
    ID_Usuario SERIAL PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Senha VARCHAR(255) NOT NULL
);

CREATE TABLE CATEGORIAS (
    ID_Categoria SERIAL PRIMARY KEY,
    Nome_Categoria VARCHAR(50) NOT NULL,
    Icone VARCHAR(50)
);

CREATE TABLE CONTAS (
    ID_Conta SERIAL PRIMARY KEY,
    Nome_Conta VARCHAR(50) NOT NULL,
    Tipo_Conta VARCHAR(30), 
    Saldo_Atual DECIMAL(10, 2) DEFAULT 0.00,
    ID_Usuario_FK INTEGER NOT NULL,
    CONSTRAINT fk_usuario_conta FOREIGN KEY (ID_Usuario_FK) REFERENCES USUARIOS(ID_Usuario) ON DELETE CASCADE
);

CREATE TABLE TRANSACOES (
    ID_Transacao SERIAL PRIMARY KEY,
    Data_Transacao DATE NOT NULL DEFAULT CURRENT_DATE,
    
    Valor DECIMAL(10, 2) NOT NULL CHECK (Valor > 0), 
    Descricao TEXT,
    Tipo_Transacao VARCHAR(10) CHECK (Tipo_Transacao IN ('RECEITA', 'DESPESA')),
    ID_Conta_FK INTEGER NOT NULL,
    ID_Categoria_FK INTEGER NOT NULL,
    CONSTRAINT fk_conta_transacao FOREIGN KEY (ID_Conta_FK) REFERENCES CONTAS(ID_Conta) ON DELETE CASCADE,
   
    CONSTRAINT fk_categoria_transacao FOREIGN KEY (ID_Categoria_FK) REFERENCES CATEGORIAS(ID_Categoria) ON DELETE RESTRICT
);


CREATE INDEX idx_transacao_data ON TRANSACOES(Data_Transacao);
CREATE INDEX idx_transacao_id_conta ON TRANSACOES(ID_Conta_FK); 


INSERT INTO USUARIOS (Nome, Email, Senha) 
VALUES ('Ana Silva', 'ana@email.com', 'senha_segura_hash_123');


INSERT INTO CATEGORIAS (Nome_Categoria, Icone) VALUES 
('Alimentação', 'icon-food'),
('Salário', 'icon-money'),
('Lazer', 'icon-fun'),
('Transporte', 'icon-bus');

INSERT INTO CONTAS (Nome_Conta, Tipo_Conta, Saldo_Atual, ID_Usuario_FK) VALUES 
('Nubank', 'Corrente', 0.00, 1),
('Carteira', 'Dinheiro', 0.00, 1);


-- Entrada de Salário (Receita) na conta Nubank 
INSERT INTO TRANSACOES (Valor, Descricao, Tipo_Transacao, ID_Conta_FK, ID_Categoria_FK) 
VALUES (3500.00, 'Salário Mensal', 'RECEITA', 1, 2);


INSERT INTO TRANSACOES (Valor, Descricao, Tipo_Transacao, ID_Conta_FK, ID_Categoria_FK) 
VALUES (450.50, 'Compras da Semana', 'DESPESA', 1, 1);

-- Gasto com Uber (Despesa) no Cartão/Conta Nubank
INSERT INTO TRANSACOES (Valor, Descricao, Tipo_Transacao, ID_Conta_FK, ID_Categoria_FK) 
VALUES (25.90, 'Uber para o trabalho', 'DESPESA', 1, 4);

SELECT 
    c.Nome_Conta, 
    SUM(CASE WHEN t.Tipo_Transacao = 'RECEITA' THEN t.Valor ELSE -t.Valor END) as Saldo_Calculado
FROM CONTAS c
LEFT JOIN TRANSACOES t ON c.ID_Conta = t.ID_Conta_FK
GROUP BY c.Nome_Conta;

-- --------------------------------------------------------
-- 1. Inserindo USUARIOS
-- --------------------------------------------------------
INSERT INTO USUARIOS (Nome, Email, Senha) VALUES 
('Carlos Mendes', 'carlos@email.com', 'senha123'), -- ID: 1
('Fernanda Souza', 'fernanda@email.com', 'senha456'), -- ID: 2
('Roberto Dias', 'roberto@email.com', 'senha789'); -- ID: 3

-- --------------------------------------------------------
-- 2. Inserindo CATEGORIAS
-- --------------------------------------------------------
INSERT INTO CATEGORIAS (Nome_Categoria, Icone) VALUES 
('Alimentação', 'fa-utensils'),  -- ID: 1
('Salário', 'fa-money-bill'),     -- ID: 2
('Lazer', 'fa-gamepad'),          -- ID: 3
('Transporte', 'fa-bus'),         -- ID: 4
('Saúde', 'fa-medkit');           -- ID: 5 (Categoria sem uso para testar LEFT JOIN)

-- --------------------------------------------------------
-- 3. Inserindo CONTAS (Vinculadas aos usuários)
-- --------------------------------------------------------
INSERT INTO CONTAS (Nome_Conta, Tipo_Conta, Saldo_Atual, ID_Usuario_FK) VALUES 
('Nubank', 'Corrente', 1500.00, 1),      -- ID: 1 (Conta do Carlos)
('Inter', 'Investimento', 5000.00, 1),   -- ID: 2 (Conta do Carlos)
('Itaú', 'Corrente', 3200.50, 2),        -- ID: 3 (Conta da Fernanda)
('Carteira', 'Dinheiro', 150.00, 3);     -- ID: 4 (Conta do Roberto)


-- 4. Inserindo TRANSACOES

-- Transações do Carlos (ID 1)
INSERT INTO TRANSACOES (Valor, Descricao, Tipo_Transacao, ID_Conta_FK, ID_Categoria_FK) VALUES 
(4500.00, 'Salário Mensal', 'RECEITA', 1, 2),
(85.90, 'Jantar Pizzaria', 'DESPESA', 1, 1),
(15.50, 'Uber Trabalho', 'DESPESA', 1, 4),
(120.00, 'Compra Jogo Steam', 'DESPESA', 1, 3);

-- Transações da Fernanda (ID 2)
INSERT INTO TRANSACOES (Valor, Descricao, Tipo_Transacao, ID_Conta_FK, ID_Categoria_FK) VALUES 
(300.00, 'Supermercado Semanal', 'DESPESA', 3, 1),
(50.00, 'Cinema', 'DESPESA', 3, 3);

-- Transações do Roberto (ID 3)
INSERT INTO TRANSACOES (Valor, Descricao, Tipo_Transacao, ID_Conta_FK, ID_Categoria_FK) VALUES 
(12.00, 'Café da Tarde', 'DESPESA', 4, 1);

SELECT 
    U.Nome AS Nome_Usuario,
    C.Nome_Conta,
    CAT.Nome_Categoria,
    T.Descricao,
    T.Valor,
    T.Tipo_Transacao,
    T.Data_Transacao
FROM TRANSACOES T
INNER JOIN CONTAS C ON T.ID_Conta_FK = C.ID_Conta
INNER JOIN USUARIOS U ON C.ID_Usuario_FK = U.ID_Usuario
INNER JOIN CATEGORIAS CAT ON T.ID_Categoria_FK = CAT.ID_Categoria
ORDER BY T.Data_Transacao DESC;

SELECT 
    U.Nome,
    T.Descricao,
    T.Valor,
    CAT.Nome_Categoria
FROM TRANSACOES T
JOIN CONTAS C ON T.ID_Conta_FK = C.ID_Conta
JOIN USUARIOS U ON C.ID_Usuario_FK = U.ID_Usuario
JOIN CATEGORIAS CAT ON T.ID_Categoria_FK = CAT.ID_Categoria
WHERE U.Nome = 'Carlos Mendes' 
  AND T.Tipo_Transacao = 'DESPESA';

SELECT 
    CAT.Nome_Categoria,
    COUNT(T.ID_Transacao) AS Qtd_Usos
FROM CATEGORIAS CAT
LEFT JOIN TRANSACOES T ON CAT.ID_Categoria = T.ID_Categoria_FK
GROUP BY CAT.Nome_Categoria
ORDER BY Qtd_Usos ASC;

SELECT 
    U.Nome AS Cliente,
    SUM(C.Saldo_Atual) AS Patrimonio_Total
FROM USUARIOS U
JOIN CONTAS C ON U.ID_Usuario = C.ID_Usuario_FK
GROUP BY U.Nome
ORDER BY Patrimonio_Total DESC;

SELECT 
    T.Descricao AS Gasto,
    T.Valor,
    C.Nome_Conta,
    U.Nome AS Dono_Da_Conta
FROM TRANSACOES T
JOIN CONTAS C ON T.ID_Conta_FK = C.ID_Conta
JOIN USUARIOS U ON C.ID_Usuario_FK = U.ID_Usuario
WHERE T.Tipo_Transacao = 'DESPESA' 
  AND T.Valor > 100.00;
