#!/usr/bin/env python

import ipdb

import argparse
import yaml
import sys

class CliNamespace(object):
    def __init__(self, argv):
        parser = argparse.ArgumentParser(
            description='Pretends to be git',
            usage='''git <command> [<args>]

The most commonly used git commands are:
   commit     Record changes to the repository
   fetch      Download objects and refs from another repository
''')
        with open('config.yml') as f:
            self.cli_tools = yaml.load(f)
        parser.add_argument('command', help='Subcommand to run')
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        self.argv = argv
        args = parser.parse_args(argv[1:2])
        if not hasattr(self, args.command):
            print 'Unrecognized command'
            parser.print_help()
            sys.exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()

    def __getattr__(self, name):
        def closure():
            parser = argparse.ArgumentParser(description=self.cli_tools[name])
            args = parser.parse_args(self.argv[2:])
            print 'Running %s' % name
        return closure
        

    def __dir__(self):
        return self.cli_tools.keys()

if __name__ == '__main__':
    #ipdb.set_trace()
    CliNamespace(sys.argv)

