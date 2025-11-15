insert into funcao (id_Funcao, nome_funcao_, descricao)
values
(1, 'Cliente', 'Usuário cliente da locadora'), -- 
(2, 'Funcionario', 'Funcionário da locadora'), --
(3, 'Gerente', 'Gerente da locadora'), -- 
(4, 'Admin', 'Administrador do sistema'), -- 
(5, 'Supervisor', 'Supervisor da locadora'); --

insert into cidade (id_cidade, nome_cidade, cep, bairro, num_casa, complemento)
values
(1, 'São Paulo', '01001000', 'Centro', 101, 'Apto 101'),
(2, 'Rio de Janeiro', '22040001', 'Copacabana', 202, 'Apto 202'),
(3, 'Belo Horizonte', '30140071', 'Savassi', 303, 'Apto 303'),
(4, 'Curitiba', '80420010', 'Batel', 404, 'Apto 404'),
(5, 'Porto Alegre', '90540000', 'Moinhos de Vento', 505, 'Casa 111');

insert into estado (id_estado, nome_estado, regiao, fk_cidade_id_cidade)
values
(1, 'São Paulo', 'Sudeste', 1),
(2, 'Minas Gerais', 'Sudeste', 3),
(3, 'Rio de Janeiro', 'Sudeste', 2),
(4, 'Amazonas', 'Norte', 4),
(5, 'Acre', 'Norte', 5);

insert into pais (id_pais, sigla_, nome_pais, fk_estado_id_estado)
values
(1, 'BR', 'Brasil', 1),
(2, 'AR', 'Argentina', 2),
(3, 'US', 'Estados Unidos', 3),
(4, 'DE', 'Alemanha', 4),
(5, 'JP', 'Japão', 5);

insert into pagamento_ (id_pagamento, valor, data_pagamento, metodo)
values
(1, 500.00, '2025-10-01', 'Cartão de Crédito'),
(2, 650.00, '2025-10-02', 'Boleto'),
(3, 800.00, '2025-10-03', 'Pix'),
(4, 720.00, '2025-10-04', 'Cartão Débito'),
(5, 950.00, '2025-10-05', 'Dinheiro');

insert into usuario_ (email, nome_completo, senha, data_nasc, cpf, id_cliente, cnh, cargo, id_funcionario, id_admin, usuario__tipo, fk_funcao_id_funcao, fk_cidade_id_cidade)
values
('joao@email.com', 'João Silva', 'senha123', '1990-05-12', '12345678901', 1, 'ABC12345678', 'Cliente', 101, 201, 1, 1, 1),
('maria@email.com', 'Maria Souza', 'senha456', '1985-07-22', '23456789012', 2, 'DEF23456789', 'Cliente', 102, 202, 1, 2, 2),
('pedro@email.com', 'Pedro Lima', 'senha789', '1992-11-03', '34567890123', 3, 'GHI34567890', 'Funcionario', 103, 203, 2, 3, 3),
('ana@email.com', 'Ana Oliveira', 'senha321', '1988-02-15', '45678901234', 4, 'JKL45678901', 'Cliente', 104, 204, 1, 4, 4),
('carlos@email.com', 'Carlos Pereira', 'senha654', '1995-09-27', '56789012345', 5, 'MNO56789012', 'Funcionario', 105, 205, 2, 5, 5);

insert into adicionais (id_adicionais, nome_adicionais, descricao, disponibilidade)
values
(1, 'GPS', 'Sistema de navegação GPS', 'disponivel'),
(2, 'Cadeirinha', 'Cadeirinha infantil até 12 anos', 'disponivel'),
(3, 'Bagageiro', 'Bagageiro para malas grandes', 'indisponivel'),
(4, 'Seguro Extra', 'Proteção contra acidentes', 'disponivel'),
(5, 'Wi-Fi', 'Internet móvel no veículo', 'disponivel');

