import socket as s
import threading
import sys
from colors import bcolors

HOST = '127.0.0.1'
PORT = 9999

global authenticated
authenticated = False

def handle_auth(sock):
  global authenticated
  global user
  valid_user = False

  try:
    while not valid_user:
      user = input(f"{bcolors.WHITE}🙂 Digite seu usuário: ")
      sock.sendall(str.encode(user))

      data = sock.recv(1024).decode()

      if data == "valid":
        valid_user = True
      else:
        print(f"{bcolors.FAIL}❌ Usuário já existe ou é inválido. Tente outro.{bcolors.ENDC}")
    
    has_password = sock.recv(1024).decode()

    if has_password == "true":
      while not authenticated:
        password = input(f"{bcolors.WHITE}🔒 Digite a senha: ")
        sock.sendall(str.encode(password))
      
        data = sock.recv(1024)

        if data.decode() != "authenticated":
          print(f"{bcolors.FAIL}❌ Senha incorreta. Tente novamente.")
        else:
          authenticated = True

    authenticated = True
    thread = threading.Thread(target=listen_server, args=(sock,))
    thread.start()
    print(f"{bcolors.OKGREEN}----------- 🌐 Você entrou no chat -----------{bcolors.ENDC}")

  except Exception:
    print(f"\n{bcolors.FAIL}❌ Erro: não foi possível autenticar.")
    sys.exit()

def listen_server(sock):
  global authenticated

  while authenticated:
    try:
      data = sock.recv(1024)
      print(data.decode())
    except Exception as e:
      print(e)
      break

def start_client():
  global user

  try:
    sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    sock.connect((HOST, PORT))

    while True:
      if not authenticated:
        handle_auth(sock)
        continue

      text = input(f"{bcolors.OKCYAN}")

      if text.startswith("/"):
        if text == "/q":
          raise KeyboardInterrupt

        try:
          pvd_user, message = text.split(" ", 1)

          sock.sendall(str.encode(f"{user}: {pvd_user}-{message}"))
        except:
          print(f"{bcolors.FAIL}❌ Comando inválido.{bcolors.ENDC}")
      else:
        sock.sendall(str.encode(f"{user}: {text}"))

  except KeyboardInterrupt:
    print(f"{bcolors.WARNING}----------- 🌐 Você saiu do chat -----------{bcolors.ENDC}")

  except Exception as e:
    print(f"{bcolors.FAIL}❌ Erro: {e}{bcolors.ENDC}")

  finally:
    sock.close()

if __name__ == "__main__":
  try:
    start_client()
  except KeyboardInterrupt:
    print(f"\n{bcolors.FAIL}----------- 🌐 Conexão encerrada  -----------{bcolors.ENDC}")
    sys.exit(0)