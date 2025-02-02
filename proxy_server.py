import socket
import logging
import json

from data_selects.find import find_in_documents

BUFFER_SIZE = 2048


def echo_server(host: str, port: int) -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    address = (host, port)

    sock.bind(address)

    logging.info(f"Echo Server started on {host}:{port}")

    try:
        while True:
            request, addr = sock.recvfrom(BUFFER_SIZE)
            if not request:
                logging.info(f"Echo Server didn't get any data from the server")
            data = json.loads(request.decode('utf8'))
            col = data.get("col")
            query = data.get("query")
            processed_data = find_in_documents(col, query)

            logging.info(f"Received echo server request: {processed_data}")
            sock.sendto(processed_data, addr)

    except KeyboardInterrupt:
        logging.info(f"Echo Server stopped")
    finally:
        sock.close()
