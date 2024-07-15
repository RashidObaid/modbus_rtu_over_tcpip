from pymodbus.client import ModbusTcpClient, ModbusSerialClient
from pymodbus.framer.rtu_framer import ModbusRtuFramer
import logging
import helper  
import struct

# Define endianness conversion functions
def to_big_endian(value):
    return struct.unpack('>H', struct.pack('H', value))[0]

def to_little_endian(value):
    little_endian_value = struct.unpack('<H', struct.pack('H', value))[0]
    return little_endian_value

def to_mixed_endian(value):
    high_byte = (value & 0xFF00) >> 8
    low_byte = (value & 0x00FF)
    mixed_value = (low_byte << 8) | high_byte
    return mixed_value

# Parse command-line arguments
args = helper.get_commandline(description="Modbus TCP/RTU Client")

# Enable logging based on the command-line argument
logging.basicConfig()
log = logging.getLogger()   
log.setLevel(getattr(logging, args.log.upper()))

# Configuration settings from parsed arguments
ip_address = args.host
port = args.port
slave_id = args.slave_id
register_address = args.address
value_to_write = args.value
endian = args.endian
count = args.count
register_type = args.register_type
function = args.function
baudrate=args.baudrate
timeout=args.timeout 

# Choose the correct client based on the communication type
if args.comm == "tcp":
    client = ModbusTcpClient(ip_address, port=port)
elif args.comm == "rtu_tcp":
    client = ModbusTcpClient(ip_address, port=port, framer=ModbusRtuFramer)
elif args.comm == "serial":
    client = ModbusSerialClient(method='rtu', port=port, baudrate=baudrate, timeout=timeout)
else:
    raise ValueError(f"Unsupported communication type: {args.comm}")

# Define functions for reading and writing with endianness handling
def read_holding_registers(client, register_address, count, slave_id, endian='big'):
    result = client.read_holding_registers(register_address, count, slave_id)
    if result.isError():
        raise ValueError(f"Error reading registers: {result}")
    values = result.registers
    if endian == 'little':
        return [to_little_endian(val) for val in values]
    elif endian == 'mixed':
        return [to_mixed_endian(val) for val in values]
    elif endian == 'big':
        return [to_big_endian(val) for val in values]    
    
def write_holding_register(client, register_address, value_to_write, slave_id, endian='big'):
    if endian == 'little':
        value_to_write = to_little_endian(value_to_write)
    elif endian == 'mixed':
        value_to_write = to_mixed_endian(value_to_write)
    elif endian == 'big':
        value_to_write = to_big_endian(value_to_write)
    result = client.write_register(register_address, value_to_write, slave_id) 
    if result.isError():
        raise ValueError(f"Error writing register: {result}")
    return result

def read_coils(client, register_address, count, slave_id):
    result = client.read_coils(register_address, count, slave_id)
    if result.isError():
        raise ValueError(f"Error reading coils: {result}")
    return result.bits

def write_coil(client, slave_id, register_address, value_to_write):
    result = client.write_coil(register_address, value_to_write, slave_id)
    if result.isError():
        raise ValueError(f"Error writing coil: {result}")
    return result

def read_input_registers(client, register_address, count, slave_id, endian='big'):
    result = client.read_input_registers(register_address, count, slave_id)
    if result.isError():
        raise ValueError(f"Error reading input registers: {result}")
    values = result.registers
    if endian == 'little':
        return [to_little_endian(val) for val in values]
    elif endian == 'mixed':
        return [to_mixed_endian(val) for val in values]
    elif endian == 'big':
        return [to_big_endian(val) for val in values]

def read_discrete_inputs(client, register_address, count, slave_id):
    result = client.read_discrete_inputs(register_address, count, slave_id)
    if result.isError():
        raise ValueError(f"Error reading discrete inputs: {result}")
    return result.bits



if client.connect():
    try:
        if function == 'write':
            if register_type == 'holding':
                # Write value to register with endianness handling
                write_holding_register(client, register_address, value_to_write, slave_id, endian)
                print(f"Value {value_to_write} written to register {register_address} with {endian} endian.")
            elif register_type == 'coil':
                # Write value to register with endianness handling
                write_coil(client, slave_id, register_address, value_to_write,)
                print(f"Value {value_to_write} written to coil register {register_address}.")

        elif function == 'read':
            if register_type == 'holding':
                result = read_holding_registers(client, register_address, count, slave_id, endian)
                for i, val in enumerate(result):
                    print(f"Read value from holding register {register_address + i}: {val} with {endian} endian.")
            elif register_type == 'coil':
                result = read_coils(client, register_address, count, slave_id)
                for i, val in enumerate(result):
                    print(f"Read value from coil register {register_address + i}: {val}.")
            elif register_type == 'input':
                result = read_input_registers(client, register_address, count, slave_id, endian)
                for i, val in enumerate(result):
                    print(f"Read value from input register {register_address + i}: {val} with {endian} endian.")
            elif register_type == 'discrete_input':
                result = read_discrete_inputs(client, register_address, count, slave_id)
                for i, val in enumerate(result):
                    print(f"Read value from discrete input register {register_address + i}: {val}.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()
else:
    print("Failed to connect to the Modbus server")
