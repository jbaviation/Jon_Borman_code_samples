''''Use this program to generate all references needed to run a spectra sensor validation.'''

from humref import spectra_equiv
import common_def
import ADC
import WVSS
import record
import time

## GUI application------------------------------------------------------------------
from PyQt5 import QtCore, QtGui, QtWidgets
import sys, os

## For the hardware setup GUI
# The following allows you to access the auto-generated gui from pyuic5
from GUIs import record_GUI as rgui
class RecGUI(QtWidgets.QDialog, rgui.Ui_dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        global avgLength, fname, outLoc

        self.selected = [self.tempFBox,self.dpFBox,self.rhBox,self.mmrBox,self.vcBox]
        self.set_selected()
        self.set_defaults()
        self.toolButton.clicked.connect(self.toolButtonClicked)

        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setText('Apply')  # Change text from Ok to Apply

    def set_selected(self):
        for box in self.selected:
            box.setChecked(True)

    def set_defaults(self):
        # Record time
        self.avgRecEdit.setText('{}'.format(avgLength))

        # Filename
        self.filenameEdit.setText('{}'.format(fname))

        # Output file location
        self.outLocEdit.setText('{}'.format(outLoc))


    def toolButtonClicked(self):
        ''' Open QFileDialog when the toolButton is clicked '''
        outLoc = str(QtWidgets.QFileDialog.getExistingDirectory())
        self.outLocEdit.setText('{}'.format(outLoc))

#----------------------------------------------------------------------------------

## For the set conditions GUI
# The following allows you to access the auto-generated gui from pyuic5
from GUIs import setConditions_GUI as scgui
class SetCondGUI(QtWidgets.QDialog, scgui.Ui_Dialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)

        self.addDDOptions()  # Add all defaults and options to the dropdown boxes

        self.setPressChkBox.stateChanged.connect(self.pressToggled)  # set pressure changes state
        self.setTempChkBox.stateChanged.connect(self.tempToggled) # set temperature changes state

# Section probably not needed
    # def getPress(self):
    #     text = str(self.pressUnitDD.currentText())
    #     print('text = '.format(text))
    #
    #     # Convert to PSI
    #     self.setPressVal = float(self.pressLineEdit.text())
    #     if text == 'Pa':
    #         self.setPressVal = self.setPressVal * 1.450377e-4
    #     elif text == 'kPa':
    #         self.setPressVal = self.setPressVal * 0.1450377
    #     elif text == 'mb':
    #         self.setPressVal = self.setPressVal * 0.01450377
    #     elif text == 'inHg':
    #         self.setPressVal = self.setPressVal * 0.491154
    #
    #
    # def getTemp(self):
    #     text = str(self.tempUnitDD.currentText())
    #
    #     # Convert to degrees Fahrenheit
    #     self.setTempVal = float(self.tempLineEdit.text())
    #     if text == 'degC':
    #         self.setTempVal = self.setTempVal*1.8 + 32
    #     elif text == 'degR':
    #         self.setTempVal = self.setTempVal + 459.67
    #     elif text == 'K':
    #         self.setTempVal = (self.setTempVal-273.15)*1.8 + 32

    def addDDOptions(self):
        ''' Add all defaults and options to all dropdown boxes'''
        # Set default values
        self.pressure = 14.696
        self.temperature = 70.0

        # Dropdown box options
        self.pressOptions = ['psi', 'Pa', 'kPa', 'mb', 'inHg']
        self.tempOptions = ['degF', 'degC', 'degR', 'K']

        # Add options to dropdown boxes
        self.pressUnitDD.addItems(self.pressOptions)
        self.tempUnitDD.addItems(self.tempOptions)

        # Set default values and dropdown selections
        self.pressLineEdit.setText(str(self.pressure))
        self.tempLineEdit.setText(str(self.temperature))
        self.pressUnitDD.setCurrentIndex(0)
        self.tempUnitDD.setCurrentIndex(0)

    def pressToggled(self, state):
        ''' Determine what happens when set pressure is checked '''
        if state > 0:   # check box is selected
            self.pressLineEdit.setEnabled(True)
            self.pressUnitDD.setEnabled(True)

            value = 14.696   # FIND A WAY TO READ THIS FROM A tmp FILE
            self.pressLineEdit.setText(str(value))
            self.pressUnitDD.setCurrentIndex(0)
        else:  # check box is not selected
            self.pressLineEdit.setEnabled(False)
            self.pressLineEdit.setText('')
            self.pressUnitDD.setEnabled(False)
            self.pressUnitDD.setCurrentText('')

    def tempToggled(self, state):
        ''' Determine what happens when set temperature is checked '''
        if state > 0:   # check box is selected
            self.tempLineEdit.setEnabled(True)
            self.tempUnitDD.setEnabled(True)

            value = 70.0    # FIND A WAY TO READ THIS FROM A tmp FILE
            self.tempLineEdit.setText(str(value))
            self.tempUnitDD.setCurrentIndex(0)
        else:  # check box is not selected
            self.tempLineEdit.setEnabled(False)
            self.tempLineEdit.setText('')
            self.tempUnitDD.setEnabled(False)
            self.tempUnitDD.setCurrentText('')

#----------------------------------------------------------------------------------

## For the hardware setup GUI
# The following allows you to access the auto-generated gui from pyuic5
from GUIs import setup_GUI as sgui
class HardwareGUI(QtWidgets.QDialog, sgui.Ui_dialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)

        global comLC, comSS

        self.lineLC.setText(comLC)
        self.lineWVSS.setText(comSS)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setText('Apply')  # Change text from Ok to Apply

        self.dpGenChkBox.setChecked(True)   # default selection is for the dew point generator only
        self.dpGenChkBox.setEnabled(False)  # Don't allow the user to change dp gen box

#----------------------------------------------------------------------------------

# Global variables go here
comLC = 'COM4'   # Default LiCor COM port
comSS = 'COM1'  # Default SS COM port

avgLength = 10   # Number of seconds to record
fname = 'humidity_cart_{}'.format(time.strftime('%Y%m%d'))   # Filename of output file
outLoc = os.getcwd()     # Location of output file



## For the main window gui
# The following allows you to access the auto-generated gui from pyuic5
from GUIs import basic_GUI as gui
class MainUiClass(QtWidgets.QMainWindow, gui.Ui_MainWindow):
    def __init__(self, parent=None):
        # super(MainUiClass, self).__init__(parent)
        super().__init__(parent)
        self.setupUi(self)
#----------------------------------------------------------------------------------

        # Initialize variables
        self.pressure = 14.696  # psi, reference static pressure (set to SL press for now)
        self.temperature = 70   # degF, reference static temperature

        self.thread = None   # Humidity generator thread
        self.threadSS = None # WVSS thread

        # Put similar widgets in lists
        self.createLists()

        # Window setup information that doesn't get auto-generated by pyuic5
        self.setupImages()      # generate self images
        self.setDefaults()      # generate defaults for certain items
        self.menuActions()    # generate activity from menubar
        self.addDDOptions()   # add options to dropdown boxes
        self.defaultDD()   # set default dropdowns
        self.editRadioButtons()   # grey out radio buttons before initializing

        # Change default formatting
        icon = QtGui.QIcon('icon.jpg')
        self.setWindowIcon(icon)  # set the icon in the upper left corner of window
        self.viewFormatting()   # set aestetics of the page

        # Initialize instance of DI-145 and WVSS (modified from setupGUIclicked())
        self.s = None
        self.ss = None

        # Connect update activity
        self.updateBackgroundConditions()    # set temperature and pressure based on input
        self.updateDDBoxes()
        self.updateStartStopButtons()
        self.closeProgram()

    def setDefaults(self):
        # Set whether pressure and temperature is measured or fixed
        self.measuredPress = False
        self.measuredTemp = False

        self.setPressActive = False
        self.setTempActive = False

        # Default temperature measurement not in counts
        self.use_temp_counts = False

        # Default recording parameters
        self.rec_defaults = ['Pressure']
        self.rec_options = ['Temperature degF','Temperature degC','Dew Point degF','Dew Point degC','Relative Humidity',\
            'Mass Mixing Ratio','Vapor Concentration','Vapor Pressure','Gamma','Density','Voltage','Counts']

        # Initialize instance of Recording class
        self.rec = record.Recording()

        # Generate the default offLED
        self.statusLED.setPixmap(self.offLED)
        self.statusLED.setScaledContents(True)

        # Set recording lineEdits to read only
        self.recLocEdit.setReadOnly(True)
        self.recLengthEdit.setReadOnly(True)
        self.rdgNumEdit.setReadOnly(True)

        # Tell if port configuration is setup correctly
        self.active = False

        # Initialize instance of RecGUI and default checked boxes
        self.rdlg = RecGUI(self)
        self.checked = [self.rdlg.tempFBox,self.rdlg.dpFBox,self.rdlg.rhBox,self.rdlg.mmrBox,self.rdlg.vcBox]
        self.chkboxes = [self.rdlg.tempFBox,self.rdlg.tempCBox,self.rdlg.dpFBox,self.rdlg.dpCBox,self.rdlg.rhBox,\
            self.rdlg.mmrBox,self.rdlg.vcBox,self.rdlg.vpBox,self.rdlg.gamBox,self.rdlg.rhoBox,self.rdlg.voltBox,\
            self.rdlg.cntBox]
        self.options = ['Temperature degF','Temperature degC','Dew Point degF','Dew Point degC','Relative Humidity',\
            'Mass Mixing Ratio','Vapor Concentration','Vapor Pressure','Gamma','Density','Voltage','Counts']

    def setupImages(self):
        # Change directory for image
        owd = os.getcwd()           # original working directory
        os.chdir(owd+'\\images')    # change directory to location of images

        # Define LED images
        self.greenLED = QtGui.QPixmap('green_led.png')
        self.amberLED = QtGui.QPixmap('amber_led.png')
        self.offLED =   QtGui.QPixmap('off_led.png')

        self.stopSign = QtGui.QPixmap('stopsign.png')

        # Go back to original directory
        os.chdir(owd)    # change directory to original working directory

    def genRecordButton(self):
        self.statusLED.setPixmap(self.amberLED)  # turn the light to amber

        self.recordButton.clicked.connect(self.recordButtonPress)
        self.recordStopButton.clicked.connect(self.recordStopButtonPress)

    def recordControls(self):
        '''Changes components that need to be modified when record changes state'''
        if self.rec.continuationLC or self.rec.continuationSS:     # we are in record mode
            self.statusLED.setPixmap(self.greenLED)
        else:       # we are not in record mode
            self.statusLED.setPixmap(self.amberLED)

    def recordStopButtonPress(self):
        '''Setup record stop button capability'''
        self.statusLED.setPixmap(self.amberLED)

        self.rec.recEnabled = False          # Indicate we are in record mode

    def recordButtonPress(self):
        '''Setup record button capability'''
        self.statusLED.setPixmap(self.greenLED)

        self.rec.check_for_latest_reading()  # Look for latest reading in the file and increment
        self.rec.recEnabled = True          # Indicate we are in record mode
        self.rec.time_start = time.time()   # Track start time with button push
        self.rec.time_end = self.rec.time_start + self.rec.record_length
        print('Recording for {} seconds'.format(self.rec.record_length))

        self.rdgNumEdit.setText(str(self.rec.rdg))  # Update the reading number in the GUI

    def createLists(self):
        self.DDitems = ['Dew Point degF','Dew Point degC','Mass Mixing Ratio','Relative Humidity','Water Vapor Concentration',\
          'Gamma','Air Density','Vapor Pressure','Counts','Voltage']
        self.boxes = [self.HumGenDDbox1, self.HumGenDDbox2, self.HumGenDDbox3]

        self.units = [self.HumGenUnits1, self.HumGenUnits2, self.HumGenUnits3]
        self.LCDs = [self.HumGenLCD1, self.HumGenLCD2, self.HumGenLCD3]

        self.unitss = [self.WVSSUnits1, self.WVSSUnits2, self.WVSSUnits3]
        self.LCDss = [self.WVSSLCD1, self.WVSSLCD2, self.WVSSLCD3]

        self.LCDair = [self.PressLCD, self.TempLCD]

        self.lcLabels = [self.lcLabel1, self.lcLabel2, self.lcLabel3]
        self.ssLabels = [self.ssLabel1, self.ssLabel2, self.ssLabel3]

        self.lcRbuttons = [self.StartButton, self.StopButton]
        self.ssRbuttons = [self.WVSSstartButton, self.WVSSstopButton]

        self.all_labels = self.lcLabels + self.ssLabels
        self.all_LCDs = self.LCDs + self.LCDss + self.LCDair
        self.all_Rbuttons = self.lcRbuttons + self.ssRbuttons

        # Airstream conditions dropdown options
        self.pressOptions = ['psi', 'Pa', 'kPa', 'mb', 'inHg']
        self.tempOptions = ['degF', 'degC', 'degR', 'K', 'counts', 'V']

    def menuActions(self):
        self.menuFile.addAction('Exit', self.close).setShortcut('Ctrl+X')  # add option for exiting program from menubar
        self.menuHardware.triggered.connect(self.setupGUIclicked)
        self.menuRecording.triggered.connect(self.recordGUIclicked)

        # Set shortcuts
        self.menuHardware.setShortcut('Ctrl+D')
        self.menuRecording.setShortcut('Ctrl+R')
        self.menuRecord.setShortcut('Ctrl+A')

    def recordGUIclicked(self):
        global avgLength, fname, outLoc

        # Read from temp file to determine defaults
        self.tmpOpen('read')

        # Connect accepted and rejected
        self.rdlg.buttonBox.accepted.connect(self.rdlg.accept)
        self.rdlg.buttonBox.rejected.connect(self.rdlg.reject)

        result = self.rdlg.exec_()
        if result == QtWidgets.QDialog.Accepted:
            # Update global variables from dialog box inputs if in valid range
            if 3 <= float(self.rdlg.avgRecEdit.text()) <= 30:
                avgLength = float(self.rdlg.avgRecEdit.text())
            else:
                msg = common_def.error_msg()
                msg.setText('Please enter an averaged reading length between 3-30 seconds')
                msg.exec_()

            fname = self.rdlg.filenameEdit.text()
            outLoc = self.rdlg.outLocEdit.text()

            # Set record length, filename and filelocation from the dialog box
            self.rec.record_length = avgLength
            self.rec.filename = fname; self.rec.fileLoc = outLoc
            self.rec.getFullFile()
            self.rec.check_for_latest_reading()

            # Set line edit values
            self.recLengthEdit.setText(str(self.rec.record_length))
            self.recLocEdit.setText(str(self.rec.full_filename))
            self.rdgNumEdit.setText(str(self.rec.rdg-1))

            print('File to be saved as: {}'.format(self.rec.full_filename))

            # Modify record button if one of the devices is setup correctly
            if self.active:
                self.genRecordButton()   # generate the record button from instance of RecordButton class
                self.recordButton.setEnabled(True)
                self.recordButton.setToolTip('Press this button to trigger a recording')
                self.recordStopButton.setEnabled(True)

                # Track output variables that are checked
                self.rec_options = []
                self.checked = []
                for chk, option in zip(self.chkboxes, self.options):
                    if chk.isChecked():
                        self.rec_options.append(option)
                        self.checked.append(chk)

                # Set proper headers
                # print(self.rec_options)
                self.rec.headers = self.rec.iheaders + self.rec_defaults + self.rec_options  # set the headers
                print('rec.headers = {}'.format(self.rec.headers))
            else:
                self.recordButton.setEnabled(False)
                self.recordButton.setToolTip('You are not configured press Ctrl+P first to ' +
                                'configure the devices, then press Ctrl+R to configure recordings')
                self.recordStopButton.setEnabled(False)

            # Store data from this editing of the record GUI
            self.tmpOpen('write')

    def setupGUIclicked(self):
        ''' Control content from setup_GUI by attempting to initiate instances
            of the LiCor and SpectraSensor'''
        global comLC, comSS
        dlg = HardwareGUI(self)
        dlg.buttonBox.accepted.connect(dlg.accept)
        dlg.buttonBox.rejected.connect(dlg.reject)

        # The following executes the dialog box and returns whether it was
        # accepted or rejected
        result = dlg.exec_()
        if result == QtWidgets.QDialog.Accepted:
            '''Try to accept the changes and initialize COM ports.  If unsuccessful,
               show a message box that request cannot be completed'''
            self.active = False
            try:
                # Activate DataQ DI145
                comLC = dlg.lineLC.text()
                self.s = ADC.DataQ_DI145(comLC)
                self.active = True    # Triggers to activate record button if one is true
                for button in self.lcRbuttons:
                    button.setEnabled(True)

                # Look for Checkboxes
                #  Dew Point Generator
                if dlg.dpGenChkBox.isChecked():
                    self.dpGenActive = True # use dew point generator humdity value
                else:  # warn users if hum generator is not selected
                    self.dpGenActive = False
                    msg = common_def.error_msg()
                    msg.setText('DataQ DI-145 is connected but Dew Point Generator is not selected')
                    msg.exec_()
                #  Temperature
                if dlg.tempChkBox.isChecked():
                    self.setTempActive = True
                else:
                    self.setTempActive = False

            except:
                self.dpGenActive = False
                self.setTempActive = False
                msg = common_def.error_msg()
                msg.setText('Could NOT initialize DataQ DI-145 from port {}'.format(comLC))
                msg.exec_()

            try:
                comSS = dlg.lineWVSS.text()
                self.ss = WVSS.WVSS_II(comSS)
                self.active = True    # Triggers to activate record button if one is true
                for button in self.ssRbuttons:
                    button.setEnabled(True)

                # Look for Pressure Checkbox
                if dlg.pressChkBox.isChecked():
                    self.setPressActive = True
                else:
                    self.setPressActive = False

            except:
                self.setPressActive = False
                msg = common_def.error_msg()
                msg.setText('Could NOT initialize Water Vapor Monitor System from port {}'.format(comSS))
                msg.exec_()

    # New Set Conditions dialog box
    def pushButtonClicked(self):

        def getPress(press, units):
            # Convert to PSI
            setPressVal = press
            if units == 'Pa':
                setPressVal = setPressVal * 1.450377e-4
            elif units == 'kPa':
                setPressVal = setPressVal * 0.1450377
            elif units == 'mb':
                setPressVal = setPressVal * 0.01450377
            elif units == 'inHg':
                setPressVal = setPressVal * 0.491154
            return setPressVal

        def getTemp(temp, units):
            # Convert to degrees Fahrenheit
            setTempVal = temp
            if units == 'degC':
                setTempVal = setTempVal * 1.8 + 32
            elif units == 'degR':
                setTempVal = setTempVal + 459.67
            elif units == 'K':
                setTempVal = (setTempVal - 273.15) * 1.8 + 32
            return setTempVal

        dlg = SetCondGUI(self)

        # Disable select option if pressure and temperature are set to read
        if self.setPressActive:
            msg='Pressure is set to read from WVSS, use Ctrl+D to reconfigure if you would like to set the '+\
                 'pressure manually'
            dlg.setPressChkBox.setChecked(False)
            dlg.setPressChkBox.setEnabled(False)
            dlg.setPressChkBox.setToolTip(msg)

            dlg.pressLineEdit.setText('')
            dlg.pressLineEdit.setEnabled(False)
            dlg.pressLineEdit.setToolTip(msg)
        else:
            dlg.setPressChkBox.setEnabled(True)
            dlg.pressLineEdit.setEnabled(True)

        if self.setTempActive:
            msg='Temperature is set to read from DataQ ADC, use Ctrl+D to reconfigure if you would like to set the '+\
                 'temperature manually'
            dlg.setTempChkBox.setChecked(False)
            dlg.setTempChkBox.setEnabled(False)
            dlg.setTempChkBox.setToolTip(msg)

            dlg.tempLineEdit.setText('')
            dlg.tempLineEdit.setEnabled(False)
            dlg.tempLineEdit.setToolTip(msg)
        else:
            dlg.setTempChkBox.setEnabled(True)
            dlg.tempLineEdit.setEnabled(True)


        dlg.buttonBox.accepted.connect(dlg.accept)
        dlg.buttonBox.rejected.connect(dlg.reject)

        # The following executes the dialog box and returns whether it was
        # accepted or rejected
        result = dlg.exec_()
        if result == QtWidgets.QDialog.Accepted:

            # Check for set pressure to be checked
            if dlg.setPressChkBox.isChecked():
                pressVal = float(dlg.pressLineEdit.text())
                units = str(dlg.pressUnitDD.currentText())
                self.updatePress(getPress(pressVal, units))
            if dlg.setTempChkBox.isChecked():
                tempVal = float(dlg.tempLineEdit.text())
                units = str(dlg.tempUnitDD.currentText())
                self.updateTemp(getTemp(tempVal, units))

    def viewFormatting(self):
        # Set tooltips
        self.StartButton.setToolTip('Start scanning the humidity generator')
        self.StopButton.setToolTip('Stop scanning the humidity generator')
        self.WVSSstartButton.setToolTip('Start scanning the WVSS')
        self.WVSSstopButton.setToolTip('Stop scanning the WVSS')
        self.pushButton.setToolTip('Manually apply airstream conditions')

        # Change theme

        # Change label colors
        for label in self.all_labels:
            label.setStyleSheet('color: black')

        # Change LCD colors
        for lcd in self.all_LCDs:
            lcd.setStyleSheet('''QLCDNumber {
                                        background-color: black;
                                        color: white; }''')

        # Record button
        self.recordButton.setEnabled(False)
        self.recordButton.setToolTip('Press Ctrl+H to configure devices before recording data')

        # TEMP GENERATE secondary stop button
        self.recordStopButton = PicButton(self.stopSign, parent=self.groupBox)
        self.recordStopButton.setGeometry(QtCore.QRect(155,25,35,35))

    def addDDOptions(self):
        ''' Add all options to all dropdown boxes'''
        for box in self.boxes:
            box.addItems(self.DDitems)

        # Add for the airstream conditions dropdowns
        self.PressureUnitDD.addItems(self.pressOptions)
        self.TemperatureUnitDD.addItems(self.tempOptions)

    def defaultDD(self):
        ''' Set default selections for dropdown menus '''
        self.HumGenDDbox1.setCurrentIndex(0)  # box1 = dew point
        self.HumGenDDbox2.setCurrentIndex(2)  # box2 = mmr
        self.HumGenDDbox3.setCurrentIndex(3)  # box3 = relative humidity

        # Update the units for each label
        for box, unit, units in zip(self.boxes, self.units, self.unitss):
            self.updateUnits(box.currentText(), unit)
            self.updateUnits(box.currentText(), units)

    def SScanClicked(self):   # Start wvss scan
        try:
            self.threadSS = self.ss
            self.threadSS.change_value.connect(self.updateLCDss)
            self.threadSS.heartbeat.connect(self.indicateScan)
            self.threadSS.start()
            print('WVSS thread started')
        except:
            print('WVSS thread NOT started')

    def SStopClicked(self):   # Stop wvss scan
        try:
            self.threadSS.stop_thread = True
            self.threadSS.exit()
            print('WVSS thread stopped')
        except:
            print('WVSS thread could NOT be stopped')

    def scanClicked(self):
        txtmsg = "Can't establish a connection with the humidity generator, " + \
        "you may need to unplug and then replug in the DataQ DI-145 then press 'Ctrl+D' to " + \
        "reconfigure COM port."

        try:
            self.s.scan()    # Start scan

            # Start thread
            ## Group of Code base on https://www.youtube.com/watch?v=eYJTcLBQKug
            self.thread = self.s

            # Check if devices are being read
            #  Dew Point Generator
            if self.dpGenActive:
                self.thread.change_value.connect(self.updateLCD)
            else:
                self.updateLCD(0)   # Should never get here because dpGenActive should always be set to true

            #  Temperature
            if self.setTempActive:
                self.use_temp_counts = True  # Indicates that temp value passed to updateTemp() is in counts
                self.thread.change_value_temp.connect(self.updateTemp)

            # [self.thread.change_value.connect(x) for x in [self.updateLCD, self.captureDataLC]]  # Connect to multiple slots

            self.thread.heartbeat.connect(self.indicateScan)
            self.thread.start()
            #---------------------------------------------------------------------------------
        except:
            # This means that we've lost comms with device
            msg = common_def.error_msg()
            msg.setText(txtmsg)
            msg.exec_()

    def stopClicked(self):
        txtmsg = "Can't establish a connection with the humidity generator, " + \
        "you may need to unplug and then replug in the DataQ DI-145 then press 'Ctrl+H' to " + \
        "reconfigure COM port."

        try:
            # Try to stop scan
            self.s.sts()    # Stop scan
            self.thread.stop_thread = True
            self.thread.exit()
        except:
            # This means that we've lost comms with device
            msg = common_def.error_msg()
            msg.setText(txtmsg)
            msg.exec_()

    def indicateScan(self, yes_no):
        ''' Connected to heartbeat to tell if we are communicating with devices.'''
        # LiCor Heartbeat
        if yes_no == 'yesLC':
            # Change label colors
            for label in self.lcLabels:
                label.setStyleSheet('color: green')

            # Change LCD colors
            for lcd in self.LCDs:
                lcd.setStyleSheet('''QLCDNumber {
                                            background-color: black;
                                            color: green; }''')
        elif yes_no == 'noLC':
            # Change label colors
            for label in self.lcLabels:
                label.setStyleSheet('color: red')

            # Change LCD colors
            for lcd in self.LCDs:
                lcd.setStyleSheet('''QLCDNumber {
                                            background-color: black;
                                            color: red; }''')
        # Spectra Heartbeat
        elif yes_no == 'yesSS':
            # Change label colors
            for label in self.ssLabels:
                label.setStyleSheet('color: green')

            # Change LCD colors
            for lcd in self.LCDss:
                lcd.setStyleSheet('''QLCDNumber {
                                            background-color: black;
                                            color: green; }''')
        elif yes_no == 'noSS':
            # Change label colors
            for label in self.ssLabels:
                label.setStyleSheet('color: red')

            # Change LCD colors
            for lcd in self.LCDss:
                lcd.setStyleSheet('''QLCDNumber {
                                            background-color: black;
                                            color: red; }''')
        else:
            print('WARNING: heartbeat unable to determine state of a device')

    def updateBackgroundConditions(self):
        self.pushButton.clicked.connect(self.pushButtonClicked)

    def updateStartStopButtons(self):
        self.StartButton.clicked.connect(self.scanClicked)
        self.StopButton.clicked.connect(self.stopClicked)

        self.WVSSstartButton.clicked.connect(self.SScanClicked)
        self.WVSSstopButton.clicked.connect(self.SStopClicked)

    def updateDDBoxes(self):
        # Connect the humidity dropdown boxes
        for box, unit, units in zip(self.boxes, self.units, self.unitss):
            box.activated[str].connect(
               lambda text, unit=unit: self.updateUnits(text, unit))
            box.activated[str].connect(
               lambda text, units=units: self.updateUnits(text, units))

        # Connect the airstream dropdown boxes
        self.PressureUnitDD.activated[str].connect(lambda text, p=self.pressure: self.updatePress(p))
        self.TemperatureUnitDD.activated[str].connect(lambda text, t=self.temperature: self.updateTemp(t))

    def updateUnits(self, text, unit):
        unit.setFont(QtGui.QFont('Arial', 20))
        if text == 'Dew Point degF':
            unit.setText('degF')
        if text == 'Dew Point degC':
            unit.setText('degC')
        elif text == 'Mass Mixing Ratio':
            unit.setText('kgH2O/kgAir')
        elif text == 'Relative Humidity':
            unit.setText('%')
        elif text == 'Counts':
            unit.setText('')
        elif text == 'Voltage':
            unit.setText('V')
        elif text == 'Water Vapor Concentration':
            unit.setText('H2Oppmv')
        elif text == 'Gamma':
            unit.setText('')
        elif text == 'Air Density':
            unit.setText('lbm/ft\N{SUPERSCRIPT THREE}')
        elif text == 'Vapor Pressure':
            unit.setText('psi')

    def updatePress(self, pressure):
        self.pressure = pressure  # pressure psi
        self.box_loop_air(self.PressLCD, self.PressureUnitDD, pressure)

    def updateTemp(self, temp):
        # Convert units from counts to V to degF
        if self.use_temp_counts:

            import TC
            self.counts = temp
            self.V = 0.0003*self.counts   # convert from counts to Volts
            temp = (self.V-1)/4*100
            # temp = TC.TC_typeJ(self.V)  # convert voltage to TdegF

        else:
            self.counts = -9999
            self.V = -9999.9

        self.temperature = temp  # temperature degrees F
        self.box_loop_air(self.TempLCD, self.TemperatureUnitDD, temp)

    def updateLCD(self, counts):
        # Calculate various atmospheric conditions
        voltage = 0.0003*counts
        TddegC = voltage*10
        TddegF = TddegC*1.8 + 32
        TK = (self.temperature-32)*5/9 + 273.15
        TdK = TddegC + 273.15
        pPa = self.pressure / (spectra_equiv.KPA2PSI/1000)
        mmr = spectra_equiv.humidity_ratio(TK, TdK, pPa)
        rh = spectra_equiv.relative_humidity2(TK, TdK, pPa)*100
        ppmv = spectra_equiv.mole_ratio(mmr)
        gam = spectra_equiv.gamma(self.temperature, self.pressure, mmr)
        rho = spectra_equiv.density(self.temperature, self.pressure, mmr)
        pv = spectra_equiv.vapor_pressure(mmr, self.pressure)

        # Loop to determine what values to put in dataset
        rec_values = self.rec_data(TddegF,TddegC,mmr,rh,counts,voltage,ppmv,gam,rho,pv)

        # Push data to recording
        self.rec.captureDataLC(rec_values)
        self.recordControls()    # change recording light

        # Combine the calculated values for live updates
        values = [TddegF, TddegC, mmr, rh, counts, voltage, ppmv, gam, rho, pv]

        # Set each LCD to the respective value based on combobox selection
        self.box_loop(self.LCDs, values)

    def rec_data(self,TddegF,TddegC,mmr,rh,counts,voltage,ppmv,gam,rho,pv):
        # Loop to determine what values to put in dataset
        rec_values = []
        rec_opts = self.rec_defaults + self.rec_options  # Add temp and press as defaults
        for text in rec_opts:
            if text == 'Dew Point degF':
                rec_values.append(TddegF)
            elif text == 'Dew Point degC':
                rec_values.append(TddegC)
            elif text == 'Mass Mixing Ratio':
                rec_values.append(mmr)
            elif text == 'Relative Humidity':
                rec_values.append(rh)
            elif text == 'Counts':
                rec_values.append(counts)
            elif text == 'Voltage':
                rec_values.append(voltage)
            elif text == 'Vapor Concentration':
                rec_values.append(ppmv)
            elif text == 'Gamma':
                rec_values.append(gam)
            elif text == 'Density':
                rec_values.append(rho)
            elif text == 'Vapor Pressure':
                rec_values.append(pv)
            elif text == 'Temperature degF':
                rec_values.append(self.temperature)
            elif text == 'Temperature degC':
                rec_values.append(self.temperature)
            elif text == 'Pressure':
                rec_values.append(self.pressure)
            else:
                rec_values.append(-9999.99)
        return rec_values

    def updateLCDss(self, raw_string):
        # Convert raw_string to list of values
        vals = WVSS.parse_string(raw_string)

        # Determine if pressure should be used
        if self.setPressActive:
            self.updatePress(vals[1] * 0.01450377)  # display pressure in psi from mb

        # Calculate relevant variables
        voltage = 9999.0
        counts = vals[3]
        ppmv = vals[0]
        mmr = spectra_equiv.humidity_ratio2(ppmv)
        TddegF = spectra_equiv.dew_point(mmr, self.pressure)
        TddegC = (TddegF - 32) / 1.8
        rh = spectra_equiv.relative_humidity1(self.temperature, mmr, self.pressure)*100
        gam = spectra_equiv.gamma(self.temperature, self.pressure, mmr)
        rho = spectra_equiv.density(self.temperature, self.pressure, mmr)
        pv = spectra_equiv.vapor_pressure(mmr, self.pressure)

        # Loop to determine what values to put in dataset
        rec_values = self.rec_data(TddegF,TddegC,mmr,rh,counts,voltage,ppmv,gam,rho,pv)

        # Push data to recording
        self.rec.captureDataSS(rec_values)
        self.recordControls()    # change recording light

        # Combine the calculated values
        values = [TddegF, TddegC, mmr, rh, counts, voltage, ppmv, gam, rho, pv]

        # Set each LCD to the respective value based on combobox selection
        self.box_loop(self.LCDss, values)

    def box_loop(self, LCDS, values):
        for lcd, box in zip(LCDS, self.boxes):
            box_val = str(box.currentText())
            if box_val == 'Dew Point degF':
                lcd.display('{:.2f}'.format(round(values[0], 2)))
            elif box_val == 'Dew Point degC':
                lcd.display('{:.2f}'.format(round(values[1], 2)))
            elif box_val == 'Mass Mixing Ratio':  # Mass mixing ratio
                lcd.display('{:.5f}'.format(round(values[2], 5)))
            elif box_val == 'Relative Humidity':  # Relative humidity
                lcd.display('{:.2f}'.format(round(values[3], 2)))
            elif box_val == 'Counts':  # Counts
                lcd.display('{0:d}'.format(int(values[4])))
            elif box_val == 'Voltage':  # Voltage
                lcd.display('{:.3f}'.format(round(values[5], 3)))
            elif box_val == 'Water Vapor Concentration':
                lcd.display('{:.1f}'.format(round(values[6], 1)))
            elif box_val == 'Gamma':
                lcd.display('{:.3f}'.format(round(values[7], 3)))
            elif box_val == 'Air Density':
                lcd.display('{:.4f}'.format(round(values[8], 4)))
            elif box_val == 'Vapor Pressure':
                lcd.display('{:.3f}'.format(round(values[9], 3)))

    def box_loop_air(self, lcd, box, value):
        import TC
        box_val = str(box.currentText())
        if box_val == 'psi':
            lcd.display('{:.3f}'.format(round(value, 3)))
        elif box_val == 'Pa':
            lcd.display('{0:d}'.format(int(value/1.450377e-4)))
        elif box_val == 'kPa':
            lcd.display('{:.3f}'.format(round(value/0.1450377, 3)))
        elif box_val == 'mb':
            lcd.display('{:.3f}'.format(round(value/0.01450377, 3)))
        elif box_val == 'inHg':
            lcd.display('{:.2f}'.format(round(value/0.491154, 2)))
        elif box_val == 'degF':
            lcd.display('{:.2f}'.format(round(value, 2)))
        elif box_val == 'degC':
            lcd.display('{:.2f}'.format(round((value-32) / 1.8, 2)))
        elif box_val == 'degR':
            lcd.display('{:.2f}'.format(round(value + 459.67, 2)))
        elif box_val == 'K':
            lcd.display('{:.2f}'.format(round((value-32)/1.8 + 273.15, 2)))
        elif box_val == 'counts':
            lcd.display('{0:d}'.format(int(self.counts)))
        elif box_val == 'V':
            lcd.display('{:.3f}'.format(round(self.V, 3)))

    def editRadioButtons(self):
        for Rbutton in self.all_Rbuttons:
            Rbutton.setEnabled(False)   # Default disable radio buttons

    def chkbox(self, list_checkboxes):
        '''Reads from tmp file to determine what should be checked'''
        [box.setChecked(False) for box in self.chkboxes]  # uncheck all boxes first
        for box in list_checkboxes:
            if box == 'Dew Point':
                self.rdlg.dpBox.setChecked(True)
            elif box == 'Mass Mixing Ratio':
                self.rdlg.mmrBox.setChecked(True)
            elif box == 'Relative Humidity':
                self.rdlg.rhBox.setChecked(True)
            elif box == 'Counts':
                self.rdlg.cntBox.setChecked(True)
            elif box == 'Voltage':
                self.rdlg.voltBox.setChecked(True)
            elif box == 'Vapor Concentration':
                self.rdlg.vcBox.setChecked(True)
            elif box == 'Gamma':
                self.rdlg.gamBox.setChecked(True)
            elif box == 'Density':
                self.rdlg.rhoBox.setChecked(True)

    def tmpOpen(self, read_write):
        '''read_write is a string that is = either "read" or "write" '''
        # global avgLength, fname, outLoc

        # If selected to write, this happens after recGUI has been accepted
        if read_write == 'write':
            fileLoc = self.rec.fileLoc

            timeval = [str(time.strftime('%Y%m%d_%H%M%S'))]
            recvals = [str(i) for i in \
                       [self.rec.rdg, self.rec.record_length, self.rec.filename, fileLoc]]
            optvals = [str(i) for i in self.rec_options]
            csvals =  ','.join(timeval+recvals+optvals)

            f = open('tmp.txt','w')
            f.write(csvals)
            f.close()

        # If selected to read, which happens when recGUI has been opened
        elif read_write == 'read':
            try:
                f = open('tmp.txt','r')
                csvals = f.read().split(',')

                # Apply fill in blanks
                # self.rec.rdg = int(csvals[1])
                self.rdlg.avgRecEdit.setText(str(csvals[2]))
                self.rdlg.filenameEdit.setText(csvals[3])
                self.rdlg.outLocEdit.setText(csvals[4])

                # Apply checkboxes
                self.chkboxes(csvals[5:])

                f.close()

            except:
                pass  # file probably doesn't exist

    def closeProgram(self):
        # self.CloseButton.clicked.connect(QtWidgets.QApplication.instance().quit)  # close program with button
        self.CloseButton.clicked.connect(QtWidgets.qApp.quit)  # close program with button


# This class is used more of a demostration to show how to configure classes which
# instances are children of the MainWindow
class RecordButton(QtWidgets.QPushButton):
    def __init__(self, text, parent):
        super().__init__(text, parent=parent)
        self.setAutoFillBackground(True)

    def _set_color(self, col):
        palette = self.palette()
        palette.setColor(self.backgroundRole(), col)
        self.setPalette(palette)

    color = QtCore.pyqtProperty(QtGui.QColor, fset=_set_color)

# Create an image pushbutton
class PicButton(QtWidgets.QAbstractButton):
    def __init__(self, pixmap, parent=None):
        super(PicButton, self).__init__(parent)
        self.pixmap = pixmap

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)

    def sizeHint(self):
        return self.pixmap.size()

# The following is to guarantee that all processes are killed, find it here:
# https://stackoverflow.com/questions/22291434/pyqt-application-closes-successfully-but-process-is-not-killed
import psutil
def kill_proc_tree(pid, including_parent=True):
    parent = psutil.Process(pid)
    for child in parent.children(recursive=True):
        child.kill()
    if including_parent:
        parent.kill()

if __name__=='__main__':
    a = QtWidgets.QApplication(sys.argv)

    # Set stylesheet
    # from BreezeStyleSheets import breeze_resources
    # file = QtCore.QFile(":/light.qss")
    # file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
    # stream = QtCore.QTextStream(file)
    # a.setStyleSheet(stream.readAll())

    app = MainUiClass()
    app.show()
    sys.exit(a.exec_())

    me = os.getpid()
    kill_proc_tree(me)
