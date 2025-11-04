/* ============================================================
 Arquivo: 01_modelo_fisico.sql
 Autor(es): Fabio Benjamin; Almir Silva; Gabriel Paiva
 Trabalho: LocarsDrive
 Curso/Turma: Desenvolvimento de Sistemas - 213 Matutino 
 SGBD: MySQL Versão: 8.0
 Objetivo: Criação do modelo físico (DDL)
 Execução esperada: rodar primeiro, em BD vazio
 ============================================================ */

CREATE DATABASE if not exists LocarsDrives;
USE LocarsDrives; 

CREATE TABLE Adicionais (
    Nome_Adicionais varchar(255) NOT NULL UNIQUE,
    id_Adicionais int PRIMARY KEY NOT NULL auto_increment,
    Descricao text,
    Disponibilidade enum('disponivel', 'indisponivel') NOT NULL
);

CREATE TABLE Agencia (
    id_Agencia int PRIMARY KEY NOT NULL auto_increment,
    Nome_Agencia varchar(255) NOT NULL,
    Num_Agencia int NOT NULL UNIQUE
);

CREATE TABLE Categoria (
    Tipos_Categorias varchar(255) NOT NULL UNIQUE,
    id_Categoria int PRIMARY KEY NOT NULL auto_increment
);

CREATE TABLE Cidade (
    Num_Casa int NOT NULL UNIQUE,
    Bairro varchar(255) NOT NULL,
    id_Cidade int PRIMARY KEY NOT NULL auto_increment,
    CEP char(8) NOT NULL UNIQUE,
    Nome_CIdade varchar(255) NOT NULL UNIQUE,
    Complemento varchar(50)
);

CREATE TABLE Estado (
    id_Estado int PRIMARY KEY NOT NULL auto_increment,
    Nome_Estado varchar(255) NOT NULL UNIQUE,
    Regiao varchar(255) NOT NULL,
    fk_Cidade_id_Cidade int
);

CREATE TABLE Funcao (
    id_Funcao int PRIMARY KEY NOT NULL auto_increment,
    Descricao text NOT NULL,
    Nome_Funcao_ varchar(255) NOT NULL UNIQUE
);

CREATE TABLE historico_km (
    id_Km INT PRIMARY KEY auto_increment,
    Km_Registrado decimal(10,2) NOT NULL,
    Data_Registro date NOT NULL
);

CREATE TABLE locacao_seguro_ (
    id_Locacao int NOT NULL auto_increment,
    id_Cliente int NOT NULL,
    id_Veiculo int NOT NULL,
    Data_Prevista_Devolucao date NOT NULL,
    Data_Devolucao date not null,
    Data_Fim date NOT NULL,
    Data_Inicio date NOT NULL,
    Valor_Multa decimal(10,2) DEFAULT 0.00,
    Agencia_Retirada varchar(255),
    id_Seguro int NOT NULL,
    Valor decimal(10,2) NOT NULL,
    fk_Pagamento__id_Pagamento INT,
    PRIMARY KEY (id_Locacao, id_Seguro)
);


CREATE TABLE Marca_Veiculo (
    Nome_Marca varchar(255) NOT NULL UNIQUE,
    id_Marca int PRIMARY KEY NOT NULL auto_increment
);

CREATE TABLE Modelo (
    Nome_Modelo varchar(255) NOT NULL UNIQUE,
    id_Modelo int PRIMARY KEY NOT NULL auto_increment
);

CREATE TABLE Multa (
    id_Multa int PRIMARY KEY NOT NULL auto_increment,
    Motivo_Multa text NOT NULL,
    Valor decimal NOT NULL,
    Data_Multa datetime NOT NULL
);

CREATE TABLE Pagamento_ (
    id_Pagamento int auto_increment PRIMARY KEY,
    Valor decimal(10,2) NOT NULL,
    Data_Pagamento date NOT NULL,
    Metodo varchar(50) NOT NULL,
    Status_Pagamento enum('Pago', 'Pendente') NOT NULL
);

CREATE TABLE Pais (
    id_Pais int PRIMARY KEY NOT NULL auto_increment,
    Sigla_ char(3) NOT NULL UNIQUE,
    Nome_Pais varchar(255) NOT NULL UNIQUE,
    fk_Estado_id_Estado int
);

CREATE TABLE Permissao (
    Acoes blob NOT NULL,
    Recursos_ blob NOT NULL,
    id_Permissoes int PRIMARY KEY NOT NULL auto_increment
);

CREATE TABLE Tipo_Veiculo (
    id_Tipo int PRIMARY KEY NOT NULL auto_increment,
    Nome_Tipo varchar(200) NOT NULL UNIQUE
);

CREATE TABLE Usuario_ (
    Email varchar(255) NOT NULL UNIQUE,
    Nome_Completo varchar(255) ,
    Senha varchar(255) NOT NULL,
    id_Usuario int NOT NULL auto_increment,
    Data_Nasc date NOT NULL,
    CPF char(11) NOT NULL UNIQUE,
    id_Cliente int NOT NULL,
    CNH char(11) NOT NULL UNIQUE,
    Cargo varchar(255) NOT NULL,
    id_Funcionario int NOT NULL,
    id_Admin int NOT NULL,
    Usuario__TIPO INT NOT NULL,
    Salario DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    fk_Funcao_id_Funcao int,
    fk_Cidade_id_Cidade int,
    PRIMARY KEY (id_Usuario, id_Cliente, id_Funcionario, id_Admin)
);

