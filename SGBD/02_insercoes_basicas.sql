/* ============================================================
 Arquivo: 02_insercoes_basicas.sql
 Autor(es): Almir Silva; Fabio Benjamin; Gabriel Paiva
 Trabalho: LocarsDrive
 Curso/Turma: Desenvolvimento de Sistemas - 213 Matutino
 SGBD: MySQL Versão: 8.0
 Objetivo: Inserção de dados básicos
 Execução esperada: após criação do modelo físico
 ============================================================ */

-- ------------------------------------------------------------
-- 1. INSERÇÕES DE BASE (FUNÇÕES, PAÍS, ESTADO)
-- ------------------------------------------------------------

INSERT IGNORE INTO funcao (id_Funcao, nome_funcao, descricao)
VALUES
(1, 'Cliente', 'Usuário cliente da locadora'),
(2, 'Funcionario', 'Funcionário da locadora'),
(3, 'Gerente', 'Gerente da locadora'),
(4, 'Admin', 'Administrador do sistema'),
(5, 'Supervisor', 'Supervisor da locadora');

INSERT IGNORE INTO pais (id_pais, nome_pais, Sigla_)
VALUES
(1, 'Brasil', 'BR'),
(2, 'Argentina', 'AR'),
(3, 'Estados Unidos', 'US'),
(4, 'Alemanha', 'DE'),
(5, 'Japão', 'JP');

INSERT IGNORE INTO estado (id_estado, nome_estado, regiao, fk_Pais_id_Pais)
VALUES
(1, 'São Paulo', 'Sudeste', 1),
(2, 'Rio de Janeiro', 'Sudeste', 1),
(3, 'Minas Gerais', 'Sudeste', 1),
(4, 'Bahia', 'Nordeste', 1),
(5, 'Paraná', 'Sul', 1);

-- ------------------------------------------------------------
-- 2. INSERÇÃO DE CIDADES (SEM CAMPOS DE ENDEREÇO)
-- ------------------------------------------------------------

INSERT IGNORE INTO cidade (id_cidade, nome_cidade, fk_Estado_id_Estado)
VALUES
(1, 'São Paulo', 1),
(2, 'Guarulhos', 1),
(3, 'Rio de Janeiro', 2),
(4, 'Belo Horizonte', 3),
(5, 'Curitiba', 5);

-- ------------------------------------------------------------
-- 3. NOVA INSERÇÃO DE ENDEREÇOS (REFERENCIANDO CIDADES)
-- ------------------------------------------------------------

INSERT IGNORE INTO Endereco (id_Endereco, CEP, Logradouro, Num_Casa, Bairro, Complemento, fk_Cidade_id_Cidade)
VALUES
-- Endereços para Agências
(1, '01311100', 'Av. Paulista', 1000, 'Bela Vista', 'Conj. 101', 1), -- SP: Agência Principal
(2, '07190100', 'Rod. Hélio Smidt', 1200, 'Aeroporto', 'Terminal 2', 2), -- Guarulhos: Agência Aeroporto
(3, '22070010', 'Rua Prudente de Morais', 500, 'Ipanema', NULL, 3), -- RJ: Agência Ipanema

-- Endereço para Cliente Admin (Roberto Campos) - (id_usuario = 1)
(4, '05407000', 'Rua Teodoro Sampaio', 2300, 'Pinheiros', 'Apto. 50', 1);


-- ------------------------------------------------------------
-- 4. INSERÇÃO DE AGÊNCIAS (REFERENCIANDO ENDEREÇOS)
-- ------------------------------------------------------------

INSERT IGNORE INTO agencia (id_Agencia, nome_agencia, Num_Agencia, fk_Endereco_id_Endereco)
VALUES
(1, 'São Paulo - Centro', 101, 1),
(2, 'Guarulhos - Aeroporto', 102, 2),
(3, 'Rio de Janeiro - Sul', 103, 3);


-- ------------------------------------------------------------
-- 5. INSERÇÃO DE VEÍCULOS (MARCA, MODELO, CATEGORIA, VEICULO)
-- ------------------------------------------------------------

-- Marca (Manutenção da estrutura original, pois não houve alteração)
INSERT IGNORE INTO Marca_Veiculo (id_Marca, Nome_Marca)
VALUES
(1, 'Chevrolet'),
(2, 'Fiat'),
(3, 'Volkswagen'),
(4, 'Toyota'),
(5, 'Honda');

-- Modelo (Manutenção da estrutura original)
INSERT IGNORE INTO Modelo (id_Modelo, Nome_Modelo)
VALUES
(1, 'Onix Plus'),
(2, 'Cronos'),
(3, 'T-Cross'),
(4, 'Corolla'),
(5, 'HR-V');

