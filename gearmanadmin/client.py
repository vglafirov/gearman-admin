"""
GearmanAdmin client interface.
"""
import gearman
from gearman.errors import ServerUnavailable
import gearmanadmin 

class GearmanConnector(object):
    """
        Gearman connector class.
    
        :Parameters:
    - `[(hostname, port)]`: list of tuples (hostname, port) describes gearman hostname and port 
    """

    connections = []
    
    def __init__(self, connectionPool):
        
        if len(connectionPool) == 0:
            raise gearmanadmin.EmptyServerListException()
            
        for server in connectionPool:
            connectionString = ':'.join([server[0],server[1]])
            self.connections.append(gearman.GearmanAdminClient([connectionString]))

    def clean_up_connections(self, ):
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
        self.connector = connector

    def get_status(self, ):
        """
        Return gearman server status
        """
        #self.connector.clean_up_connections()
        for connection in self.connector.connections:
            print connection.get_status()