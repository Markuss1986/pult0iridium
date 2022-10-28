# Импорт kivy библиотек
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock

# Импорт Java классов
# Нужно прописать в системных переменных путь до Java.(JAVA_HOME и PATH)
# https://pyjnius.readthedocs.io/en/stable/installation.html#installation-for-windows
from jnius import autoclass

# Импорт системных библиотек
import os

# Подключаем потоки
import threading

# Библиотека для упаковки и распаковки бинарных данных(байт в инт и обратно)
import struct

# Для работы с CSV
import csv

# Импорт порльзовательских библиотек и классов
import crc
import RS485

# Импорт отображения даты и времени и 1с задержки
from time import strftime
from datetime import date
import time

# Импорт библиотек для работы с USB и разрешения
from kivy.utils import platform
if platform == 'android':
    from usb4a import usb
    from usbserial4a import serial4a
    from android.permissions import request_permissions, Permission

else:
    from serial.tools import list_ports
    from serial import Serial


class HomePage(MDScreen):
    'Home Page'

class MainApp(MDApp):

    # метод инициализации переменных класса
    def __init__(self, *args, **kwargs):
        self.uiDict = {}
        self.device_name_list = []
        self.serial_port = None
        self.text_btn = ""
        self.sol_text = ""

        # Инициализация времени
        self.sw_started= False                      #
        self.sw_seconds = 0                         #

        self.Settings = RS485.SettingsParametrs()   # Обьекты классов принимаемых сообщений по RS485
        self.Status = RS485.StatusSystem()          # Обьекты классов принимаемых сообщений по RS485
        self.percent_transmit = 0                   # Процент отправки сообщения
        self.flag_alarm_pause = 0                   # Флаг того что сейчас пауза Alarm
        self.alarm_time_counter = 0                 # Счетчик секунд паузы Alarm
        self.flag_tags = 0                          # Флаг того что передаем таги
        self.flag_alarm = 0                         # Флаш того что сейчас Alaram включен
        self.flag_thread = False                    # Флаг применого потока

        self.Number_light = []                      # Массив фонарей
        self.Number_tag = []                     # Массив тагов
        self.serial_flag = 0                        # Флаг того что включен сериал порт
        self.received_msg = bytearray(402)             # Входной програмный буффер для данных RS485
        self.com_count = 0                          # Счетчик Com портов
        self.sdpathfile = 0                         # Путь к файлу base.csv
        self.count_recive = 1
        self.count_recive_i = 0
        self.count_recive_i1 = 0
        self.read_thread = None
        self.port_thread_lock = threading.Lock()
        self.start = 0
        self.gui_count_sek = 29

        super(MainApp, self).__init__(*args, **kwargs)

    # метод созданий интерфейса из kv файла
    def build(self):
        Builder.load_file('MainApp.kv')
        return HomePage()

