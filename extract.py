import socket
import ac
import acsys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 9999))
server.listen(1)

def acMain(ac_version):
    ac.log("Socket server started")
    conn, addr = server.accept()

    while True:
        speed = ac.getCarState(0, acsys.CS.SpeedKMH)
        conn.send(f"Speed: {speed}\n".encode())
