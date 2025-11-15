# Smart-Room-Monitor
Smart Room Monitor is a hybrid embedded system built using:

Arduino Uno (for fast analog sampling)

STM32L476 Nucleo (for processing and visual indication)

Light sensor (photoresistor)

Sound sensor

Thermistor (temperature sensor)

🔍 How it works

The Arduino reads 3 analog sensors:

Light intensity

Sound level

Temperature (thermistor)

Arduino formats the sensor values into a text string like:

L:350 S:128 T:29.4


Arduino sends these packets to the STM32 over UART2.(PC is the bridge)

The STM32 receives each packet using bare-metal UART code.
No HAL. No libraries. Everything is manual and lightweight.

After decoding the message, the STM32:

Turns Green LED ON for light updates

Turns Blue LED ON for temperature updates

Turns Red LED ON for sound spikes

Flashes LEDs whenever new data is received

Data and sensor values graphs are shown on the pc in real Time with Warning messages.

The system updates in real time, allowing you to watch the LEDs reflect sensor changes immediately.

NOTE: i only used arduino uno because the stm32 gave me a hard time with the adc readings either constant with barely any changes just nonsense and i think this is due to the board having many pins conflicts visible even on cubeMx so i had to go with the arduino for the adc readings
