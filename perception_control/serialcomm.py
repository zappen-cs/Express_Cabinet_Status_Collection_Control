import serial
import time
from PyQt5.Qt import QThread,pyqtSignal
import threading
class SerialAssistant(QThread):
    mysingal=pyqtSignal(list)

    collect_temp=30.0
    set_temp=4.0
    engine_state='停止'

    lock1_state = 0
    lock2_state =0
    lock3_state = 0
    lock4_state = 0
    lock5_state = 0
    lock6_state = 0
    lock7_state = 0
    lock8_state = 0
    lock9_state = 0
    lock10_state =0
    #关闭柜子的信号
   # signal_close_lock=0



    def __init__(self):
        super(SerialAssistant, self).__init__()
        self.serial = serial.Serial('COM2', 38400, timeout=0.5)

        self.data = ['00'] * 44
        self.ack = ['00'] * 14
        self.control_engine_state = 'off'
        self.resend_command_state = 0
        self.temp_byte = '08'
        self.temp_offset_byte = '02'
        self.device_code_byte = '10 01 25 F0 02'
        self.device_address_byte = '01'
        self.interval_byte = '1E'
        self.set_up_prestart_interval(1)

    def run(self):
        while True:
            l=[]
            #采集温度
            l.append(self.collect_temp)
            #设定温度
            l.append(self.set_temp)
            #压缩机状态
            l.append(self.engine_state)
            #锁的状态
            l.append(self.lock1_state)
            l.append(self.lock2_state)
            l.append(self.lock3_state)
            l.append(self.lock4_state)
            l.append(self.lock5_state)
            l.append(self.lock6_state)
            l.append(self.lock7_state)
            l.append(self.lock8_state)
            l.append(self.lock9_state)
            l.append(self.lock10_state)
           # l.append(self.signal_close_lock)
           # print(self.signal_close_lock)



            self.mysingal.emit(l)
            time.sleep(0.1)

    def send_command(self,command,flag=1):
        global num
        self.send_command_state=1
        command = command.strip()
        command_str=command
        send_list = []
        while command != '':
            try:
                num = int(command[0:2], 16)
            except ValueError as e:
                print(e)
            command = command[2:].strip()
            send_list.append(num)
        command = bytes(send_list)
        self.serial.write(command)
        time.sleep(1)
        if flag==1:
            self.check(command_str)
            self.success_flag=1

    def recv(self,serial):
        while True:
            data = serial.read_all()
            if data == '':
                continue
            else:
                break
            time.sleep(0.02)
        return data

    def recv_data(self):
        while True:
            data = self.recv(self.serial)
            if data != b'':
                data = data.hex().upper()
                if len(data) == 88:
                    self.data = ' '.join([data[2 * i:2 * (i + 1)] for i in range(int(len(data)/2))]).split(' ')
                   # print(self.data)
                    self.get_device_code()
                    #self.get_device_state()
                    self.get_set_temp()
                    self.get_temp_offset()
                    self.get_collect_temp()
                    self.get_engine_state()
                    self.get_lock_state()
                elif len(data)==28:
                    self.ack = ' '.join([data[2 * i:2 * (i + 1)] for i in range(int(len(data) / 2))]).split(' ')
                    #print(self.ack)

    def get_device_code(self):
        self.device_code = ''.join([self.data[i] for i in range(6, 11)])
        #print(f'设备编码:{self.device_code}')

    def get_device_state(self):
        data_device_state=self.data[-14]
       # print(self.data)
        #print(self.data[-14])
        if int(data_device_state, 2) == 0:
            self.device_state = '停机'
        elif int(data_device_state, 2) == 1:
            self.device_state = '预启动'
        else:
            self.device_state = '运行'
        #print(f'设备状态:{self.device_state}')

    def get_device_address(self):
        self.device_address = int(self.data[11], 16)
        #print(f'设备地址:{self.device_address}')

    def get_collect_temp(self):
        data_collect_temp = bin(int(self.data[-11], 16))[2:].zfill(8)
        self.collect_temp = int(data_collect_temp[1:-1], 2)
        if int(data_collect_temp[-1]):
            self.collect_temp += 0.5
        self.collect_temp = self.collect_temp * (-1) if int(data_collect_temp[0]) == 1 else self.collect_temp



        #print(f'采集温度:{self.collect_temp}')

    def get_set_temp(self):
        data_set_temp = bin(int(self.data[-12], 16))[2:].zfill(8)
        self.set_temp = int(data_set_temp[1:-1], 2)
        if int(data_set_temp[-1]):
            self.set_temp += 0.5
        self.set_temp = self.set_temp * (-1) if int(data_set_temp[0]) == 1 else self.set_temp
       # print(f'设定温度:{self.set_temp}')

    def get_lock_state(self):
        data_lock_state=bin(int(self.data[-8]+self.data[-7],16))[2:].zfill(16)
        self.lock1_state=data_lock_state[7]

        self.lock2_state = data_lock_state[6]
        self.lock3_state = data_lock_state[5]
        self.lock4_state = data_lock_state[4]
        self.lock5_state = data_lock_state[3]
        self.lock6_state = data_lock_state[2]
        self.lock7_state = data_lock_state[1]
        self.lock8_state = data_lock_state[0]
        self.lock9_state = data_lock_state[15]
        self.lock10_state=data_lock_state[14]
        #print(data_lock_state)

    def get_engine_state(self):
        data_engine_state = bin(int(self.data[-13], 16))[2:].zfill(8)
        if int(data_engine_state, 2) == 0:
            self.engine_state = '停止'
        elif int(data_engine_state, 2) == 1:
            self.engine_state = '预启动'
        elif int(data_engine_state, 2) == 2:
            self.engine_state = '运行'
        else:
            self.engine_state = '故障'
        #print(f'压缩机运行状态:{self.engine_state}')

    def get_temp_offset(self):
        self.temp_offset = int(self.data[18], 16)
        #print(f'温度控制偏差为:{self.temp_offset}')



    def set_up_temp(self,temp):
        bin_temp = bin(int(str(int(abs(temp))), 10))[2:].zfill(6)
        if temp % 1 == 0:
            final_bin_byte = '0' + bin_temp + '0' if temp >= 0 else '1' + bin_temp + '0'
        else:
            final_bin_byte = '0' + bin_temp + '1' if temp >= 0 else '1' + bin_temp + '1'
        final_byte=hex(int(final_bin_byte, 2))[2:].upper().zfill(2)
        self.temp_byte=hex(int(final_bin_byte,2))[2:].upper().zfill(2)
        final_command = 'FF FF 0B 78 01 04 ' + final_byte + ' 8C C2 FF F7'
        self.send_command(final_command)


    def open_clock(self,drawer_id):
        raw1 = [0] * 8
        raw2 = [0] * 8
        for id in drawer_id:
            if id < 9:
                raw1[8 - id] = 1
            elif id < 11:
                raw2[16 - id] = 1
        raw1_str = ''.join([str(i) for i in raw1])
        raw2_str = ''.join([str(i) for i in raw2])
        first_byte = hex(int(raw1_str, 2))[2:].upper().zfill(2)
        second_byte = hex(int(raw2_str, 2))[2:].upper().zfill(2)
        final_byte = first_byte + ' ' + second_byte
        final_command='FF FF 0C 77 01 03 '+final_byte+' 1E 58 FF F7'
        self.send_command(final_command)

    def set_up_temp_offset(self, offset):
        # 最高为10度
        offset_byte = hex(int(offset))[2:].upper().zfill(2)
        final_command = 'FF FF 0B 80 01 06 ' + offset_byte + ' 60 C8 FF F7'
        self.send_command(final_command)

    def set_up_prestart_interval(self, interval):
        self.interval_byte = hex(int(interval))[2:].upper().zfill(2)
        self.send_total_command()

    def control_engine(self):
        time.sleep(0.5)

        def inner():
            while True:
                final_start_command = 'FF FF 0B 76 01 02 01 60 C8 FF F7'
                final_stop_command = 'FF FF 0B 76 01 02 00 60 C8 FF F7'
                if self.collect_temp - self.set_temp > self.temp_offset / 2 and self.engine_state == '停止':
                    self.send_command(final_start_command)
                   # print('------------已发送启动命令----------')
                elif self.set_temp - self.collect_temp > self.temp_offset / 2 and self.engine_state == '运行':
                    self.send_command(final_stop_command)
                    #print('------------已发送停止命令----------')
                if self.control_engine_state == 'off':
                    self.send_command(final_stop_command)
                    break

        if self.control_engine_state == 'off':
            self.control_engine_state = 'on'
            t = threading.Thread(target=inner)
            t.setDaemon(True)
            t.start()
            # inner()
        else:
            self.control_engine_state = 'off'

    def check(self, command):
        command_list = command.split(' ')

        def innner():
            count = 0
            while True:
                # time.sleep(1)
                if self.ack[2] == '0E' and self.ack[5] == command_list[5]:
                   # print('-----------------------校验成功-----------------------')
                    #self.success_flag=1
                    self.ack = ['00'] * 14
                    break
                else:
                    count += 1
                    time.sleep(1)
                    if count == 2:
                        self.resend_command = 1
                       # print(f'-----------------------已重发命令-------------------------命令为{command}')
                        self.send_command(command, flag=0)
                        count = 0

        if self.resend_command_state == 0:
            t=threading.Thread(target=innner)
            t.setDaemon(True)
            t.start()
            #innner()

    def send_total_command(self):
        first_byte = 'FF FF 1C 75 7F 05 ' + self.device_code_byte + ' ' + self.device_address_byte + ' 0A 01 '
        last_byte = ' FF 03 FF 03 20 36 E8 FF F7'
        final_command = first_byte + self.interval_byte + ' 07 08 ' + self.temp_byte + ' ' + self.temp_offset_byte + last_byte
        self.send_command(final_command)



    def set_up_device_code(self, device_code):
        if len(device_code) == 14:
            self.device_code_byte = device_code
            self.send_total_command()

    def set_up_device_address(self, device_address):
        if int(device_address) < 120 and int(device_address) > 0:
            self.device_address_byte = hex(int(device_address))[2:].upper().zfill(2)
            self.send_total_command()

