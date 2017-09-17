# ===== Configuration for Elevate IoT (CF 4.0 Version) ========

cloud_system='trial.canary.cp.iot.sap'
cloud_system_port_mqtt=8883
cloud_system_url_extension='measures/'
cloud_system_profile_id=48
cloud_system_log_node_addr=2

path_to_certificate='./certificates/client.crt.pem'
path_to_private_key='./certificates/client.key.pem'
path_to_landscape_certificate='./certificates/cacerts.pem'
#path_to_landscape_certificate='./certificates/eu10cpiotsap.crt'

device_mac_address='74:da:38:56:03:f0'

measure_light_sensor='100'
measure_temperature_sensor='101'
measure_vibration_sensor='102'
measure_distance_sensor='103'
measure_smoke_sensor='104'
measure_humidity_sensor='105'

light_sensor_analog_register=0

pause_interval_detection=5
pause_interval_message=2

# This section will contain the mappings used in the examples
pin_traffic_light_red=9
pin_traffic_light_yellow=10
pin_traffic_light_green=11
pin_analog_spimosi=24
pin_analog_spimiso=23
pin_analog_spiclk=18
pin_analog_spics=25
pin_smoke_digital=26
pin_smoke_analog=1
pin_temp=4
pin_vibration=12
pin_ultrasonic_dist_trig=17
pin_ultrasonic_dist_echo=27

# ===== nothing to be changed / configured below this line ===========