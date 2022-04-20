from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

import sys

from django_react_toolkit import proxy

class Command(BaseCommand):
    def add_arguments(self, parser) -> None:
        parser.add_argument('--port', default=8080, type=int)
        parser.add_argument('--host', default='127.0.0.1', type=str)

    def handle(self, *args, **options):
        self.stdout.write('Starting proxy server...')
        server = proxy.ReverseProxy(
            options['host'],
            options['port'],
            getattr(settings,'DJ_REACT_PROXY_RULE',[])
            )
        try:
            self.stdout.write("Waiting for connections")
            server.start()
            
        except KeyboardInterrupt:
            server.server.close()
            self.stdout.write("Ctrl C - Stopping server")
            sys.exit(1)
