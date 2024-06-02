from pymodbus.client import ModbusTcpClient, ModbusSerialClient
from pymodbus.framer.rtu_framer import ModbusRtuFramer
import logging
import helper  # Assuming helper.py is in the same directory

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

# Choose the correct client based on the communication type
if args.comm == "tcp":
    client = ModbusTcpClient(ip_address, port=port)
elif args.comm == "rtu_tcp":
    client = ModbusTcpClient(ip_address, port=port, framer=ModbusRtuFramer)
elif args.comm == "serial":
    client = ModbusSerialClient(method='rtu', port=ip_address, baudrate=args.baudrate, timeout=args.timeout)
else:
    raise ValueError(f"Unsupported communication type: {args.comm}")

if client.connect():
    try:
        # Write value to register
        result = client.write_register(register_address, value_to_write, slave=slave_id)
        if result.isError():
            print(f"Write result: Modbus Error: {result}")
        else:
            print(f"Write result: {result}")

        # Verify the write by reading the register
        result = client.read_holding_registers(register_address, 1, slave=slave_id)
        if result.isError():
            print(f"Read result: Modbus Error: {result}")
        else:
            print(f"Read result: {result.registers[0]}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()
else:
    print("Failed to connect to the Modbus server")
