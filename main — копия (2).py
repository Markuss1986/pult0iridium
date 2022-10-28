# Импорт kivy библиотек
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen

# Импорт системных библиотек
import sys
import os
import threading

# Импорт порльзовательских библиотек и классов
import crc
import RS485

# Библиотека для упаковки и распаковки бинарных данных(байт в инт и обратно)
import struct

# Импорт отображения даты и времени и 1с задержки
from time import strftime
from datetime import date
from kivy.clock import Clock
import time

# Импорт библиотек для работы с USB
from kivy.utils import platform
if platform == 'android':
    from usb4a import usb
    from usbserial4a import serial4a

else:
    from serial.tools import list_ports
    from serial import Serial

# Импорт библиотек для считыванмия из файла
import csv


# Нужно прописать в системных переменных путь до Java.(JAVA_HOME и PATH)
# https://pyjnius.readthedocs.io/en/stable/installation.html#installation-for-windows
#from jnius import autoclass
#if platform == 'android':
#    try:
#        Environment = autoclass('android.os.Environment')
#        sdpath = Environment.getExternalStorageDirectory()
#    # Not on Android
#    except:
#        sdpath = App.get_running_app().user_data_dir


class HomePage(MDScreen):
    'Home Page'

class MainApp(MDApp):

    def __init__(self, *args, **kwargs):
        self.uiDict = {}
        self.device_name_list = []
        self.serial_port = None
        self.read_thread = None
        self.port_thread_lock = threading.Lock()
        self.text_btn = ""
        self.sol_text = ""
        super(MainApp, self).__init__(*args, **kwargs)


        # Инициализация времени
        self.sw_started= False
        self.sw_seconds = 0
        self.Settings = RS485.SettingsParametrs()
        self.Status = RS485.StatusSystem()
        self.percent_transmit = 0
        self.flag_alarm_pause = 0
        self.alarm_time_counter = 0
        self.flag_tags = 0
        self.flag_alarm = 0
        self.flag_thread = False
        self.flag_thread_on = 0

        self.Number_light = []
        self.Number_person = []
        self.serial_flag = 0
        self.device_name_list = []
        self.received_msg = 0
        self.com_count = 0

        #self.init_com()

        if platform == 'android':
            sdpath = MainApp.get_running_app().user_data_dir
        else:
            sdpath = os.path.dirname(os.path.abspath(__file__))
        print(sdpath)

        # считываем из файла
        #with open(sdpath + '/test.csv', newline='') as csvfile:
        #    reader = csv.DictReader(csvfile)
        #    for row in reader:
        #        self.Number_light.append (int(row['Number_light']))
        #        self.Number_person.append ( int(row['Number_person']))

    def build(self):
        Builder.load_file('MainApp.kv')
        return HomePage()

    def on_btn_screen_1(self):
        self.uiDict['sm'].current = 'screen_send'

    # Active button 2 display screen_send
    def on_btn_screen_2(self):
        self.uiDict['sm'].current = 'enter_menu'

    # Active button 3 display command
    def on_btn_screen_3(self):
        self.uiDict['sm'].current = 'Command'

    def on_btn_screen_status(self):
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
        if self.Settings.uint8_t_alarm_msg == 0:
            if self.root.ids.MainApp.antenna_state_1 == self.root.ids.MainApp.antenna_state_ok:
                # Выключаем антенну 1
                self.write_rs485(b'\x30\x00\x00\x00\x00' + crc.crc_stm32(b'\x30\x00\x00\x00' + b'\x00\x00\x00\x00'))
            if self.root.ids.MainApp.antenna_state_1 == self.root.ids.MainApp.antenna_state_no:
                # Включаем антенну 1
                self.write_rs485(b'\x30\x01\x00\x00\x00' + crc.crc_stm32(b'\x30\x00\x00\x00' + b'\x01\x00\x00\x00'))

    def on_btn_turn_antenna_2(self):
        if self.Settings.uint8_t_alarm_msg == 0:
            if self.root.ids.MainApp.antenna_state_2 == self.root.ids.MainApp.antenna_state_ok:
               # Выключаем антенну 2
                self.write_rs485(b'\x31\x00\x00\x00\x00' + crc.crc_stm32(b'\x31\x00\x00\x00' + b'\x00\x00\x00\x00'))
            if self.root.ids.MainApp.antenna_state_2 == self.root.ids.MainApp.antenna_state_no:
                # Включаем антенну 2
                self.write_rs485(b'\x31\x01\x00\x00\x00' + crc.crc_stm32(b'\x31\x00\x00\x00' + b'\x01\x00\x00\x00'))

    def on_btn_turn_antenna_3(self):
        if self.Settings.uint8_t_alarm_msg == 0:
            if self.root.ids.MainApp.antenna_state_3 == self.root.ids.MainApp.antenna_state_ok:
                # Выключаем антенну 3
                self.write_rs485(b'\x32\x00\x00\x00\x00' + crc.crc_stm32(b'\x32\x00\x00\x00' + b'\x00\x00\x00\x00'))
            if self.root.ids.MainApp.antenna_state_3 == self.root.ids.MainApp.antenna_state_no:
                # Включаем антенну 3
                self.write_rs485(b'\x32\x01\x00\x00\x00' + crc.crc_stm32(b'\x32\x00\x00\x00' + b'\x01\x00\x00\x00'))

    def on_btn_turn_antenna_4(self):
        if self.Settings.uint8_t_alarm_msg == 0:
            if self.root.ids.MainApp.antenna_state_4 == self.root.ids.MainApp.antenna_state_ok:
                # Выключаем антенну 4
                self.write_rs485(b'\x33\x00\x00\x00\x00' + crc.crc_stm32(b'\x33\x00\x00\x00' + b'\x00\x00\x00\x00'))
            if self.root.ids.MainApp.antenna_state_4 == self.root.ids.MainApp.antenna_state_no:
                # Включаем антенну 4
                self.write_rs485(b'\x33\x01\x00\x00\x00' + crc.crc_stm32(b'\x33\x00\x00\x00' + b'\x01\x00\x00\x00'))


    def on_btn_turn_on_alarm(self):
        self.uiDict['sm'].current = 'screen_send'
        self.write_rs485(b'\x2B\x01\x00\x00\x00' + crc.crc_stm32(b'\x2B\x00\x00\x00' + b'\x01\x00\x00\x00'))
        self.flag_alarm_pause == 0
        self.flag_alarm = 1

    def on_btn_turn_off_alarm(self):
        self.write_rs485(b'\x2B\x00\x00\x00\x00' + crc.crc_stm32(b'\x2B\x00\x00\x00' + b'\x00\x00\x00\x00'))
        self.flag_alarm = 0
        self.flag_alarm_pause = 0


    def on_btn_turn_on_tags(self):
        self.flag_tags = 1
        self.root.ids.status_bar.text = 'Введите номер метки'
        self.root.ids.break_button.text = 'Тест всех меток'
        self.root.ids.solution.text = ''
        self.uiDict['sm'].current = 'screen_send'

    def on_btn_turn_off_tags(self):
        self.flag_tags = 0
        self.root.ids.break_button.text = 'Прервать передачу'
        self.root.ids.status_bar.text = ''
        self.root.ids.solution.text = ''
        self.uiDict['sm'].current = 'screen_send'

    def on_btn_break_up(self):
        if self.Settings.uint8_t_alarm_msg == 0:
            if self.Status.uint8_t_trans_state == 1:
                # Оправка по RS485 строки прекращения передачи
                self.write_rs485(b'\x21\x00\x00\x00\x00' + crc.crc_stm32(b'\x21\x00\x00\x00'+ b'\x00\x00\x00\x00'))
                self.root.ids.progress_bar.opacity = 0
                # сброс ползунка
                self.root.ids.MainApp.percent_transmit = str(0)
                self.root.ids.status_bar.text = 'Передача прервана'
                self.flag_alarm_pause = 0

            # Если включено тестирование меток
            if self.flag_tags == 1:
                # Тест всех меток
                U2CT_DATA = b'\x0A' + struct.pack("<I", 4294967295) + crc.crc_stm32(b'\x0A\x00\x00\x00'+ struct.pack("<I", 4294967295))
                U2CT_TEST_TAG = b'\x2E\x01\x00\x00\x00' + crc.crc_stm32(b'\x2E\x00\x00\x00' + b'\x01\x00\x00\x00')
                Command_tags = U2CT_DATA + U2CT_TEST_TAG
                self.write_rs485(Command_tags)
                self.root.ids.status_bar.text = 'Диагностика'



    # Метод обработки нажатий кнопок отправить, очистить и цифр
    def on_button_press(self, text_btn, sol_text):
        if self.Settings.uint8_t_alarm_msg == 0:
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

                # Сверка из файла
                for i in range(0, len(self.Number_light), 1):
                    if self.Number_light[i] == int(sol_text):
                        sol_text = self.Number_person[i]
                        if self.flag_tags == 0:
                            # Оправка запрос фонаря
                            U2CT_DATA = b'\x0A' + struct.pack("<I", int(sol_text)) + crc.crc_stm32(b'\x0A\x00\x00\x00'+ struct.pack("<I", int(sol_text)))
                            U2CT_COMMAND = b'\x2F\x01\x00\x00\x00'  + crc.crc_stm32(b'\x2F\x00\x00\x00'+ b'\x01\x00\x00\x00')
                            U2CT_ENABLE = b'\x21\x01\x00\x00\x00' + crc.crc_stm32(b'\x21\x00\x00\x00'+ b'\x01\x00\x00\x00')
                            command = U2CT_DATA + U2CT_COMMAND + U2CT_ENABLE
                            self.write_rs485(command)

                        # Если включено тестирование меток, отправляем номер метки
                        if self.flag_tags == 1:
                            U2CT_DATA = b'\x0A' + struct.pack("<I", int(sol_text)) + crc.crc_stm32(b'\x0A\x00\x00\x00'+ struct.pack("<I", int(sol_text)))
                            U2CT_TEST_TAG = b'\x2E\x00\x00\x00\x00' + crc.crc_stm32(b'\x2E\x00\x00\x00' + b'\x00\x00\x00\x00')
                            Command_tags = U2CT_DATA + U2CT_TEST_TAG
                            self.write_rs485(Command_tags)
                        break

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
            return ''

    def init_com(self):

        # For Android
        if platform == 'android':
            usb_device_list = usb.get_usb_device_list()
            self.device_name_list = [device.getDeviceName() for device in usb_device_list]
            if len(self.device_name_list) >= 1:
                    # Обнуление для инициализации
                if self.com_count < 2:  # выключаем Com port пока переназначем
                    self.com_count = 1
                    try:
                        self.serial_port = serial4a.get_serial_port(usb_device_list[-1].getDeviceName(), 57600, 8, 'N', 1,timeout=1)
                        self.flag_thread = True # включаем Com port пока переназначем

                    except:
                        a=5
                        #self.flag_thread = False
                        #self.serial_port = None
                        #self.flag_thread = True
            #else:
                #self.flag_thread = False
                #self.serial_port = None
            time.sleep(5)

        # For Win and Linux
        else:
            # Setup COM port
            usb_device_list = list_ports.comports()
            if len(usb_device_list) >= 1:
                self.flag_thread = True
                self.device_name_list = [port.device for port in usb_device_list]
                # Обнуление для инициализации
                if not self.serial_port:
                    self.serial_port = Serial(self.device_name_list[-1], 57600, 8, 'N', 1, timeout=1)


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
                        a=6
                        #self.serial_port = None



    def read_msg_thread(self):
        while True:
            self.root.ids.MainApp.background_color_ant3 = self.root.ids.MainApp.background_color_red
            self.root.ids.MainApp.background_color_ant4 = self.root.ids.MainApp.background_color_red
            self.root.ids.MainApp.background_color_ant2 = self.root.ids.MainApp.background_color_red
            self.root.ids.MainApp.background_color_ant1 = self.root.ids.MainApp.background_color_red
            while self.flag_thread:
                try:
                    with self.port_thread_lock:
                        if len(self.device_name_list) >= 1:
                            # Если приняли 402 байты - 2 структуры
                            if self.serial_port:
                                if self.serial_port.in_waiting == 402:
                                    self.uiDict['sm'].current = 'screen_send'

                                    # read to buffer
                                    try:
                                        received_msg = self.serial_port.read(self.serial_port.in_waiting)
                                    # print('Длина принятого сообщения  = ',len(received_msg))

                                        RS485.SettingsParametrs.read_Settings(self.Settings,received_msg, 1)
                                        RS485.StatusSystem.read_Status(self.Status,received_msg, 190)
                                    except:
                                        a=5


                                    # Обновление Флага интерфейса
                                if self.serial_port.in_waiting > 402:
                                    # чистим буффер в зашлущку
                                    trash = self.serial_port.in_waiting

                except Exception as ex:
                    #self.serial_port = None
                    raise ex
        # time.sleep(0.3)



    # -------------------Time---------------------------
    def update_time(self, nap):

        if self.sw_started:
            self.sw_seconds += nap
            minutes, seconds = divmod(self.sw_seconds, 60)

        self.root.ids.time.text = strftime('%H.%M.%S')
        self.root.ids.date.text = strftime('%d.%m.%Y')

        self.init_com()

        self.interface_update()


        # ------------------interface-----------------
        #self.interface_update(self.Settings,self.Status)

        # Screen No Connection if no comport
        if platform == 'android':
            usb_device_list = usb.get_usb_device_list()
            self.device_name_list = [device.getDeviceName() for device in usb_device_list]
            if len(self.device_name_list) >= 1:
                # Убираем экран нет подключения
                if self.uiDict['sm'].current == 'screen_no_connection' or self.uiDict['sm'].current == 'probe':
                    self.uiDict['sm'].current = 'screen_send'
                    self.root.ids.MainApp.background_color_connection = self.root.ids.MainApp.background_color_green
            else:
                self.uiDict['sm'].current = 'screen_no_connection'
                self.interface_update()
                self.root.ids.MainApp.background_color_ant1 = self.root.ids.MainApp.background_color_yellow
                self.root.ids.MainApp.background_color_ant2 = self.root.ids.MainApp.background_color_yellow
                self.root.ids.MainApp.background_color_ant3 = self.root.ids.MainApp.background_color_yellow
                self.root.ids.MainApp.background_color_ant4 = self.root.ids.MainApp.background_color_yellow
                self.root.ids.MainApp.background_color_connection = self.root.ids.MainApp.background_color_red
        # Если Win or linux
        else:
            if len(list_ports.comports()) == 0:
                print(list_ports.comports())
                self.uiDict['sm'].current = 'screen_no_connection'
                self.root.ids.MainApp.background_color_connection = self.root.ids.MainApp.background_color_red
            else:
                print(self.serial_port)
                self.root.ids.MainApp.background_color_connection = self.root.ids.MainApp.background_color_green
                if self.uiDict['sm'].current == 'screen_no_connection' or self.uiDict['sm'].current == 'probe':
                    # Инициализируем Comport
                    #self.init_com()
                    self.uiDict['sm'].current = 'screen_send'


        # Запрос статуса
        CT_GET_STATUS = b'\x6F\x01\x00\x00\x00' + crc.crc_stm32(b'\x6F\x00\x00\x00' + b'\x01\x00\x00\x00')
        self.write_rs485(CT_GET_STATUS)

        # -----------------Com-----------------
        if self.flag_thread_on == 0 and self.flag_thread:
            self.flag_thread_on = 1
            # Включаем поток приема по RS485
            self.read_thread = threading.Thread(target=self.read_msg_thread)
            self.read_thread.start()


    def on_start(self):
        Clock.schedule_interval(self.update_time, 1)

    def time_screen(self):
        return date.today()

    def canvas_color(self,color):
        return color

    def interface_color(self,background_color):
        return background_color

    def interface_update(self):

        # состояние антенн 0 - отключена, 1 - подключена, -1 - не задействована, 2 - обрыв, 3 замыкание
        # Антенна 1
        if self.Status.int8_t_ant_state[0] == 1:
            self.root.ids.MainApp.background_color_ant1 = self.root.ids.MainApp.background_color_green
            self.root.ids.MainApp.antenna_state_1 = self.root.ids.MainApp.antenna_state_ok
        if (self.Status.int8_t_ant_state[0] == 0 or self.Status.int8_t_ant_state[0] == -1):
            self.root.ids.MainApp.background_color_ant1 = self.root.ids.MainApp.background_color_yellow
            self.root.ids.MainApp.antenna_state_1 = self.root.ids.MainApp.antenna_state_no
        if (self.Status.int8_t_ant_state[0] == 2 or self.Status.int8_t_ant_state[0] == 3):
            self.root.ids.MainApp.background_color_ant1 = self.root.ids.MainApp.background_color_red
            self.root.ids.MainApp.antenna_state_1 = self.root.ids.MainApp.antenna_state_alarm

        # Антенна 2
        if self.Status.int8_t_ant_state[1] == 1:
            self.root.ids.MainApp.background_color_ant2 = self.root.ids.MainApp.background_color_green
            self.root.ids.MainApp.antenna_state_2 = self.root.ids.MainApp.antenna_state_ok
        if (self.Status.int8_t_ant_state[1] == 0 or self.Status.int8_t_ant_state[1] == -1):
            self.root.ids.MainApp.background_color_ant2 = self.root.ids.MainApp.background_color_yellow
            self.root.ids.MainApp.antenna_state_2 = self.root.ids.MainApp.antenna_state_no
        if (self.Status.int8_t_ant_state[1] == 2 or self.Status.int8_t_ant_state[1] == 3):
            self.root.ids.MainApp.background_color_ant2 = self.root.ids.MainApp.background_color_red
            self.root.ids.MainApp.antenna_state_2 = self.root.ids.MainApp.antenna_state_alarm
        # Антенна 3
        if self.Status.int8_t_ant_state[2] == 1:
            self.root.ids.MainApp.background_color_ant3 = self.root.ids.MainApp.background_color_green
            self.root.ids.MainApp.antenna_state_3 = self.root.ids.MainApp.antenna_state_ok
        if (self.Status.int8_t_ant_state[2] == 0 or self.Status.int8_t_ant_state[2] == -1):
            self.root.ids.MainApp.background_color_ant3 = self.root.ids.MainApp.background_color_yellow
            self.root.ids.MainApp.antenna_state_3 = self.root.ids.MainApp.antenna_state_no
        if (self.Status.int8_t_ant_state[2] == 2 or self.Status.int8_t_ant_state[2] == 3):
            self.root.ids.MainApp.background_color_ant3 = self.root.ids.MainApp.background_color_red
            self.root.ids.MainApp.antenna_state_3 = self.root.ids.MainApp.antenna_state_alarm
        #  Антенна 4
        if self.Status.int8_t_ant_state[3] == 1:
            self.root.ids.MainApp.background_color_ant4 = self.root.ids.MainApp.background_color_green
            self.root.ids.MainApp.antenna_state_4 = self.root.ids.MainApp.antenna_state_ok
        if (self.Status.int8_t_ant_state[3] == 0 or self.Status.int8_t_ant_state[3] == -1):
            self.root.ids.MainApp.background_color_ant4 = self.root.ids.MainApp.background_color_yellow
            self.root.ids.MainApp.antenna_state_4 = self.root.ids.MainApp.antenna_state_no
        if (self.Status.int8_t_ant_state[3] == 2 or self.Status.int8_t_ant_state[3] == 3):
            self.root.ids.MainApp.background_color_ant4 = self.root.ids.MainApp.background_color_red
            self.root.ids.MainApp.antenna_state_4 = self.root.ids.MainApp.antenna_state_alarm

        # название шахты
        self.root.ids.mine_name.text = self.Settings.char_MineName

        # 220V и 380V
        if (self.Settings.uint8_t_supply_level  == 0):
            self.root.ids.MainApp.background_color_faza_1 = self.root.ids.MainApp.background_color_green
            self.root.ids.MainApp.background_color_faza_3 = self.root.ids.MainApp.background_color_red
        else:
            self.root.ids.MainApp.background_color_faza_1 = self.root.ids.MainApp.background_color_red
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
        self.root.ids.MainApp.ant1_R = str(round(self.Status.float_ra[0], 3))
        self.root.ids.MainApp.ant2_R = str(round(self.Status.float_ra[1], 3))
        self.root.ids.MainApp.ant3_R = str(round(self.Status.float_ra[2], 3))
        self.root.ids.MainApp.ant4_R = str(round(self.Status.float_ra[3], 3))

        # индуквтиность
        self.root.ids.MainApp.ant1_L = str(round(self.Status.float_l[0], 3))
        self.root.ids.MainApp.ant2_L = str(round(self.Status.float_l[1], 3))
        self.root.ids.MainApp.ant3_L = str(round(self.Status.float_l[2], 3))
        self.root.ids.MainApp.ant4_L = str(round(self.Status.float_l[3], 3))

        # ёмкость
        self.root.ids.MainApp.ant1_C = str(round(self.Status.float_c[0], 3))
        self.root.ids.MainApp.ant2_C = str(round(self.Status.float_c[1], 3))
        self.root.ids.MainApp.ant3_C = str(round(self.Status.float_c[2], 3))
        self.root.ids.MainApp.ant4_C = str(round(self.Status.float_c[3], 3))

        # напряжение
        # self.root.ids.MainApp.ant1_C = str(self.Status.float_c[0][0])
        # self.root.ids.MainApp.ant2_C = str(self.Status.float_c[1][0])
        # self.root.ids.MainApp.ant3_C = str(self.Status.float_c[2][0])
        # self.root.ids.MainApp.ant4_C = str(self.Status.float_c[3][0])

        # Длинна сообщения 22 бита
        if self.Settings.uint8_t_alarm_msg == 0:
            self.root.ids.progress_bar.opacity = 1
            if self.Status.uint8_t_repeat_cur == 0:
                self.Status.uint8_t_repeat_cur = 1
            self.percent_transmit = round(self.Status.uint8_t_bit_num * 100 / (22 * self.Status.uint8_t_repeat_cur))
            self.root.ids.MainApp.percent_transmit = str(self.percent_transmit)
            if self.percent_transmit > 0:
                if self.Status.uint8_t_trans_state == 1:
                    #if self.flag_tags == 0:
                    #if self.flag_tags == 1:
                    #print(self.Status.uint32_t_data)
                    # Сверка из файла
                    for i in range(0, len(self.Number_person), 1):

                        if self.Status.uint32_t_data == self.Number_person[i]:
                            self.root.ids.solution.text = str(self.Number_light[i])
                            break
                        else:
                            self.root.ids.solution.text = ''

                    self.root.ids.status_bar.text = "Передача сообщения"


            if self.percent_transmit > 90:
                if self.flag_tags == 1:
                    self.root.ids.status_bar.text = ''
                    self.root.ids.solution.text = ''
                    self.root.ids.progress_bar.opacity = 0
                if self.flag_tags == 0:
                    if self.percent_transmit == 100:

                        self.root.ids.status_bar.text = ''
                        self.root.ids.solution.text = ''
                        self.root.ids.progress_bar.opacity = 0
            # не доходит до 100% при контроле меток

        # Если авария
        if self.Settings.uint8_t_alarm_msg == 1:
            self.flag_alarm = 1
            self.root.ids.progress_bar.opacity = 1
            # если передатчик включен то Alarm передача сообщения
            if self.Status.uint8_t_trans_state == 1:
                self.root.ids.status_bar.text = 'Авария (отправка сообщения)'
                self.percent_transmit = round(self.Status.uint8_t_bit_num * 100 / self.Settings.uint16_t_alarm_time)
                self.root.ids.MainApp.percent_transmit = str(self.percent_transmit)
                if self.percent_transmit >= 90:
                    self.alarm_time_counter = 0
                    self.flag_alarm_pause = 1

            # если передатчик выключен то Alarm пауза
            if self.Status.uint8_t_trans_state == 0:
                self.root.ids.status_bar.text = 'Авария (пауза)'
                self.alarm_time_counter += 1
                self.percent_transmit = round(self.alarm_time_counter * 100 / self.Settings.uint16_t_alarm_pause)
                self.root.ids.MainApp.percent_transmit = str(self.percent_transmit)
                if self.percent_transmit == 100:
                    self.flag_alarm_pause = 0


        # заглушка от преждевременного показываия статус бара
        if (self.Settings.uint8_t_alarm_msg == 0) and (self.root.ids.status_bar.text == 'Авария (отправка сообщения)'):
            self.root.ids.status_bar.text == ''

        # Управляет показывать или пнет ползунок, если передача есть показать
        if self.Status.uint8_t_trans_state == 1:
            self.root.ids.progress_bar.opacity = 1
        else:
            if self.Status.uint8_t_trans_state == 2:
                self.root.ids.status_bar.text = 'Диагностика'

            # показать если пауза при аварии
            if self.flag_alarm_pause == 1:
                self.root.ids.progress_bar.opacity = 1
            else:
                self.root.ids.progress_bar.opacity = 0
                if (self.root.ids.status_bar.text == 'Авария (отправка сообщения)') or ( self.root.ids.status_bar.text == 'Авария (пауза)'):
                    self.root.ids.status_bar.text = ''

MainApp().run()

