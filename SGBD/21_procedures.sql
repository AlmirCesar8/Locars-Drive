/* ============================================================
 Arquivo: 21_procedures.sql
 Autor(es): Fabio Benjamin; Almir Silva; Gabriel Paiva 
 Trabalho: LocarsDrive
 Curso/Turma: Desenvolvimento de Sistemas - 213 Matutino 
 SGBD: MySQL 8.0
 Objetivo: Procedures e funções úteis para o sistema
 ============================================================ */
 
 -- P = Parametros
 -- V = Variaveis
 
 -- Procedure 1: Aplicação de multa por atraso de devolução 
 -- Motivação: Calcular a multa de atraso automaticamente e atualizar o status da locação  
 -- Parâmetros:
	-- P_id_Locacao = Identificar o ID da Locacao
	-- P_Data_Devolucao = Data posta para a devolução do veiculo
    
 delimiter $$
 
create procedure mul_Aplicacao_Multa(
    in P_id_Locacao int,
    in P_Data_Devolucao date
)
begin
    declare V_Data_Prevista date;
    declare V_Dias_Atraso int;

    select Data_Prevista_Devolucao into V_Data_Prevista
    from Locacao_Seguro_
    where id_Locacao = P_id_Locacao;

    -- Calculo de atraso
    set V_Dias_Atraso = datediff(P_Data_Devolucao, V_Data_Prevista);

    -- Atualizar multa caso tenha atraso 
    if V_Dias_Atraso > 0 then
        update Locacao_Seguro_
        set Valor_Multa = V_Dias_Atraso * 20  
        where id_Locacao = P_id_Locacao;
    end if;

end;

delimiter ;

-- Chamada da procedure para calcular multa
call mul_Aplicacao_Multa(101, '2025-11-06'); 
call mul_Aplicacao_Multa(102, '2025-10-30');  
call mul_Aplicacao_Multa(103, '2025-11-04'); 

select id_Locacao, Data_Prevista_Devolucao, Data_Devolucao, Valor_Multa
from Locacao_Seguro_;


-- Procedure 2: Contagem de kilometragem após cada uso
-- Motivação: Para manter controle de uso dos veículos 
-- Parâmetros: 
	-- P_id_Veiculo = Identificar o ID do Veículo
	-- P_Km_Final = Kilometragem final após o uso do veiculo

delimiter $$

create procedure Contagem_Km (
	in P_id_Veiculo int,
    in P_Km_Final decimal(10,2)
)
begin 
	declare V_Km_Antigo decimal (10,2);
    
    select Km_Rodado into V_Km_Antigo
    from Veiculo
    where id_Veiculo = P_id_Veiculo;
    
    -- Validação para nao ter valor negativo
    if P_Km_Final < V_Km_Antigo then
			signal sqlstate '45000'
            set message_text = "Kilometragem final não pode ser menor que a kilometragem atual do veículo";
		end if;
    
    -- Atualiza os kilometragens que foram usados 
    update Veiculo
    Set Km_Rodado = P_Km_Final
    where id_Veiculo = P_id_Veiculo;
    
    insert into Historico_Km (id_Veiculo, Km_Registrado, Data_Registro)
    values (P_id_Veiculo, (P_Km_Final - V_Km_Antigo), curdate());
    
    -- Km rodado desde do último registro 
    select P_id_Veiculo as Veiculo,
		  (P_Km_Final - V_Km_Antigo) as Km_Usado;
    
end$$ 

delimiter ;

call Contagem_Km(1, 350);   -- veículo 1001 rodou +350 km
call Contagem_Km(2, 120);   -- veículo 1002 rodou +120 km
call Contagem_Km(3, 480);   -- veículo 1003 rodou +480 km

select id_Veiculo, Placa, Km_Rodado
from Veiculo;

select * from Historico_Km