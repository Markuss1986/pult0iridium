import struct

class SettingsParametrs:
    def __init__(self, *args, **kwargs):
        self.uint16_t_f1 = 0
        self.uint16_t_f2 = 0
        self. uint16_t_br = 0
        self.uint8_t_deadtime = 0
        self.uint8_t_overlap = 0
        self.uint16_t_time_limit = 0
        self.uint16_t_diag_period = 0
        self.uint8_t_current_limit_a = 0
        self.uint8_t_overtick = 0
        self.float_c = [0,0,0,0]
        self.float_l = [0,0,0,0]
        self.float_r = [0,0,0,0]
        self.uint8_t_i_break = 0
        self.uint8_t_i_fuse = 0
        self.uint8_t_repeat_num = 0
        self.uint8_t_enable = 0
        self.uint8_t_mode = 0
        self.uint8_t_soft_start = 0
        self.uint8_t_current_limit = 0
        self.uint8_t_diag = 0
        self.uint8_t_cap = 0
        self.uint8_t_modulation = 0
        self.uint8_t_code_mode = 0
        self.uint8_t_overload_mode = 0
        self.uint8_t_supp_voltage = 0
        self.uint8_t_alarm_msg = int(0)
        self.uint8_t_test_tag = 0
        self.uint8_t_command = 0
        self.int8_t_antenna  = [0,0,0,0]
        self.uint8_t_ant_level = [0,0,0,0]
        self.uint16_t_turns_ant = [0,0,0,0]
        self.uint16_t_turns_prim = 0
        self.uint8_t_supply_level = 0
        self.uint8_t_standby = 0
        self.uint16_t_alarm_pause = 0
        self.uint16_t_alarm_time = 0
        self.LogLevel_Type_log_level = 0
        self.uint8_t_temp_level1_fanon = 0
        self.uint8_t_temp_level1_fanoff = 0
        self.uint8_t_temp_level2_fanon = 0
        self.uint8_t_temp_level2_fanoff = 0
        self.uint8_t_temp_halt_level = 0
        self.uint8_t_dhcp = 0
        self.uint8_t_IP_ADDRESS = [0,0,0,0]
        self.uint8_t_NETMASK_ADDRESS = [0,0,0,0]
        self.uint8_t_GATEWAY_ADDRESS = [0,0,0,0]
        self.char_MineName = 'Название шахты'
        self.float_limit_R_status = 0
        self.float_limit_L_status = 0
        self.float_limit_C_status = 0
        self.uint8_t_PIN_LVL = 0
        self.uint16_t_PIN_100 = 0
        self.uint16_t_PIN_150 = 0
        self.uint16_t_PIN_500 = 0

    def read_Settings(self,received_msg,i):
        self.uint16_t_f1 = int.from_bytes(received_msg[i:(i+0x01) + 1], 'little')
        self.uint16_t_f2 = int.from_bytes(received_msg[(i+0x02):(i+0x03) + 1], 'little')
        self.uint16_t_br = int.from_bytes(received_msg[(i+0x04):(i+0x05) + 1], 'little')
        self.uint8_t_deadtime = received_msg[i+0x06]
        self.uint8_t_overlap = received_msg[i+0x07]
        self.uint16_t_time_limit = int.from_bytes(received_msg[(i+0x08):(i+0x09) + 1],'little')
        self.uint16_t_diag_period = int.from_bytes(received_msg[(i+0x0A):(i+0x0B) + 1], 'little')
        self.uint8_t_current_limit_a = received_msg[i+0x0C]
        self.uint8_t_overtick = received_msg[i+0x0D]
        self.float_c = [struct.unpack("<f", received_msg[(i+0x10):(i+0x13) + 1])[0], struct.unpack("<f", received_msg[(i+0x14):(i+0x17)  + 1])[0],
                   struct.unpack("<f", received_msg[(i+0x18):(i+0x1B)  + 1])[0], struct.unpack("<f", received_msg[(i+0x1C):(i+0x1F) + 1])[0]]
        self.float_l = [struct.unpack("<f", received_msg[(i+0x20):(i+0x23) + 1])[0], struct.unpack("<f", received_msg[(i+0x24):(i+0x27) + 1])[0],
                   struct.unpack("<f", received_msg[(i+0x28):(i+0x2B) + 1])[0], struct.unpack("<f", received_msg[(i+0x2C):(i+0x2F) + 1])[0]]
        self.float_r = [struct.unpack("<f", received_msg[(i+0x30):(i+0x33) + 1])[0], struct.unpack("<f", received_msg[(i+0x34):(i+0x37) + 1])[0],
                   struct.unpack("<f", received_msg[(i+0x38):(i+0x3B) + 1])[0], struct.unpack("<f", received_msg[(i+0x3C):(i+0x3F) + 1])[0]]
        self.uint8_t_i_break = list(received_msg[(i+0x40):(i+0x43) + 1])
        self.uint8_t_i_fuse = list(received_msg[(i+0x44):(i+0x47) + 1])
        self.uint8_t_repeat_num = received_msg[i+0x48]
        self.uint8_t_enable = received_msg[i+0x49]
        self.uint8_t_mode = received_msg[i+0x4A]
        self.uint8_t_soft_start = received_msg[i+0x4B]
        self.uint8_t_current_limit = received_msg[i+0x4C]
        self.uint8_t_diag = received_msg[i+0x4D]
        self.uint8_t_cap = received_msg[i+0x4E]
        self.uint8_t_modulation = received_msg[i+0x4F]
        self.uint8_t_code_mode = received_msg[i+0x50]
        self.uint8_t_overload_mode = received_msg[i+0x51]
        self.uint8_t_supp_voltage = received_msg[i+0x52]
        self.uint8_t_alarm_msg = int(received_msg[i+0x53])
        self.uint8_t_test_tag = received_msg[i+0x54]
        self.uint8_t_command = received_msg[i+0x55]
        # обратный порядок байт
        self.int8_t_antenna = [int(received_msg[(i + 0x56)]), int(received_msg[(i + 0x57)]),
                               int(received_msg[(i+0x58)]), int(received_msg[(i+0x59)])]

        self.uint8_t_ant_level = list(received_msg[(i+0x5A):(i+0x5D) + 1])

        self.uint16_t_turns_ant = [int.from_bytes(received_msg[(i+0x5E):(i+0x5F) + 1], 'little'),
                                   int.from_bytes(received_msg[(i + 0x60):(i + 0x61) + 1], 'little'),
                                   int.from_bytes(received_msg[(i + 0x62):(i + 0x63) + 1], 'little'),
                                   int.from_bytes(received_msg[(i + 0x64):(i + 0x65) + 1], 'little')]

        self.uint16_t_turns_prim = int.from_bytes(received_msg[(i+0x66):(i+0x67) + 1], 'little')
        self.uint8_t_supply_level = received_msg[i+0x68]
        self.uint8_t_standby = received_msg[i+0x69]
        self.uint16_t_alarm_pause = int.from_bytes(received_msg[(i+0x6A):(i+0x6B) + 1], 'little')
        self.uint16_t_alarm_time = int.from_bytes(received_msg[(i+0x6C):(i+0x6D) + 1], 'little')
        self.LogLevel_Type_log_level = received_msg[i+0x6E]
        self.uint8_t_temp_level1_fanon = received_msg[i+0x6F]
        self.uint8_t_temp_level1_fanoff = received_msg[i+0x70]
        self.uint8_t_temp_level2_fanon = received_msg[i+0x71]
        self.uint8_t_temp_level2_fanoff = received_msg[i+0x72]
        self.uint8_t_temp_halt_level = received_msg[i+0x73]
        self.uint8_t_dhcp = received_msg[i+0x74]

        self.uint8_t_IP_ADDRESS = list(received_msg[(i+0x75):(i+0x78) + 1])
        self.uint8_t_NETMASK_ADDRESS = list(received_msg[(i+0x79):(i+0x7C) + 1])
        self.uint8_t_GATEWAY_ADDRESS = list(received_msg[(i+0x7D):(i+0x80) + 1])
        self.char_MineName = received_msg[(i+0x81):(i+0xA0) + 1].decode('utf-8','replace' )
        self.float_limit_R_status = struct.unpack("<f", received_msg[(i+0xA4):(i+0xA7) + 1])
        self.float_limit_L_status = struct.unpack("<f", received_msg[(i+0xA8):(i+0xAB)  + 1])
        self.float_limit_C_status = struct.unpack("<f", received_msg[(i+0xAC):(i+0xAF) + 1])
        self.uint8_t_PIN_LVL = received_msg[i+0xB0]
        self.uint16_t_PIN_100 = int.from_bytes(received_msg[(i+0xB2):(i+0xB3) + 1], 'little')
        self.uint16_t_PIN_150 = int.from_bytes(received_msg[(i+0xB4):(i+0xB5) + 1], 'little')
        self.uint16_t_PIN_500 = int.from_bytes(received_msg[(i+0xB6):(i+0xB7) + 1], 'little')

