"""
GearmanAdmin Exceptions
"""

class GearmanAdminException(Exception):
    """
    Base class for GearmanAdmin exceptions
    """

class EmptyServerListException(GearmanAdminException):
    """
    Server list is empty
    """
    pass
class MalformedHostListException(GearmanAdminException):
    """
    Host list is wrong
    """
    def __init__(self, hostList):
        self.hostList = hostList

    def __str__(self):
        return "MalformedHostListException: %s" % repr(self.hostList)