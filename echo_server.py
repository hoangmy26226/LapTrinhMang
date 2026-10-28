# Nhóm       : Nhóm 12
# Người viết : Trần Thị Hoàng My  3120224095
# Cách chạy  : python echo_server.py
# echo_server.py - Server TCP đa luồng (phục vụ nhiều client cùng lúc)
import socket
import threading

HOST = "0.0.0.0"   # lắng nghe trên mọi giao diện
PORT = 9012        # có thể đổi thành cổng nhóm

def handle_client(conn, addr, listener):
    with conn:  # 'with' cho socket phiên
        print(f"[+] Client {addr} kết nối")
        print("listener.getsockname() =", listener.getsockname())
        print("conn.getsockname() =", conn.getsockname())
        print("conn.getpeername() =", conn.getpeername())
        while True:
            data = conn.recv(1024)
            if not data:  # khi client đóng kết nối
                print(f"[-] Client {addr} đã đóng kết nối")
                break
            text = data.decode("utf-8", errors="replace")  # chỉ để log
            print(f"  Nhận {len(data)} byte từ {addr}: {text[:60]!r}")
            conn.sendall(data)  # echo nguyên byte

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  # socket lắng nghe
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # bắt buộc trước bind()
        s.bind((HOST, PORT))
        s.listen()
        print("Server lắng nghe tại", s.getsockname())
        try:
            while True:
                conn, addr = s.accept()
                threading.Thread(target=handle_client,
                                 args=(conn, addr, s), daemon=True).start()
        except KeyboardInterrupt:
            print("\nServer dừng.")

if __name__ == "__main__":
    main()
