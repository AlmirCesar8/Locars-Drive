/* ============================================================
 Arquivo: 10_queries_basicas.sql
 Autor(es): Fabio Benjamin; Almir Silva; Gabriel Paiva 
 Trabalho: LocarsDrive
 Curso/Turma: Desenvolvimento de Sistemas - 213 Matutino 
 SGBD: MySQL 8.0
 Objetivo: Consultas SQL básicas
 ============================================================ */
 
 -- Consulta 1: Listagem de todos os tipos de usuario 
 select id_Usuario, 
		Nome_Completo, 
        CPF, 
        Usuario__TIPO
        
 from Usuario_ ;
 
 -- Consulta 2: Join entre 2+ tabelas --
 select Usuario_.id_Usuario, 
		Usuario_.Nome_Completo, 
        Usuario_.CPF,
        Usuario_.Usuario__TIPO,
        Cidade.id_Cidade,
        Cidade.Nome_Cidade

from Usuario_

join Cidade on Usuario_.fk_Cidade_id_Cidade = Cidade.id_Cidade;

-- Consulta 3: Where com filtros
-- Listam apenas usuários do tipo 2 (Funcionário)
select id_Usuario, 
		Nome_Completo, 
        CPF, 
        Usuario__TIPO

from Usuario_

where Usuario__TIPO = 4;

-- Consulta 4: Agregações com GROUP BY 

select Usuario__TIPO,
	   count(*) as Quantidade_Usuario

from Usuario_

group by Usuario__TIPO;

-- Consulta 5: Ordenação por ORDEM BY

select id_Usuario, 
		Nome_Completo, 
        CPF, 
        Usuario__TIPO

from Usuario_

order by Nome_Completo asc;