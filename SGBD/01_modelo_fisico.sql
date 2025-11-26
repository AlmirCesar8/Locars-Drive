/* ============================================================
    Arquivo: 01_modelo_fisico.sql
    Autor(es): Almir Silva; Fabio Benjamin; Gabriel Paiva
    Trabalho: LocarsDrive
    Curso/Turma: Desenvolvimento de Sistemas - 213 Matutino
    SGBD: MySQL Versão: 8.0
    Objetivo: Criação e povoamento do modelo físico (DDL + DML)
    Execução esperada: rodar em BD vazio
    ============================================================ */

-- REMOVENDO BD ANTERIOR PARA GARANTIR EXECUÇÃO LIMPA
DROP DATABASE IF EXISTS LocarsDrives;
CREATE DATABASE LocarsDrives;
USE LocarsDrives;

-- =============================================================
-- DDL - DEFINIÇÃO DA ESTRUTURA
-- =============================================================

CREATE TABLE Adicionais (
    Nome_Adicionais varchar(255) NOT NULL UNIQUE,
    id_Adicionais int PRIMARY KEY NOT NULL auto_increment,
    Descricao text,
    Disponibilidade enum('disponivel', 'indisponivel') NOT NULL
);

CREATE TABLE Agencia (
    id_Agencia INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    Nome_Agencia VARCHAR(255) NOT NULL,
    Num_Agencia INT NOT NULL UNIQUE
);

CREATE TABLE Categoria (
    Tipos_Categorias varchar(255) NOT NULL UNIQUE,
    id_Categoria int PRIMARY KEY NOT NULL auto_increment
);

CREATE TABLE Cidade (
    Num_Casa int NOT NULL, -- Removido UNIQUE (várias pessoas/agências podem ter o mesmo número em casas diferentes)
    Bairro varchar(255) NOT NULL,
    id_Cidade int PRIMARY KEY NOT NULL auto_increment,
    CEP char(8) NOT NULL UNIQUE,
    Nome_CIdade varchar(255) NOT NULL UNIQUE,
    Complemento varchar(50)
);

-- Tabela Estado: Removida a FK para Cidade (fk_Cidade_id_Cidade) - Relação Invertida
CREATE TABLE Estado (
    id_Estado int PRIMARY KEY NOT NULL auto_increment,
    Nome_Estado varchar(255) NOT NULL UNIQUE,
    Regiao varchar(255) NOT NULL
);

CREATE TABLE Funcao (
    id_Funcao int PRIMARY KEY NOT NULL auto_increment,
    Descricao text NOT NULL,
    Nome_Funcao varchar(255) NOT NULL UNIQUE -- Corrigido: Removido o underscore (Nome_Funcao_)
);

CREATE TABLE historico_km (
    id_Km INT PRIMARY KEY auto_increment,
    Km_Registrado decimal(10,2) NOT NULL,
    Data_Registro date NOT NULL
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
    Valor decimal(10,2) NOT NULL,
    Data_Multa datetime NOT NULL
);

CREATE TABLE Pagamento_ (
    id_Pagamento int auto_increment PRIMARY KEY,
    Valor decimal(10,2) NOT NULL,
    Data_Pagamento date NOT NULL,
    Metodo varchar(50) NOT NULL,
    Status_Pagamento enum('Pago', 'Pendente') NOT NULL
);

