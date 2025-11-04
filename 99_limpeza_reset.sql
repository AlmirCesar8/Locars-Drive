/* ============================================================
 Arquivo: 99_limpeza_reset.sql
 Autor(es): Fabio Benjamin; Almir Silva; Gabriel Paiva
 Trabalho: LocarsDrive
 Curso/Turma: Desenvolvimento de Sistemas - 213 Matutino 
 SGBD: MySQL 8.0
 Objetivo: Resetar todas as tabelas para novo ciclo de testes
 ============================================================ */
 
-- Observações
	-- Rodando os comandos o banco ficará completamente vazio não possuindo tabelas e dados
	-- Você precisará executar novamente o script de criação das tabelas (01_modelo_fisico) para voltar o banco
	-- Recomendado fazer backup antes de executar.
    
-- Deleta o banco de dados por completo 
drop database locarsdrives;

-- Funcionalidade:
	-- Apaga o banco de dados por completo, removendo todos os dados em apenas um comando.


-- Deleta registros de tabelas dependentes 

DELETE FROM Historico_Km;
DELETE FROM locacao_seguro_;
DELETE FROM Pagamento_;
DELETE FROM Multa;
DELETE FROM Usuario_;
DELETE FROM Veiculo;
DELETE FROM Categoria;
DELETE FROM Funcao;
DELETE FROM Modelo;
DELETE FROM Marca_Veiculo;
DELETE FROM Tipo_Veiculo;
DELETE FROM Cidade;
DELETE FROM Estado;
DELETE FROM Pais;
DELETE FROM Adicionais;
DELETE FROM Permissao;
DELETE FROM Agencia;

-- Funcionalidade:
	-- Remove todos os dados manualmente (opcional se for usar DROP)


--  Apaga dados e reseta AUTO_INCREMENT

TRUNCATE TABLE Historico_Km;
TRUNCATE TABLE locacao_seguro_;
TRUNCATE TABLE Pagamento_;
TRUNCATE TABLE Multa;
TRUNCATE TABLE Usuario_;
TRUNCATE TABLE Veiculo;
TRUNCATE TABLE Categoria;
TRUNCATE TABLE Funcao;
TRUNCATE TABLE Modelo;
TRUNCATE TABLE Marca_Veiculo;
TRUNCATE TABLE Tipo_Veiculo;
TRUNCATE TABLE Cidade;
TRUNCATE TABLE Estado;
TRUNCATE TABLE Pais;
TRUNCATE TABLE Adicionais;
TRUNCATE TABLE Permissao;
TRUNCATE TABLE Agencia;

-- Funcionalidade:
	-- Apaga todos os registros e reinicia IDs automáticos


-- Drop de todas as tabelas

DROP TABLE IF EXISTS Historico_Km;
DROP TABLE IF EXISTS locacao_seguro_;
DROP TABLE IF EXISTS Pagamento_;
DROP TABLE IF EXISTS Multa;
DROP TABLE IF EXISTS Usuario_;
DROP TABLE IF EXISTS Veiculo;
DROP TABLE IF EXISTS Categoria;
DROP TABLE IF EXISTS Funcao;
DROP TABLE IF EXISTS Modelo;
DROP TABLE IF EXISTS Marca_Veiculo;
DROP TABLE IF EXISTS Tipo_Veiculo;
DROP TABLE IF EXISTS Cidade;
DROP TABLE IF EXISTS Estado;
DROP TABLE IF EXISTS Pais;
DROP TABLE IF EXISTS Adicionais;
DROP TABLE IF EXISTS Permissao;
DROP TABLE IF EXISTS Agencia;

-- Funcionalidade:
	-- Remove completamente todas as tabelas do banco