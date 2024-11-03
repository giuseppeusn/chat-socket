# Chat simultâneo - socket

## Projeto

Esse projeto foi desenvolvido para a disciplina de Conectividade em Sistemas Ciberfísicos do curso de Engenharia de Software da PUC-PR. O intuito é construir um chat que possa ter múltiplas conexões aplicando os conceitos aprendidos de redes, socket e threads. O software consiste em dois principais scripts, um do servidor que receberá todas as mensagens e fará o gerenciamento e o outro do cliente que enviará as mensagens para o servidor.

## Desenvolvido com:

> Python

## Como utilizar:

- Clone o projeto
- Abra a pasta `/chat-socket`
- Abra um terminal, execute o comando `python server.py` e defina uma senha (opcional)
- Abra outros terminais (quantos quiser), execute o comando `python cliente.py`, defina o nome de usuário e insira a senha do servidor (se possuir)
- A partir desse momento os clientes podem trocar mensagens simultaneamente
