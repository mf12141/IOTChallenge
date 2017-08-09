# ===== Your specific configuration goes below / please adapt ========

# the HCP account id - trial accounts typically look like p[0-9]*trial
hcp_account_id='i010317trial'

# you only need to adapt this part of the URL if you are NOT ON TRIAL but e.g. on PROD
hcp_landscape_host='.hanatrial.ondemand.com'
# hcp_landscape_host='.hana.ondemand.com' # this is used on PROD

# optional network proxy, set if to be used, otherwise set to ''
proxy_url=''
# proxy_url='http://proxy_host:proxy_port'

# these credentials are used from applications with the "push messages to devices" API
hcp_user_credentials="User:Password"

# the following values need to be taken from the IoT Cockpit
device_id='3fcb3eb7-cdd4-49b3-8ceb-4b1bb1ca36bf'
oauth_credentials_for_device='e58f3ecf72d2e25b767b2b914fe4ea'

message_type_id_isOpen='933de88a047f40c61a42'
message_type_id_Distance='933de88a047f40c61a42'

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
# ===== nothing to be changed / configured below this line ===========