# Hashim Bukhtiar (bukhtiah)
# Team 6 Computing

from time import sleep
from gpiozero import Motor, LED
from sensor_library import *
import matplotlib.pyplot as plt

def rolling_average(data_points, num_points):
    # Calculates the rolling average of the last n data points
    data_points = [float(dp) for dp in data_points] # Converts all data points into floats

    if len(data_points) < num_points: # Average is None if there are less than n data points
        return None
    else:
        return round(sum(data_points[-num_points:]) / num_points, 2) # returns rolling average rounded to 2 decimals

def plot_points(readings_lst, reading_avg_lst):
    # PROCESS 2:
    # Take rolling average and distance at each reading and plot both with
    # respect to the reading number
    reading_nums = [i for i in range(1,len(readings_lst)+1)] # Creates a list of numbers from 1 to number of readings
    plt.plot(reading_nums, readings_lst, label = "Distance Readings") # Plots distances
    plt.plot(reading_nums, reading_avg_lst, label = "Rolling Average") # Plots averages
    plt.xlabel('Reading Number')
    plt.ylabel('Distance (mm)')
    plt.title("Distances and Rolling Averages")
    plt.legend()
    plt.show() # Display plot
    

def check_valid_range(shelf_status, number_points):
    # Continuously gets input from Distance Sensor and ensures that the user's hand is in
    # the proper range for mechanism activation
    # PROCESS 1:
    # Compare rolling average to target distance and activate motor in response to this

    sensor = Distance_Sensor()
    readings_list = []
    avgs_list = []
    num_readings = 0
    TARGET_DISTANCE = 75 # mm
    reading_avg = float('inf')
    print("\nReading\t\tDistance (mm)\t\tAverage")
            
    while reading_avg > TARGET_DISTANCE: # Rolling average in given iteration is greater than the target distance
        sensor_reading = sensor.distance() # Distance reading from sensor
        num_readings += 1
        readings_list.append(sensor_reading) # Add reading to readings list 
        reading_avg = rolling_average(readings_list, number_points)
        avgs_list.append(reading_avg) # Add rolling average to averages list
        print(f"{num_readings}\t\t{sensor_reading}\t\t\t{reading_avg}")

        if reading_avg == None: # If there are not enough data points (<n) keep the loop going
            reading_avg = float('inf')
        sleep(0.1)

    if shelf_status == 'Top': # Update shelf position and return list of readings and averages
        return 'Bottom', readings_list, avgs_list
    else:
        return 'Top', readings_list, avgs_list

def motor_led_activation(shelf_status):
    # Activates motors in CW or CCW direction depending on shelf position
    # If motors are spinning, the LED is lit, indicating
    # to the user that the motors are spinning
    motor1 = Motor(forward=12, backward=16)
    motor2 = Motor(forward=20, backward=7)
    red_led = LED(13)
    
    if shelf_status == 'Bottom':
        print("\nDC MOTORS SPINNING CCW") # Message output to user
        motor1.backward()
        motor2.forward()
    else:
        print("\nDC MOTORS SPINNING CW") # Message output to user
        motor1.forward()
        motor2.backward()

    red_led.on()
    print("LIGHT ON\n") # Message output to user
    sleep(16) # change rotation time after testing
    motor1.stop()
    motor2.stop()
    red_led.off()
    print("LIGHT OFF\n") # Message output to user
