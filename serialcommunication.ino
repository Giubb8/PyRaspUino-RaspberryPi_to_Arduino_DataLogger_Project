//www.elegoo.com
//2018.10.25
String command;

#include <dht_nonblocking.h>
#define DHT_SENSOR_TYPE DHT_TYPE_11
#define sensor 3
#define greenLed 10

static const int DHT_SENSOR_PIN = 3;
DHT_nonblocking dht_sensor( DHT_SENSOR_PIN, DHT_SENSOR_TYPE );



/*
 * Initialize the serial port.
 */
void setup( )
{
  Serial.begin(9600);
  pinMode(greenLed,OUTPUT);
  //Serial.println("arduino ready");
}



/*
 * Poll for a measurement, keeping the state machine alive.  Returns
 * true if a measurement is available.
 */
static bool measure_environment( float *temperature, float *humidity )
{
  static unsigned long measurement_timestamp = millis( );

  /* Measure once every four seconds. */
  if( millis( ) - measurement_timestamp > 3000ul )
  {
    if( dht_sensor.measure( temperature, humidity ) == true )
    {
      measurement_timestamp = millis( );
      return( true );
    }
  }
  //Serial.println("false");
  return( false );
}



/*
 * Main program loop.
 */
void loop( )
{
  float temperature;
  float humidity;

  /* Measure temperature and humidity.  If the functions returns
     true, then a measurement is available. */
  if( measure_environment( &temperature, &humidity ) == true ){   
    //digitalWrite(greenLed,HIGH);
    //Serial.print( "T = " );
    Serial.println(temperature);
    Serial.println(humidity);
    /*Serial.print( " deg. C, H = " );
    Serial.print( humidity, 1 );
    Serial.println( "%" );*/
    
    if(Serial.available() >0){//se la comunicazione seriale e' attiva 
      command=Serial.readStringUntil('\n');//legge fino a quando non incontro uno \n
      command.trim();//leva gli spazi bianchi
      if(command.equals("light")){
        digitalWrite(greenLed,HIGH);  
      }
      else if(command.equals("off")){
        digitalWrite(greenLed,LOW);
      }  
    }
    delay(1000);//lo mettiamo alla fine perche altrimenti creerebbe problemi con la comunicazione
  }

 
  
}
