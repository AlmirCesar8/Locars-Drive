/* ============================================================
 Arquivo: 20_triggers.sql
 Autor(es): Fabio Benjamin; Almir Silva; Gabriel Paiva 
 Trabalho: LocarsDrive
 Curso/Turma: Desenvolvimento de Sistemas - 213 Matutino
 SGBD: MySQL 8.0
 Objetivo: Criar triggers para automatizar regras de negócio
 ============================================================ */

-- Trigger 1: Validação de CPF antes de adiciona-lo a um usuário

delimiter $$

create trigger vld_Valida_cpf 

before insert on Usuario_ 
for each row begin 
	if new.CPF is null or trim(new.CPF) = ' ' then 
		signal sqlstate '45000'
        set message_text = "CPF não pode estar vazio";
	end if;
end; 

delimiter ;

-- Trigger 2: Validação do pagamento

delimiter $$

create trigger vld_Valida_pagamento

before update on pagamento_
for each row begin
	if trim(new.Status_Pagamento) = 'Pago' then
		if new.Valor is null or new.Valor <= 0 then
			signal sqlstate '45000'
            set message_text = "Valor não pago";
		end if;
	end if;
end$$

delimiter ;


-- INICIO DAS DML DE TESTE

-- DML da trigger 1: Validação do CPF

-- válido - campo cpf preenchido
insert into usuario_ 
(email, nome_completo, senha, data_nasc, cpf, id_cliente, cnh, cargo, id_funcionario, id_admin, usuario__tipo, salario)
values 
('cpfvalido@email.com', 'CPF Válido', '123', '2025-05-10', '11122233344', 20, 'CNH12345678', 'Cliente', 120, 220, 1, 1500.00);

-- inválido - campo cpf vazio
insert into usuario_ 
(email, nome_completo, senha, data_nasc, cpf, id_cliente, cnh, cargo, id_funcionario, id_admin, usuario__tipo, salario)
values 
('cpfvazio@email.com', 'CPF Vazio', '123', '2025-01-01', '', 21, 'CNH00000000', 'Cliente', 121, 221, 1, 1500.00);

-- inválido - campo cpf nulo
insert into usuario_ 
(email, nome_completo, senha, data_nasc, cpf, id_cliente, cnh, cargo, id_funcionario, id_admin, usuario__tipo, salario)
values 
('cpfnullo@email.com', 'CPF Nulo', '123', '2025-02-02', null, 22, 'CNH87654321', 'Cliente', 122, 222, 1, 1500.00);

select id_Usuario, Nome_Completo, CPF
from Usuario_;

-- DML da trigger 2: Validação do pagamento

-- Válido - Pagamento pendente
insert into pagamento_ (id_Pagamento, Valor, Metodo, Data_Pagamento, Status_Pagamento)
values
(1, 0, 'Pix', '2025-01-11', 'Pendente');

-- Inválido - Marcação de Pago sem valor
update pagamento_
set Status_Pagamento = 'Pago' -- Sem o valor
where id_Pagamento = 1;

-- Válido -- Definido valor antes de marcar como Pago
update pagamento_
set Valor = 1000.00, Status_Pagamento = 'Pago' -- Com o valor
where id_Pagamento = 1;

select id_Pagamento, Valor, Metodo, Data_Pagamento, Status_Pagamento
from pagamento_