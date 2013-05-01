"""
Gearman admin command line interface.
Main module inspired by python-novaclient
"""

import os
import argparse
import logging
import sys
import prettytable
import gearman
#import gearmanadmin

logger = logging.getLogger(__name__)



class GearmanAdminArgumentParser(argparse.ArgumentParser):
    """
    Parse command string arguments
    """

    def __init__(self, *args, **kwargs):
        super(GearmanAdminArgumentParser, self).__init__(*args, **kwargs)



class GearmanAdminShell(object):
    """
    Class for manipulate shell option parameters
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
            add_help=False
#            formatter_class=OpenStackHelpFormatter,
        )

        parser.add_argument('-h', '--help',
            action='store_true',
            help=argparse.SUPPRESS,
        )

        parser.add_argument('--version',
                            action='version')#,
#                            version=gearmanadmin.__version__)

        parser.add_argument('--debug',
            default=False,
            action='store_true',
            help="Print debugging output")

        return parser


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

        print "Hello"




def main():
    try:
        GearmanAdminShell().main(sys.argv[1:])
    except Exception as e:
        logger.debug(e, exc_info=1)
        print("ERROR: %s" % unicode(e))
        sys.exit(1)


if __name__ == '__main__':
    main()