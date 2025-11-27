/* ============================================================
    Arquivo: 01_modelo_fisico.sql
    Autor(es): Almir Silva; Fabio Benjamin; Gabriel Paiva
    Trabalho: LocarsDrive
    Curso/Turma: Desenvolvimento de Sistemas - 213 Matutino
    SGBD: MySQL Versão: 8.0
    Objetivo: Criação e povoamento do modelo físico (DDL + DML)
    Execução esperada: rodar em BD vazio
============================================================ */

DROP DATABASE IF EXISTS LocarsDrives;
CREATE DATABASE LocarsDrives;
USE LocarsDrives;

-- =============================================================
-- DDL - DEFINIÇÃO DA ESTRUTURA (TABELAS BASE)
-- =============================================================

CREATE TABLE Adicionais (
    id_Adicionais INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    Nome_Adicionais VARCHAR(255) NOT NULL UNIQUE,
    Descricao TEXT,
    Disponibilidade ENUM('disponivel', 'indisponivel') NOT NULL
);

CREATE TABLE Agencia (
    id_Agencia INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    Nome_Agencia VARCHAR(255) NOT NULL,
    Num_Agencia INT NOT NULL UNIQUE
);

CREATE TABLE Categoria (
    id_Categoria INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    Tipos_Categorias VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE Cidade (
    id_Cidade INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    Nome_Cidade VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE Estado (
    id_Estado INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    Nome_Estado VARCHAR(255) NOT NULL UNIQUE,
    Regiao VARCHAR(255) NOT NULL
);

CREATE TABLE Pais (
    id_Pais INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    Sigla_ CHAR(3) NOT NULL UNIQUE,
    Nome_Pais VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE Endereco (
    id_Endereco INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    CEP CHAR(8) NOT NULL,
    Logradouro VARCHAR(255) NOT NULL,
    Num_Casa INT NOT NULL,
    Bairro VARCHAR(255) NOT NULL,
    Complemento VARCHAR(50),
    fk_Cidade_id_Cidade INT NOT NULL,
    FOREIGN KEY (fk_Cidade_id_Cidade) REFERENCES Cidade(id_Cidade)
);

CREATE TABLE Funcao (
    id_Funcao INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    Descricao TEXT NOT NULL,
    Nome_Funcao VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE historico_km (
    id_Km INT PRIMARY KEY AUTO_INCREMENT,
    Km_Registrado DECIMAL(10,2) NOT NULL,
    Data_Registro DATE NOT NULL
);

CREATE TABLE Marca_Veiculo (
    id_Marca INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    Nome_Marca VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE Modelo (
    id_Modelo INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    Nome_Modelo VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE Multa (
    id_Multa INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    Motivo_Multa TEXT NOT NULL,
    Valor DECIMAL(10,2) NOT NULL,
    Data_Multa DATETIME NOT NULL
);

CREATE TABLE Pagamento_ (
    id_Pagamento INT AUTO_INCREMENT PRIMARY KEY,
    Valor DECIMAL(10,2) NOT NULL,
    Data_Pagamento DATE NOT NULL,
    Metodo VARCHAR(50) NOT NULL,
    Status_Pagamento ENUM('Pago', 'Pendente') NOT NULL
);

CREATE TABLE Permissao (
    id_Permissoes INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    Acoes BLOB NOT NULL,
    Recursos_ BLOB NOT NULL
);

-- ================================================
-- *** CORREÇÃO AQUI ***
-- Modelo agora compatível com o Flask:
-- id_Tipo em vez de id_Tipo_Veiculo
-- ================================================
CREATE TABLE Tipo_Veiculo (
    id_Tipo INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    Nome_Tipo VARCHAR(200) NOT NULL UNIQUE
);

CREATE TABLE Usuario_ (
    id_Usuario INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Email VARBINARY(255) NOT NULL UNIQUE,
    Nome_Completo VARCHAR(255),
    Senha VARCHAR(255) NOT NULL,
    Data_Nasc DATE NOT NULL,
    CPF CHAR(11) NOT NULL UNIQUE,
    id_Cliente INT,
    CNH CHAR(11) UNIQUE,
    Cargo VARCHAR(255),
    id_Funcionario INT,
    id_Admin INT,
    Usuario__TIPO INT,
    Salario DECIMAL(10,2) DEFAULT 0.00,
    Pontuacao_Reputacao FLOAT DEFAULT 5.0,
    fk_Funcao_id_Funcao INT,
    data_criacao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fk_endereco_id INT,
    tipo_perfil VARCHAR(50),
    notif_interesse TINYINT(1) DEFAULT 0,
    notif_vencimento TINYINT(1) DEFAULT 0,
    notif_promos TINYINT(1) DEFAULT 0,
    fk_funcao_id INT,
    fk_cidade_id_cidade INT,
    FOREIGN KEY (fk_Funcao_id_Funcao) REFERENCES Funcao(id_Funcao),
    FOREIGN KEY (fk_endereco_id) REFERENCES Endereco(id_Endereco)
);

-- =============================================
-- FK CORRIGIDA para usar id_Tipo
-- =============================================
CREATE TABLE Veiculo (
    id_Veiculo INT PRIMARY KEY AUTO_INCREMENT,
    Frota INT NOT NULL,
    Placa CHAR(7) UNIQUE,
    Km_Rodado DECIMAL(10,2) NOT NULL,
    StatusVeiculo ENUM('Disponível','Indisponível') NOT NULL,
    fk_Categoria_id_Categoria INT NOT NULL,
    fk_Tipo_Veiculo_id_Tipo INT,
    fk_Marca_id_Marca INT,
    fk_Modelo_id_Modelo INT,
    FOREIGN KEY (fk_Categoria_id_Categoria) REFERENCES Categoria(id_Categoria),
    FOREIGN KEY (fk_Tipo_Veiculo_id_Tipo) REFERENCES Tipo_Veiculo(id_Tipo),
    FOREIGN KEY (fk_Marca_id_Marca) REFERENCES Marca_Veiculo(id_Marca),
    FOREIGN KEY (fk_Modelo_id_Modelo) REFERENCES Modelo(id_Modelo)
);

ALTER TABLE historico_km
ADD COLUMN id_Veiculo INT NOT NULL,
ADD CONSTRAINT FK_HistoricoKm_Veiculo
FOREIGN KEY (id_Veiculo) REFERENCES Veiculo(id_Veiculo);

CREATE TABLE aluguel (
    id_aluguel INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    fk_usuario_id INT NOT NULL,
    fk_veiculo_id INT NOT NULL,
    data_retirada DATETIME NOT NULL,
    data_devolucao_prevista DATETIME NOT NULL,
    data_devolucao_real DATETIME,
    status VARCHAR(50) NOT NULL DEFAULT 'Reservado',
    valor_diaria DECIMAL(10, 2) NOT NULL,
    valor_total_previsto DECIMAL(10, 2) NOT NULL,
    valor_extra DECIMAL(10, 2) DEFAULT 0.00,
    FOREIGN KEY (fk_usuario_id) REFERENCES Usuario_(id_Usuario),
    FOREIGN KEY (fk_veiculo_id) REFERENCES Veiculo(id_Veiculo)
);

CREATE TABLE vistoria (
    id_vistoria INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    fk_aluguel_id INT NOT NULL,
    tipo VARCHAR(10) NOT NULL,
    nivel_combustivel DECIMAL(3, 2) NOT NULL,
    quilometragem INT NOT NULL,
    avarias_json TEXT,
    data_vistoria DATETIME NOT NULL,
    FOREIGN KEY (fk_aluguel_id) REFERENCES aluguel(id_aluguel)
);

CREATE TABLE locacao_seguro_ (
    id_Locacao INT NOT NULL AUTO_INCREMENT,
    id_Cliente INT NOT NULL,
    id_Veiculo INT NOT NULL,
    Data_Prevista_Devolucao DATE,
    Data_Devolucao DATE NOT NULL,
    Data_Fim DATE NOT NULL,
    Data_Inicio DATE NOT NULL,
    Valor_Multa DECIMAL(10,2) DEFAULT 0.00,
    Agencia_Retirada VARCHAR(255),
    id_Seguro INT NOT NULL,
    Valor DECIMAL(10,2) NOT NULL,
    fk_Pagamento__id_Pagamento INT,
    PRIMARY KEY (id_Locacao, id_Seguro),
    FOREIGN KEY (fk_Pagamento__id_Pagamento) REFERENCES Pagamento_(id_Pagamento)
);

CREATE TABLE notificacao (
    id_notificacao INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    fk_usuario_id INT NOT NULL,
    fk_aluguel_id INT,
    tipo VARCHAR(50) NOT NULL,
    mensagem TEXT NOT NULL,
    data_envio DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    lida BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (fk_usuario_id) REFERENCES Usuario_(id_Usuario),
    FOREIGN KEY (fk_aluguel_id) REFERENCES aluguel(id_aluguel)
);

CREATE TABLE avaliacao_servico (
    id_avaliacao INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    fk_aluguel_id INT NOT NULL UNIQUE,
    nota INT NOT NULL,
    comentarios TEXT,
    data_avaliacao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    avaliacao_cliente INT,
    FOREIGN KEY (fk_aluguel_id) REFERENCES aluguel(id_aluguel)
);

-- ============================================================
-- RELACIONAMENTOS PAIS > ESTADO > CIDADE
-- ============================================================

ALTER TABLE Estado
ADD COLUMN fk_Pais_id_Pais INT NOT NULL,
ADD CONSTRAINT FK_Estado_Pais
FOREIGN KEY (fk_Pais_id_Pais) REFERENCES Pais(id_Pais);

ALTER TABLE Cidade
ADD COLUMN fk_Estado_id_Estado INT NOT NULL,
ADD CONSTRAINT FK_Cidade_Estado
FOREIGN KEY (fk_Estado_id_Estado) REFERENCES Estado(id_Estado);

ALTER TABLE Agencia
ADD COLUMN fk_Endereco_id_Endereco INT NOT NULL,
ADD CONSTRAINT FK_Agencia_Endereco
FOREIGN KEY (fk_Endereco_id_Endereco) REFERENCES Endereco(id_Endereco);

ALTER TABLE veiculo
ADD COLUMN imagem_principal VARCHAR(255) NULL;


-- ============================================================
-- ÍNDICES ESSENCIAIS
-- ============================================================

CREATE INDEX uniy_agencia ON Agencia (Nome_Agencia);
CREATE INDEX uniy_nome_usuario ON Usuario_ (Nome_Completo);
CREATE INDEX uniy_cargo_usuario ON Usuario_ (Cargo);
CREATE INDEX uniy_fk_funcao ON Usuario_ (fk_Funcao_id_Funcao);
CREATE INDEX idx_fk_endereco ON Usuario_ (fk_endereco_id);
CREATE INDEX uniy_nome_modelo ON Modelo (Nome_Modelo);
CREATE INDEX uniy_nome_tipo ON Tipo_Veiculo (Nome_Tipo);
CREATE INDEX uniy_nome_marca ON Marca_Veiculo (Nome_Marca);
CREATE INDEX uniy_statusVeiculo ON Veiculo (StatusVeiculo);
CREATE INDEX uniy_frota ON Veiculo (Frota);
CREATE INDEX uniy_km_rodado ON Veiculo (Km_Rodado);
CREATE INDEX uniy_data_multa ON Multa (Data_Multa);
CREATE INDEX uniy_valor_multa ON Multa (Valor);
CREATE INDEX uniy_nome_funcao ON Funcao (Nome_Funcao);
CREATE INDEX uniy_nome_cidade ON Cidade (Nome_Cidade);
CREATE INDEX uniy_fk_estado ON Cidade (fk_Estado_id_Estado);
CREATE INDEX uniy_cep ON Endereco (CEP);
CREATE INDEX uniy_bairro ON Endereco (Bairro);
CREATE INDEX uniy_fk_cidade ON Endereco (fk_Cidade_id_Cidade);
CREATE INDEX uniy_regiao ON Estado (Regiao);
CREATE INDEX uniy_fk_pais ON Estado (fk_Pais_id_Pais);
CREATE INDEX uniy_sigla ON Pais (Sigla_);
CREATE INDEX uniy_data_registo ON historico_km (Data_Registro);
CREATE INDEX uniy_acoes ON Permissao (Acoes(255));
CREATE INDEX uniy_recursos ON Permissao (Recursos_(255));
CREATE INDEX idx_aluguel_usuario ON aluguel (fk_usuario_id);
CREATE INDEX idx_aluguel_veiculo ON aluguel (fk_veiculo_id);
CREATE INDEX idx_vistoria_aluguel ON vistoria (fk_aluguel_id);
CREATE INDEX idx_notificacao_usuario ON notificacao (fk_usuario_id);
CREATE INDEX uniy_agencia_retirada ON locacao_seguro_ (Agencia_Retirada);
CREATE INDEX uniy_data_inicio ON locacao_seguro_ (Data_Inicio);
CREATE INDEX uniy_data_fim ON locacao_seguro_ (Data_Fim);
CREATE INDEX uniy_fk_pagamento ON locacao_seguro_ (fk_Pagamento__id_Pagamento);