-- Tabela Pais: Removida a FK para Estado (fk_Estado_id_Estado) - Relação Invertida
CREATE TABLE Pais (
    id_Pais int PRIMARY KEY NOT NULL auto_increment,
    Sigla_ char(3) NOT NULL UNIQUE,
    Nome_Pais varchar(255) NOT NULL UNIQUE
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

/* =============================
    TABELA Usuario_ ATUALIZADA
    ============================= */
CREATE TABLE Usuario_ (
    Email VARBINARY(255) NOT NULL UNIQUE,
    Nome_Completo varchar(255),
    Senha varchar(255) NOT NULL,
    id_Usuario int NOT NULL auto_increment,
    Data_Nasc date NOT NULL,
    CPF char(11) NOT NULL UNIQUE,

    -- Campos opcionais
    id_Cliente int NULL,
    CNH char(11) UNIQUE,
    Cargo varchar(255),
    id_Funcionario int NULL,
    id_Admin int NULL,
    Usuario__TIPO INT NULL,

    Salario DECIMAL(10,2) DEFAULT 0.00, -- Corrigido: Permitido NULL ou Default
    Pontuacao_Reputacao FLOAT DEFAULT 5.0,
    fk_Funcao_id_Funcao int,
    fk_Cidade_id_Cidade int,
    data_criacao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (id_Usuario)
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

-- =================================================-----
-- NOVAS TABELAS PARA O RMS E CONTROLE DE RISCO/QUALIDADE
-- =================================================-----

-- Tabela `aluguel` (RMS Central)
CREATE TABLE IF NOT EXISTS aluguel (
    id_aluguel INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    fk_usuario_id INT NOT NULL,
    fk_veiculo_id INT NOT NULL,
    
    data_retirada DATETIME NOT NULL,
    data_devolucao_prevista DATETIME NOT NULL,
    data_devolucao_real DATETIME NULL,
    
    status VARCHAR(50) NOT NULL DEFAULT 'Reservado',
    valor_diaria DECIMAL(10, 2) NOT NULL,
    valor_total_previsto DECIMAL(10, 2) NOT NULL,
    valor_extra DECIMAL(10, 2) DEFAULT 0.00,
    
    -- Chaves Estrangeiras
    FOREIGN KEY (fk_usuario_id) REFERENCES Usuario_(id_usuario),
    FOREIGN KEY (fk_veiculo_id) REFERENCES Veiculo(id_Veiculo)
);

-- Tabela `vistoria` (Check-in/Check-out)
CREATE TABLE IF NOT EXISTS vistoria (
    id_vistoria INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    fk_aluguel_id INT NOT NULL,
    
    tipo VARCHAR(10) NOT NULL,
    nivel_combustivel DECIMAL(3, 2) NOT NULL,
    quilometragem INT NOT NULL,
    avarias_json TEXT NULL,
    data_vistoria DATETIME NOT NULL,
    
    FOREIGN KEY (fk_aluguel_id) REFERENCES aluguel(id_aluguel)
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

-- Tabela `notificacao` (Comunicação)
CREATE TABLE IF NOT EXISTS notificacao (
    id_notificacao INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    fk_usuario_id INT NOT NULL,
    fk_aluguel_id INT NULL,
    
    tipo VARCHAR(50) NOT NULL,
    mensagem TEXT NOT NULL,
    data_envio DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    lida BOOLEAN DEFAULT FALSE,
    
    FOREIGN KEY (fk_usuario_id) REFERENCES Usuario_(id_usuario),
    FOREIGN KEY (fk_aluguel_id) REFERENCES aluguel(id_aluguel)
);

-- Tabela `avaliacao_servico` (Reputação)
CREATE TABLE IF NOT EXISTS avaliacao_servico (
    id_avaliacao INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    fk_aluguel_id INT NOT NULL UNIQUE,
    
    nota INT NOT NULL,
    comentarios TEXT NULL,
    data_avaliacao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    avaliacao_cliente INT NULL,
    
    FOREIGN KEY (fk_aluguel_id) REFERENCES aluguel(id_aluguel)
);


-- ALTER TABLES --

ALTER TABLE Agencia
ADD COLUMN Id_Cidade INT NOT NULL;

ALTER TABLE Agencia ADD CONSTRAINT FK_Agencia__2
FOREIGN KEY (Id_Cidade)
    REFERENCES Cidade (id_Cidade)
    ON DELETE RESTRICT;

ALTER TABLE Historico_Km
ADD COLUMN id_Veiculo INT NOT NULL;

ALTER TABLE Historico_Km ADD CONSTRAINT FK_HistoricoKm_Veiculo
    FOREIGN KEY (id_Veiculo) 
    REFERENCES Veiculo(id_Veiculo)
    ON DELETE RESTRICT;

ALTER TABLE Usuario_ ADD CONSTRAINT FK_Usuario__2
    FOREIGN KEY (fk_Funcao_id_Funcao)
    REFERENCES Funcao (id_Funcao)
    ON DELETE RESTRICT;

ALTER TABLE Usuario_ ADD CONSTRAINT FK_Usuario__3
    FOREIGN KEY (fk_Cidade_id_Cidade)
    REFERENCES Cidade (id_Cidade)
    ON DELETE RESTRICT;
    
ALTER TABLE Usuario_
ADD COLUMN tipo_perfil VARCHAR(50);

ALTER TABLE usuario_
ADD COLUMN notif_interesse TINYINT(1) DEFAULT 0;

ALTER TABLE usuario_
ADD COLUMN notif_vencimento TINYINT(1) DEFAULT 0;


ALTER TABLE usuario_
ADD COLUMN notif_promos TINYINT(1) DEFAULT 0;

ALTER TABLE veiculo
    ADD COLUMN fk_Marca_id_Marca INT NULL,
    ADD COLUMN fk_Modelo_id_Modelo INT NULL,
    ADD CONSTRAINT fk_veiculo_marca
        FOREIGN KEY (fk_Marca_id_Marca)
        REFERENCES Marca_Veiculo(id_Marca);

ALTER TABLE veiculo
    ADD CONSTRAINT fk_veiculo_modelo
        FOREIGN KEY (fk_Modelo_id_Modelo)
        REFERENCES Modelo(id_Modelo);


ALTER TABLE Cidade
ADD COLUMN fk_Estado_id_Estado INT NOT NULL;

ALTER TABLE Cidade ADD CONSTRAINT FK_Cidade_Estado
    FOREIGN KEY (fk_Estado_id_Estado)
    REFERENCES Estado(id_Estado)
    ON DELETE RESTRICT;
    
ALTER TABLE Estado
ADD COLUMN fk_Pais_id_Pais INT NOT NULL;

ALTER TABLE Estado ADD CONSTRAINT FK_Estado_Pais
    FOREIGN KEY (fk_Pais_id_Pais)
    REFERENCES Pais(id_Pais)
    ON DELETE RESTRICT;
    
ALTER TABLE Locacao_Seguro_ ADD CONSTRAINT FK_Locacao_Seguro__2
    FOREIGN KEY (fk_Pagamento__id_Pagamento)
    REFERENCES Pagamento_ (id_Pagamento)
    ON DELETE RESTRICT;
    
ALTER TABLE locacao_seguro_ 
MODIFY COLUMN Data_Prevista_Devolucao DATE DEFAULT NULL;
-- ============================================================


-- Índices essenciais (Ajustados) --

-- AGENCIA --
create index uniy_agencia on Agencia (Nome_Agencia);

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
create index uniy_nome_funcao on Funcao (Nome_Funcao); -- Corrigido: Nome_Funcao

-- CIDADE --
create index uniy_nome_cidade on Cidade (Nome_CIdade); 
create index uniy_bairro on Cidade (Bairro);
create index uniy_fk_estado on Cidade (fk_Estado_id_Estado); -- Novo índice

-- ESTADO --
create index uniy_regiao on Estado (Regiao);
create index uniy_fk_pais on Estado (fk_Pais_id_Pais); -- Novo índice

-- PAIS --
create index uniy_sigla on Pais (Sigla_);

-- HISTORICO KM -- 
create index uniy_data_registo on Historico_Km (Data_Registro);

-- PERMISSÃO --
create index uniy_acoes on Permissao (Acoes(255)); -- Corrigido: Tamanho do prefixo para BLOB
create index uniy_recursos on Permissao (Recursos_(255)); -- Corrigido: Tamanho do prefixo para BLOB

-- NOVOS ÍNDICES PARA RMS
create index idx_aluguel_usuario on aluguel (fk_usuario_id);
create index idx_aluguel_veiculo on aluguel (fk_veiculo_id);
create index idx_vistoria_aluguel on vistoria (fk_aluguel_id);
create index idx_notificacao_usuario on notificacao (fk_usuario_id);

--  LOCADORA --
create index uniy_agencia_retirada on Locacao_Seguro_ (Agencia_Retirada);
create index uniy_data_inicio on Locacao_Seguro_ (Data_Inicio);
create index uniy_data_fim on Locacao_Seguro_ (Data_Fim);
create index uniy_fk_pagamento on Locacao_Seguro_ (fk_Pagamento__id_Pagamento);

-- ============================================================
