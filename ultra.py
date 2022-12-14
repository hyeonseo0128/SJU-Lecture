import RPi.GPIO as GPIO
import time

import http_adn
import conf

http_adn.crtae(conf.conf['ae']['parent'], conf.conf['ae']['name'], conf.conf['ae']['appid'])
http_adn.crtct(conf.conf['cnt']['parent'], 'ultrasonic', 0)
http_adn.crtct(conf.conf['cnt']['parent'], 'servo-motor', 0)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

TRIG = 13
ECHO = 19

RED = 22
GREEN = 27
BLUE = 17

GPIO.setup(RED, GPIO.OUT)
GPIO.setup(GREEN, GPIO.OUT)
GPIO.setup(BLUE, GPIO.OUT)
print("초음파 거리 측정기")

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.output(TRIG, False)
print("초음파 출력 초기화")
time.sleep(2)

try:
    while True:
        GPIO.output(TRIG,True)
        time.sleep(0.00001)        # 10uS의 펄스 발생을 위한 딜레이
        GPIO.output(TRIG, False)

        while GPIO.input(ECHO)==0:
            start = time.time()     # Echo핀 상승 시간값 저장

        while GPIO.input(ECHO)==1:
            stop = time.time()      # Echo핀 하강 시간값 저장

        check_time = stop - start
        distance = check_time * 34300 / 2
        if distance < 50:
            GPIO.output(RED, True)
            GPIO.output(BLUE, False)
        else:
            GPIO.output(BLUE, True)
            GPIO.output(RED, False)

        http_adn.crtci(conf.conf['cnt']['parent'] + '/ultrasonic', distance, None)
        print("Distance : %.1f cm" % distance)
        time.sleep(0.4)

except KeyboardInterrupt:
    print("거리 측정 완료 ")
    GPIO.cleanup()