# ------------- обработчики кнопок ------------------
    def on_btn_screen_1(self):
        if self.uiDict['sm'].current != 'screen_no_connection' and self.uiDict['sm'].current != 'screen_message':
            self.uiDict['sm'].current = 'screen_send'

    # Active button 2 display screen_send
    def on_btn_screen_2(self):
        if self.uiDict['sm'].current != 'screen_no_connection' and self.uiDict['sm'].current != 'screen_message':
            self.uiDict['sm'].current = 'enter_menu'

    # Active button 3 display command
    def on_btn_screen_3(self):
        if self.uiDict['sm'].current != 'screen_no_connection' and self.uiDict['sm'].current != 'screen_message':
            self.uiDict['sm'].current = 'Command'

    def on_btn_screen_status(self):
        if self.uiDict['sm'].current != 'screen_no_connection' and self.uiDict['sm'].current != 'screen_message':
            self.uiDict['sm'].current = 'status'

    def on_btn_screen_antenna_1(self):
        if self.Status.int8_t_ant_state[0] == 1:
            self.uiDict['sm'].current = 'antenna_1'

    def on_btn_screen_antenna_2(self):
        if self.Status.int8_t_ant_state[1] == 1:
            self.uiDict['sm'].current = 'antenna_2'

    def on_btn_screen_antenna_3(self):
        if self.Status.int8_t_ant_state[2] == 1:
            self.uiDict['sm'].current = 'antenna_3'

    def on_btn_screen_antenna_4(self):
        if self.Status.int8_t_ant_state[3] == 1:
            self.uiDict['sm'].current = 'antenna_4'

    # экран включчение и отключения
    def on_btn_screen_turn_antenna(self):
        self.uiDict['sm'].current = 'turn_antenna'

    # Подключение и отключение антенн
    def on_btn_turn_antenna_1(self):
        if self.Settings.uint8_t_alarm_msg == 0 and self.Status.uint8_t_trans_state == 0:
            if self.root.ids.MainApp.antenna_state_1 == self.root.ids.MainApp.antenna_state_ok:
                # Выключаем антенну 1
                self.write_rs485(b'\x30\x00\x00\x00\x00' + crc.crc_stm32(b'\x30\x00\x00\x00' + b'\x00\x00\x00\x00'))
            if self.root.ids.MainApp.antenna_state_1 == self.root.ids.MainApp.antenna_state_no:
                # Включаем антенну 1
                self.write_rs485(b'\x30\x01\x00\x00\x00' + crc.crc_stm32(b'\x30\x00\x00\x00' + b'\x01\x00\x00\x00'))

    def on_btn_turn_antenna_2(self):
        if self.Settings.uint8_t_alarm_msg == 0 and self.Status.uint8_t_trans_state == 0:
            if self.root.ids.MainApp.antenna_state_2 == self.root.ids.MainApp.antenna_state_ok:
               # Выключаем антенну 2
                self.write_rs485(b'\x31\x00\x00\x00\x00' + crc.crc_stm32(b'\x31\x00\x00\x00' + b'\x00\x00\x00\x00'))
            if self.root.ids.MainApp.antenna_state_2 == self.root.ids.MainApp.antenna_state_no:
                # Включаем антенну 2
                self.write_rs485(b'\x31\x01\x00\x00\x00' + crc.crc_stm32(b'\x31\x00\x00\x00' + b'\x01\x00\x00\x00'))

    def on_btn_turn_antenna_3(self):
        if self.Settings.uint8_t_alarm_msg == 0 and self.Status.uint8_t_trans_state == 0:
            if self.root.ids.MainApp.antenna_state_3 == self.root.ids.MainApp.antenna_state_ok:
                # Выключаем антенну 3
                self.write_rs485(b'\x32\x00\x00\x00\x00' + crc.crc_stm32(b'\x32\x00\x00\x00' + b'\x00\x00\x00\x00'))
            if self.root.ids.MainApp.antenna_state_3 == self.root.ids.MainApp.antenna_state_no:
                # Включаем антенну 3
                self.write_rs485(b'\x32\x01\x00\x00\x00' + crc.crc_stm32(b'\x32\x00\x00\x00' + b'\x01\x00\x00\x00'))

    def on_btn_turn_antenna_4(self):
        if self.Settings.uint8_t_alarm_msg == 0 and self.Status.uint8_t_trans_state == 0:
            if self.root.ids.MainApp.antenna_state_4 == self.root.ids.MainApp.antenna_state_ok:
                # Выключаем антенну 4
                self.write_rs485(b'\x33\x00\x00\x00\x00' + crc.crc_stm32(b'\x33\x00\x00\x00' + b'\x00\x00\x00\x00'))
            if self.root.ids.MainApp.antenna_state_4 == self.root.ids.MainApp.antenna_state_no:
                # Включаем антенну 4
                self.write_rs485(b'\x33\x01\x00\x00\x00' + crc.crc_stm32(b'\x33\x00\x00\x00' + b'\x01\x00\x00\x00'))

    def on_btn_turn_on_alarm(self):
        if self.Settings.uint8_t_alarm_msg == 0 and self.Status.uint8_t_trans_state == 0:
            self.uiDict['sm'].current = 'screen_send'
            self.write_rs485(b'\x2B\x01\x00\x00\x00' + crc.crc_stm32(b'\x2B\x00\x00\x00' + b'\x01\x00\x00\x00'))
            self.flag_alarm_pause == 0
            self.flag_alarm = 1

    def on_btn_turn_off_alarm(self):
        self.write_rs485(b'\x2B\x00\x00\x00\x00' + crc.crc_stm32(b'\x2B\x00\x00\x00' + b'\x00\x00\x00\x00'))
        self.flag_alarm = 0
        self.flag_alarm_pause = 0
        self.alarm_time_counter = 0
        #self.root.ids.status_bar.text = ''
        #self.root.ids.progress_bar.opacity = 0


    def on_btn_turn_on_tags(self):
        self.flag_tags = 1
        self.root.ids.break_button.text = 'Тест всех меток'
        self.root.ids.solution.text = ''
        self.uiDict['sm'].current = 'screen_send'

    def on_btn_turn_off_tags(self):
        self.flag_tags = 0
        self.root.ids.break_button.text = 'Прервать передачу'
        self.root.ids.status_bar.text = ''
        self.root.ids.solution.text = ''
        self.uiDict['sm'].current = 'screen_send'
        self.flag_alarm_pause = 0

    def on_btn_break_up(self):
        if self.Settings.uint8_t_alarm_msg == 0:
            if self.Status.uint8_t_trans_state == 1:
                # Оправка по RS485 строки прекращения передачи
                self.write_rs485(b'\x21\x00\x00\x00\x00' + crc.crc_stm32(b'\x21\x00\x00\x00'+ b'\x00\x00\x00\x00'))
                self.flag_alarm_pause = 0
                self.alarm_time_counter = 0
                #self.root.ids.status_bar.text = ''
                #self.root.ids.progress_bar.opacity = 0

            # Если включено тестирование меток
            if self.flag_tags == 1:
                # Тест всех меток
                U2CT_DATA = b'\x0A' + struct.pack("<I", 4294967295) + crc.crc_stm32(b'\x0A\x00\x00\x00'+ struct.pack("<I", 4294967295))
                U2CT_TEST_TAG = b'\x2E\x01\x00\x00\x00' + crc.crc_stm32(b'\x2E\x00\x00\x00' + b'\x01\x00\x00\x00')
                Command_tags = U2CT_DATA + U2CT_TEST_TAG
                self.write_rs485(Command_tags)
                #self.root.ids.status_bar.text = 'Контроль'
        else:
            self.on_btn_turn_off_alarm()

    def on_btn_clear(self):
        if self.Settings.uint8_t_alarm_msg == 0 and self.Status.uint8_t_trans_state == 0:
            self.root.ids.status_bar.text = ''
            self.root.ids.solution.text = ''
            self.root.ids.progress_bar.opacity = 0

    # Метод обработки нажатий кнопок отправить, очистить и цифр
    def on_button_press(self, text_btn, sol_text):
        if self.Settings.uint8_t_alarm_msg == 0 and self.Status.uint8_t_trans_state == 0:
            # Очистка текстового поля с решением
            if text_btn == "Очистка" or (text_btn == "0" and sol_text == "0"):
                return ""

            # Проверка на корретность номера фонаря
            if text_btn == "Отправить":

                # Если 0 выводим ошибку
                if sol_text == "0" or sol_text == "":
                    return "Ошибка: номер фонаря не можеть быть 0"

                # Если текст то ощибка
                if sol_text == "Отправка: авария" or sol_text == "Ошибка: введите номер фонаря" or \
                        sol_text == "Ошибка: номер фонаря не можеть быть 0" or sol_text == "Номер фонаря отправлен" or \
                        sol_text == "Ошибка: номер фоанря больше 65535":
                    return "Ошибка: введите номер фонаря"

                if sol_text.isdigit():
                    if int(sol_text) > 65535:
                        return "Ошибка: номер фонаря больше 65535"

                self.read_csv()

                # Сверка из файла
                for i in range(0, len(self.Number_light), 1):

                    if self.Number_light[i] == int(sol_text):
                        sol_text = self.Number_tag[i]

                        if self.flag_tags == 0:
                            # Оправка запрос фонаря
                            U2CT_DATA = b'\x0A' + struct.pack("<I", int(sol_text)) + crc.crc_stm32(b'\x0A\x00\x00\x00'+ struct.pack("<I", int(sol_text)))
                            U2CT_COMMAND = b'\x2F\x01\x00\x00\x00'  + crc.crc_stm32(b'\x2F\x00\x00\x00'+ b'\x01\x00\x00\x00')
                            U2CT_ENABLE = b'\x21\x01\x00\x00\x00' + crc.crc_stm32(b'\x21\x00\x00\x00'+ b'\x01\x00\x00\x00')
                            command = U2CT_DATA + U2CT_COMMAND + U2CT_ENABLE
                            #self.write_rs485(command)
                            self.write_rs485(U2CT_DATA)
                            self.write_rs485(U2CT_COMMAND)
                            self.write_rs485(U2CT_ENABLE)
                            print(U2CT_DATA)
                            print(U2CT_COMMAND)
                            print(U2CT_ENABLE)

                        # Если включено тестирование меток, отправляем номер метки
                        if self.flag_tags == 1:
                            U2CT_DATA = b'\x0A' + struct.pack("<I", int(sol_text)) + crc.crc_stm32(b'\x0A\x00\x00\x00'+ struct.pack("<I", int(sol_text)))
                            U2CT_TEST_TAG = b'\x2E\x00\x00\x00\x00' + crc.crc_stm32(b'\x2E\x00\x00\x00' + b'\x00\x00\x00\x00')
                            Command_tags = U2CT_DATA + U2CT_TEST_TAG
                            self.write_rs485(Command_tags)
                        break
                    else:
                        if i == len(self.Number_light)-1:
                            return 'Номер отсутствует в базе'
                # Вывод в строку
                return ""

            # Если цифра то
            if (text_btn == "0" or text_btn == "1" or text_btn == "2" or text_btn == "3" or text_btn == "4" or text_btn == "5" or \
                 text_btn == "6" or text_btn == "7" or text_btn == "8" or text_btn == "9"):

                # Делаем так чтобы если в тексте стоит 0 не получилось 0000
                if sol_text == "0":
                    return text_btn

                # Сброс текста и вывод цифры
                if sol_text == "Ошибка: номер фонаря не можеть быть 0" or sol_text == "Отправка: авария" or \
                        sol_text == "Ошибка: введите номер фонаря" or sol_text == "Номер фонаря отправлен" or \
                        sol_text == "Ошибка: номер фоанря больше 65535":
                    return text_btn
                return sol_text + text_btn
        else:
            return self.root.ids.solution.text

