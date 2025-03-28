#!/usr/bin/env python3

import rclpy
import time 

from rclpy.node import Node
from math import atan2, pow, sqrt, degrees, radians, sin, cos
from functools import partial # this is to the SstreamRate service call

from geometry_msgs.msg import Pose, PoseStamped, Point, Quaternion
from geographic_msgs.msg import GeoPoseStamped, GeoPoint
from nav_msgs.msg import Odometry  
from mavros_msgs.srv import StreamRate  # to be able to receive something in global_position/local 
from mavros_msgs.srv import CommandBool # this works for cmd/arming 
from mavros_msgs.srv import CommandTOL # this works for cmd/land and cmd/takeoff

from mavros.base import SENSOR_QOS  # this is for the quality of singal mismatch in the local pos
from mavros_msgs.msg import State
from mavros_msgs.srv import CommandLong
from mavros_msgs.srv import SetMode
from mavros_msgs.srv import CommandInt # for any mavlink command, like ROI
from sensor_msgs.msg import NavSatFix # for global_postition/global
from sensor_msgs.msg import TimeReference #for gps time
from pygeodesy.geoids import GeoidPGM # to measure correct altitude
from std_msgs.msg import String # used to send messages to mqtt

_egm96 = GeoidPGM('/usr/share/GeographicLib/geoids/egm96-5.pgm', kind=-3)

