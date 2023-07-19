import atexit
import odroid_wiringpi as wpi
from time import sleep
from common import LED_WIRINGPI_PIN

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

  # Blink LED 5 times
  for _ in range(5):
    wpi.digitalWrite(LED_WIRINGPI_PIN, wpi.HIGH)
    sleep(0.5)
    wpi.digitalWrite(LED_WIRINGPI_PIN, wpi.LOW)
    sleep(0.1)
    wpi.digitalWrite(LED_WIRINGPI_PIN, wpi.HIGH)
    sleep(0.1)
    wpi.digitalWrite(LED_WIRINGPI_PIN, wpi.LOW)
    sleep(0.1)
    wpi.digitalWrite(LED_WIRINGPI_PIN, wpi.HIGH)
    sleep(0.1)

  # Make sure LED is off
  wpi.digitalWrite(LED_WIRINGPI_PIN, wpi.LOW)
