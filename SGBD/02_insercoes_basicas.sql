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
-- 1. INSERÇÕES DE BASE (FUNÇÕES, PAÍS, ESTADO, CIDADE)
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
(2, 'Minas Gerais', 'Sudeste', 1),
(3, 'Rio de Janeiro', 'Sudeste', 1),
(4, 'Paraná', 'Sul', 1),
(5, 'Rio Grande do Sul', 'Sul', 1);

INSERT IGNORE INTO cidade (id_cidade, nome_cidade, cep, bairro, num_casa, complemento, fk_Estado_id_Estado)
VALUES
(1, 'São Paulo', '01001000', 'Centro', 101, 'Apto 101', 1),
(2, 'Rio de Janeiro', '22040001', 'Copacabana', 202, 'Apto 202', 3),
(3, 'Belo Horizonte', '30140071', 'Savassi', 303, 'Apto 303', 2),
(4, 'Curitiba', '80420010', 'Batel', 404, 'Apto 404', 4),
(5, 'Porto Alegre', '90540000', 'Moinhos de Vento', 505, 'Casa 111', 5);

-- ------------------------------------------------------------
-- 2. USUÁRIOS E SUBTIPOS
-- ------------------------------------------------------------

INSERT IGNORE INTO usuario_
(email, nome_completo, senha, data_nasc, cpf, fk_funcao_id_funcao, fk_cidade_id_cidade)
VALUES
(AES_ENCRYPT('joao@email.com', 'chaveSegura123'), 'João Silva', SHA2('senha123',256), '1990-05-12', '12345678901', 1, 1),
(AES_ENCRYPT('maria@email.com', 'chaveSegura123'), 'Maria Souza', SHA2('senha456',256), '1985-07-22', '23456789012', 1, 2),
(AES_ENCRYPT('pedro@email.com', 'chaveSegura123'), 'Pedro Lima', SHA2('senha789',256), '1992-11-03', '34567890123', 2, 3),
(AES_ENCRYPT('ana@email.com', 'chaveSegura123'), 'Ana Oliveira', SHA2('senha321',256), '1988-02-15', '45678901234', 1, 4),
(AES_ENCRYPT('carlos@email.com','chaveSegura654'), 'Carlos Pereira', SHA2('senha654',256), '1995-09-27', '56789012345', 2, 5);


-- ------------------------------------------------------------
-- 3. PAGAMENTOS, VEÍCULOS, AGENCIAS E MULTAS
-- ------------------------------------------------------------

INSERT IGNORE INTO pagamento_ (id_pagamento, valor, data_pagamento, metodo)
VALUES
(1, 500.00, '2025-10-01', 'Cartão de Crédito'),
(2, 650.00, '2025-10-02', 'Boleto'),
(3, 800.00, '2025-10-03', 'Pix'),
(4, 720.00, '2025-10-04', 'Cartão Débito'),
(5, 950.00, '2025-10-05', 'Dinheiro');

INSERT IGNORE INTO adicionais (id_adicionais, nome_adicionais, descricao, disponibilidade)
VALUES
(1, 'GPS', 'Sistema de navegação GPS', 'disponivel'),
(2, 'Cadeirinha', 'Cadeirinha infantil', 'disponivel'),
(3, 'Bagageiro', 'Bagageiro grande', 'indisponivel'),
(4, 'Seguro Extra', 'Proteção completa', 'disponivel'),
(5, 'Wi-Fi', 'Rede móvel', 'disponivel');

INSERT IGNORE INTO multa (id_multa, motivo_multa, valor, data_multa)
VALUES
(1, 'Excesso de velocidade', 200, '2025-10-01 10:00:00'),
(2, 'Estacionamento irregular', 150, '2025-10-02 12:30:00'),
(3, 'Danos ao veículo', 500, '2025-10-03 15:45:00'),
(4, 'Atraso na devolução', 100, '2025-10-04 09:20:00'),
(5, 'Não uso de cinto', 50, '2025-10-05 11:10:00');

INSERT IGNORE INTO agencia (id_agencia, nome_agencia, num_agencia, Id_Cidade)
VALUES
(1, 'locars Central', 1001, 1),
(2, 'locars Norte', 1002, 1),
(3, 'locars Sul', 1003, 2),
(4, 'locars Leste', 1004, 2),
(5, 'locars Oeste', 1005, 3);

