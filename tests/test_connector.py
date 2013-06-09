import unittest
from mock import patch
import gearmanadmin


class testGeramanConnector(unittest.TestCase):

    @patch('gearman.GearmanAdminClient')
    def setUp(self, stub):
        stub.ping_server.return_value = 0.38103294372558594
        self.connector = gearmanadmin.GearmanConnector([('localhost', '4730')])

    def test_instance(self, ):
        self.assertIsInstance(self.connector, gearmanadmin.GearmanConnector)
        
    def test_ping(self,):
        for server in self.connector.connections:
            server.ping_server()
            
    def test_emptyServerList(self, ):
        with self.assertRaises(gearmanadmin.EmptyServerListException):
            self.connector = gearmanadmin.GearmanConnector([])


if __name__ == '__main__':
    unittest.main()