class MiNodo(Node):
    def __init__(self):
        super().__init__("uav") # type: ignore # node name
        #  define here the namespace instead of /mavros/, example for the following launch:
        #  ros2 launch mavros apm.launch dev_url:=ip_address:15200 namespace:=hola 
        self.namespace = "/uavLeader"  
        self.get_logger().info("Nodo uav creado")
        self.time_0 = 0
        self.current_state = State()
        self.c_pose = Odometry()
        self.global_position = NavSatFix()
        self.waypoint_global = GeoPoseStamped()
        self.MAS_position = GeoPoseStamped() # not used
        self.mqtt_msg = String()
        self.alt0 = 0.0 # initial altitude for taking off
        self.alt_after_T_Off_geoid=0 # initial altitude in geoidesic after takeoff
        self.floor_geoid =0.0
        self.alt_AMSL = 0.0
        self.frec = 100.0 # (Hz), con esto, spin_once hace un delay de 10ms
        self.looprate = self.create_rate(self.frec, self.get_clock())
        self.time_gps = TimeReference()
        #self.smoke_level = MCP3202(0) #smoke sensor

        #self.publisher2_ = self.create_publisher(Int64,"number_count",2)
        #self.create_timer( 1 , self.publicar )
        self.cont = 0
        
        #publisher setpoint_position/global topic
        self.gl_pos_pub = self.create_publisher(
            GeoPoseStamped,
            self.namespace+"/setpoint_position/global",
            qos_profile=SENSOR_QOS
        )

        #publisher uav1/GPSposition topic 
        self.MAS_pub = self.create_publisher(
            GeoPoseStamped,
            "/uav1/GPSposition",
            qos_profile=SENSOR_QOS
        )        

       #publisher string_example topic
        self.topic_ping_ros = self.create_publisher(
            String,
            #"/ping/ros",
            "/ros2mqtt/pos",
            1 
        )        
        ###################################
        # SUBSCRIBERS
        ###################################
                #subscriber to the local position
        self.pos_sub=self.create_subscription(
            Odometry, 
            self.namespace+"/global_position/local", 
            self.pos_cb, 
            qos_profile=SENSOR_QOS
        )

        #subscriber to the globl position
        self.gl_pos_sub=self.create_subscription(
            NavSatFix, 
            self.namespace+"/global_position/global", 
            self.global_position_cb, 
            qos_profile=SENSOR_QOS
        )

        self.state_sub=self.create_subscription(
            State,
            self.namespace+"/state", #ojo
            self.state_cb,
            1
        ) 
        self.time_ref_sub=self.create_subscription(
            TimeReference,
            self.namespace+"/time_referece", 
            self.time_ref_cb,
            1
        ) 
  
        self.smoke_sub=self.create_subscription(
            String,
            "/smoke", 
            self.smoke_cb,
            1
        ) 
                 
        #self.create_timer( 10.0 , self.timer_callback)
        self.counter_=0

    def new_method(self):
        return GeoPoseStamped
      
    def pos_cb(self,msg):
        #self.get_logger().info(str(msg.pose.pose.position)) #print the pose       
        self.c_pose = msg
        x = self.c_pose.pose.pose.position.x
        y = self.c_pose.pose.pose.position.y
        z = self.c_pose.pose.pose.position.z
        #self.get_logger().info("x y z ="+str(x)+", "+str(y)+", "+str(z)) #print the pose       
    
    def global_position_cb(self,msg):
        self.global_position = msg
        lat = self.global_position.latitude
        lon = self.global_position.longitude
        alt =  self.global_position.altitude
        time_stamp = self.global_position.header.stamp
        
        #self.get_logger().info("lat lon alt="+str(lat)+", "+str(lon)+", "+str(alt))
        timeROS = self.get_clock().now().to_msg()
        #self.get_logger().info("Elapsed time ="+str(time_1) )
        
        #self.mqtt_msg.data="data: lat lon alt="+str(lat)+","+str(lon)+","+str(alt)
        self.mqtt_msg.data='{"name":"drone1","lat":'+str(lat)+',"lon":'+str(lon)+',"alt":'+str(alt)+',"timeROS":'+str(time_stamp.sec)+"."+str(time_stamp.nanosec)+',"timeGPS":'+str(self.time_gps.time_ref.sec)+"."+str(self.time_gps.time_ref.nanosec)+"}"# timeROS gives the same time as in the global_position, variations of 1ms approx, is the same?
        if (lat ==0.0) & (lon==0.0):
            self.mqtt_msg.data='{"name":"drone1","lat":--,"lon":--,"alt":--,"timeStmp":'+str(time_stamp.sec)+"."+str(time_stamp.nanosec)+"}"
        else:
            self.mqtt_msg.data='{"name":"drone1","lat":'+str(lat)+',"lon":'+str(lon)+',"alt":'+str(alt)+',"timeStmp":'+str(time_stamp.sec)+"."+str(time_stamp.nanosec)+"}"# timeROS gives the same time as in the global_position, variations of 1ms approx, is the same?
        #self.mqtt_msg.data='{"name":"drone1","lat":'+str(lat)+',"lon":'+str(lon)+',"alt":'+str(alt)+',"timeGPS":'+str(time_stamp.sec)+"."+str(time_stamp.nanosec)+"}"

        self.topic_ping_ros.publish(self.mqtt_msg)
           
    
    def state_cb(self,msg):
        self.current_state = msg     

    def time_ref_cb(self,msg):
        self.time_gps = msg

    def smoke_cb(self,msg):
        humo=msg
        self.get_logger().info("Smoke level: " +str(humo.data))
        with open("humo.txt",   "a") as obj_file:
            print(f"{humo.data}",file = obj_file)
  
    def timer_callback(self):
        self.counter_-=1
        for i in range(10):# va de 1 a 10
             self.get_logger().info("cont " +str(self.counter_))

    def wait4connect(self):
        """ Wait until status of uav is connected
        Returns:
                0 (int): Connected to FCU.
                -1 (int): Failed to connect to FCU.
        """
        self.get_logger().info("Waiting for 'connected' status")
        while rclpy.ok() and not self.current_state.connected:
            rclpy.spin_once(self)
            #self.get_logger().info("Despues del loop sleep")        
        else:
            if self.current_state.connected:
                self.get_logger().info("Pixhawk connected")
                return 0
            else:
                self.get_logger().error("Error connecting Pixhawk")
                return -1


    def wait4start(self):
        """ Wait until pilot put uav in Guided (via RC or GCS)
        Returns:
                0 (int): guided.
                -1 (int): fail guided.
        """
        self.get_logger().info("Waiting for user to set mode to GUIDED")
        #while rclpy.ok() and not self.current_state.guided: #este guided es diferente al mode.GUIDED
        while rclpy.ok() and not self.current_state.mode == "GUIDED": #este guided es diferente al mode.GUIDED
            rclpy.spin_once(self)
        else:
            if self.current_state.mode == "GUIDED":
                self.get_logger().info("mode =" +str(self.current_state.mode))
                self.get_logger().info("Mode set to GUIDED. Starting Mission...")
                return 0
            else:
                self.get_logger().error("mode =" +str(self.current_state.mode))
                self.get_logger().error("Error starting Mission...")
                return -1
            
    # SERVICES:
    def arming(self):
        client_a = self.create_client(CommandBool, self.namespace+"/cmd/arming")
        #response = 1
        #while response != 0 and self.current_state.mode == "GUIDED":
        while not client_a.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn('service *arming* not available, waiting again...')
        req = CommandBool.Request()
        req.value = True
        future = client_a.call_async(req)
        future.add_done_callback(partial(self.call_arming_cb))
        self.get_logger().info("arming...")
            #response = future.result
            #if response !=0:
            #    self.get_logger().info("response to arm(): "+str(response))
            #    self.sleep(5)
        

    def call_arming_cb(self, future):
        try:
            response = future.result()
        except Exception as e:
            self.get_logger().error("Service 'arming' call failed %r" % (e))
        self.get_logger().info("response to arm(): "+str(response))
        
    
    def takingoff(self, altitude):
        client_t = self.create_client(CommandTOL, self.namespace+"/cmd/takeoff")
        if self.current_state.mode == "GUIDED":
            while not client_t.wait_for_service(timeout_sec=1.0):
                self.get_logger().warn('service *takeoff* not available, waiting again...')
            req = CommandTOL.Request()
            req.min_pitch = 0.0
            req.altitude = altitude # based on the example mavros/issues/1718
            req.yaw = 0.0
            future = client_t.call_async(req)
            future.add_done_callback(partial(self.call_takingoff_cb))
            self.get_logger().info("takingoff...")

    def call_takingoff_cb(self, future):
        try:
            response = future.result()
        except Exception as e:
            self.get_logger().error("Service 'takingoff' call failed %r" % (e,))
        self.get_logger().info("response to take off: "+str(response))

    def landing(self):
        client_l = self.create_client(CommandTOL, self.namespace+"/cmd/land")
        while not client_l.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn('service landing not available, waiting again...')
        req = CommandTOL.Request()
        req.yaw = 0.0 # there are others like lat, lon, alt, i dont know if they are needed
        future = client_l.call_async(req)
        future.add_done_callback(partial(self.call_landing_cb))
        self.get_logger().info("landing...")

    def call_landing_cb(self, future):
        try:
            response = future.result()
        except Exception as e:
            self.get_logger().error("Service 'landing' call failed %r" % (e,))
        self.get_logger().info("response to landing: "+str(response))

    def start_stream(self):
        """function will start the stream of global_position/local and others. This is necessary for Real Time flight instead of Gazebo
        Returns:
                0 (int):  successful.
                -1 (int):  unsuccessful.        """
        client = self.create_client(StreamRate, self.namespace +"/set_stream_rate")
        while not client.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn('service set_stream_rate not available, trying again...')
        req = StreamRate.Request()
        req.stream_id = 0
        req.message_rate = 1 # Hz, the maximum I saw was like 7Hz
        req.on_off = True
        #future is a functionality of python , not from  ros
        future = client.call_async(req)
        #the following add_done_callback is a functionallity of future to handole more services without crashing
        future.add_done_callback(partial(self.callback_call_stream))

    def callback_call_stream(self, future):
        try:
            response = future.result()
        except Exception as e:
            self.get_logger().error("Service call failed %r" % (e,))
        self.get_logger().info("response from stream service: "+str(response))


    def geoid_hight(self, lat,lon):
        """Calculates AMSL to ellipsoid conversion offset.
        Uses EGM96 data with 5' grid and cubic interpolation.
        The value returned can help you convert from meters 
        above mean sea level (AMSL) to meters above
        the WGS84 ellipsoid.
    	If you want to go from AMSL to ellipsoid height, add the value.
        To go from ellipsoid height to AMSL, subtract this value.
        setpoint_position/global uses AMSL
        global_position/global uses ellipsoid
         """
        return _egm96.height(lat,lon)
    
    def set_global_destination(self, lat, lon, alt):
        # alt is wrt floor, we convert to avobe mean sea level to publish it
        # alt_AMSL = alt + self.alt_after_T_Off_geoid - self.geoid_hight(lat,lon)
        self.alt_AMSL = alt +  self.floor_geoid - self.geoid_hight(lat,lon)
        #self.waypoint_global.pose.position = GeoPoint(lat,lon,alt_AMSL) this didnt work for me, I use the following 3
        self.waypoint_global.pose.position.altitude = self.alt_AMSL
        self.waypoint_global.pose.position.longitude= lon
        self.waypoint_global.pose.position.latitude = lat
        self.gl_pos_pub.publish(self.waypoint_global)

    def sleep(self,secs):
        #minimum delay is 1/frec = 10ms, this is, secs = 0.01
        ii = 0
        while ii<int(self.frec*secs): #delay s
            rclpy.spin_once(self)
            ii+=1


