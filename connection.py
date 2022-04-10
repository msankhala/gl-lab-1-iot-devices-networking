from re import L
import pymysql.cursors
import os
from dotenv import load_dotenv

load_dotenv()

MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')

# Connect to the database
connection = pymysql.connect(host=MYSQL_HOST,
                             user=MYSQL_USER,
                             password=MYSQL_PASSWORD,
                             database=MYSQL_DATABASE,
                             cursorclass=pymysql.cursors.DictCursor)

# Check if device_id already exists in devices table
# if not Insert device_id into devices table
def create_device(device_id, description):
    try:
        with connection.cursor() as cursor:
          # Check if device_id already exists in devices table
          sql = "SELECT * FROM devices WHERE device_id = %s"
          cursor.execute(sql, (device_id))
          result = cursor.fetchone()
          if result is None:
              # Insert device_id into devices table
              sql = "INSERT INTO devices (device_id, description) VALUES (%s, %s)"
              cursor.execute(sql, (device_id, description))
              connection.commit()
          else:
            print(f'Device with device_id {device_id} already exists in devices table')
    except Exception as e:
        print(e)

# First get the device_id from devices table and then create data record
# in sensor_data table for device_id in devices table
def create_device_data(device_id, location, temperature, humidity, pressure, reading_time):
    try:
        with connection.cursor() as cursor:
          # Get the device_id from devices table
          sql = "SELECT * FROM devices WHERE device_id = %s"
          cursor.execute(sql, (device_id))
          result = cursor.fetchone()
          if result is not None:
              # Create data record in sensor_data table for device_id in devices table
              sql = "INSERT INTO sensor_data (device_id, location, temperature, humidity, pressure, reading_time) VALUES (%s, %s, %s, %s, %s, %s)"
              cursor.execute(sql, (result['id'], location, temperature, humidity, pressure, reading_time))
              connection.commit()
              print(f'Data record created for device_id {device_id}')
          else:
            print(f'Device with device_id {device_id} does not exist in devices table')
    except Exception as e:
        print(e)

# First get the device_id from devices table and then get the data from
# sensor_data table for device_id in devices table
def get_device_data(device_id):
    try:
        with connection.cursor() as cursor:
          # Get the device_id from devices table
          sql = "SELECT * FROM devices WHERE device_id = %s"
          cursor.execute(sql, (device_id))
          result = cursor.fetchone()
          if result is not None:
              # Get the data from sensor_data table for device_id in devices table
              sql = "SELECT * FROM sensor_data WHERE device_id = %s"
              cursor.execute(sql, (result['id']))
              result = cursor.fetchone()
              if result is not None:
                  print(f'Data for device_id {device_id} is {result}')
              else:
                  print(f'No data for device_id {device_id}')
          else:
            print(f'Device with device_id {device_id} does not exist in devices table')
    except Exception as e:
        print(e)
