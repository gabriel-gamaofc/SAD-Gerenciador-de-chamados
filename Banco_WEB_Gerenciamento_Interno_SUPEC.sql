create database expresso_conectado;
use expresso_conectado;
create table Chamados_ti_pina(
id integer primary key auto_increment,
chamado_data datetime default current_timestamp,
orgao varchar(50) not null,
Solicitacao varchar(200) not null
);
select * from Chamados_ti_pina;

CREATE TABLE maquinas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    orgao VARCHAR(255),
    ip VARCHAR(15),
    tombamento VARCHAR(50),
    guiche varchar(50)
);

SELECT * FROM chamados_ti;

-- Criação da tabela de chamados_ti
CREATE TABLE chamados_ti (
    id INT AUTO_INCREMENT PRIMARY KEY,
    orgao VARCHAR(255) NOT NULL,
    requerente VARCHAR(255) NOT NULL,
    solicitacao TEXT NOT NULL,
    status ENUM('Resolvido', 'Em andamento', 'Não visto') DEFAULT 'Em andamento'
);

-- Criação da tabela de autenticação centralzada do pina
CREATE TABLE Aut_cent_pina (
    id INT AUTO_INCREMENT PRIMARY KEY,
    orgao VARCHAR(255) NOT NULL,
    Login VARCHAR(255) NOT NULL,
    Matricula int NOT NULL,
    status ENUM('Ativo', 'Em manutenção', 'Inativo') DEFAULT 'Inativo'
);

CREATE TABLE Chamado_Predial_Pina (
    id INT AUTO_INCREMENT PRIMARY KEY,
    orgao VARCHAR(255) NOT NULL,
    requerente VARCHAR(255) NOT NULL,
    solicitacao TEXT NOT NULL,
    status ENUM('Resolvido', 'Em andamento', 'Não visto') DEFAULT 'Em andamento'
);

create table usuarios(
id integer primary key auto_increment,
email varchar(250),
senha varchar(250)
);
DROP TABLE Aut_cent_pina;

insert into usuarios (email,senha) values('gabriel.gama@sad.pe.gov.br','Gabriel@2801');
select * from Aut_cent_pina;