#----------- Методы работы с Com port ---------------------
    def init_com(self):

        # For Android
        if platform == 'android':
            usb_device_list = usb.get_usb_device_list()
            self.device_name_list = [device.getDeviceName() for device in usb_device_list]
            if len(self.device_name_list) == 0:
                self.serial_port = None
            if len(self.device_name_list) == 1:
                try:
                    self.serial_port = serial4a.get_serial_port(usb_device_list[0].getDeviceName(), 57600, 8, 'N', 1,timeout=1)
                    self.flag_thread = True  # включаем Com port пока переназначем
                except:
                    a=5
            if len(self.device_name_list) > 1:
                try:
                    self.serial_port = serial4a.get_serial_port(usb_device_list[-1].getDeviceName(), 57600, 8, 'N', 1,timeout=1)
                    self.flag_thread = True # включаем Com port пока переназначем
                except:
                    a=5

        # For Win and Linux
        else:
            # Setup COM port
            usb_device_list = list_ports.comports()
            if len(usb_device_list) >= 1:
                self.flag_thread = True
                self.device_name_list = [port.device for port in usb_device_list]
                # Обнуление для инициализации
                print(self.serial_port)
                if not self.serial_port:
                    self.serial_port = Serial(self.device_name_list[0], 57600, 8, 'N', 1, timeout=1)

    def write_rs485(self, data):
        # Write data to RS485 with convert to bytes
        if len(self.device_name_list) == 0:
            return
        else:
            if self.serial_port and self.serial_port.is_open:
                if self.flag_thread == True:
                    try:
                        self.serial_port.write(data)
                    except:
                        if platform == 'android':
                            a=4
                        #else:
                        #    self.serial_port = None

    def read_rs485(self):
        if len(self.device_name_list) >= 1:
            if self.serial_port and self.serial_port.is_open:
                #try:
                if self.serial_port.in_waiting == 402:
                    self.received_msg = self.serial_port.read(402)
                    # Расчет котнрольной
                    CRC_Settings = crc.crc_stm32(
                        struct.pack("<h", self.received_msg[0]) + b'\x00\x00' + self.received_msg[1:185])
                    CRC_Status = crc.crc_stm32(
                        struct.pack("<h", self.received_msg[189]) + b'\x00\x00' + self.received_msg[190:398])

                    # Сверка контролбной суммы
                    if (CRC_Settings == self.received_msg[185:189]) and (CRC_Status == self.received_msg[398:403]):
                        self.count_recive = 0
                        # Сохрание принятых данных в структуры
                        RS485.SettingsParametrs.read_Settings(self.Settings, self.received_msg, 1)
                        RS485.StatusSystem.read_Status(self.Status, self.received_msg, 190)
                    else:
                        self.count_recive = 1
                    #except:
                    #    self.count_recive = 1
                #else:
                    #if platform == 'android':
                    #self.count_recive = 1
        #else:
            #self.count_recive = 1
               # except:
               #     if platform == 'android':
               #         self.count_recive = 1

    def read_msg_thread(self):
        while True:
            if platform == 'android':
                with self.port_thread_lock:
                    # Если ком порт подключен
                        if len(self.device_name_list) >= 1:
                            # Если ком порт есть и он открыт
                            if self.serial_port and self.serial_port.is_open:

                                try:
                                    self.count_recive_i = 0
                                    # Если приняли 402 байта
                                    self.received_msg = self.serial_port.read(402)
                                    # Расчет котнрольной
                                    CRC_Settings = crc.crc_stm32(struct.pack("<h", self.received_msg[0]) + b'\x00\x00' + self.received_msg[1:185])
                                    CRC_Status = crc.crc_stm32(struct.pack("<h", self.received_msg[189]) + b'\x00\x00' + self.received_msg[190:398])

                                    time.sleep(1)

                                    # Сверка контролбной суммы
                                    if (CRC_Settings == self.received_msg[185:189]) and (
                                            CRC_Status == self.received_msg[398:403]):
                                        self.count_recive = 0
                                        # Сохрание принятых данных в структуры
                                        RS485.SettingsParametrs.read_Settings(self.Settings, self.received_msg, 1)
                                        RS485.StatusSystem.read_Status(self.Status, self.received_msg, 190)

                                        # self.CountReceiveOld = self.CountReceive
                                        # self.CountReceive += 1

                                    else:
                                        self.count_recive_i += 1
                                        if self.count_recive_i >= 10:
                                            self.count_recive_i = 0
                                            self.count_recive = 1
                                except:
                                    time.sleep(1)
                                    self.count_recive_i += 1
                                    if self.count_recive_i >= 10:
                                        self.count_recive_i = 0
                                        self.count_recive = 1
                            else:
                                self.count_recive_i += 1
                                if self.count_recive_i >= 10:
                                    self.count_recive_i = 0
                                    self.count_recive = 1
                        else:
                            self.count_recive_i += 1
                            if self.count_recive_i >= 10:
                                self.count_recive_i = 0
                                self.count_recive = 1

            else:
                time.sleep(0.5)
                try:
                    with self.port_thread_lock:
                        # Если ком порт подключен
                        if len(self.device_name_list) >= 1:
                            # Если ком порт есть и он открыт
                            if self.serial_port and self.serial_port.is_open:

                                if self.serial_port.in_waiting == 402:

                                    self.count_recive_i = 0
                                    # Если приняли 402 байта
                                    self.received_msg = self.serial_port.read(402)
                                    # Расчет котнрольной
                                    CRC_Settings = crc.crc_stm32(
                                        struct.pack("<h", self.received_msg[0]) + b'\x00\x00' + self.received_msg[1:185])
                                    CRC_Status = crc.crc_stm32(
                                        struct.pack("<h", self.received_msg[189]) + b'\x00\x00' + self.received_msg[190:398])

                                    #time.sleep(1)

                                    # Сверка контролбной суммы
                                    if (CRC_Settings == self.received_msg[185:189]) and (
                                            CRC_Status == self.received_msg[398:403]):
                                        self.count_recive = 0

                                        print("CRC - OK",  self.root.ids.time.text )
                                        # Сохрание принятых данных в структуры
                                        RS485.SettingsParametrs.read_Settings(self.Settings, self.received_msg, 1)
                                        RS485.StatusSystem.read_Status(self.Status, self.received_msg, 190)
                                    else:
                                        self.count_recive = 1
                                        print("CRC - BAD", self.root.ids.time.text)



                                if self.serial_port.in_waiting < 402:
                                    print("<402 - BAD", self.root.ids.time.text)
                                    self.count_recive_i+=1
                                    #time.sleep(1)

                                    if self.count_recive_i >= 10:
                                        self.count_recive_i = 0
                                        self.count_recive = 1

                                if self.serial_port.in_waiting > 402:
                                    Litter = self.serial_port.read(self.serial_port.in_waiting)
                except:
                    print("EXCEPT - BAD", self.root.ids.time.text)
                    if self.count_recive_i >= 10:
                        self.count_recive_i = 0
                        self.count_recive = 1


