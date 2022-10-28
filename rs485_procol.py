from serial.tools import list_ports
from serial import Serial
import libscrc
import stm32_crc_tool

#print(hex(stm32_crc_tool.embedded_crc(476758147072)))
custom_crc_table = {}

def int_to_bytes(i):
    return [(i >> 24) & 0xFF, (i >> 16) & 0xFF, (i >> 8) & 0xFF, i & 0xFF]


def generate_crc32_table(_poly):

    global custom_crc_table

    for i in range(256):
        c = i << 24

        for j in range(8):
            c = (c << 1) ^ _poly if (c & 0x80000000) else c << 1

        custom_crc_table[i] = c & 0xffffffff


def custom_crc32(buf):

    global custom_crc_table
    crc = 0xffffffff

    for integer in buf:
        b = int_to_bytes(integer)

        for byte in b:
            crc = ((crc << 8) & 0xffffffff) ^ custom_crc_table[(crc >> 24) ^ byte]

    return crc

poly = 0x04C11DB7
buf = [0x6F, 0x01, 0x00, 0x00, 0x00]

generate_crc32_table(poly)
custom_crc = custom_crc32(buf)

print("Custom crc          " + hex(custom_crc))
print(libscrc.stm32(bytearray(buf)))


device_name_list = []
usb_device_list = list_ports.comports()
if len(usb_device_list) >= 1:
    device_name_list = [port.device for port in usb_device_list]
    serial_port = Serial(device_name_list[0], 57600, 8, 'N', 1, timeout=1)
    if serial_port and serial_port.is_open:
        serial_port.write(b'\x6f\x01\x00\x00\x00\x00\xf2\x77\x9f\x2d')


