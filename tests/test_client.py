import unittest
from mock import patch
from gearmanadmin import GearmanConnector, GearmanAdminClient
from gearman.errors import ServerUnavailable


class testGeramanClient(unittest.TestCase):

    @patch('gearman.GearmanAdminClient')  
    def setUp(self, stub):
        stub.get_version.return_value = '0.1'
        self.client = GearmanAdminClient(GearmanConnector([
            ('dummyhost1', '4730'),
            ('dummyhost2', '4730'),
            ('brokenhost1','4730')
        ]))

    def test_instance(self, ):
        self.assertIsInstance(self.client, GearmanAdminClient)

    def test_verison(self, ):
        print self.client.get_version()
        #self.assertEqual(self.client.get_version(), '0.1')
        