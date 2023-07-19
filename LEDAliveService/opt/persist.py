import atexit
from threading import Thread
import odroid_wiringpi as wpi
from time import sleep
from common import LED_WIRINGPI_PIN

DELAY_MULTIPLIER = 1.5
HEARTBEAT_SEQ = [(True, 0.1), (False, 0.1), (True, 0.1), (False, 1.7)]

def heartbeat():
  while True:
    for item in HEARTBEAT_SEQ:
      wpi.digitalWrite(LED_WIRINGPI_PIN, wpi.HIGH if item[0] else wpi.LOW)
      sleep(item[1] * DELAY_MULTIPLIER)

def exit_handler():
  # Make sure LED is off
  wpi.digitalWrite(LED_WIRINGPI_PIN, wpi.LOW)

if __name__ == "__main__":
  # WiringPi setup
  wpi.wiringPiSetup()

  # Set LED Pin mode to output
  wpi.pinMode(LED_WIRINGPI_PIN, wpi.OUTPUT)

  # Register program exit handler
  atexit.register(exit_handler)

  # Start heartbeat thread
  heartbeat_thread = Thread(target=heartbeat)
  heartbeat_thread.start()