INSERT IGNORE INTO categoria (id_categoria, tipos_categorias)
VALUES
(1,'SUV'), (2,'Sedan'), (3,'Hatch'), (4,'Picape'), (5,'Esportivo');

INSERT IGNORE INTO modelo (id_modelo, nome_modelo)
VALUES
(1,'Corolla'), (2,'Civic'), (3,'Golf'), (4,'Hilux'), (5,'Mustang');

INSERT IGNORE INTO tipo_veiculo (id_tipo, nome_tipo)
VALUES
(1,'Carro'), (2,'Moto'), (3,'Caminhão'), (4,'Van'), (5,'Ônibus');

INSERT IGNORE INTO marca_veiculo (id_marca, nome_marca)
VALUES
(1,'Toyota'), (2,'Honda'), (3,'Volkswagen'), (4,'Ford'), (5,'Chevrolet');

INSERT IGNORE INTO veiculo
(id_veiculo, frota, placa, km_rodado, statusveiculo, fk_categoria_id_categoria)
VALUES
(1,1001,'ABC1234',12000.50,'Disponível',1),
(2,1002,'XYZ5678',34500.75,'Indisponível',2),
(3,1003,'KLM4321',23000.00,'Disponível',1),
(4,1004,'DEF7654',54000.20,'Disponível',3),
(5,1005,'GHI1111',98765.10,'Indisponível',2);

INSERT IGNORE INTO historico_km (id_Km, id_Veiculo, Km_Registrado, Data_Registro)
VALUES
(1,1,12000.50,'2025-10-01'),
(2,2,34500.75,'2025-10-02'),
(3,3,23000.00,'2025-10-03'),
(4,4,54000.20,'2025-10-04'),
(5,5,98765.10,'2025-10-05');

-- ------------------------------------------------------------
-- 4. LOCAÇÕES
-- ------------------------------------------------------------

INSERT IGNORE INTO locacao_seguro_
(id_Locacao, id_Seguro, id_Cliente, id_Veiculo, Data_Prevista_Devolucao, 
Data_Inicio, Data_Fim, Data_Devolucao, Valor, fk_Pagamento__id_Pagamento)
VALUES
(1,101,1,1,'2025-10-01','2025-10-05','2025-10-05','2025-10-05',500,1),
(2,102,2,2,'2025-10-03','2025-10-06','2025-10-06','2025-10-06',650,2),
(3,103,4,3,'2025-10-04','2025-10-08','2025-10-08','2025-10-08',800,3),
(4,104,1,4,'2025-10-02','2025-10-07','2025-10-07','2025-10-07',720,4),
(5,105,2,5,'2025-10-05','2025-10-10','2025-10-10','2025-10-10',950,5);

-- ------------------------------------------------------------
-- 5. VISTORIAS
-- ------------------------------------------------------------

INSERT IGNORE INTO vistoria
(id_vistoria,fk_aluguel_id,tipo,nivel_combustivel,quilometragem,avarias_json,data_vistoria)
VALUES
(1,1,'saida',0.80,12010,'{"amassados":[],"arranhoes":[]}','2025-10-01 09:00:00'),
(2,1,'entrada',0.60,12045,'{"amassados":["parachoque"]}','2025-10-05 10:30:00'),
(3,2,'saida',0.90,34510,'{}','2025-10-03 14:00:00'),
(4,2,'entrada',0.40,34590,'{"arranhoes":["lateral"]}','2025-10-06 16:40:00'),
(5,3,'saida',1.00,23010,'{}','2025-10-04 16:00:00');

-- ------------------------------------------------------------
-- 6. NOTIFICAÇÕES
-- ------------------------------------------------------------

INSERT IGNORE INTO notificacao
(id_notificacao, mensagem, data_envio, fk_usuario_id)
VALUES
(1,'Seu veículo foi reservado com sucesso!','2025-10-01 08:00:00',1),
(2,'Pagamento confirmado.','2025-10-02 09:00:00',2),
(3,'Devolução prevista amanhã.','2025-10-04 10:00:00',4),
(4,'Multa adicionada ao contrato.','2025-10-05 11:00:00',1),
(5,'Agradecemos sua locação!','2025-10-10 12:00:00',2);

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
