# Complete Modbus Communication
Modbus RTU over TCP/IP, Modbus TCP and Serial Communication Support

## Description
Personalized script to read/write modbus registers, specially Modbus RTU over TCP/IP communication. 
Support TCP, RTU over TCP, and Serial Communications. 

Read/Write Modbus Registers, with the preferred endianness.  

Input Register and Discrete Input Registers cannot be written to, they are read only registers.

Holding Registers and Coils can be read and written to.

## Author
rashidobaid9@gmail.com

## Date
2024-06-04

## Copyright
MPL 2.0

## Installation
1. Install pymodbus.

```pip install pymodbus```

2. Download this complete repository, browse to the folder in the terminal and run these (a few examples displayed):

For RTU over TCPIP (please adjust all parameters as requried e.g host 192.168.X.X, etc etc): 

```python gensetReadWrite.py --comm rtu_tcp --host 127.0.0.1 --port 502 --log debug --slave_id 1 --address 128 --value 1```

For TCP:

Read Holding Registers:

```python gensetReadWrite.py --comm tcp --host 127.0.0.1 --port 502 --log debug --slave_id 1 --address 3 --function read --register_type holding --endian little  --count 10```

Read Coils:

```python gensetReadWrite.py --comm tcp --host 127.0.0.1 --port 502 --log debug --slave_id 1 --address 3 --function read --register_type coil --count 10```

Read Input Register:

```python gensetReadWrite.py --comm tcp --host 127.0.0.1 --port 502 --log debug --slave_id 1 --address 2 --function read --register_type input --endian little --count 1```

Write Holding Register:

```python gensetReadWrite.py --comm tcp --host 127.0.0.1 --port 502 --log debug --slave_id 1 --address 3 --function write --value 10000 --register_type holding --endian little  --count 1```

Write Coil:

```python gensetReadWrite.py --comm tcp --host 127.0.0.1 --port 502 --log debug --slave_id 1 --address 3 --function write --value 1 --register_type coil  --count 1```

## Usage
We can select tcp, rtu_tcp (for rtu over tcp) and serial communication.