#----------- метод чтения из файла -------------------
    def read_csv(self):
        if platform == 'android':
            try:
                # Получение пути до файла
                request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
                Environment = autoclass('android.os.Environment')
                sdpath = Environment.getExternalStorageDirectory().getAbsolutePath()

                #sdpath = MainApp.get_running_app().user_data_dir
                #sdpath = Environment.getExternalFilesDirs()
                sdpath = os.path.join(sdpath, 'Download')
                self.sdpathfile = os.path.join(sdpath, 'base.csv')
                self.Number_light = []
                self.Number_tag = []
                try:
                    with open(self.sdpathfile, newline='') as csvfile:
                        reader = csv.DictReader(csvfile, delimiter=';')
                        for row in reader:
                            self.Number_light.append (int(row['Number_light']))
                            self.Number_tag.append ( int(row['Number_tag']))
                except:
                    self.root.ids.status_bar.text = "Нет базы данных"
            except:
                a=5
        else:
            sdpath = os.path.dirname(os.path.abspath(__file__))
            self.sdpathfile = sdpath + '/base.csv'
            self.Number_light = []
            self.Number_tag = []
            try:
                with open(self.sdpathfile, newline='') as csvfile:
                    reader = csv.DictReader(csvfile, delimiter=';')
                    for row in reader:
                        self.Number_light.append ( int(row['Number_light']) )
                        self.Number_tag.append ( int(row['Number_tag']) )
                        #print(self.Number_tag)
            except:
                self.root.ids.status_bar.text = "Нет базы данных"

