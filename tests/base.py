import unittest

class DomainScoreTestCase(unittest.TestCase):


    def setUp(self):

        self.client = "FooBar"
        """
        self.redis = redis.StrictRedis(db=self.db)
        if self.redis.dbsize():
            raise EnvironmentError('Redis database number %d is not empty, '
                                   'tests could harm your data.' % self.db)
        """
    def tearDown(self):
        pass