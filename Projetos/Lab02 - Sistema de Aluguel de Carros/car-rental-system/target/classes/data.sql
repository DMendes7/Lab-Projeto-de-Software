-- ===========================
-- CONTRATANTES (admin + clientes)
-- ===========================
-- Observação: 'senha_hash' aqui é apenas placeholder para efeito de seed.
-- Se o login efetivo estiver lendo do banco, substitua por hashes BCrypt reais.
MERGE INTO contratante KEY(id) VALUES
  (1, CURRENT_TIMESTAMP, '00000000000', 'admingia',       'Rua Admin, 100',  'Administrador', 'Administrador', 'ADM-1',    'ADMIN',  'dummy'),
  (2, CURRENT_TIMESTAMP, '11111111111', 'alice@demo.com', 'Rua Alpha, 123',  'Alice Demo',    'Designer',      'RG-ALICE', 'CLIENT', 'dummy'),
  (3, CURRENT_TIMESTAMP, '22222222222', 'bruno@demo.com', 'Rua Beta, 456',   'Bruno Demo',    'Analista',      'RG-BRUNO', 'CLIENT', 'dummy');

-- Colunas, na ordem:
-- (id, created_at, documento, email, endereco, nome, profissao, rg, role, senha_hash)


-- ===========================
-- AUTOMÓVEIS (4 modelos)
-- ===========================
MERGE INTO automovel KEY(id) VALUES
  (1, 2022, TRUE, 'Toyota',    'Corolla', 'ABC-1A23', '12345678901'),
  (2, 2021, TRUE, 'Honda',     'Civic',   'DEF-4B56', '23456789012'),
  (3, 2023, TRUE, 'Chevrolet', 'Onix',    'GHI-7C89', '34567890123'),
  (4, 2020, TRUE, 'Hyundai',   'HB20',    'JKL-0D12', '45678901234');

-- Colunas, na ordem:
-- (id, ano, ativo, marca, modelo, placa, renavam)


-- ===========================
-- PEDIDOS (4 pedidos, 2 p/ cada cliente, com status diferentes)
-- Status válidos (ajuste se o Enum mudar): NOVO, EM_AVALIACAO, APROVADO, REPROVADO, EM_EXECUCAO, CANCELADO
-- ===========================
MERGE INTO pedido KEY(id) VALUES
  -- Alice: NOVO (futuro)
  (1, 1, 2, CURRENT_TIMESTAMP,
      DATEADD('DAY',  1, CURRENT_DATE),  -- inicio amanhã
      DATEADD('DAY',  8, CURRENT_DATE),  -- fim em 7 dias
      'NOVO'),

  -- Alice: APROVADO (passado)
  (2, 2, 2, CURRENT_TIMESTAMP,
      DATEADD('DAY', -10, CURRENT_DATE), -- iniciou há 10 dias
      DATEADD('DAY',  -3, CURRENT_DATE), -- terminou há 3 dias
      'APROVADO'),

  -- Bruno: EM_AVALIACAO (janela atual)
  (3, 3, 3, CURRENT_TIMESTAMP,
      DATEADD('DAY', -1, CURRENT_DATE),  -- ontem
      DATEADD('DAY',  5, CURRENT_DATE),  -- daqui 5 dias
      'EM_AVALIACAO'),

  -- Bruno: CANCELADO (futuro curto)
  (4, 4, 3, CURRENT_TIMESTAMP,
      DATEADD('DAY',  2, CURRENT_DATE),  -- começa em 2 dias
      DATEADD('DAY',  4, CURRENT_DATE),  -- termina em 4 dias
      'CANCELADO');

-- Colunas, na ordem:
-- (id, automovel_id, contratante_id, data_criacao, periodo_inicio, periodo_fim, status)
