import socket
import argparse

parser = argparse.ArgumentParser(
    description='Python command line tool to check for open ports on a host',
    epilog="python portCheck.py --host 192.168.1.221 --port 3389"
)
parser.add_argument("--host", required=True, help="IP of machine running to check")
parser.add_argument("--port", required=True, type=int, help="Port of machine to check")
args = parser.parse_args()

a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result_of_check = a_socket.connect_ex((args.host,args.port))

if result_of_check == 0:
   print(f"Port {args.port} is open")
else:
   print(f"Port {args.port} is not open")

a_socket.close()