def main(args=None):
    #initializing ROS node
    rclpy.init(args=args)

    # creation of node
    node=MiNodo()
    
    node.time_0 = node.get_clock().now().to_msg().sec
    print("Init time: {}".format(node.time_0))
    
    #request service stream rate start
    node.start_stream()

    # Wait for FCU connection.
    node.wait4connect()

    # Wait for the mode to be switched to GUIDED.
    node.wait4start()
    
    #request service stream rate start
    node.start_stream()
    
    #request service arming
    node.arming()
    node.sleep(1.0) 

    #request takeoff
    node.alt0 = 2.0  # floating point necessary
    print("Geod altitude before takeoff: {}".format(node.global_position))
    node.takingoff(node.alt0) 
    node.sleep(3.0) 
    node.get_logger().info("sleep 5s elapsed")
    print("Geod altitude after  takeoff: {}".format(node.global_position))

    #calculate the floor compensation
    node.floor_geoid = node.global_position.altitude
    print("Floor in geoid is: {}".format(node.floor_geoid))
    
   
    # Specify some global waypoints
    # square
    goals =[[51.768998000, 14.3233080000,node.alt0],  # WP 1
            [51.7690358, 14.32301660,node.alt0],  # WP 3
            [51.7692120, 14.32306877,node.alt0],  # WP 4
            [51.7691758, 14.32335417,node.alt0], # WP 5
            [51.768998, 14.323308,node.alt0]]  # Back to WP 1
    
    i = 0  
    contador = 0
    while i < len(goals):

        lat = goals[i][0]
        lon = goals[i][1]
        alt = goals[i][2]

        node.set_global_destination(lat,lon,alt) # alt wrt floor 
        
        # measured coords:
        c_lat = node.global_position.latitude
        c_lon = node.global_position.longitude
        c_alt = node.global_position.altitude
        print("Current  global LLA: {},  {} , {}".format(c_lat,c_lon,c_alt))
        print("Setpoint global LLA: {},  {} , {}".format(lat,lon,node.alt_AMSL))
        
        node.sleep(1.0)
        contador+= 1
        if contador ==17:
            contador = 0
            i+=1
    print("Waypoints completed!")

    node.sleep(60)
       
    # request service landing
    node.landing()

    rclpy.spin(node)
    rclpy.shutdown()
    
if __name__=="__main__":
    main()