insert into multa (id_multa, motivo_multa, valor, data_multa)
values
(1, 'Excesso de velocidade', 200.00, '2025-10-01 10:00:00'),
(2, 'Estacionamento irregular', 150.00, '2025-10-02 12:30:00'),
(3, 'Danos ao veículo', 500.00, '2025-10-03 15:45:00'),
(4, 'Atraso na devolução', 100.00, '2025-10-04 09:20:00'),
(5, 'Não utilização do cinto', 50.00, '2025-10-05 11:10:00');

insert into locacao_seguro_ (id_locacao, id_seguro, id_Cliente, id_Veiculo, agencia_retirada, data_inicio, data_fim, data_prevista_devolucao, data_devolucao, valor, fk_pagamento__id_pagamento)
values
(1, 101, 1, 1001, 'locars Central', '2025-10-01', '2025-10-05', '2025-10-05', '2025-10-05', 500.00, 1),
(2, 102, 2, 1002, 'locars Norte', '2025-10-03', '2025-10-06', '2025-10-06', '2025-10-06', 650.00, 2),
(3, 103, 3, 1003, 'locars Sul', '2025-10-04', '2025-10-08', '2025-10-08', '2025-10-08', 800.00, 3),
(4, 104, 4, 1004, 'locars Leste', '2025-10-02', '2025-10-07', '2025-10-07', '2025-10-07', 720.00, 4),
(5, 105, 5, 1005, 'locars Oeste', '2025-10-05', '2025-10-10', '2025-10-10', '2025-10-10', 950.00, 5);



insert into agencia (id_agencia, nome_agencia, num_agencia)
values
(1, 'locars Central', 1001),
(2, 'locars Norte', 1002),
(3, 'locars Sul', 1003),
(4, 'locars Leste', 1004),
(5, 'locars Oeste', 1005);

insert into categoria (id_categoria, tipos_categorias)
values
(1, 'SUV'),
(2, 'Sedan'),
(3, 'Hatch'),
(4, 'Picape'),
(5, 'Esportivo');

insert into modelo (id_modelo, nome_modelo)
values
(1, 'Corolla'),
(2, 'Civic'),
(3, 'Golf'),
(4, 'Hilux'),
(5, 'Mustang');

insert into tipo_veiculo (id_tipo, nome_tipo)
values
(1, 'Carro'),
(2, 'Moto'),
(3, 'Caminhão'),
(4, 'Van'),
(5, 'Ônibus');

insert into marca_veiculo (id_marca, nome_marca)
values
(1, 'Toyota'),
(2, 'Honda'),
(3, 'Volkswagen'),
(4, 'Ford'),
(5, 'Chevrolet');

insert into veiculo (id_veiculo, frota, placa, km_rodado, statusveiculo, fk_Categoria_id_Categoria)
values 
(1, 1001, 'ABC1234', 12000.50, 'Disponível', 1),
(2, 1002, 'XYZ5678', 34500.75, 'Indisponível', 2),
(3, 1003, 'KLM4321', 23000.00, 'Disponível', 1),
(4, 1004, 'DEF7654', 54000.20, 'Disponível', 3),
(5, 1005, 'GHI1111', 98765.10, 'Indisponível', 2);

INSERT INTO historico_km (id_Km, id_Veiculo, Km_Registrado, Data_Registro)
VALUES
(1, 1, 12000.50, '2025-10-01'),
(2, 2, 34500.75, '2025-10-02'),
(3, 3, 23000.00, '2025-10-03'),
(4, 4, 54000.20, '2025-10-04'),
(5, 5, 98765.10, '2025-10-05');

INSERT INTO locacao_seguro_  (id_Locacao, id_Seguro, id_Cliente, id_Veiculo, Data_Prevista_Devolucao, Data_Inicio, Data_Fim, Data_Devolucao, Valor, fk_Pagamento__id_Pagamento)
VALUES
(101, 201, 1, 1001, '2025-11-01', '2025-10-28', '2025-11-05', '2025-11-05', 500.00, 1), -- 4 de atraso
(102, 202, 2, 1002, '2025-10-30', '2025-10-25', '2025-10-30', '2025-10-30', 650.00, 2), -- prazo
(103, 203, 3, 1003, '2025-11-03', '2025-11-01', '2025-11-03', '2025-11-03', 800.00, 3); -- 1 de atraso