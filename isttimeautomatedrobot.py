import network
import ntptime
import machine
import time

ir_sensor_pin = machine.Pin(12, machine.Pin.IN)
ir_sensor_pin1 = machine.Pin(13, machine.Pin.IN)
led = machine.Pin(32, machine.Pin.OUT)
led2 = machine.Pin(33, machine.Pin.OUT)
led.off()
led2.off()

def connect_wifi(ssid, password):
    # Connect to the Wi-Fi network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print("Connecting to Wi-Fi...")
        sta_if.active(True)
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            pass
    print("Connected to Wi-Fi:", sta_if.ifconfig())

def get_ntp_time():
    # Set the NTP server
    ntptime.host = "pool.ntp.org"
    # Get the NTP time
    ntptime.settime()
    # Get the local time
    t = machine.RTC().datetime()
    print("NTP Time:", t)
    return t

# Connect to the mobile hotspot
connect_wifi("Skilancer solar 5G", "solar@5274")

# Get the NTP time
while True:
    t = get_ntp_time()
    # Calculate the IST time from the NTP time
    ist_hour = t[4] + 5
    ist_minute = t[5] + 30

    if ist_hour >= 24:
        ist_hour -= 24

    if ist_minute >= 60:
        ist_minute -= 60
        ist_hour += 1

    # Print the values of the IST time
    print("Year:", t[0])
    print("Month:", t[1])
    print("Day:", t[2])
    print("Hour (IST):", ist_hour)
    print("Minute (IST):", ist_minute)
    # Check if the time matches the requirement
    if ist_hour == 16 and ist_minute == 35:
        print("LED turning on")
        led.on()
        print("robot is moving forward")
        ir_value=ir_sensor_pin.value()
        while ir_value==1:
            ir_value=ir_sensor_pin.value()
            if ir_value==0:
                led.off()
                print("Forward motion is stopped")
                led2.on()
                print("Backward motion start")
                ir_value1=ir_sensor_pin1()
                while ir_value1==1:
                    ir_value1=ir_sensor_pin1()
                    if ir_value1==0:
                        print("The robot is going to stop")
                        led2.off()
                        break
                break
    else:
        print("bye ")
    time.sleep(60)


