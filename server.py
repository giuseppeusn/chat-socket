import socket as s
import threading
import sys
from colors import bcolors, ucolors

HOST = '127.0.0.1'
PORT = 9999

global users
users = []

global chat_pass
chat_pass = ""

def create_user(username, conn, addr):
  color_attributes = [attr for attr in dir(ucolors) if not attr.startswith('__')]
  
  color_index = len(users) % len(color_attributes)
  color = color_attributes[color_index]

  new_user = {
    "username": username,
    "addr": addr,
    "conn": conn,
    "color": ucolors.__dict__[color]
  }

  users.append(new_user)

  broadcast_msg(f"\n{new_user['color']}----------- 🌐 {new_user['username']} ({new_user['addr'][0]}:{new_user['addr'][1]}) entrou no chat -----------{bcolors.ENDC}", addr)


def broadcast_msg(msg, addr):
  global users
  print(msg)

  for user in users:
    if user['addr'] != addr:
      user['conn'].sendall(str.encode(msg))


def disconnect_user(conn, addr):
  global users

  dc_user = next((u for u in users if u['addr'] == addr), None)
  broadcast_msg(f"----------- 🌐 {bcolors.WARNING}{dc_user['username']} ({dc_user['addr'][0]}:{dc_user['addr'][1]}) desconectou do chat ----------- {bcolors.ENDC}", addr)
  users.remove(dc_user)

  conn.close()

def handle_auth(conn, addr):
  authenticated = False
  global chat_pass

  try:
    username = conn.recv(1024).decode()

    if username == "":
      return False

    if chat_pass == "":
      conn.sendall(str.encode("false"))
    else:
      conn.sendall(str.encode("true"))

      while not authenticated:
        password = conn.recv(1024).decode()

        if password == chat_pass:
          conn.sendall(str.encode("authenticated"))
          authenticated = True
        else:
          conn.sendall(str.encode("fail"))
    
    create_user(username, conn, addr)
    return True
  except Exception:
    return False

def receive_msg(conn, addr):
  global users

  while True:
    try:
      data = conn.recv(1024)

      if not data:
        disconnect_user(conn, addr)
        break 

      username, message = data.decode().split(": ", 1)

      user = next((u for u in users if u['username'] == username.strip()), None)

      broadcast_msg(f"💬 {user['color']}{user['username']}: {ucolors.LIGHTWHITE}{message}{bcolors.ENDC}{bcolors.OKCYAN}", addr)

    except ValueError as e:
      print(f"🔊 {bcolors.FAIL}Mensagem inválida.{bcolors.ENDC}")
      break

    except Exception as e:
      if e.errno == 10054:
        disconnect_user(conn, addr)
        break

      print(f"{bcolors.FAIL}❌ Erro: {e}{bcolors.ENDC}")
      break
    
  conn.close()

def connect_user(conn, addr):
  authenticated = handle_auth(conn, addr)

  if authenticated:
    thread = threading.Thread(target=receive_msg, args=(conn, addr))
    thread.start()

def start_server():
  global chat_pass
  chat_pass = input("🔒 Defina uma senha de acesso: ")

  sock = s.socket(s.AF_INET, s.SOCK_STREAM)
  sock.bind((HOST, PORT))
  sock.listen()

  print(f"{bcolors.OKGREEN}----------- 🌐 Servidor iniciado ({HOST}:{PORT}) -----------{bcolors.ENDC}")

  while True:
    conn, addr = sock.accept()
    connect_user(conn, addr)

if __name__ == "__main__":
  try:
    start_server()
  except KeyboardInterrupt:
    print(f"\n{bcolors.FAIL}----------- 🌐 Servidor encerrado -----------{bcolors.ENDC}")
    sys.exit(0)