#--------- метод обновление раз в секунду---------------------------
    def update_time(self, nap):

        if self.sw_started:
            self.sw_seconds += nap
            minutes, seconds = divmod(self.sw_seconds, 60)

        self.root.ids.time.text = strftime('%H.%M.%S')
        self.root.ids.date.text = strftime('%d.%m.%Y')

        if self.start == 0:
            self.read_thread = threading.Thread(target=self.read_msg_thread)
            self.read_thread.start()
            self.start = 1

        self.init_com()
        self.interface_alarm_message()
        self.interface_update()

        # Запрос статуса
        CT_GET_STATUS = b'\x6F\x01\x00\x00\x00' + crc.crc_stm32(b'\x6F\x00\x00\x00' + b'\x01\x00\x00\x00')
        self.write_rs485(CT_GET_STATUS)

        #self.read_rs485()

        # Screen No Connection if no comport
        if platform == 'android':
            usb_device_list = usb.get_usb_device_list()
            self.device_name_list = [device.getDeviceName() for device in usb_device_list]
            #if len(self.device_name_list) >= 1 or self.count_recive == 0:
            if len(self.device_name_list) >= 1:
                if self.count_recive == 1: # если не принимаем данные по RS485
                    # обнуляем все цвета и надписи если нет связи
                    self.interface_no_connection()
                else:
                    # Убираем экран нет подключения
                    if self.uiDict['sm'].current == 'screen_no_connection' or self.uiDict['sm'].current == 'probe':
                        self.uiDict['sm'].current = 'screen_send'
                        self.root.ids.MainApp.background_color_connection = self.root.ids.MainApp.background_color_green
            else:
                self.interface_no_connection()
        # Если Win or linux
        else:
            if len(list_ports.comports()) == 0:
                # обнуляем все цвета и надписи если нет связи
                self.interface_no_connection()

            else:
                self.root.ids.MainApp.background_color_connection = self.root.ids.MainApp.background_color_green
                if self.count_recive == 1: # если не принимаем данные по RS485
                    self.interface_no_connection()

                else:
                    if self.uiDict['sm'].current == 'screen_no_connection' or self.uiDict['sm'].current == 'probe':
                        self.uiDict['sm'].current = 'screen_send'

    def interface_no_connection(self):
        self.uiDict['sm'].current = 'screen_no_connection'
        self.root.ids.MainApp.background_color_ant1 = self.root.ids.MainApp.background_color_grey
        self.root.ids.MainApp.background_color_ant2 = self.root.ids.MainApp.background_color_grey
        self.root.ids.MainApp.background_color_ant3 = self.root.ids.MainApp.background_color_grey
        self.root.ids.MainApp.background_color_ant4 = self.root.ids.MainApp.background_color_grey
        self.root.ids.MainApp.background_color_connection = self.root.ids.MainApp.background_color_red
        self.root.ids.MainApp.background_color_faza_1 = self.root.ids.MainApp.background_color_grey
        self.root.ids.MainApp.background_color_faza_3 = self.root.ids.MainApp.background_color_grey
        self.root.ids.MainApp.background_active_text = "Нет"
        self.root.ids.MainApp.background_color_active = self.root.ids.MainApp.background_color_grey

    def on_start(self):
        Clock.schedule_interval(self.update_time, 1)

    def time_screen(self):
        return date.today()

    def interface_alarm_message(self):
        if self.Status.uint8_t_trans_ok == 0: # если нет ошибок

            # и если нет рабочих антенн
            if (self.Status.int8_t_ant_state[0] != 1) and (self.Status.int8_t_ant_state[1] != 1)  and \
               (self.Status.int8_t_ant_state[2] != 1) and (self.Status.int8_t_ant_state[3] != 1):
                if  self.uiDict['sm'].current != 'screen_no_connection':
                    self.root.ids.status_bar.text = self.root.ids.MainApp.screen_message_no_ant

            # Если есть рабочие антенны и экран не равен (нет связи) показываем экран ввода сообщения
            else:
                if self.root.ids.status_bar.text == self.root.ids.MainApp.screen_message_no_ant:
                    self.root.ids.status_bar.text = ""

            # выключение экрана аварии после ее устранения
            if self.uiDict['sm'].current == 'screen_message':
                if self.root.ids.MainApp.screen_message_text == self.root.ids.MainApp.screen_message_220V or \
                   self.root.ids.MainApp.screen_message_text == self.root.ids.MainApp.screen_message_380V or \
                   self.root.ids.MainApp.screen_message_text == self.root.ids.MainApp.screen_message_current_overload or \
                   self.root.ids.MainApp.screen_message_text == self.root.ids.MainApp.screen_message_overheating or \
                   self.root.ids.MainApp.screen_message_text == self.root.ids.MainApp.screen_message_driver or \
                   self.root.ids.MainApp.screen_message_text == self.root.ids.MainApp.screen_message_driver_connection or \
                   self.root.ids.MainApp.screen_message_text ==  self.root.ids.MainApp.screen_message_ABP or \
                   self.root.ids.MainApp.screen_message_text == self.root.ids.MainApp.screen_message_I2C:
                    self.uiDict['sm'].current = 'screen_send'

        # если ошибки
        else:
            self.uiDict['sm'].current = 'screen_message'
            # если ошибка  показываем экран сообщения и соответсвующий текст
            if self.Status.uint8_t_trans_ok & 1 == 1: # нет 220В
                self.root.ids.MainApp.screen_message_text = self.root.ids.MainApp.screen_message_220V
                self.root.ids.MainApp.background_color_faza_1 = self.root.ids.MainApp.background_color_red

            if self.Status.uint8_t_trans_ok & 2 == 2: # нет 380В
                self.root.ids.MainApp.screen_message_text = self.root.ids.MainApp.screen_message_380V
                self.root.ids.MainApp.background_color_faza_3 = self.root.ids.MainApp.background_color_red

            if self.Status.uint8_t_trans_ok & 4 == 4: # Перегрузка по току
                self.root.ids.MainApp.screen_message_text = self.root.ids.MainApp.screen_message_current_overload

            if self.Status.uint8_t_trans_ok & 8 == 8: # перегрев
                self.root.ids.MainApp.screen_message_text = self.root.ids.MainApp.screen_message_overheating

            if self.Status.uint8_t_trans_ok & 16 == 16: # нет связи с драйвером
                self.root.ids.MainApp.screen_message_text = self.root.ids.MainApp.screen_message_driver

            if self.Status.uint8_t_trans_ok & 32 == 32: # авария в драйвере
                self.root.ids.MainApp.screen_message_text = self.root.ids.MainApp.screen_message_driver_connection

            if self.Status.uint8_t_trans_ok & 64 == 64: # АВР заблокирован
                self.root.ids.MainApp.screen_message_text = self.root.ids.MainApp.screen_message_ABP

            if self.Status.uint8_t_trans_ok & 128 == 128: # ошибка шины I2C
                self.root.ids.MainApp.screen_message_text = self.root.ids.MainApp.screen_message_I2C

