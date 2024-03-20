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
     tipo varchar(255) not null,
    solicitacao TEXT NOT NULL,
     Data_Abertura timestamp default current_timestamp,
    status ENUM('Resolvido', 'Em andamento', 'Não visto') DEFAULT 'Em andamento',
    Tipo_ac varchar(250),
    Andamento varchar(250),
    Situacao varchar(350),
    Obs varchar(250)
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
    Tipo Varchar(255) Not Null,
    solicitacao TEXT NOT NULL,
	status ENUM('Resolvido', 'Em andamento', 'Não visto') DEFAULT 'Não Visto',
    Tipo_ac varchar(250),
    Data_Abertura timestamp default current_timestamp,
    Andamento varchar(250),
    Situacao varchar(350),
    Obs varchar(250)
   );
   
   
create table controle_Patrimonial_Pina(
id integer primary key auto_increment,
orgao varchar(255) not null,
requerente varchar(255) not null,
monitor1_tombamento varchar(255) not null,
monitor1_serie varchar(255) not null,
monitor2_tombamento varchar(255),
monitor2_serie varchar(255),
gabiente_tombamento varchar(255) not null,
gabiente_serie varchar(255) not null,
status ENUM('Resolvido', 'Em andamento', 'Não visto') DEFAULT 'Não Visto',
Data_Abertura timestamp default current_timestamp

);


SELECT * FROM controle_Patrimonial_Pina ORDER BY Data_Abertura DESC;
DROP TABLE controle_Patrimonial_Pina;
create table usuarios(
id integer primary key auto_increment,
email varchar(250),
senha varchar(250)
);

select * from Aut_cent_pina;
