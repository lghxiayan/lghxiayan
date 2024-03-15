import pyshark

# cap = pyshark.FileCapture('flag.pcapng')
cap = pyshark.FileCapture('keyboard.pcapng', tshark_path='C:\Program Files\Wireshark')
data = ''
for packet in cap:
    # print(packet.usb)
    print(packet[packet.highest_layer])
    # data = '' + packet[packet.highest_layer].data
    # print(chr(int(data, 16)), end='')
# cap.close()

# var = pyshark
