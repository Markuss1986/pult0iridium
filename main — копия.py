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
        self.root.ids.MainApp.ant1_R = str(round(self.Status.float_ra[0], 3)) +'  ( ' + str(round(self.Status.float_r[0], 3)) +' )'
        self.root.ids.MainApp.ant2_R = str(round(self.Status.float_ra[1], 3)) +'  ( ' + str(round(self.Status.float_r[1], 3)) +' )'
        self.root.ids.MainApp.ant3_R = str(round(self.Status.float_ra[2], 3)) +'  ( ' + str(round(self.Status.float_r[2], 3)) +' )'
        self.root.ids.MainApp.ant4_R = str(round(self.Status.float_ra[3], 3)) +'  ( ' + str(round(self.Status.float_r[3], 3)) +' )'

        # индуквтиность
        self.root.ids.MainApp.ant1_L = str(round(self.Status.float_l[0], 3)) + '  ( '+ str(round(self.Settings.float_l[0], 3)) + ' )'
        self.root.ids.MainApp.ant2_L = str(round(self.Status.float_l[1], 3)) + '  ( '+ str(round(self.Settings.float_l[1], 3)) + ' )'
        self.root.ids.MainApp.ant3_L = str(round(self.Status.float_l[2], 3)) + '  ( '+ str(round(self.Settings.float_l[2], 3)) + ' )'
        self.root.ids.MainApp.ant4_L = str(round(self.Status.float_l[3], 3)) + '  ( '+ str(round(self.Settings.float_l[3], 3)) + ' )'

        # ёмкость
        self.root.ids.MainApp.ant1_C = str(round(self.Settings.float_c[0], 3)) + '  ( '+ str(round(self.Status.float_c[0], 3))+' )'
        self.root.ids.MainApp.ant2_C = str(round(self.Settings.float_c[1], 3)) + '  ( '+ str(round(self.Status.float_c[1], 3))+' )'
        self.root.ids.MainApp.ant3_C = str(round(self.Settings.float_c[2], 3)) + '  ( '+ str(round(self.Status.float_c[2], 3))+' )'
        self.root.ids.MainApp.ant4_C = str(round(self.Settings.float_c[3], 3)) + '  ( '+ str(round(self.Status.float_c[3], 3))+' )'

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
                            self.root.ids.status_bar.text = "Вызов тага"
                            #self.root.ids.solution.text = str(self.Status.uint32_t_data)


                if self.Status.uint8_t_trans_state == 0:
                    self.root.ids.status_bar.text = ""

            # очистка статус бара  если Alarm выключили
            if self.root.ids.status_bar.text == 'Аварийный вызов' or \
               self.root.ids.status_bar.text == 'Аварийный вызов (пауза)':
                self.root.ids.status_bar.text = ''


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
                self.root.ids.status_bar.text = 'Аварийный вызов'
                self.root.ids.solution.text = ''
                self.percent_transmit = round(self.Status.uint8_t_bit_num * 100 / self.Settings.uint16_t_alarm_time)
                self.root.ids.MainApp.percent_transmit = str(self.percent_transmit)
                if self.percent_transmit >= 90:
                    self.alarm_time_counter = 0
                    self.flag_alarm_pause = 1

            # если передатчик выключен то Alarm пауза
            if self.Status.uint8_t_trans_state == 0:
                self.root.ids.status_bar.text = 'Аварийный вызов (пауза)'
                self.root.ids.solution.text = ''
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
                self.root.ids.status_bar.text = 'Контроль'
            if self.Status.uint8_t_trans_state == 0 and self.root.ids.status_bar.text == 'Контроль':
                self.root.ids.status_bar.text = ''



            # показать если пауза при аварии
            if self.flag_alarm_pause == 1:
                self.root.ids.progress_bar.opacity = 1
            else:
                self.root.ids.progress_bar.opacity = 0
                if (self.root.ids.status_bar.text == 'Авария (отправка сообщения)') or ( self.root.ids.status_bar.text == 'Авария (пауза)'):
                    self.root.ids.status_bar.text = ''

        #self.root.ids.status_bar.text = self.sdpathfile