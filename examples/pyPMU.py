from synchrophasor.pmu import Pmu
from synchrophasor.frame import *
import random
import socket
import struct

"""
pyPMU is custom configured PMU simulator. Code below represents
PMU described in IEEE C37.118.2 
"""
SIMULINK_UDP_IP = "127.0.0.1"
SIMULINK_UDP_PORT = 1410

pmu = Pmu(ip="127.0.0.1", port=4713)

# ph_v_conversion = int(300000.0 / 32768 * 100000)  # Voltage phasor conversion factor
ph_v_conversion = int(1)
ph_i_conversion = int(15000.0 / 32768 * 100000)  # Current phasor conversion factor
# ph_i_conversion = int(1)

cfg = ConfigFrame2(1,  # PMU_ID
                   1000000,  # TIME_BASE
                   1,  # Number of PMUs included in data frame
                   "PMU#1",  # Station name
                   7754,  # Data-stream ID(s)
                   (False, True, True, False),  # Data format - Check ConfigFrame2 set_data_format()
                   21,  # Number of phasors
                   3,  # Number of analog values
                   1,  # Number of digital status words
                   ["VA", "VB", "VC", 
                    "I1A", "I1B", "I1C", 
                    "I2A", "I2B", "I2C", 
                    "I3A", "I3B", "I3C", 
                    "I4A", "I4B", "I4C", 
                    "I5A", "I5B", "I5C",
                    "I6A", "I6B", "I6C",
                    "ANALOG1", "ANALOG2", "ANALOG3", "BREAKER 1 STATUS",
                    "BREAKER 2 STATUS", "BREAKER 3 STATUS", "BREAKER 4 STATUS", "BREAKER 5 STATUS",
                    "BREAKER 6 STATUS", "BREAKER 7 STATUS", "BREAKER 8 STATUS", "BREAKER 9 STATUS",
                    "BREAKER A STATUS", "BREAKER B STATUS", "BREAKER C STATUS", "BREAKER D STATUS",
                    "BREAKER E STATUS", "BREAKER F STATUS", "BREAKER G STATUS"],  # Channel Names
                   [(0, 'v'),(0, 'v'),(0, 'v'),
                    (ph_i_conversion, 'i'),(ph_i_conversion, 'i'),(ph_i_conversion, 'i'),
                    (0, 'i'),(0, 'i'),(0, 'i'),
                    (0, 'i'),(0, 'i'),(0, 'i'),
                    (0, 'i'),(0, 'i'),(0, 'i'),
                    (0, 'i'),(0, 'i'),(0, 'i'),
                    (0, 'i'),(0, 'i'),(0, 'i')],  # Conversion factor for phasor channels
                   [(1, 'pow'), (1, 'rms'), (1, 'peak')],  # Conversion factor for analog channels
                   [(0x0000, 0xffff)],  # Mask words for digital status words
                   60,  # Nominal frequency
                   1,  # Configuration change count
                   240)  # Rate of phasor data transmission)


hf = HeaderFrame(7,  # PMU_ID
                 "This is the test program")  # Header Message

pmu.set_configuration(cfg)
pmu.set_header(hf)
pmu.run()

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((SIMULINK_UDP_IP, SIMULINK_UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    parsData = struct.unpack('45d', data)
    df = DataFrame(int(parsData[0]),  # PMU_ID
               ('ok', True, 'timestamp', False, False, False, 0, '<10', 0),  # STAT WORD - Check DataFrame set_stat()
               [(parsData[3], parsData[4]), (parsData[5], parsData[6]), (parsData[7], parsData[8]), (parsData[9], 0),(parsData[11], 0), (parsData[13], 0), (0, 0), (0, 0),
                (0, 0), (0, 0), (0, 0), (0, 0),(0, parsData[28]), (0,parsData[30]), (0,parsData[32]), (0, 0),
                (0, 0), (0, 0), (0, 0), (0, 0),(0, 0)],  # PHASORS (3 - v, 1 - i)
               int(parsData[2]),  # Frequency deviation from nominal in mHz
               0,  # Rate of Change of Frequency 
               [100, 1000, 10000],  # Analog Values
               [0x3c12],  # Digital status word
               0x0006)  # Data Format
    pmu.send(df) 
# pmu.join()
