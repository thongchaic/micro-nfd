# Copyright 2020 LeMaRiva|tech lemariva.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
TTN_FREQS = {0: (0xe6, 0xCC, 0xF4), # 923.2 Mhz
 1: (0xe6, 0xD9, 0xC0), # 923.4 Mhz
 2: (0xe6, 0xe6, 0x66), # 923.6 Mhz
 3: (0xe6, 0xf3, 0x33), # 923.8 Mhz
 4: (0xe7, 0x00, 0x00), # 924.0 Mhz
 5: (0xe7, 0x0C, 0xCC), # 924.2 Mhz
 6: (0xe7, 0x19, 0x99), # 924.4 Mhz
 7: (0xe7, 0x26, 0x66)} # 924.6 Mhz

lora._mod->setRegValue(SX1278_REG_FRF_MSB, 0x6C);
lora._mod->setRegValue(SX1278_REG_FRF_MID, 0x80);
lora._mod->setRegValue(SX1278_REG_FRF_LSB, 0x00);

device_config = {
    'miso':19,
    'mosi':23,
    'ss':5,
    'sck':18,
    'dio_0':26,
    'reset':36,
    'led':12, 
}

# ES32 TTGO v1.0 
device_config = {
    'miso':19,
    'mosi':27,
    'ss':18,
    'sck':5,
    'dio_0':26,
    'reset':14,
    'led':2, 
}

# M5Stack ATOM Matrix
device_config = {
    'miso':23,
    'mosi':19,
    'ss':22,
    'sck':33,
    'dio_0':25,
    'reset':21,
    'led':12, 
}
"""

appEui = "70B3D57ED00336F0"
appKey = "81EFF308C0E6111761FC71D963B06522"

# ES32 TTGO v1.0 (https://github.com/Xinyuan-LilyGO/LilyGO-T-Beam/blob/master/src/board_def.h)
#define LORA_SCK        5
#define LORA_MISO       19
#define LORA_MOSI       27
#define LORA_SS         18
#define LORA_DI0        26
#define LORA_RST        23
#define LORA_DIO1       33
#define LORA_BUSY       32
# https://github.com/kizniche/ttgo-tbeam-ttn-tracker/blob/master/main/configuration.h

#if defined(T_BEAM_V07)
#define GPS_RX_PIN      12
#define GPS_TX_PIN      15
#elif defined(T_BEAM_V10)
#define GPS_RX_PIN      34
#define GPS_TX_PIN      12
#endif
#define SCK_GPIO        5
#define MISO_GPIO       19
#define MOSI_GPIO       27
#define NSS_GPIO        18
#define RESET_GPIO      23
#define DIO0_GPIO       26
#define DIO1_GPIO       33
#define DIO2_GPIO       32

device_config = {
    'miso':19,
    'mosi':27,
    'ss':18,
    'sck':5,
    'dio_0':26,
    'reset':23,
    'led':2, 
}

app_config = {
    'loop': 200,
    'sleep': 100,
}

lora_parameters = {
    'frequency': 9232E6, 
    'tx_power_level': 14, 
    'signal_bandwidth': 125E3,    
    'spreading_factor': 7, 
    'coding_rate': 4, 
    'preamble_length': 8,
    'implicit_header': False, 
    'sync_word': 0x12, 
    'enable_CRC': False,
    'invert_IQ': False,
}

wifi_config = {
    'ssid':'CSOffice2',
    'password':''
}


