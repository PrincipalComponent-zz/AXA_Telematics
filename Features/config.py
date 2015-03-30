import ConfigParser, os

config = ConfigParser.ConfigParser()
config.read(['telematics.cfg', os.path.expanduser('~/.telematics.cfg'),
             '/etc/telematics/telematics.cfg'])

