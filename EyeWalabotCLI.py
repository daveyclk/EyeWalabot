from __future__ import print_function
from __future__ import division
from sys import platform
from os import system
import WalabotAPI
import time

#import DRV2605 module from location
from imp import load_source
DRV2605 = load_source('DRV2605', '/home/pi/Adafruit_DRV2605_Library/DRV2605.py')

class Haptic:

    def __init__(self):
        self.hptc = DRV2605.DRV2605()
        self.hptc.set_library(1)
        self.hptc.set_mode(0x00)

    def buzzer(self):
        global zval
        global xval
        #print(zval)
        if ((zval >= 180) & (zval < 200)):
            print("between 180cm and 200cm")            
            self.hptc.set_waveform(0, 51)
            if((xval < 70) & (xval > 20)):
                self.hptc.set_waveform(1, 75) #object coming from the right
                print("object coming from the right")
            elif((xval < 20) & (xval > -20)):
                self.hptc.set_waveform(1, 0) #object dead ahead
                print("object dead ahead") 
            elif((xval > -70) & (xval < -20)):
                self.hptc.set_waveform(1, 87) #object coming from the left                
                print("object coming from the left") 
            self.hptc.go()
        elif ((zval < 180) & (zval >= 150)):
            print("between 180cm and 150cm")                
            self.hptc.set_waveform(0, 50)
            if((xval < 65) & (xval > 18)):
                self.hptc.set_waveform(1, 74) #object coming from the right
                print("object coming from the right")
            elif((xval < 20) & (xval > -20)):
                self.hptc.set_waveform(1, 0) #object dead ahead
                print("object dead ahead") 
            elif((xval > -65) & (xval < -20)):
                self.hptc.set_waveform(1, 86) #object coming from the left                
                print("object coming from the left") 
            self.hptc.go()            
        elif ((zval < 150) & (zval >= 120)):
            print("between 150cm and 120cm")            
            self.hptc.set_waveform(0, 49)
            if((xval < 60) & (xval > 20)):
                self.hptc.set_waveform(1, 73) #object coming from the right
                print("object coming from the right")
            elif((xval < 20) & (xval > -20)):
                self.hptc.set_waveform(1, 0) #object dead ahead
                print("object dead ahead") 
            elif((xval > -60) & (xval < -20)):
                self.hptc.set_waveform(1, 85) #object coming from the left                
                print("object coming from the left") 
            self.hptc.go()             
        elif ((zval < 120) & (zval >= 90)):
            print("betweem 120cm and 90cm")              
            self.hptc.set_waveform(0, 48)
            if((xval < 55) & (xval > 20)):
                self.hptc.set_waveform(1, 72) #object coming from the right
                print("object coming from the right")
            elif((xval < 20) & (xval > -20)):
                self.hptc.set_waveform(1, 0) #object dead ahead
                print("object dead ahead") 
            elif((xval > -55) & (xval < -20)):
                self.hptc.set_waveform(1, 84) #object coming from the left                
                print("object coming from the left") 
            self.hptc.go()             
        
        elif ((zval < 90) & (zval >= 70)):
            print("between 70cm and 90 cm")  
            self.hptc.set_waveform(0, 47)
            if((xval < 50) & (xval > 20)):
                self.hptc.set_waveform(1, 71) #object coming from the right
                print("object coming from the right")
            elif((xval < 20) & (xval > -20)):
                self.hptc.set_waveform(1, 0) #object dead ahead
                print("object dead ahead") 
            elif((xval > -50) & (xval < -20)):
                self.hptc.set_waveform(1, 83) #object coming from the left                
                print("object coming from the left") 
            self.hptc.go()
        elif (zval < 70):
            print("closer than 70cm")
            self.hptc.set_waveform(0, 15)
            if((xval < 45) & (xval > 20)):
                self.hptc.set_waveform(1, 70) #object coming from the right
                print("object coming from the right")
            elif((xval < 20) & (xval > -20)):
                self.hptc.set_waveform(1, 0) #object dead ahead
                print("object dead ahead ") 
            elif((xval > -45) & (xval < -20)):
                self.hptc.set_waveform(1, 82) #object coming from the left                
                print("object coming from the left") 
            self.hptc.go()
       
    def stop(self):
        self.hptc.stop()

class Walabot:

    def __init__(self):
        self.wlbt = WalabotAPI
        self.wlbt.Init()
        self.wlbt.SetSettingsFolder()
        self.isConnected = False
        self.isTargets = False

          
    def connect(self):
        # walabot default values
        R_MAX = 200
        R_MIN = 10
        R_RES = 2
        THETA_MAX = 20
        THETA_RES = 10
        PHI_MAX = 5
        PHI_RES = 1
        THRESHOLD = 100
        try:
            self.wlbt.ConnectAny()
            self.isConnected = True
            self.wlbt.SetProfile(self.wlbt.PROF_SENSOR_NARROW)
            self.wlbt.SetDynamicImageFilter(self.wlbt.FILTER_TYPE_MTI)
            #self.wlbt.SetDynamicImageFilter(self.wlbt.FILTER_TYPE_NONE)
            #self.wlbt.SetDynamicImageFilter(self.wlbt.FILTER_TYPE_DERIVATIVE)            
            self.wlbt.SetArenaTheta(-THETA_MAX, THETA_MAX, THETA_RES)
            self.wlbt.SetArenaPhi(-PHI_MAX, PHI_MAX, PHI_RES)
            self.wlbt.SetArenaR(R_MIN, R_MAX, R_RES)
            self.wlbt.SetThreshold(THRESHOLD)
        except self.wlbt.WalabotError as err:
            if err.code != 19:  # 'WALABOT_INSTRUMENT_NOT_FOUND'
                raise err

    def start(self):
        self.wlbt.Start()

    def calibrate(self):
        self.wlbt.StartCalibration()

    def get_targets(self):
        self.wlbt.Trigger()
        return self.wlbt.GetSensorTargets()

    def stop(self):
        self.wlbt.Stop()

    def disconnect(self):
        self.wlbt.Disconnect()


def main():
    global zval
    global xval   
    hptc = Haptic()
    wlbt = Walabot()
    wlbt.connect()
    if not wlbt.isConnected:
        print('Not Connected')
    else:
        print('Connected')
    wlbt.start()
    print('Starting Walabot')    

    while True:
        targets = wlbt.get_targets()
        if len(targets) > 0:
            targets = wlbt.get_targets()
            if len(targets) > 0:
                print(len(targets))
                targets = targets[0]
                zval = int(targets.zPosCm)
                xval = int(targets.xPosCm)
                print("zval =")
                print(zval)
                print("xval =")
                print(xval)                
            else:
                print("no targets")
                hptc.stop()                   
            hptc.buzzer()
        else:    
            print("no targets")
            hptc.stop()
    wlbt.stop()
    wlbt.disconnect()

if __name__ == '__main__':
    zval = 0
    xval = 0
    while True:
        main()
        