class StatusSystem:
    def __init__(self, *args, **kwargs):
        self.int8_t_current_temp_1 = 0
        self.int8_t_current_temp_2 = 0
        self.uint8_t_log_status = 0
        self.uint8_t_trx_role = 0
        self.uint8_t_addr_dev = 0
        self.uint8_t_abb_state = 0
        self.uint8_t_abb_sw_cnt = 0
        self.uint8_t_draw_menu_state_AVR = 0
        self.uint8_t_draw_menu_state_SYNC = 0
        self.uint8_t_draw_menu_state_LOG = 0
        self.uint8_t_draw_menu_state_TEMP1 = 0
        self.uint8_t_draw_menu_state_TEMP2 = 0
        self.uint8_t_SYNC_CNT = 0
        self.uint8_t_SYNC_CHECK = 0
        self.uint8_t_SYNC_OK = 0
        self.uint8_t_SYNC_DRV_CNT = 0
        self.uint8_t_SYNC_DRV_CHECK = 0
        self.uint8_t_SYNC_DRV_OK = 0
        self.uint32_t_rmt_cnt = 0
        self.uint8_t_rmt_ok = 0
        self.uint8_t_State_220V = 0
        self.uint8_t_State_380V = 0
        self.uint8_t_status_page = 0
        self.uint32_t_data = 0
        self.uint8_t_send_cmd = 0
        self.uint8_t_overload_cnt = 0
        self.float_overload_curr = 0
        self.uint8_t_bit_num = 0
        self.uint8_t_repeat_cur = 1
        self.float_ia = [0,0,0,0]
        self.float_im = [0,0,0,0]
        self.float_pa = [0,0,0,0]
        self.float_pm = [0,0,0,0]
        self.float_ra = [0,0,0,0]
        self.float_c = [0,0,0,0]
        self.float_l = [0,0,0,0]
        self.float_r = [0,0,0,0]
        self.uint8_t_trans_ok = 0
        self.uint8_t_trans_state = 0
        self.uint8_t_drv_enable = 0
        self.uint8_t_ant_fuse = [0,0,0,0]
        self.uint8_t_ant_break = [0,0,0,0]
        self.uint16_t_driver_fw = 0
        self.uint16_t_driver_bl = 0
        self.int8_t_ant_state = [1,0,0,0]
        self.uint8_t_led_POWER_state = 0
        self.uint8_t_led_ACT_state = 0
        self.uint8_t_led_380V_state = 0
        self.uint8_t_led_220V_state = 0
        self.uint8_t_led_PC_state = 0
        self.uint8_t_led_RC_state = 0
        self.uint8_t_led_OUT1_state = 0
        self.uint8_t_led_OUT2_state = 0
        self.uint8_t_led_OUT3_state = 0
        self.uint8_t_led_OUT4_state = 0
        self.uint8_t_led_CRNT_state = 0
        self.uint8_t_led_TEMP_state = 0

    def read_Status(self, received_msg, i):
        self.int8_t_current_temp_1 = int(received_msg[i])
        self.int8_t_current_temp_2 = int(received_msg[i+0x01])
        self.uint8_t_log_status = int(received_msg[i+0x02])
        self.uint8_t_trx_role = int(received_msg[i+0x03])
        self.uint8_t_addr_dev = int(received_msg[i+0x04])
        self.uint8_t_abb_state = int(received_msg[i+0x05])
        self.uint8_t_abb_sw_cnt = int(received_msg[i+0x06])
        self.uint8_t_draw_menu_state_AVR = int(received_msg[i+0x07])
        self.uint8_t_draw_menu_state_SYNC = int(received_msg[i+0x08])
        self.uint8_t_draw_menu_state_LOG = int(received_msg[i+0x09])
        self.uint8_t_draw_menu_state_TEMP1 = int(received_msg[i+0x0A])
        self.uint8_t_draw_menu_state_TEMP2 = int(received_msg[i+0x0B])
        self.uint8_t_SYNC_CNT = int(received_msg[i+0x0C])
        self.uint8_t_SYNC_CHECK = int(received_msg[i+0x0D])
        self.uint8_t_SYNC_OK = int(received_msg[i+0x0E])
        self.uint8_t_SYNC_DRV_CNT = int(received_msg[i+0x0F])
        self.uint8_t_SYNC_DRV_CHECK = int(received_msg[i+0x10])
        self.uint8_t_SYNC_DRV_OK = int(received_msg[i+0x11])

        self.uint32_t_rmt_cnt = int.from_bytes(received_msg[(i+0x14):(i+0x17) + 1], 'little')
        self.uint8_t_rmt_ok = int(received_msg[i+0x18])
        self.uint8_t_State_220V = int(received_msg[i+0x19])
        self.uint8_t_State_380V = int(received_msg[i+0x1A])
        self.uint8_t_status_page = int(received_msg[i+0x1B])
        self.uint32_t_data = int.from_bytes(received_msg[(i+0x1C):(i+0x1F) + 1], 'little')
        self.uint8_t_send_cmd = int(received_msg[i+0x20])
        self.uint8_t_overload_cnt = int(received_msg[i+0x21])
        self.float_overload_curr =  struct.unpack("<f", received_msg[(i+0x24):(i+0x27) + 1])
        self.uint8_t_bit_num = int(received_msg[i+0x28])
        self.uint8_t_repeat_cur = int(received_msg[i+0x29])
        self.float_ia =  [ struct.unpack("<f", received_msg[(i+0x2C):(i+0x2F) + 1])[0],  struct.unpack("<f", received_msg[(i+0x30):(i+0x33) + 1])[0],
                      struct.unpack("<f", received_msg[(i+0x34):(i+0x37) + 1])[0],  struct.unpack("<f", received_msg[(i+0x38):(i+0x3B) + 1])[0]]

        self.float_im  = [ struct.unpack("<f", received_msg[(i+0x3C):(i+0x3F) + 1])[0],  struct.unpack("<f", received_msg[(i+0x40):(i+0x43) + 1])[0],
                      struct.unpack("<f", received_msg[(i+0x44):(i+0x47) + 1])[0],  struct.unpack("<f", received_msg[(i+0x48):(i+0x4B) + 1])[0]]

        self.float_pa  = [ struct.unpack("<f", received_msg[(i+0x4C):(i+0x4F) + 1])[0],  struct.unpack("<f", received_msg[(i+0x50):(i+0x53) + 1])[0],
                      struct.unpack("<f", received_msg[(i+0x54):(i+0x57) + 1])[0],  struct.unpack("<f", received_msg[(i+0x58):(i+0x5B) + 1])[0]]

        self.float_pm  = [ struct.unpack("<f", received_msg[(i+0x5C):(i+0x5F) + 1])[0],  struct.unpack("<f", received_msg[(i+0x60):(i+0x63) + 1])[0],
                      struct.unpack("<f", received_msg[(i+0x64):(i+0x67) + 1])[0],  struct.unpack("<f", received_msg[(i+0x68):(i+0x6B) + 1])[0]]

        self.float_ra  = [ struct.unpack("<f", received_msg[(i+0x6C):(i+0x6F) + 1])[0],  struct.unpack("<f", received_msg[(i+0x70):(i+0x73) + 1])[0],
                      struct.unpack("<f", received_msg[(i+0x74):(i+0x77) + 1])[0],  struct.unpack("<f", received_msg[(i+0x78):(i+0x7B) + 1])[0]]

        self.float_c =   [ struct.unpack("<f", received_msg[(i+0x7C):(i+0x7F) + 1])[0],  struct.unpack("<f", received_msg[(i+0x80):(i+0x83) + 1])[0],
                      struct.unpack("<f", received_msg[(i+0x84):(i+0x87) + 1])[0],  struct.unpack("<f", received_msg[(i+0x88):(i+0x8B) + 1])[0]]

        self.float_l =  [ struct.unpack("<f", received_msg[(i+0x8C):(i+0x8F)+ 1])[0],  struct.unpack("<f", received_msg[(i+0x90):(i+0x93) + 1])[0],
                     struct.unpack("<f", received_msg[(i+0x94):(i+0x97) + 1])[0],  struct.unpack("<f", received_msg[(i+0x98):(i+0x9B) + 1])[0]]

        self.float_r =  [ struct.unpack("<f", received_msg[(i+0x9C):(i+0x9F) + 1])[0],  struct.unpack("<f", received_msg[(i+0xA0):(i+0xA3) + 1])[0],
                     struct.unpack("<f", received_msg[(i+0xA4):(i+0xA7) + 1])[0],  struct.unpack("<f", received_msg[(i+0xA8):(i+0xAB) + 1])[0]]

        self.uint8_t_trans_ok = int(received_msg[i+0xAC])
        self.uint8_t_trans_state = int(received_msg[i+0xAD])
        self.uint8_t_drv_enable = int(received_msg[i+0xAE])
        self.uint8_t_ant_fuse = list(received_msg[(i+0xAF):(i+0xB2) + 1])
        self.uint8_t_ant_break = list(received_msg[(i+0xB3):(i+0xB6) + 1])
        self.uint16_t_driver_fw = int.from_bytes(received_msg[(i+0xB8):(i+0xB9) + 1], 'little')
        self.uint16_t_driver_bl = int.from_bytes(received_msg[(i+0xBA):(i+0xBB) + 1], 'little')
        self.int8_t_ant_state = list(received_msg[(i+0xBC):(i+0xBF) + 1])
        self.uint8_t_led_POWER_state = int(received_msg[(i+0xC0)])
        self.uint8_t_led_ACT_state = int(received_msg[(i+0xC1)])
        self.uint8_t_led_380V_state = int(received_msg[(i+0xC2)])
        self.uint8_t_led_220V_state = int(received_msg[(i+0xC3)])
        self.uint8_t_led_PC_state = int(received_msg[(i+0xC4)])
        self.uint8_t_led_RC_state = int(received_msg[(i+0xC5)])
        self.uint8_t_led_OUT1_state = int(received_msg[(i+0xC6)])
        self.uint8_t_led_OUT2_state = int(received_msg[(i+0xC7)])
        self.uint8_t_led_OUT3_state = int(received_msg[(i+0xC8)])
        self.uint8_t_led_OUT4_state = int(received_msg[(i+0xC9)])
        self.uint8_t_led_CRNT_state = int(received_msg[(i+0xCA)])
        self.uint8_t_led_TEMP_state = int(received_msg[(i+0xCB)])
        self.uint8_t_ChangeSetup = int(received_msg[(i+0xCC)])

class stm32_crc32:

    def dothething(inbytes, le=True, rr=False, xx=False, init=0xffffffff):
        POLY = 0x4c11db7
        crc = init
        inbytes = bytes(inbytes)

        for n in range(0, len(inbytes), 4):
            if le:
                x = inbytes[n] << 0 | inbytes[n + 1] << 1 | inbytes[n + 2] << 2 | inbytes[n + 3] << 3
            else:
                x = inbytes[n] << 3 | inbytes[n + 1] << 2 | inbytes[n + 2] << 1 | inbytes[n + 3] << 0

            if rr:
                x = rev_bits_in_word(x)

            crc = crc ^ x

            for n in range(32):
                crc = (crc << 1)
                if crc & (1 << 31):
                    crc = crc ^ POLY
                crc = crc & 0xffffffff  # clamp to 32 bits

            if rr:
                crc = rev_bits_in_word(crc)

            if xx:
                crc = crc ^ 0xffffffff

        return crc