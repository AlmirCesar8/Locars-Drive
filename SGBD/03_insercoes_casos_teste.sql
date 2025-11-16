/* ============================================================
 Arquivo: 03_insercoes_casos_teste.sql
 Autor(es): Benjamin, Fabio; Silva, Almir; Paiva, Gabriel
 Trabalho: LocarsDrive
 Curso/Turma: Desenvolvimento de Sistemas - 213 Matutino
 SGBD: MySQL Versão: 8.0
 Objetivo: Inserir dados de teste para validação de regras
 Execução esperada: após inserções básicas
 ============================================================ */
 
 
-- Cenário A: Usuário sem cidade (violação de FK)
	-- Objetivo: Testar se o sistema exige cidade vinculada corretamente
    
insert into Usuario_ (Email, Nome_Completo, Senha, Data_Nasc, CPF, id_Cliente, CNH, Cargo, id_Funcionario, id_Admin, Usuario__TIPO, fk_Funcao_id_Funcao, fk_Cidade_id_Cidade)
values 
('SemCidade@email.com', 'Usuário Sem Cidade', 'senha000', '2000-01-01', '99988877766', 7, 'ZZZ12345678', 'Cliente', 107, 207, 1, 3, null);

-- Cenário B: Usuario sem ter finalizado o pagamento 
	-- Objetivo: Teste se o sistema permite exige que o usuario faça pagamento
    
insert into Locacao_Seguro_ (id_Locacao, id_Seguro, Agencia_Retirada, Data_Inicio, Data_Fim, Valor, fk_Pagamento__id_Pagamento)
values 
(99, 999, 'Locars Teste', '2025-11-01', '2025-11-05', 700.00, null);

-- Cenário C: Funcionário com salário negativo
	-- Objetivo: Testar se o sistema valida corretamente o valor do salário, impedindo valores negativos
		-- O erro que aparecera é o 'error code: 3819', mas ao parecer mostrará que está correto, (1)
		-- pois este erro impede valores negativos no campo 'Salario' como feito no alter table usuario_ (erro esperado e totalmente coerente, (2)
    
insert into Usuario_ (Nome_Completo, Email, Senha, Data_Nasc, CPF, id_Cliente, CNH, Cargo, id_Funcionario, id_Admin, Usuario__TIPO, fk_Funcao_id_Funcao, Salario)
values
('João Salário Positivo', 'joao.positivo@email.com', 'senha123', '1990-01-01', '98765432100', 10, 'XYZ98765432', 'Funcionario', 110, 210, 2, 2, 1500.00), -- correto
('João Salário Positivo', 'joao.negativo@email.com', 'senha123', '1990-01-01', '12345678911', 1, 'ABC12345678', 'Funcionario', 101, 201, 2, 2, -1500.00); -- error 3819


-- Cenário D: Veiculo sem categoria 
	-- Objetivo: Testar se o sistema exige categoria vinculada em veiculo

insert into Veiculo (id_Veiculo, Frota, Placa, Km_Rodado, StatusVeiculo, fk_Categoria_id_Categoria)
values 
(10, 2001, 'JKL9876', 15000.00, 'Disponível', null), -- com valor null no fk_Categoria_id_Categoria (erro de integridade, pois nao pode ser 'null' o valor)
(11, 2002, 'JKL9877', 15000.00, 'Indisponível', 1); -- com valor no fk_Categoria_id_Categoria (roda normalmente)
