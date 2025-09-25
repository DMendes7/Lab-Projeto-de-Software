-- H2: garantir que a JPA já criou as tabelas e limpar em ordem segura
SET REFERENTIAL_INTEGRITY FALSE;

TRUNCATE TABLE pedido;
TRUNCATE TABLE automovel;
TRUNCATE TABLE contratantes;

SET REFERENTIAL_INTEGRITY TRUE;

-- =========================
-- CONTRATANTES (IDs 1..3)
-- =========================
INSERT INTO contratantes (id, nome, documento, email, profissao, rg, endereco, role, senha_hash, created_at)
VALUES
  (1, 'Administrador', '00000000000', 'admingia',        'Administrador', 'ADM-1',   'Sede',         'ADMIN', 'dummy', CURRENT_TIMESTAMP),
  (2, 'Alice Demo',    '11111111111', 'alice@demo.com',  'Designer',      'RG-ALICE','Rua A, 100',   'CLIENT','dummy', CURRENT_TIMESTAMP),
  (3, 'Bruno Demo',    '22222222222', 'bruno@demo.com',  'Analista',      'RG-BRUNO','Rua B, 200',   'CLIENT','dummy', CURRENT_TIMESTAMP);

-- =========================
-- AUTOMÓVEIS (IDs 1..4)
-- =========================
INSERT INTO automovel (id, marca, modelo, ano, placa, renavam, ativo)
VALUES
  (1, 'Toyota',  'Corolla', 2022, 'ABC1A23', 'REN-0001', TRUE),
  (2, 'Honda',   'Civic',   2021, 'DEF4B56', 'REN-0002', TRUE),
  (3, 'Volks',   'T-Cross', 2023, 'GHI7C89', 'REN-0003', TRUE),
  (4, 'Chevy',   'Onix',    2020, 'JKL0D12', 'REN-0004', TRUE);

-- =========================
-- PEDIDOS (IDs 101..104)
-- Status válidos: NOVO, EM_AVALIACAO, APROVADO, REPROVADO, EM_EXECUCAO, CANCELADO
-- =========================
INSERT INTO pedido (id, automovel_id, contratante_id, data_criacao, periodo_inicio, periodo_fim, status)
VALUES
  (101, 1, 2, CURRENT_TIMESTAMP, DATE '2025-09-25', DATE '2025-10-01', 'NOVO'),
  (102, 2, 2, CURRENT_TIMESTAMP, DATE '2025-10-10', DATE '2025-10-15', 'EM_AVALIACAO'),
  (103, 3, 3, CURRENT_TIMESTAMP, DATE '2025-09-20', DATE '2025-09-28', 'APROVADO'),
  (104, 4, 3, CURRENT_TIMESTAMP, DATE '2025-10-05', DATE '2025-10-12', 'EM_EXECUCAO');
