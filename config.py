# ===== Your specific configuration goes below / please adapt ========

# the HCP account id - trial accounts typically look like p[0-9]*trial
# hcp_account_id='i010317trial'
hcp_account_id='a5d3e8f71'

# you only need to adapt this part of the URL if you are NOT ON TRIAL but e.g. on PROD
# hcp_landscape_host='.hanatrial.ondemand.com'
hcp_landscape_host='.hana.ondemand.com' # this is used on PROD

# optional network proxy, set if to be used, otherwise set to ''
proxy_url=''
# proxy_url='http://proxy_host:proxy_port'

# the following values need to be taken from the IoT Cockpit
device_id='75d508bf-ec32-4ec8-8529-e29af6f49e08'

oauth_credentials_for_device='6bc49e1165b51eb96612ae5b4a641b3'

message_type_light_level='222b307aac9ff9177a28'
message_type_smoke_level='9dd63cb7f6a0b3ff8505'
message_type_temperature='753da6331383fdcbd599'
message_type_vibration='3ebf8cc38dc914529a39'
message_type_distance='f954cefa8749880cd2d0'
message_type_light_trigger='a612167cbda443f0a7c0'
message_type_full_elevator='fec73e1913d23988e371'

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

# Other Custom Values
elevator_id='GDH1'
# ===== nothing to be changed / configured below this line ===========