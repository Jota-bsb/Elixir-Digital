-- 1. Criar e usar o banco
CREATE DATABASE IF NOT EXISTS ElixirDigital;
USE ElixirDigital;

-- 2. Tabelas

-- Administrador
CREATE TABLE administrador (
    id_administrador INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL
);

-- Cliente
CREATE TABLE cliente (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    telefone VARCHAR(20)
);

-- Membro
CREATE TABLE membro (
    id_membro INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    foto VARCHAR(255),
    descricao TEXT,
    linkedin VARCHAR(255),
    github VARCHAR(255),
    fk_administrador INT,
    FOREIGN KEY (fk_administrador) REFERENCES administrador(id_administrador)
);

-- Pedido - TABELA CORRIGIDA
CREATE TABLE pedido (
    id_pedido INT AUTO_INCREMENT PRIMARY KEY,
    descricao TEXT NOT NULL,
    dt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status ENUM('Em análise', 'Em produção', 'Não aceito', 'Finalizando') DEFAULT 'Em análise' NOT NULL,
    tecnologias_preferidas VARCHAR(255),
    fk_cliente INT NOT NULL,
    fk_administrador INT,
    FOREIGN KEY (fk_cliente) REFERENCES cliente(id_cliente),
    FOREIGN KEY (fk_administrador) REFERENCES administrador(id_administrador)    
);

-- Feedback
CREATE TABLE feedback (
    id_feedback INT AUTO_INCREMENT PRIMARY KEY,
    mensagem TEXT NOT NULL,
    dt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    origem_cliente BOOLEAN NOT NULL,
    autor VARCHAR(100) NOT NULL,
    email VARCHAR (255) NOT NULL,
	projeto TEXT,
    avaliacao TINYINT CHECK (avaliacao >= 0 AND avaliacao <= 5),
    fk_cliente INT,
    fk_administrador INT,
    fk_pedido INT,
    FOREIGN KEY (fk_cliente) REFERENCES cliente(id_cliente),
    FOREIGN KEY (fk_administrador) REFERENCES administrador(id_administrador),
    FOREIGN KEY (fk_pedido) REFERENCES pedido(id_pedido)
);

-- Post Blog
CREATE TABLE post_blog (
    id_post INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    conteudo TEXT NOT NULL,
    dt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    imagem VARCHAR(255),
    fk_administrador INT NOT NULL,
    FOREIGN KEY (fk_administrador) REFERENCES administrador(id_administrador)
);

-- 3. INSERTs de exemplo

-- Administradores
INSERT INTO administrador (nome, email, senha) VALUES
('Vinicius Aquino', 'vinicius@elixirdigital.com', 'senha123'),
('Maria Silva', 'maria@elixirdigital.com', 'senha456');

-- Clientes
INSERT INTO cliente (nome, email, telefone) VALUES
('Ana Souza', 'ana.souza@gmail.com', '(11) 99999-1234'),
('João Pereira', 'joao.pereira@hotmail.com', '(21) 98888-5678');

-- Membros
INSERT INTO membro (nome, foto, descricao, linkedin, github, fk_administrador) VALUES
('Lucas Mendes', 'lucas.jpg', 'Front-end Developer', 'https://linkedin.com/in/lucas', 'https://github.com/lucasmendes', 1),
('Beatriz Costa', 'beatriz.jpg', 'Back-end Developer', 'https://linkedin.com/in/beatriz', 'https://github.com/beatrizcosta', 2);

-- Pedidos - AGORA COM OS NOVOS STATUS
INSERT INTO pedido (descricao, status, tecnologias_preferidas, fk_cliente, fk_administrador) VALUES
('Desenvolvimento de site institucional', 'Em análise', 'React, Node.js, MongoDB', 1, NULL),
('Manutenção de plataforma existente', 'Em produção', 'Python, Django, PostgreSQL', 2, 1),
('Desenvolvimento de aplicativo mobile', 'Não aceito', 'React Native, Firebase', 1, 2),
('Sistema de gestão empresarial', 'Finalizando', 'Java, Spring Boot, PostgreSQL', 2, NULL);

-- Feedbacks
INSERT INTO feedback (mensagem, origem_cliente, autor, email, avaliacao, fk_cliente, fk_administrador, fk_pedido) VALUES
('Excelente serviço, muito satisfeito!', TRUE, 'Ana Souza', 'ana.souza@gmail.com', 5, 1, NULL, 1),
('Projeto entregue com qualidade, recomendo!', TRUE, 'João Pereira', 'joao.pereira@hotmail.com', 4, 2, NULL, 2),
('Feedback interno cadastrado pelo admin', FALSE, 'Vinicius Aquino', 'vinicius@elixirdigital.com', 3, NULL, 1, NULL);

-- Posts do Blog
INSERT INTO post_blog (titulo, conteudo, imagem, fk_administrador) VALUES
('Novo Projeto de Front-end', 'Descrição do projeto de front-end.', 'frontend.jpg', 1),
('Atualização do Blog', 'Novidades da turma em setembro.', 'novidades.jpg', 2);

-- 4. CONSULTA PARA VERIFICAR OS PEDIDOS
SELECT id_pedido, descricao, status, tecnologias_preferidas 
FROM pedido 
ORDER BY id_pedido;