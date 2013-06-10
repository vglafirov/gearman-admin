import prettytable
import gearman
from gearmanadmin import exceptions
from gearmanadmin import GearmanAdminClient
from gearmanadmin import GearmanConnector



def arg(*args, **kwargs):
    """Decorator for CLI args."""
    def _decorator(func):
        add_arg(func, *args, **kwargs)
        return func
    return _decorator


def env(*args, **kwargs):
    """
    returns the first environment variable set
    if none are non-empty, defaults to '' or keyword arg default
    """
    for arg in args:
        value = os.environ.get(arg, None)
        if value:
            return value
    return kwargs.get('default', '')


def add_arg(f, *args, **kwargs):
    """Bind CLI arguments to a shell.py `do_foo` function."""

    if not hasattr(f, 'arguments'):
        f.arguments = []

    # NOTE(sirp): avoid dups that can occur when the module is shared across
    # tests.
    if (args, kwargs) not in f.arguments:
        # Because of the sematics of decorator composition if we just append
        # to the options list positional options will appear to be backwards.
        f.arguments.insert(0, (args, kwargs))

@arg('server',
     metavar='<server>',
     help='Comma separated list of pairs hostname:port, port is optional default is 4730')
def do_status(args):
    """
    Shows gearmand server status
    """
    connectionString = []
    hostlist = args.server.split(',')
        
    for i in xrange(0,len(hostlist)):
        pair = hostlist[i].split(':')
        if len(pair) > 2:
            raise exceptions.MalformedHostListException(pair)
        else:
            try:
                connectionString.append((pair[0],pair[1]))
            except IndexError:
                connectionString.append((pair[0],'4730'))
    clientConnector = GearmanConnector(connectionString)
    client = GearmanAdminClient(clientConnector)
    client.get_status()