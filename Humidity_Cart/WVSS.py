''' WVSS.py is a class to establish communication with the SpectraSensors WVSS-II
      RS-232 connection.
'''

import serial
import time
import sys
import threading
import inspect
from PyQt5 import QtGui, QtCore

class WVSS_II(QtCore.QThread):
    # Declare signal variables for the class
    change_value = QtCore.pyqtSignal(str)   # Code based on https://www.youtube.com/watch?v=eYJTcLBQKug
    heartbeat = QtCore.pyqtSignal(str)      # Heartbeat to confirm device is connected

    def __init__(self, comm_port='COM1'):
        ''' Initialize instance variable defaults for the WVSS_II class

        Variable Descriptions:
            comm_port - RS232 communication port of WVSS device
        '''
        super(WVSS_II, self).__init__()

        # Setup communication variables
        self.comm_port = comm_port
        self.baud_rate = 9600
        self.parity = None
        self.data_bits = 8
        self.stop_bits = 1

        # Calculated condition variables
        # self.set_zeros()

        # Threading variables
        self.stop_thread = True

        try:
            self.serWVSS = serial.Serial(self.comm_port, self.baud_rate, timeout=6)  # initiate communication with WVSS

        # Check for connection issues --------------------------------------
        except:
            self.connection_issues(0)   # Device not connecting issue

        if self.serWVSS.read() == b'':
            self.connection_issues(1)   # Device not reading issue
        #-------------------------------------------------------------------


    def connection_issues(self, err_num):
        try:
            self.serWVSS.close()   # Close serial connection before raising exception
        except:
            pass

        if err_num == 0:   # Device not connecting issue
            comment = "{} does not exist. Please enter the correct COM port for the \
            Water Vapor Monitor System.".format(self.comm_port)
            raise serial.serialutil.SerialException(inspect.cleandoc(comment))

        elif err_num == 1:  # Device not reading issue
            comment = 'The Water Vapor Monitor System is not properly connected to this PC. \n\n \
            Spectra Sensor or Monitor System are either not connected or not properly powered on.\n \
            Please re-check power and connections.'
            raise serial.serialutil.SerialException(inspect.cleandoc(comment))


    @QtCore.pyqtSlot()
    def run(self):
        ''' Thread to run for continuously taking data from WVSS '''
        self.stop_thread = False

        while True:
            # try:
            if self.stop_thread:
                break

            self.raw_string = self.serWVSS.readline().decode()    # Read entire line into one string
            self.change_value.emit(self.raw_string)
            self.heartbeat.emit('yesSS')

        self.heartbeat.emit('noSS')


def parse_string(raw_output_string):
    ''' This function converts the output of Water Vapor Monitor System to individual
        floating point values'''
    string = raw_output_string.strip('\r\n')    # Convert to unicode and remove characters
    list_string = string.split(' ')                      # Split into a list

    # With the way that the padding works, some elements return empty strings
    list_string = list(filter(None, list_string))    # to remove empty strings
    try:
        list_vals = [float(s) for s in list_string]      # convert to floating points
    except:
        print('Could NOT parse Spectra Sensor data')
        list_vals = [0.0 for s in list_string]

# Section currently NOT USED --------------------------------------------------------------
    # try:
    #     wv_ppmv,p_mbar,t_C,pp2f_cts,lasPow_cnts,pkI_cnts, \
    #         null_cnts,midPt_mA,amidPt_mA,p_cf,bl_cf = list_vals
    # except:
    #     print('WARNING -- Could not parse data from the Water Vapor Monitor System; all values set to zero')
    #     wv_ppmv=0;p_mbar=0;t_C=0;pp2f_cts=0;lasPow_cnts=0;pkI_cnts=0;null_cnts=0;midPt_mA=0;amidPt_mA=0;p_cf=0;bl_cf=0
# -----------------------------------------------------------------------------------------

    return list_vals




if __name__ == '__main__':
    sess = WVSS_II()
    t1 = threading.Thread(target=sess.run)
    t1.start()
    time.sleep(3)
    sess.stop_thread = True
    t1.join()
