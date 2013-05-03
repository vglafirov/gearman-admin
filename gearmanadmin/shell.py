"""
Gearman admin command line interface.
"""
import argparse
import logging
import sys

import gearmanadmin
import actions


logger = logging.getLogger(__name__)


class GearmanAdminArgumentParser(argparse.ArgumentParser):
    """
    Parse command string arguments
    """

    def __init__(self, *args, **kwargs):
        super(GearmanAdminArgumentParser, self).__init__(*args, **kwargs)


class GearmanAdminShell(object):
    """
    Class for manipulate shell optional parameters
    """
    def get_base_parser(self, ):
        """
        Parse agrument paramenters and return parser object
        """
        parser = GearmanAdminArgumentParser(
            prog='gearmanadmin',
            description=__doc__.strip(),
            epilog='See "gearman-admin help COMMAND" '
                   'for help on a specific command.',
            add_help=False,
            formatter_class=GearmanAdminHelpFormatter,
        )

        parser.add_argument('-h', '--help',
                            action='store_true',
                            help=argparse.SUPPRESS)

        parser.add_argument('--version',
                            action='version',
                            version=gearmanadmin.__version__)

        parser.add_argument('--debug',
                            default=False,
                            action='store_true',
                            help="Print debugging output")

        return parser

    def get_subcommand_parser(self, ):
        """
        Returns subcommand parser
        """

        parser = self.get_base_parser()

        subparsers = parser.add_subparsers(metavar='<subcommand>')

        self.subcommands = {}

        actions_module = actions

        self._find_actions(subparsers, actions_module)
        self._find_actions(subparsers, self)

        return parser

    def _find_actions(self, subparsers, actions_module):
        """
        Find actions in action module.
        Action is a function starts with do_
        """
        for attr in (a for a in dir(actions_module) if a.startswith('do_')):
            command = attr[3:].replace('_', '-')
            callback = getattr(actions_module, attr)
            desc = callback.__doc__ or ''
            action_help = desc.strip().split('\n')[0]
            arguments = getattr(callback, 'arguments', [])

            subparser = subparsers.add_parser(command,
                                              help=action_help,
                                              description=desc,
                                              add_help=False,
                                              formatter_class=GearmanAdminHelpFormatter)
            subparser.add_argument('-h', '--help',
                                   action='help',
                                   help=argparse.SUPPRESS,)
            self.subcommands[command] = subparser
            for (args, kwargs) in arguments:
                subparser.add_argument(*args, **kwargs)
                subparser.set_defaults(func=callback)

    def setup_debugging(self, debug):
        if not debug:
            return

        streamformat = "%(levelname)s (%(module)s:%(lineno)d) %(message)s"
        # Set up the root logger to debug so that the submodules can
        # print debug messages
        logging.basicConfig(level=logging.DEBUG,
                            format=streamformat)

    def main(self, argv):
        """
        Main function with arguments passed
        """
        parser = self.get_base_parser()
        (options, args) = parser.parse_known_args(argv)
        self.setup_debugging(options.debug)

        subcommand_parser = self.get_subcommand_parser()
        self.parser = subcommand_parser

        if options.help or not argv:
            subcommand_parser.print_help()
            return 0

        args = subcommand_parser.parse_args(argv)
        print args._get_args()
        # Short-circuit and deal with help right away.
        # if args.func == self.do_help:
        #     self.do_help(args)
        #     return 0

        args.func(self, args)


class GearmanAdminHelpFormatter(argparse.HelpFormatter):
    def start_section(self, heading):
        heading = '%s%s' % (heading[0].upper(), heading[1:])
        super(GearmanAdminHelpFormatter, self).start_section(heading)


def main():
    try:
        GearmanAdminShell().main(sys.argv[1:])
    except Exception as e:
        logger.debug(e, exc_info=1)
        print("ERROR: %s" % unicode(e))
        sys.exit(1)


if __name__ == '__main__':
    main()
