/* ============================================================
 Arquivo: 90_verificacoes_pos_execucao.sql
 Autor(es): Benjamin, Fabio; Silva, Almir; Paiva, Gabriel
 Trabalho: LocarsDrive
 Curso/Turma: Desenvolvimento de Sistemas - 213 Matutino
 SGBD: MySQL Versão: 8.0
 Objetivo: Validações após execução completa do projeto
 Execução esperada: etapa final, após todos os demais scripts
 ============================================================ */
 
-- Contagem de registros por tabela 
	-- Utiliza a função "COUNT(*)" para contar

select count(*) as Total_Locacoes from Locacao_Seguro_;
	-- Total de locações registradas no sistema 
    
select count(*) as Total_Veiculos from Veiculo;
	-- Total de veículos registrados no sistemas
    
select count(*) as Total_Historico_Km from Historico_Km;
	-- Total de km inseridos no registro do sistemas
    
select count(*) as Total_Multas from Multa;
	-- Total de multas aplicadas foram registradas no sistemas
    
select count(*) as Total_Agencia from Agencia;
	-- Total de agências registradas no sistemas
    
select count(*) as Total_Usuarios from Usuario_;
	-- Total de usuários registrados no sistemas
    
select count(*) as Total_Pagamentos from Pagamento_;
	-- Total de pagamento efetuados registrados no sistemas
    
   select count(*) as Total_Categorias from Categoria;
	-- Total de categorias existentes no sistemas 
    
select count(*) as Total_Cidade from Cidade;
	-- Total de cidades registradas no sistemas
    
    
-- Valores máximos e mínimos de colunas cruciais 
	-- Utiliza as funções "MAX" e "MIN" que pega os valores maximos e mínimos

-- Kilometragem --
select max(Km_Rodado) as Km_Maximo,
	   min(Km_Rodado) as Km_Minimo 
       from Veiculo;

	-- Faz a verificação dos km mais altos e dos mais baixos dos veículos

-- Valor Pagamentos --
select max(Valor) as Pagamento_Max,
	   min(Valor) as Pagamento_Min
       from Pagamento_;

	-- Valor dos pagamentos registrados

-- Valor Multa --
select max(Valor) as Multa_Max,
	   min(Valor) as Multa_Min
       from Multa;
       
	-- Valores de multas aplicadas nas locações -- 
    
    
-- Verificação de integridade 
	-- Utiliza as funções "JOIN" para combinar dados
    -- "GROUP BY" para agrupar os resultados
    -- "HAVING" para filtrar os grupos criados 
    -- "COUNT(*)" para contar os registros de cada grupo
    
-- Verifica locações com data de devolução anterior à data de início 
select id_Locacao, Data_Inicio, Data_Devolucao
from Locacao_Seguro_
where Data_Devolucao < Data_Inicio; 

	-- Garante que não haja devoluções antes do início
    
-- Verifica os veículos que estão locados, mas com marcação de disponíveis 
	-- l = locadora
	-- v = veiculo
    
select v.id_Veiculo, 
    v.Placa, 
    v.StatusVeiculo, 
    l.id_Locacao
from Veiculo v
join Locacao_Seguro_ l on v.id_Veiculo = l.id_Veiculo
where v.StatusVeiculo = 'Disponível' and l.Data_Devolucao is null;

    
    -- Identifica veículos que estão com locação ativa
    
-- Usuário com CPF duplicado
select CPF, count(*) as Duplicacao_CPF
from Usuario_
group by CPF
having count(*) > 1;

	-- Evita as duplicações de CPF no banco de dados

-- Histórico de Km sem veículo válido
		-- v = Veiculo
        -- h = Historico_Km
select h.id_Km, h.id_Veiculo
from Historico_Km h
left join Veiculo v on h.id_Veiculo = v.id_Veiculo
where v.id_Veiculo is null;

	-- Históricos de km vinculado a veículo existente
