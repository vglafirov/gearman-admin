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