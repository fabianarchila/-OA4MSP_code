#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from dronekit import connect, VehicleMode, LocationGlobalRelative
from sensor_msgs.msg import NavSatFix
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String
#from gpiozero import MCP3008
import time

from mavros.base import SENSOR_QOS

class Node1(Node):

    def __init__(self):
        super().__init__("uav_node2")
        self.get_logger().info("Hello from ROS2")
        self.pos_subscriber = self.create_subscription(NavSatFix,"/uavLeader/global_position/global",self.pos_callback,qos_profile=SENSOR_QOS)
        #self.lidar_subscriber = self.create_subscription(LaserScan,"/scan",self.lidar_callback,qos_profile=SENSOR_QOS)
        self.input_val = self.create_subscription(String,"/key_input",self.action_selection,1)
        self.logs_out = self.create_publisher(String,"/logs_out",1)
        #self.smoke_topic = self.create_publisher(String,"/smoke",1)
        self.msg_temp=String()
        self.msg_temp.data = "-----Initializing drone 2----"

        
        self.logs_out.publish(self.msg_temp)
        #self.smoke_m_object = MCP3008(0)
        #self.msg_smoke = String()
        #self.create_timer(0.1,self.share_smoke)
        #self.start_to_share_smoke = False
        #self.logs = "" 
        self.conn_state= False
        self.go_to_state = False
        self.create_timer(0.05,self.go_to_follow)
        self.latitude = 0.0
        self.longitude = 0.0
        self.altitude =0.0
        self.data_recieved =0
    def timer_callback(self):
        self.get_logger().info("2 Battery: %s" % self.vehicle.battery)
    def go_to_follow(self):
        if self.go_to_state == True:
            #self.vehicle.mode = VehicleMode("GUIDED")
            point = LocationGlobalRelative(self.latitude+0.00006, self.longitude+0.00006, 3)
            self.vehicle.simple_goto(point)
    # def share_smoke(self):
    #     if (self.go_to_state == True) or (self.start_to_share_smoke == True):
    #         self.msg_smoke.data=str(self.smoke_m_object.value)
    #         self.smoke_topic.publish(self.msg_smoke)
            

    def action_selection(self, msg: String):
        if msg.data =="enable_connection" and self.conn_state== False:
            self.get_logger().info("Connecting")
            self.msg_temp.data = "Connecting"
            self.logs_out.publish(self.msg_temp)
            try:
                #self.vehicle = connect('/dev/ttyAMA0', wait_ready=True, baud=921600,source_system=1)
                self.vehicle = connect('/dev/ttyAMA0', wait_ready=True, baud=921600)
                self.get_logger().info("2 Global Location: %s" % self.vehicle.location.global_frame)
                self.get_logger().info("2 Device conected")
                self.msg_temp.data = "2 Device conected"
                self.logs_out.publish(self.msg_temp)
                self.conn_state=True
            except:
                self.msg_temp.data = "2 Connection not available"
                self.logs_out.publish(self.msg_temp)
            
        elif msg.data == "close_connection"and self.conn_state==True:
            self.vehicle.close()
            self.get_logger().info("2 Connection finished")
            self.msg_temp.data = "2 Connection finished"
            self.logs_out.publish(self.msg_temp)
            self.conn_state=False
        elif msg.data == "drone_mode" and  self.conn_state==True:
            self.msg_temp.data = self.vehicle.mode.name
            self.logs_out.publish(self.msg_temp)
        elif msg.data == "drone_info" and  self.conn_state==True:
            temp_var=self.vehicle.location.global_relative_frame
            self.msg_temp.data = "2 Is_arm : {} \n logore:lat={}, lon={},alt={}\nBattery={}".format(self.vehicle.is_armable,temp_var.lat,temp_var.lon,temp_var.alt,self.vehicle.battery)
            self.logs_out.publish(self.msg_temp)
        elif msg.data == "landing" and  self.conn_state==True:
            self.vehicle.mode = VehicleMode("LAND")
            self.msg_temp.data = "2 Finishing following"
            self.logs_out.publish(self.msg_temp)
            self.go_to_state = False
        elif msg.data == "takeoff" and self.conn_state == True:
            self.msg_temp.data = "2 Takeoff starting"
            self.logs_out.publish(self.msg_temp)
            if self.vehicle.is_armable == True:
                self.vehicle.armed = True
                self.msg_temp.data = "2 Waiting for arming..."
                now=time.time()
                while (not self.vehicle.armed and time.time()-now<5):
                    self.logs_out.publish(self.msg_temp)
                    time.sleep(1)
                if self.vehicle.armed ==True:
                    self.vehicle.mode = VehicleMode("GUIDED")
                    altitude = 3
                    self.msg_temp.data = "2 Taking off!"
                    self.logs_out.publish(self.msg_temp)
                    self.vehicle.simple_takeoff(altitude)  # Take off to target altitude
                    now=time.time()
                    while True and time.time()-now<5:
                        self.msg_temp.data = "2 Altitude: {}".format(self.vehicle.location.global_relative_frame.alt)
                        self.logs_out.publish(self.msg_temp)
                        # Break and return from function just below target altitude.
                        if self.vehicle.location.global_relative_frame.alt >= altitude * 0.95:
                            self.msg_temp.data = "2 Reached target altitude"
                            self.logs_out.publish(self.msg_temp)
                            break
                        time.sleep(1)

                else:
                    self.msg_temp.data = "2 Not armed"
                    self.logs_out.publish(self.msg_temp)

            else:
                self.msg_temp.data = "2 Not armable"
                self.logs_out.publish(self.msg_temp)
        elif msg.data == "start_mission" and self.conn_state == True:
            if self.go_to_state == False:
                self.msg_temp.data = "2 Starting following"
                self.logs_out.publish(self.msg_temp)
                self.vehicle.mode = VehicleMode("GUIDED")
                self.go_to_state = True
            else:
                self.msg_temp.data = " Finishing following"
                self.logs_out.publish(self.msg_temp)
                self.go_to_state = False


        elif msg.data == "temp":
            self.msg_temp.data = "2 posodro:lat={}, lon={},alt={}, n_data={}".format(self.latitude,self.longitude,self.altitude,self.data_recieved)
            self.logs_out.publish(self.msg_temp)
            # if self.start_to_share_smoke ==False:
            #     self.msg_temp.data = " Starting smoking measurment"
            #     self.logs_out.publish(self.msg_temp)
            #     self.start_to_share_smoke = True
            # else:
            #     self.msg_temp.data = " Finishing smoking measurment"
            #     self.logs_out.publish(self.msg_temp)
            #     self.start_to_share_smoke = False
        # if msg.data =="a" and self.latitude != 0.0:
        #     self.get_logger().info(msg.data)
        #     self.vehicle.mode = dronekit.VehicleMode("GUIDED")
        #     point = dronekit.LocationGlobalRelative(self.latitude, self.longitude, self.altitude)
        #     self.vehicle.simple_goto(point)
    def pos_callback(self,msg : NavSatFix):  
        self.latitude = msg.latitude
        self.longitude = msg.longitude
        self.altitude =msg.altitude
        self.data_recieved+=1

    def lidar_callback(self,msg : LaserScan):  
        pass
        
        



def main(args=None):
    rclpy.init(args=args)
    node = Node1()
    rclpy.spin(node) # For run continuosly de node

    rclpy.shutdown()

if __name__ == '__main__':
    main()