#!/usr/bin/env python

try:
        import time
        from time import sleep
        import datetime
        import os
        import RPi.GPIO as GPIO

        # BLINK CYCLE ENDING WITH LED OFF
        def Blink(pin):
                GPIO.output(pin,GPIO.HIGH)
                sleep(.1)
                GPIO.output(pin,GPIO.LOW)
                sleep(.1)
                return

        # BLINK CYCLE ENDING WITH LED ON
        def AltBlink(pin):
                for i in range(0, 20):
                        GPIO.output(pin,GPIO.LOW)
                        sleep(.1)
                        GPIO.output(pin,GPIO.HIGH)
                        sleep(.1)
                return

        # TRIGGER A JobA or JobB BUILD DEPENDING ON THE INPUT
        def runTheBuild(targetJob):
                # REPLACE ITEMS INSIDE SQUARE BRACKETS WITH YOUR CREDS 
                GPIO.output(blinker,GPIO.HIGH)
                print('Triggered a build of ' + job + ' at ' + renderedTime)
                if ( targetJob == jobATarget ):
                        os.system("curl -v -u [USERNAME]:[PASSWORD] http://[JENKINS URL]/job/JobA/build --request POST")
                        AltBlink(branchA_LED)
                else :
                        os.system("curl -v -u [USERNAME]:[PASSWORD] http://[JENKINS URL]/job/JobB/build --request POST")
                        AltBlink(branchB_LED)
                sleep(5)
                GPIO.output(blinker,GPIO.LOW)

        # GPIO PINS FOR INTERACTIONS (BCM)
        blinker = 17
        armingSwitch = 24
        launchButton = 18
        branchButton = 23
        branchA_LED = 22
        branchB_LED = 25

        # SET YOR JOB TARGETS
        jobATarget = "JobA"
        jobBTarget = "JobB"

        # SET THE DEFAULT BRANCH TARGET
        targetJob = jobATarget

        # GPIO SETUP
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(launchButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(armingSwitch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(blinker, GPIO.OUT)
        GPIO.setup(branchButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(branchA_LED, GPIO.OUT)
        GPIO.setup(branchB_LED, GPIO.OUT)

        ts = time.time()
        renderedTime = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

        while True:
                launchButtonState = GPIO.input(launchButton)
                branchButtonState = GPIO.input(branchButton)

                if ( GPIO.input(armingSwitch) == True ):
                        armed = True
                        #print("armed")
                        Blink(blinker)
                else:
                        armed = False
                        #print("unarmed")

                # BRANCH SWITCHING
                if ( branchButtonState == 0 ):
                        if ( targetJob == jobATarget ):
                                targetJob = jobBTarget
                                GPIO.output(branchA_LED,GPIO.LOW)
                                GPIO.output(branchB_LED,GPIO.HIGH)
                                print("Switched to JobA")
                                print(targetJob)
                        elif ( targetJob == jobBTarget ):
                                targetJob = jobATarget
                                GPIO.output(branchA_LED,GPIO.HIGH)
                                GPIO.output(branchB_LED,GPIO.LOW)
                                print("Switched to JobB")
                                print(targetJob)
                sleep(0.2)

                # BUTTON HANDLING/DEBOUNCING
                if ( armed == True ):
                        if ( launchButtonState == 0 ) and ( targetJob == jobATarget ):
                                runTheBuild(jobATarget)
                                sleep(0.5)

                        elif ( launchButtonState == 0 ) and ( targetJob == jobBTarget ):
                                runTheBuild(jobBTarget)
                                sleep(0.5)
                        sleep(0.1)
                sleep(0.1)


except KeyboardInterrupt:
        GPIO.cleanup()