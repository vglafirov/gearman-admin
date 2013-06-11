import time
import os
import subprocess
import platform
from prettytable import PrettyTable
from gearmanadmin import exceptions
from gearmanadmin import GearmanAdminClient
from gearmanadmin import GearmanConnector


def clear():
    subprocess.Popen(
        "cls" if platform.system() == "Windows"
        else "clear", shell=True
    )


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

    if (args, kwargs) not in f.arguments:
        f.arguments.insert(0, (args, kwargs))


@arg('server',
     metavar='<server>',
     help="""Comma separated list of pairs hostname:port,
          port is optional default is 4730""")
@arg("-t", "--total", action="store_true", dest="total",
     help="""Show totals for each gearmand server""")
@arg("-v", "--version", action="store_true", dest="version",
     help="""Show gearmand server version""")
def do_status(args):
    """
    Shows gearmand server status
    """
    connectionString = []
    hostlist = args.server.split(',')

    for i in xrange(0, len(hostlist)):
        pair = hostlist[i].split(':')
        if len(pair) > 2:
            raise exceptions.MalformedHostListException(pair)
        else:
            try:
                connectionString.append((pair[0], pair[1]))
            except IndexError:
                connectionString.append((pair[0], '4730'))
    clientConnector = GearmanConnector(connectionString)
    client = GearmanAdminClient(clientConnector)
    
    if args.version:
        for (i, connection) in enumerate(connectionString):
            print "{}: {}".format(connection[0], client.get_version()[i])
        exit(0)

    result = client.get_status()
    table = PrettyTable(["Server", "Task", "Queued", "Running", "Workers"])
    table.align["Task"] = 'l'
    table.padding_width = 1

    for row in result:
            table.add_row([str(connectionString[0][0]), "", "", "", ""])
            queued_sum = 0
            running_sum = 0
            workers_sum = 0
            for column in row:
                queued_sum = queued_sum + int(column["queued"])
                running_sum = running_sum + int(column["running"])
                workers_sum = workers_sum + int(column["workers"])
                table.add_row([
                    "",
                    str(column["task"]),
                    str(column["queued"]),
                    str(column["running"]),
                    str(column["workers"])
                ])
            if args.total:
                table.add_row([
                    "Total:",
                    "",
                    queued_sum,
                    running_sum,
                    workers_sum
                ])
                table.add_row(["", "", "", "", ""])
    print table
    