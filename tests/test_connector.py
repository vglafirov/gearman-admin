import unittest
from mock import patch
from gearmanadmin import GearmanConnector
from gearmanadmin.exceptions import EmptyServerListException
from gearman.errors import ServerUnavailable


class testGeramanConnector(unittest.TestCase):

    @patch('gearman.GearmanAdminClient')
    def setUp(self, stub):
        stub.ping_server.return_value = 0.38103294372558594
        if stub.call_count == 3:
            stub.ping_server.side_effect = ServerUnavailable
        self.connector = GearmanConnector([
            ('dummyhost1', '4730'),
            ('dummyhost2', '4730'),
            ('brokenhost1','4730')
        ])

    def test_instance(self, ):
        self.assertIsInstance(self.connector, GearmanConnector)
                    
    def test_empty_server_list(self, ):
        with self.assertRaises(EmptyServerListException):
            self.connector = GearmanConnector([])

    def test_clean_up_connection(self, ):
        self.connector.clean_up_connections()
        cleanConnector = GearmanConnector([
            ('dummyhost1', '4730'),
            ('dummyhost2', '4730'),
        ])
        
        self.assertEqual(len(self.connector.connections),len(cleanConnector.connections))
        
        for (i, connection) in enumerate(self.connector.connections):
            self.assertEqual(connection.connection_list, cleanConnector.connections[i].connection_list)


if __name__ == '__main__':
    unittest.main()