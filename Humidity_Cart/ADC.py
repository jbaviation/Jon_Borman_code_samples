''' ADC.py is a class to establish communication with DataQ Instruments DI-145
        for more information on the DI-145 communication protocol goto:
        https://www.dataq.com/resources/installations/web-help/sdk/Content/Function%20Reference/di_open.htm
'''
import serial
import time
import sys
import threading
from PyQt5 import QtGui, QtCore


class DataQ_DI145(QtCore.QThread):  # added inheritance from QThread for signals
    # Declare signal variables for the class
    change_value = QtCore.pyqtSignal(float)   # Code based on https://www.youtube.com/watch?v=eYJTcLBQKug
    change_value_temp = QtCore.pyqtSignal(float)
    heartbeat = QtCore.pyqtSignal(str)        # Heartbeat to confirm device is connected

    def __init__(self, comm_port='COM4', baud_rate=4800):
        ''' Initialize instance variable defaults for the DataQ_DI145 class

        Variable Descriptions:
            comm_port - USB communication port of ADC device (default: COM4 on 17021058 Machine)
            baud_rate - baud rate of the device (default: 4800 for DI145)
            C1 - Slope coefficient of counts vs Volts (default: 0.0003 for nominal conversion)
            C0 - Offset coefficient of counts vs Volts (default: 0.0 for nominal conversion)
        '''
        super(DataQ_DI145, self).__init__()   # Code based on https://www.youtube.com/watch?v=ivcxZSHL7jM

        self.comm_port = comm_port
        self.baud_rate = baud_rate

        # Cancel any threading that may be taking place already
        self.stop_thread = True

        # Try to scan the device, otherwise try to initialize it
        try:
            self.scan()
            self.sts()
        except:
            self.serDataq = serial.Serial(comm_port, baud_rate)  # initiate communication with ADC device
            self.serDataq.write(b'S0\r')   # force device to stop scanning if was left scanning
            self.serDataq.write(b'C3')     # enable channels 1 and 3


    def scan(self):
        ''' Initiate device scan '''
        self.stop_thread = False

        self.serDataq.write(b'S1')      # start scanning
        print('Scan started')


    def sts(self):
        ''' Initiate device stop '''
        self.stop_thread = True

        self.serDataq.write(b'S0')      # stop scanning
        print('Scan stopped')

    @QtCore.pyqtSlot()
    def run(self):
        ''' Meant to run as a thread for taking voltage and counts from the ADC device'''
        byte_count = 1       # initialize byte_count variable
        old_byte = 83        # initialize old_byte variable
        while True:
            try:
                if self.stop_thread:
                    break

                string = self.serDataq.read()
                self.heartbeat.emit('yesLC')
                byte = ord(string)

                if byte & 1 == 0:           # this is the first byte
                    byte_count = 1          # indicate that this is the first byte

                elif byte & 1 == 1:         # this is not the first byte
                    byte_count += 1         # increment byte count

                    if byte_count == 2 or byte_count == 4:     # second byte completes the channel
                        # combine 1st and 2nd bytes with shift for syncing
                        data = (old_byte >> 1) + ((byte & 254) << 6)
                        data = data << 2    # shift left 2 bits for 16-bit value
                        data = data - 32768 # subtract 1000 0000 0000 0000 for raw ADC count

                        # emit data depending on which byte we are referring to
                        self.change_value.emit(data) if byte_count==2 else self.change_value_temp.emit(data)

                old_byte = byte     # track the last byte

            except:
                self.heartbeat.emit('noLC')
                pass

        self.heartbeat.emit('noLC')
