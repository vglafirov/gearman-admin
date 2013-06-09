"""
GearmanAdmin client interface.
"""
import gearman
from gearman.errors import ServerUnavailable
import gearmanadmin 

class GearmanConnector(object):
    """
    """
    connections = []
    
    def __init__(self, connectionPool):
        """
        Gearman connector class.
        
        :Parameters:
         - `[(hostname, port)]`: list of tuples (hostname, port) describes gearman hostname and port 
        """
        
        if len(connectionPool) == 0:
            raise gearmanadmin.EmptyServerListException()
            
        for server in connectionPool:
            connectionString = ':'.join([server[0],server[1]])
            self.connections.append(gearman.GearmanAdminClient([connectionString]))

    def cleanConnections(self, ):
        """
        Clean up server list. Remove all broken servers from connection pool.
        """
        for host in self.connections:
            try:
                host.ping_server()
            except ServerUnavailable:
                self.connections.remove(host)
        


class GearmanAdminClient(object):
    """
    Gearman client class
    """
    
    def __init__(self, connector):
        """
        Default constructor
        """
        pass
        
        
        