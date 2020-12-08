import mysql.connector
import datetime
import time
from Adafruit_IO import Client, Feed, RequestError
import pyfirmata

#Connect to database oh yeah
mydb = mysql.connector.connect( 
	host="localhost",
	user="root",
	password="passord",
	database="3elda1"
)

mycursor = mydb.cursor()

print("Connected...")

sql = "INSERT INTO sensor(verdi,tid) VALUES (%s,%s)"

#Brukernavn og nøkkel til adafruit
run_count = 0
ADAFRUIT_IO_USERNAME = "tryors"
ADAFRUIT_IO_KEY = "aio_bxyX27dbupJJuKugYVtaq2VDqKOC"

aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

#Velger COM4 som port til arduino
board = pyfirmata.Arduino('COM4')

it = pyfirmata.util.Iterator(board)
it.start()

#Velger pin 12 som digitalt output og pin A0 som analog input
digital_output = board.get_pin('d:12:o')

analog_input = board.get_pin('a:0:i')

#Sender data til database og adafruit
try:
	digital = aio.feeds('poo')
except RequestError:
	feed = Feed(name='poo')
	digital = aio.create_feed(feed)

while True:

	#Sender verdien på potentiometer til databasen 
	verdi = analog_input.read()
	tid = datetime.datetime.now() 

	val = (verdi, tid)


	mycursor.execute(sql, val)
	mydb.commit()

	#Sender data fra potentiometer til adafruit 
	print('Sending count:', run_count)
	run_count += 1
	aio.send_data('counter', run_count)
	aio.send_data('chart', analog_input.read())
	data = aio.receive(digital.key)

	print('Data: ', data.value)

	if data.value == "ON":
		digital_output.write(True)
	else:
		digital_output.write(False)

	time.sleep(3)