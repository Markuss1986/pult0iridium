import struct

class SettingsParametrs:
    uint8_t_SendId = 0                              # Отправитель сообщения (Display1/Display2)
    uint8_t_GeneralState = 0                        # Общий статус передатчика
    uint16_t_ModSelect = 0                          # Подключенные модуляторы
    uint16_t_PSSelect = 0                           # Подключенные источники питания
    uint16_t_ModConnStat = [0, 0, 0, 0, 0, 0, 0, 0] # Статус подключения модуляторов
    uint16_t_PSConnStat = 0                         # Статус подключения источников питания
    uint8_t_Ant = [0, 0, 0, 0]                      # Подключенные антенны
    uint16_t_L = [0, 0, 0, 0]                       # Индуктивность антенны
    uint16_t_R = [0, 0, 0, 0]                       # Сопротивление антенны
    uint8_t_Cur = [0, 0, 0, 0]                      # Ток антенны
    uint8_t_RepeatNum = 0                           # Количество отправленных сообщений
    uint8_t_BitNum = 0                              # Количество отправленных бит в данном сообщении
    uint8_t_Code = 0                                # Кодировка
    uint16_t_PowerCount = [0, 0]                    # Мощность на выходе источника питания
    uint16_t_U = [0, 0]                             # Напряжение на выходе источника питания
    uint16_t_crc = 0                                # Контрольная сумма

    def read_Settings(self, received_msg):
        uint8_t_SendId = received_msg[0]
        uint8_t_GeneralState = received_msg[1]
        uint16_t_ModSelect = int.from_bytes(received_msg[2:3 + 1], 'little')
        uint16_t_PSSelect = int.from_bytes(received_msg[2:3 + 1], 'little')
        uint16_t_ModConnStat = [struct.unpack("<f", received_msg[4:5 + 1]), struct.unpack("<f", received_msg[6:7 + 1]),
                                struct.unpack("<f", received_msg[8:9 + 1]), struct.unpack("<f", received_msg[10:11 + 1]),
                                struct.unpack("<f", received_msg[12:13 + 1]), struct.unpack("<f", received_msg[14:15 + 1]),
                                struct.unpack("<f", received_msg[16:17 + 1]), struct.unpack("<f", received_msg[18:19 + 1])]
        uint16_t_PSConnStat = int.from_bytes(received_msg[20:21 + 1], 'little')
        uint8_t_Ant = list(received_msg[22:25 + 1])
        uint16_t_L = [struct.unpack("<f", received_msg[26:27 + 1]), struct.unpack("<f", received_msg[28:29 + 1]),
                      struct.unpack("<f", received_msg[30:31 + 1]), struct.unpack("<f", received_msg[32:33 + 1])]
        uint16_t_R = [struct.unpack("<f", received_msg[34:35 + 1]), struct.unpack("<f", received_msg[36:37 + 1]),
                      struct.unpack("<f", received_msg[38:39 + 1]), struct.unpack("<f", received_msg[40:41 + 1])]
        uint8_t_Cur = list(received_msg[42:45 + 1])
        uint8_t_RepeatNum = received_msg[46]
        uint8_t_BitNum = received_msg[47]
        uint8_t_Code = received_msg[48]
        uint16_t_PowerCount = int.from_bytes(received_msg[49:51 + 1], 'little')
        uint16_t_U = int.from_bytes(received_msg[52:53 + 1], 'little')
        uint16_t_crc = int.from_bytes(received_msg[54:55 + 1], 'little')

class PultComand:
    uint8_t_SendId      # Отправитель сообщения(Remote)
    uint8_t_Ant[4]      # Подключенные антенны
    uint8_t_Send        # Запуск передачи
    uint16_t_IDtag      # ID метки
    uint8_t_Command     # Команда вызова
    uint16_t_crc        # Контрольная сумма