#------ обновление интерфейса --------------
    def interface_update(self):

        if self.Status.uint8_t_trx_role == 0:  # резервный
            self.root.ids.MainApp.background_color_active = self.root.ids.MainApp.background_color_green
            self.root.ids.MainApp.background_active_text = "Резервный"
        if self.Status.uint8_t_trx_role == 1:  # активен
            self.root.ids.MainApp.background_color_active = self.root.ids.MainApp.background_color_green
            self.root.ids.MainApp.background_active_text = "Основной"
        if self.Status.uint8_t_trx_role == 2:  # отключен от АВР
            self.root.ids.MainApp.background_color_active = self.root.ids.MainApp.background_color_red
            self.root.ids.MainApp.background_active_text = "Отключен от АВР"

        # состояние антенн 0 - отключена, 1 - подключена, -1 - не задействована, 2 - обрыв, 3 замыкание
        # Антенна 1
        if self.Status.int8_t_ant_state[0] == -1:  # не используется
            self.root.ids.MainApp.background_color_ant1 = self.root.ids.MainApp.background_color_yellow
            self.root.ids.MainApp.antenna_state_1 = self.root.ids.MainApp.antenna_state_absent
        if self.Status.int8_t_ant_state[0] == 0: # отключена
            self.root.ids.MainApp.background_color_ant1 = self.root.ids.MainApp.background_color_yellow
            self.root.ids.MainApp.antenna_state_1 = self.root.ids.MainApp.antenna_state_no
        if self.Status.int8_t_ant_state[0] == 1: # антенна подключна
            self.root.ids.MainApp.background_color_ant1 = self.root.ids.MainApp.background_color_green
            self.root.ids.MainApp.antenna_state_1 = self.root.ids.MainApp.antenna_state_ok
        if self.Status.int8_t_ant_state[0] == 2: # обрыв
            self.root.ids.MainApp.background_color_ant1 = self.root.ids.MainApp.background_color_red
            self.root.ids.MainApp.antenna_state_1 = self.root.ids.MainApp.antenna_state_breakage
        if self.Status.int8_t_ant_state[0] == 3: # короткое замыкание
            self.root.ids.MainApp.background_color_ant1 = self.root.ids.MainApp.background_color_red
            self.root.ids.MainApp.antenna_state_1 = self.root.ids.MainApp.antenna_state_short_circuit

        # Антенна 2
        if self.Status.int8_t_ant_state[1] == -1:  # не используется
            self.root.ids.MainApp.background_color_ant2 = self.root.ids.MainApp.background_color_yellow
            self.root.ids.MainApp.antenna_state_2 = self.root.ids.MainApp.antenna_state_absent
        if self.Status.int8_t_ant_state[1] == 0: # отключена
            self.root.ids.MainApp.background_color_ant2 = self.root.ids.MainApp.background_color_yellow
            self.root.ids.MainApp.antenna_state_2 = self.root.ids.MainApp.antenna_state_no
        if self.Status.int8_t_ant_state[1] == 1: # антенна подключна
            self.root.ids.MainApp.background_color_ant2 = self.root.ids.MainApp.background_color_green
            self.root.ids.MainApp.antenna_state_2 = self.root.ids.MainApp.antenna_state_ok
        if self.Status.int8_t_ant_state[1] == 2: # обрыв
            self.root.ids.MainApp.background_color_ant2 = self.root.ids.MainApp.background_color_red
            self.root.ids.MainApp.antenna_state_2 = self.root.ids.MainApp.antenna_state_breakage
        if self.Status.int8_t_ant_state[1] == 3: # короткое замыкание
            self.root.ids.MainApp.background_color_ant2 = self.root.ids.MainApp.background_color_red
            self.root.ids.MainApp.antenna_state_2 = self.root.ids.MainApp.antenna_state_short_circuit

        # Антенна 3
        if self.Status.int8_t_ant_state[2] == -1:  # не используется
            self.root.ids.MainApp.background_color_ant3 = self.root.ids.MainApp.background_color_yellow
            self.root.ids.MainApp.antenna_state_3 = self.root.ids.MainApp.antenna_state_absent
        if self.Status.int8_t_ant_state[2] == 0: # отключена
            self.root.ids.MainApp.background_color_ant3 = self.root.ids.MainApp.background_color_yellow
            self.root.ids.MainApp.antenna_state_3 = self.root.ids.MainApp.antenna_state_no
        if self.Status.int8_t_ant_state[2] == 1: # антенна подключна
            self.root.ids.MainApp.background_color_ant3 = self.root.ids.MainApp.background_color_green
            self.root.ids.MainApp.antenna_state_3 = self.root.ids.MainApp.antenna_state_ok
        if self.Status.int8_t_ant_state[2] == 2: # обрыв
            self.root.ids.MainApp.background_color_ant3 = self.root.ids.MainApp.background_color_red
            self.root.ids.MainApp.antenna_state_3 = self.root.ids.MainApp.antenna_state_breakage
        if self.Status.int8_t_ant_state[2] == 3: # короткое замыкание
            self.root.ids.MainApp.background_color_ant3 = self.root.ids.MainApp.background_color_red
            self.root.ids.MainApp.antenna_state_3 = self.root.ids.MainApp.antenna_state_short_circuit

        #  Антенна 4
        if self.Status.int8_t_ant_state[3] == -1:  # не используется
            self.root.ids.MainApp.background_color_ant4 = self.root.ids.MainApp.background_color_yellow
            self.root.ids.MainApp.antenna_state_4 = self.root.ids.MainApp.antenna_state_absent
        if self.Status.int8_t_ant_state[3] == 0: # отключена
            self.root.ids.MainApp.background_color_ant4 = self.root.ids.MainApp.background_color_yellow
            self.root.ids.MainApp.antenna_state_4 = self.root.ids.MainApp.antenna_state_no
        if self.Status.int8_t_ant_state[3] == 1: # антенна подключна
            self.root.ids.MainApp.background_color_ant4 = self.root.ids.MainApp.background_color_green
            self.root.ids.MainApp.antenna_state_4 = self.root.ids.MainApp.antenna_state_ok
        if self.Status.int8_t_ant_state[3] == 2: # обрыв
            self.root.ids.MainApp.background_color_ant4 = self.root.ids.MainApp.background_color_red
            self.root.ids.MainApp.antenna_state_4 = self.root.ids.MainApp.antenna_state_breakage
        if self.Status.int8_t_ant_state[3] == 3: # короткое замыкание
            self.root.ids.MainApp.background_color_ant4 = self.root.ids.MainApp.background_color_red
            self.root.ids.MainApp.antenna_state_4 = self.root.ids.MainApp.antenna_state_short_circuit

        # название шахты
        self.root.ids.mine_name.text = self.Settings.char_MineName

        # 220V и 380V
        if (self.Settings.uint8_t_supp_voltage  == 0) and (self.root.ids.MainApp.screen_message_text != self.root.ids.MainApp.screen_message_220V):
            self.root.ids.MainApp.background_color_faza_1 = self.root.ids.MainApp.background_color_green
            self.root.ids.MainApp.background_color_faza_3 = self.root.ids.MainApp.background_color_grey
        if (self.Settings.uint8_t_supp_voltage == 1) and (self.root.ids.MainApp.screen_message_text != self.root.ids.MainApp.screen_message_220V):
            self.root.ids.MainApp.background_color_faza_1 = self.root.ids.MainApp.background_color_green
            self.root.ids.MainApp.background_color_faza_3 = self.root.ids.MainApp.background_color_green


        # обновление статуса и праметров антенн
        # ток
        self.root.ids.MainApp.ant1_current = str(round(self.Status.float_ia[0], 2))
        self.root.ids.MainApp.ant2_current = str(round(self.Status.float_ia[1], 2))
        self.root.ids.MainApp.ant3_current = str(round(self.Status.float_ia[2], 2))
        self.root.ids.MainApp.ant4_current = str(round(self.Status.float_ia[3], 2))

        # мощность
        self.root.ids.MainApp.ant1_P = str(round(self.Status.float_pa[0], 2))
        self.root.ids.MainApp.ant2_P = str(round(self.Status.float_pa[1], 2))
        self.root.ids.MainApp.ant3_P = str(round(self.Status.float_pa[2], 2))
        self.root.ids.MainApp.ant4_P = str(round(self.Status.float_pa[3], 2))

        # сопротивление
        self.root.ids.MainApp.ant1_R = str(round(self.Status.float_ra[0], 3)) +'  ( ' + str(round(self.Status.float_r[0], 3)) + ' )'
        self.root.ids.MainApp.ant2_R = str(round(self.Status.float_ra[1], 3)) +'  ( ' + str(round(self.Status.float_r[1], 3)) + ' )'
        self.root.ids.MainApp.ant3_R = str(round(self.Status.float_ra[2], 3)) +'  ( ' + str(round(self.Status.float_r[2], 3)) + ' )'
        self.root.ids.MainApp.ant4_R = str(round(self.Status.float_ra[3], 3)) +'  ( ' + str(round(self.Status.float_r[3], 3)) + ' )'

        # индуквтиность
        self.root.ids.MainApp.ant1_L = str(round(self.Status.float_l[0], 3)) + '  ( '+ str(round(self.Settings.float_l[0], 3)) + ' )'
        self.root.ids.MainApp.ant2_L = str(round(self.Status.float_l[1], 3)) + '  ( '+ str(round(self.Settings.float_l[1], 3)) + ' )'
        self.root.ids.MainApp.ant3_L = str(round(self.Status.float_l[2], 3)) + '  ( '+ str(round(self.Settings.float_l[2], 3)) + ' )'
        self.root.ids.MainApp.ant4_L = str(round(self.Status.float_l[3], 3)) + '  ( '+ str(round(self.Settings.float_l[3], 3)) + ' )'

        # ёмкость
        self.root.ids.MainApp.ant1_C = str(round(self.Settings.float_c[0], 3)) + '  ( '+ str(round(self.Status.float_c[0], 3)) + ' )'
        self.root.ids.MainApp.ant2_C = str(round(self.Settings.float_c[1], 3)) + '  ( '+ str(round(self.Status.float_c[1], 3)) + ' )'
        self.root.ids.MainApp.ant3_C = str(round(self.Settings.float_c[2], 3)) + '  ( '+ str(round(self.Status.float_c[2], 3)) + ' )'
        self.root.ids.MainApp.ant4_C = str(round(self.Settings.float_c[3], 3)) + '  ( '+ str(round(self.Status.float_c[3], 3)) + ' )'

        # напряжение
        # Антена 1
        if self.Settings.uint8_t_ant_level[0] == 0:
            self.root.ids.MainApp.ant1_U = "Напряжение низкое"
        else:
            self.root.ids.MainApp.ant1_U = "Напряжение высокое"

        # Антена 2
        if self.Settings.uint8_t_ant_level[1] == 0:
            self.root.ids.MainApp.ant2_U = "Напряжение низкое"
        else:
            self.root.ids.MainApp.ant2_U = "Напряжение высокое"

        # Антена 3
        if self.Settings.uint8_t_ant_level[2] == 0:
            self.root.ids.MainApp.ant3_U = "Напряжение низкое"
        else:
            self.root.ids.MainApp.ant3_U = "Напряжение высокое"

        # Антена 4
        if self.Settings.uint8_t_ant_level[3] == 0:
            self.root.ids.MainApp.ant4_U = "Напряжение низкое"
        else:
            self.root.ids.MainApp.ant4_U = "Напряжение высокое"

        #  отображение ползунка - Длинна сообщения 22 бита
        if self.Settings.uint8_t_alarm_msg == 0:

            if self.Status.uint8_t_trans_state == 1:
                self.root.ids.MainApp.repeat_num = "Статус выполнения (" + str(self.Status.uint8_t_repeat_cur) + "/" + str(self.Settings.uint8_t_repeat_num) + ")"

            if self.Status.uint8_t_repeat_cur == 0:
                self.Status.uint8_t_repeat_cur = 1
            self.percent_transmit = round(self.Status.uint8_t_bit_num * 100 / (22))
            self.root.ids.MainApp.percent_transmit = str(self.percent_transmit)
            if self.percent_transmit > 0:
                if self.Status.uint8_t_trans_state == 1:
                    self.root.ids.progress_bar.opacity = 1
                    #if self.flag_tags == 0:
                    #if self.flag_tags == 1:
                    #print(self.Status.uint32_t_data)

                    # Сверка из файла

                    self.read_csv()

                    for i in range(0, len(self.Number_tag), 1):

                        if self.Status.uint32_t_data == self.Number_tag[i]:
                            self.root.ids.solution.text = str(self.Number_light[i])
                            break
                        else:
                            self.root.ids.solution.text = 'Номер отсутствует в базе'

                    # Если вызов метки то выводим другое в стаус бар
                    if self.flag_tags == 0:
                        self.root.ids.status_bar.text = "Вызов"
                    else:
                        if self.Status.uint32_t_data == 0xFFFFFFFF:
                            self.root.ids.status_bar.text = "Тестирование Тагов"
                            self.root.ids.solution.text = ''
                        else:
                            self.root.ids.status_bar.text = "Тест фонаря"
                            #self.root.ids.solution.text = str(self.Status.uint32_t_data)


                #if self.Status.uint8_t_trans_state == 0:
                #    if self.root.ids.status_bar.text != 'Номер отсутствует в базе':
                #        self.root.ids.status_bar.text = ""

            # очистка статус бара  если Alarm выключили
            if self.root.ids.status_bar.text == 'Аварийный вызов' or \
               self.root.ids.status_bar.text == 'Аварийный вызов (пауза)':
                    self.root.ids.status_bar.text = ''


            if self.percent_transmit > 90:
                if self.flag_tags == 1:
                    self.root.ids.status_bar.text = ''
                    self.root.ids.solution.text = ''
                    self.root.ids.progress_bar.opacity = 0
                    self.percent_transmit = 0
                if self.flag_tags == 0:
                    if self.percent_transmit == 100:
                        self.root.ids.status_bar.text = ''
                        self.root.ids.solution.text = ''
                        self.root.ids.progress_bar.opacity = 0
                        self.percent_transmit = 0
            # не доходит до 100% при контроле меток

        # Если авария
        if self.Settings.uint8_t_alarm_msg == 1:
            self.flag_alarm = 1
            self.alarm_time_counter += 1
            # если передатчик включен то Alarm передача сообщения
            if self.Status.uint8_t_trans_state == 1:
                self.root.ids.MainApp.repeat_num = "Статус выполнения"
                self.root.ids.status_bar.text = 'Аварийный вызов'
                self.root.ids.solution.text = ''
                self.root.ids.progress_bar.opacity = 1
                self.percent_transmit = round((self.alarm_time_counter  * 100) / self.Settings.uint16_t_alarm_time)
                self.root.ids.MainApp.percent_transmit = str(self.percent_transmit)
                if self.percent_transmit >= 98:
                    self.alarm_time_counter = 0
                    self.flag_alarm_pause = 1

            # если передатчик выключен то Alarm пауза
            if self.Status.uint8_t_trans_state == 0:
                self.flag_alarm_pause = 1
                self.root.ids.status_bar.text = 'Аварийный вызов (пауза)'
                self.root.ids.solution.text = ''
                self.root.ids.MainApp.repeat_num = "Статус выполнения"
                #self.alarm_time_counter += 1
                self.percent_transmit = round(self.alarm_time_counter * 100 / self.Settings.uint16_t_alarm_pause)
                self.root.ids.MainApp.percent_transmit = str(self.percent_transmit)
                if self.percent_transmit == 100:
                    self.flag_alarm_pause = 0

        # заглушка от преждевременного показываия статус бара
        if (self.Settings.uint8_t_alarm_msg == 0) and (self.root.ids.status_bar.text == 'Аварийный вызов'):
            self.root.ids.status_bar.text = ''


        # Управляет показывать или нет ползунок, если передача есть показать
        if self.Status.uint8_t_trans_state == 1:
            self.root.ids.progress_bar.opacity = 1
        else:
            if self.Status.uint8_t_trans_state == 2:
                self.root.ids.status_bar.text = 'Контроль'
                self.alarm_time_counter = 0
                self.root.ids.progress_bar.opacity = 0
                self.root.ids.MainApp.repeat_num = "Статус выполнения"
            if self.Status.uint8_t_trans_state == 0 and self.root.ids.status_bar.text == 'Контроль':
                self.root.ids.status_bar.text = ''
            if self.Status.uint8_t_trans_state == 0:
                #self.alarm_time_counter = 0
                self.percent_transmit = 0
                self.root.ids.progress_bar.opacity = 0

        # показать если пауза при аварии
        if self.flag_alarm_pause == 1:
            self.root.ids.progress_bar.opacity = 1
        else:
            self.root.ids.progress_bar.opacity = 0
            if (self.root.ids.status_bar.text == 'Аварийный вызов') or ( self.root.ids.status_bar.text == 'Аварийный вызов (пауза)'):
                self.root.ids.status_bar.text = ''
                self.root.ids.progress_bar.opacity = 0

        # если передача показать ползунок
        if self.Status.uint8_t_trans_state == 1:
            self.root.ids.progress_bar.opacity = 1

        # Если вызов окнчен
        if self.Status.uint8_t_trans_state == 0:
            if self.root.ids.status_bar.text == 'Вызов':
                self.root.ids.status_bar.text = ''
                self.root.ids.solution.text = ''
            if self.root.ids.status_bar.text == 'Номер отсутствует в базе':
                self.root.ids.progress_bar.opacity = 0
            if self.root.ids.status_bar.text == 'Введите номер':
                self.root.ids.progress_bar.opacity = 0


        # Выключение статус бара если контроль или пустое поле
        if self.root.ids.status_bar.text == '':
            self.root.ids.progress_bar.opacity = 0
        if self.root.ids.status_bar.text == 'Контроль':
            self.root.ids.progress_bar.opacity = 0

        if (self.Status.uint8_t_trans_state == 0) and (self.Settings.uint8_t_alarm_msg == 0):
            self.gui_count_sek += 1
            if self.gui_count_sek >= 30:
                self.gui_count_sek = 0
                self.root.ids.solution.text = ''
                self.root.ids.status_bar.text = 'Введите номер'
                self.percent_transmit = 0
                #self.root.ids.status_bar.text = ''

MainApp().run()

