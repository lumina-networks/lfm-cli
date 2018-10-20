import click
import json
from api import Client as fmclient
from topology import api as topology_api

CONTEXT_SETTINGS = dict(auto_envvar_prefix='FLOW_MANAGER')


class Context(object):

    def __init__(self):
        self.topology = None
        self.verify = True
        self.controller = {
          'ip': '127.0.0.1',
          'port': 8181,
          'user': 'admin',
          'password': 'admin',
          'protocol': 'http',
          'timeout': 5,
          'verify': self.verify
        }
        self.fm = fmclient(**{'config':self.controller})

    def set_topology(self, topology_file):
        self.topology = topology_api.read_topology(topology_file)
        if self.topology.controllers:
            controller = self.topology.controllers[0]
            self.controller['ip'] = controller['ip']
            if 'vip' in controller:
                self.controller['ip'] = controller['vip']
            if 'timeout' in controller:
                self.controller['timeout'] = controller['timeout']
            self.controller['user'] = controller['user']
            self.controller['password'] = controller['password']
            self.controller['protocol'] = controller['protocol']
            self.controller['port'] = controller['port']
            self.fm = fmclient(**{'config':self.controller})

    def set_verify(self, verify):
        self.verify = verify
        self.controller['verify'] = verify

    def print_json(self, result):
        print json.dumps(result,
                         default=lambda o: o.__dict__,
                         sort_keys=True,
                         indent=4)


pass_context = click.make_pass_decorator(Context, ensure=True)