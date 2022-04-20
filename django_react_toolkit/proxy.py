'''
proxy inspired by:
voorloop@gmail.com - https://gist.github.com/voorloopnul/415cb75a3e4f766dc590#file-proxy-py
yuichi@yuichi.com - https://github.com/yuichi110/Python_HTTP_Proxy

ReverseProxy that works on socket TCP connection using standard python library so we doesn't care about HTTP or WS or anything else.
We just care about connections

'''
import socket
from ipaddress import ip_address
import select
import time
import sys
import re


class ProxyBase:
    """Base for other proxy classes
    """

    def __init__(self, rule_list):
        proxy_matcher_list = []

        for (ip, port, urlpat_list) in rule_list:
            for urlpat in urlpat_list:
                t = (re.compile(urlpat), ip, port)
                proxy_matcher_list.append(t)
        self.proxy_matcher_list = proxy_matcher_list

    @staticmethod
    def is_port_ok(port):
        port_ok = True
        if type(port) is not int:
            port_ok = False
        if port < 0:
            port_ok = False
        if port > 65535:
            port_ok = False
        return port_ok

    @staticmethod
    def is_ip_ok(ip):
        try:
            ip_address(ip)
        except ValueError:
            return False
        return True

    @staticmethod
    def parse_ip_port(ip, port, throw_error=True):
        error = []
        if not ProxyBase.is_ip_ok(ip):
            error.append(
                'Illegal IP address string "{}" is passed\n'.format(ip))

        # Port check
        if not ProxyBase.is_port_ok(port):
            error.append('Illegal Port number "{}" is passed'.format(port))

        if throw_error and len(error):
            for i in error:
                raise Exception(i)
        return error

    def get_matched_host(self, data):
        """Returns first matched host from proxy_matcher_list

        Args:
            data (_type_): string that is raw HTTP request

        Raises:
            Exception: When url is wrong parsed

        Returns:
            tuple: (id,port) of the host
        """
        url = data.split('\r\n', 1)[0]
        url = re.match('^.+?(/.*)?HTTP', url).group(1)
        url = url.strip(' ')

        for (matcher, ip, port) in self.proxy_matcher_list:
            if matcher.match(url):
                return ip, port
        raise Exception('Wrong parsing', url)


class Forward:
    def __init__(self):
        self.forward = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self, host, port):
        try:
            self.forward.connect((host, port))
            return self.forward
        except Exception as e:
            print(e)
            return False


class ReverseProxy(ProxyBase):
    input_list = []
    channel = {}

    buffer_size = 4096
    delay = 0.0001

    def __init__(self, host, port, rule_list, *args, **kwargs):
        self.parse_ip_port(host, port)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # aviod OSError Address already in use
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.server.bind((host, port))
        self.server.listen(10)

        super().__init__(rule_list)

    def start(self):
        self.input_list.append(self.server)
        while 1:
            time.sleep(self.delay)

            # check for sockets that are not empty
            ready_to_read, _, _ = select.select(self.input_list, [], [])

            for self.current_reader in ready_to_read:
                # new incoming connection
                if self.current_reader == self.server:
                    self.on_accept()
                    break

                self.data = self.current_reader.recv(self.buffer_size)

                # if socket data is empty that means, it closed connection
                if len(self.data) == 0:
                    self.on_close()
                    break
                else:
                    self.on_recv()

    def on_accept(self):
        clientsock, clientaddr = self.server.accept()

        encoded_data = clientsock.recv(self.buffer_size)

        decoded_data = encoded_data.decode()

        host, port = self.get_matched_host(decoded_data)

        # create connections to destination host
        forward = Forward().start(host, port)
        if forward:

            self.input_list.append(clientsock)
            self.input_list.append(forward)
            self.channel[clientsock] = forward
            self.channel[forward] = clientsock
            forward.send(encoded_data)
        else:
            print("Closing connection with client side", clientaddr)
            clientsock.close()

    def on_close(self):
        # remove objects from input_list
        self.input_list.remove(self.current_reader)
        self.input_list.remove(self.channel[self.current_reader])

        out = self.channel[self.current_reader]
        # close the connection with client
        # equivalent to do self.current_reader.close()
        self.channel[out].close()
        # close the connection with remote server
        self.channel[self.current_reader].close()
        # delete both objects from channel dict
        del self.channel[out]
        del self.channel[self.current_reader]

    def on_recv(self):
        data = self.data
        # here we can parse and/or modify the data before send forward
        # print(data)
        self.channel[self.current_reader].send(data)


if __name__ == '__main__':
    forward_to = [
        ('127.0.0.1', 8000, ['/api', '/admin']),
        ('127.0.0.1', 3000, ['.*']),
    ]
    
    server = ReverseProxy('127.0.0.1', 9092, forward_to)
    try:
        server.start()
    except KeyboardInterrupt:
        server.server.close()
        print("Ctrl C - Stopping server")
        sys.exit(1)
