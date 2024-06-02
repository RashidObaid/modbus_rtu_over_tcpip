# Project Title
Modbus RTU over TCP/IP

## Description
Personalized script to read/write modbus registers, specially Modbus RTU over TCP/IP communication 

## Installation
1. Install pymodbus.
```pip install pymodbus```
2. Download this complete repository, browse to the folder in the terminal and run this: 
```python gensetReadWrite.py --comm rtu_tcp --host 127.0.0.1 --port 502 --log debug --slave_id 1 --address 128 --value 1```

## Usage
We can select tcp, rtu_tcp (for rtu over tcp) and serial communication