CREATE TABLE Veiculo (
    id_Veiculo int PRIMARY KEY auto_increment,
    Frota int NOT NULL,
    Placa char(7) NOT NULL UNIQUE,
    Km_Rodado decimal(10,2) NOT NULL,
    StatusVeiculo enum('Disponível','Indisponível') NOT NULL,
    fk_Categoria_id_Categoria int NOT NULL,
    FOREIGN KEY (fk_Categoria_id_Categoria) REFERENCES Categoria(id_Categoria)
);


-- ALTER TABLES UTILIZADOS --

ALTER TABLE Historico_Km
ADD COLUMN id_Veiculo INT NOT NULL;

ALTER TABLE Historico_Km ADD CONSTRAINT FK_HistoricoKm_Veiculo
	FOREIGN KEY (id_Veiculo) 
    REFERENCES Veiculo(id_Veiculo)
	ON DELETE RESTRICT;

ALTER TABLE Locacao_Seguro_ ADD CONSTRAINT FK_Locacao_Seguro__2
    FOREIGN KEY (fk_Pagamento__id_Pagamento)
    REFERENCES Pagamento_ (id_Pagamento)
    ON DELETE RESTRICT;
 
ALTER TABLE Usuario_ ADD CONSTRAINT FK_Usuario__2
    FOREIGN KEY (fk_Funcao_id_Funcao)
    REFERENCES Funcao (id_Funcao)
    ON DELETE RESTRICT;

 
ALTER TABLE Usuario_ ADD CONSTRAINT FK_Usuario__3
    FOREIGN KEY (fk_Cidade_id_Cidade)
    REFERENCES Cidade (id_Cidade)
    ON DELETE RESTRICT;
 
ALTER TABLE Estado ADD CONSTRAINT FK_Estado_2
    FOREIGN KEY (fk_Cidade_id_Cidade)
    REFERENCES Cidade (id_Cidade)
    ON DELETE RESTRICT;
 
ALTER TABLE Pais ADD CONSTRAINT FK_Pais_Estado
	FOREIGN KEY (fk_Estado_id_Estado)
	REFERENCES Estado(id_Estado)
	ON DELETE RESTRICT;
    
ALTER TABLE locacao_seguro_ 
MODIFY COLUMN Data_Prevista_Devolucao DATE DEFAULT NULL;


-- Índices essenciais --

-- AGENCIA --
create index uniy_agencia on Agencia (Nome_Agencia);

--  LOCADORA --
create index uniy_agencia_retirada on Locacao_Seguro_ (Agencia_Retirada);
create index uniy_data_inicio on Locacao_Seguro_ (Data_Inicio);
create index uniy_data_fim on Locacao_Seguro_ (Data_Fim);
create index uniy_fk_pagamento on Locacao_Seguro_ (fk_Pagamento__id_Pagamento);

-- USUARIO -- 
create index uniy_nome_usuario on Usuario_ (Nome_Completo);
create index uniy_cargo_usuario on Usuario_ (Cargo);
create index uniy_fk_funcao on Usuario_ (fk_Funcao_id_Funcao);
create index uniy_fk_cidade on Usuario_ (fk_Cidade_id_Cidade);

-- MODELO --
create index uniy_nome_modelo on Modelo (Nome_Modelo);

-- TIPO VEICULO --
create index uniy_nome_tipo on Tipo_Veiculo (Nome_Tipo);

-- MARCA VEICULO --
create index uniy_nome_marca on Marca_Veiculo (Nome_Marca);

-- VEICULO --
create index uniy_statusVeiculo on Veiculo (statusVeiculo); 
create index uniy_frota on Veiculo (Frota);
create index uniy_km_rodado on Veiculo (Km_Rodado);

-- MULTA -- 
create index uniy_data_multa on Multa (Data_Multa);
create index uniy_valor_multa on Multa (Valor);

-- FUNCAO --
create index uniy_nome_funcao on Funcao (Nome_Funcao_);

-- CIDADE --
create index uniy_nome_cidade on Cidade (Nome_CIdade); 
create index uniy_bairro on Cidade (Bairro);

-- ESTADO --
create index uniy_regiao on Estado (Regiao);
create index uniy_fk_cidade on Estado (fk_Cidade_id_Cidade);

-- PAIS --
create index uniy_sigla on Pais (Sigla_);
create index uniy_fk_estado on Pais (fk_Estado_id_Estado);

-- HISTORICO KM -- 
create index uniy_km_registro on Historico_Km (Data_Registro);
create index uniy_data_registo on Historico_Km (Km_Registrado);

-- PERMISSÃO --
create index uniy_acoes on Permissao (Acoes(300)); 
create index uniy_recursos on Permissao (Recursos_(300));