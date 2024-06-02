import argparse

def get_commandline(server=True, description=None, cmdline=None):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "-c", "--comm", choices=["tcp", "udp", "serial", "tls", "rtu_tcp"], default="tcp"
    )
    parser.add_argument(
        "-f", "--framer", choices=["ascii", "rtu", "socket", "tls"], default="rtu"
    )
    parser.add_argument("-l", "--log", choices=["critical", "error", "warning", "info", "debug"], default="info")
    parser.add_argument("-p", "--port", type=int, default=502)
    parser.add_argument("--baudrate", type=int, default=9600)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--timeout", type=int, default=3)
    parser.add_argument("-s","--slave_id", type=int, default=1)
    parser.add_argument("--address", type=int, default=128)
    parser.add_argument("--value", type=int, default=0)
    
    return parser.parse_args(cmdline)

def get_certificate(cert_type):
    return f"certificates/{cert_type}.crt"  # Adjust the path as necessary
