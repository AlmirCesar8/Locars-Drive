/* ============================================================
 Arquivo: 11_queries_relatorios.sql
 Autor(es): Fabio Benjamin; Almir Silva; Gabriel Paiva
 Trabalho: LocarsDrive
 Curso/Turma: Desenvolvimento de Sistemas - 213 Matutino 
 SGBD: MySQL 8.0
 Objetivo: Relatórios do sistema e consultas analíticas
 ============================================================ */

-- Relatorio 1: Quantidade de usuários por tipo

-- Problema que responde:
	-- Relatorio feito para mostrar a quantidade existente por cada tipo de usuário
    -- (Cliente, Funcionario e Administrador).

-- Por que a escolha desta abordagem:
	-- Para agrupar os usuários utilizando as funções COUNT(*) e GROUP BY  
    -- Permitindo identificar o tipo do usuário de forma mais clama e eficiente
    
select Usuario__TIPO,
	   count(*) as Quantidade_Usuario

from Usuario_

group by Usuario__TIPO;


-- Relatorio 2: Usuário e suas cidades
-- Problema que responde:
	-- Saber qual cidade cada usuário está vinculada.

-- Por que a escolha desta abordagem:
	-- Para relacionar as informações usuário e localidade
    -- Utilia do JOIN entre as tabelas "Usuario_" e "Cidade"

select U.Nome_Completo,
	   U.CPF,
       C.Nome_Cidade
       
from Usuario_ as U

join Cidade as C on U.fk_Cidade_id_Cidade = C.id_Cidade
order by C.Nome_Cidade asc;


-- Relatorio 3: Usuário por tipo e as idades médias
-- Problema que responde:
	-- Faixeitaria média que cada tipo de usuário possui.
    
-- Por que a escolha desta abordagem:
	-- Utiliza a função AVG para saber a diferença entre a data atual 
    -- e a Data_Nasc dos usuários, fazendo agrupamento por tipo

select Usuario__TIPO, 
	   round( avg(timestampdiff(year, Data_Nasc, curdate())), 1) as Media_Idade

from Usuario_

group by Usuario__TIPO;


-- Relatorio 4: Funcionário com salário acima da média  
-- Problema que responde:
	-- Fazer a identificação dos funcionários que possuem salário maior que a média geral
    
-- Por que a escolha desta abordagem:
	-- Para saber quem possui o salário maior que a média geral utilizando uma subquery
    -- Filtrando apenas os funcionários que ultrapassam este valor.

select Nome_Completo,
	   Cargo, 
       Salario 

from Usuario_
where Cargo = 'Funcionario'
	and Salario > (select avg(Salario) from Usuario_ where Cargo = 'Funcionario')
order by Salario desc;


-- Relatorio 5: Cidades com maior número de usuários cadastrados
-- Problema que responde:
	-- Mostrar as cidades com o maior número de usuários registrados no sistema
    
-- Por que a escolha desta abordagem:
	-- Para gerar um ranking de cidades e permitindo também a consolidação de dados
    -- Utiliza-se de GROUP BY e COUNT para fazer a junção de "Usuario_" e "Cidade"
    
select c.Nome_Cidade, 
	   count(u.id_Usuario) as Quantidade_Usuario
from Usuario_ as u
join Cidade as c on u.fk_Cidade_id_Cidade = c.id_Cidade
group by c.Nome_Cidade
order by Quantidade_Usuario desc;