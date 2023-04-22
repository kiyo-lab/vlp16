import struct
import socket
import numpy as np
UDP_IP = "192.168.1.201"  # VLP16のIPアドレス
UDP_PORT = 2368  # VLP16のポート番号
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
data = np.zeros((16, 360))
while True:
    packet, addr = sock.recvfrom(1206)  # 1パケットあたり1206バイト
    # パケットの解析
    for i in range(0, 12):
        offset = i * 100
        data_block = packet[offset + 4: offset + 100]
        azi = int.from_bytes(data_block[2:4], byteorder='little') / 100  # 水平角度
        for j in range(0, 32):
            dist = int.from_bytes(data_block[j*3:j*3+2], byteorder='little') / 500  # 距離
            data[j*16 + i][int(azi*2)] = dist
    # 2周目のデータを受信したら、データを処理する
    if int.from_bytes(packet[1200:1202], byteorder='little') == 1:
        #　データ処理を行う
        process_data(data)