-- Categoria (Manutenção da estrutura original)
INSERT IGNORE INTO Categoria (id_Categoria, Tipos_Categorias)
VALUES
(1, 'Sedan Compacto'),
(2, 'Sedan Médio'),
(3, 'SUV Compacto'),
(4, 'Hatch'),
(5, 'Premium');

-- Veiculo (Manutenção da estrutura original)
INSERT IGNORE INTO Veiculo (id_Veiculo, Frota, Placa, Km_Rodado, StatusVeiculo, fk_Categoria_id_Categoria, fk_Marca_id_Marca, fk_Modelo_id_Modelo)
VALUES
(1, 2025001, 'ABC1234', 12000.50, 'Disponível', 1, 1, 1),
(2, 2025002, 'XYZ9876', 34500.00, 'Indisponível', 3, 3, 3),
(3, 2025003, 'DEF5678', 23000.75, 'Disponível', 2, 4, 4);

-- ------------------------------------------------------------
-- 6. INSERÇÃO DE USUÁRIOS
-- ------------------------------------------------------------

INSERT IGNORE INTO Usuario_ (id_Usuario, Email, Nome_Completo, Senha, Data_Nasc, CPF, CNH, Cargo, Salario, Pontuacao_Reputacao, fk_Funcao_id_Funcao, fk_Endereco_id_Endereco, id_Cliente, id_Funcionario, id_Admin, tipo_perfil)
VALUES
(1, 'roberto.admin@locarsdrive.com', 'Roberto Campos (Admin)', '$2b$12$...', '1990-05-15', '12345678901', 'ABC12345678', 'Administrador Geral', 10000.00, 5.0, 4, 4, 1, 1, 1, 'misto'), -- Ref. Endereço 4
(2, 'joao.cliente@mail.com', 'João Silva', '$2b$12$...', '1985-11-20', '98765432109', 'DEF87654321', NULL, 0.00, 4.5, 1, NULL, 2, 0, 0, 'alugador'), -- Sem endereço
(3, 'maria.func@mail.com', 'Maria Souza (Func)', '$2b$12$...', '1995-03-10', '45612378900', 'GHI09876543', 'Atendente', 3000.00, 5.0, 2, NULL, 0, 2, 0, 'locador'); -- Sem endereço

-- ------------------------------------------------------------
-- 7. RMS e Outras Tabelas
-- ------------------------------------------------------------

INSERT IGNORE INTO aluguel (id_aluguel, fk_usuario_id, fk_veiculo_id, data_retirada, data_devolucao_prevista, data_devolucao_real, status, valor_diaria, valor_total_previsto)
VALUES
(1, 2, 1, '2025-10-01 08:00:00', '2025-10-05 10:00:00', '2025-10-05 10:30:00', 'Devolvido', 120.00, 480.00),
(2, 2, 2, '2025-10-03 14:00:00', '2025-10-06 17:00:00', '2025-10-06 16:40:00', 'Devolvido', 150.00, 450.00),
(3, 1, 3, '2025-10-04 16:00:00', '2025-10-10 16:00:00', NULL, 'Em Uso', 130.00, 780.00);

INSERT IGNORE INTO vistoria (id_vistoria,fk_aluguel_id,tipo,nivel_combustivel,quilometragem,avarias_json,data_vistoria)
VALUES
(1,1,'saida',0.80,12010,'{"amassados":[],"arranhoes":[]}','2025-10-01 09:00:00'),
(2,1,'entrada',0.60,12045,'{"amassados":["parachoque"]}','2025-10-05 10:30:00'),
(3,2,'saida',0.90,34510,'{}','2025-10-03 14:00:00'),
(4,2,'entrada',0.40,34590,'{"arranhoes":["lateral"]}','2025-10-06 16:40:00'),
(5,3,'saida',1.00,23010,'{}','2025-10-04 16:00:00');

INSERT IGNORE INTO notificacao (id_notificacao, mensagem, data_envio, fk_usuario_id)
VALUES
(1,'Seu veículo foi reservado com sucesso!','2025-10-01 08:00:00',1),
(2,'Pagamento confirmado.','2025-10-02 09:30:00',2),
(3,'Lembrete: Sua locação termina em 24h.','2025-10-09 16:00:00',1);

-- ------------------------------------------------------------
-- 7. AVALIAÇÕES DE SERVIÇO
-- ------------------------------------------------------------

INSERT IGNORE INTO avaliacao_servico
(id_avaliacao, nota, comentarios, data_avaliacao, fk_aluguel_id)
VALUES
(1,5,'Excelente atendimento.','2025-10-06',1),
(2,4,'Boa experiência.','2025-10-07',2),
(3,5,'Veículo impecável.','2025-10-08',3),
(4,3,'Atraso na entrega.','2025-10-10',4),
(5,4,'Recomendaria a amigos.','2025-10-12',5);
