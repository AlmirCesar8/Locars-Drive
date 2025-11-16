SELECT email, senha FROM usuario_; -- Teste para ver criptografia após a execução de tudo


select * from usuario_ 
where email = AES_ENCRYPT('joao@email.com', 'chaveSegura123')
  and senha = SHA2('senha123', 256);
