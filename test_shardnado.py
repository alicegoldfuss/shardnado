import unittest
import shardnado

class ShardnadoTests(unittest.TestCase):
    def test_get_shards(self):

        # Execute code against running test_server
        test = shardnado.get_shards('127.0.0.1')

        expected = [['test_index', '1', 'r', 'UNASSIGNED', '52679412', '4.6gb', '127.0.0.1', 'elasticsearch-node']]

        # and verify the results
        self.assertEqual(test, expected)

    def test_get_nodes(self):

        # Execute code against running test_server
        test = shardnado.get_nodes('127.0.0.1')

        expected = ['127.0.0.1']

        # and verify the results
        self.assertEqual(test, expected)

    def test_assign_shards(self):

        # Execute code against running test_server
        test = shardnado.assign_shards([['test_index', '1', 'r', 'UNASSIGNED', '52679412', '4.6gb', '127.0.0.1', 'elasticsearch-node']],
            ['127.0.0.1'], '127.0.0.1')

        expected = []

        # and verify the results
        self.assertEqual(test, expected)

if __name__ == '__main__':
    unittest.main()


