from ping3 import ping


def server_ping(host: str):
    delay = ping(dest_addr=host, unit='ms')

    return int(delay) if type(delay) == float else None