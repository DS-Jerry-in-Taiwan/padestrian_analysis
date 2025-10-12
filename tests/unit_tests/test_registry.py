import unittest
from preprocess.registry import register_preprocessor, get_preprocessor

class DummyPreprocessor:
    def __init__(self, value=0):
        self.value = value
    def __call__(self, data):
        return data + self.value

class DummyPreprocessorInstance:
    def __call__(self, data):
        return data * 2

class TestRegistryFactory(unittest.TestCase):
    def setUp(self):
        # 清空 registry
        from preprocess.registry import PREPROCESSOR_REGISTRY
        PREPROCESSOR_REGISTRY.clear()

    def test_register_and_get_instance(self):
        inst = DummyPreprocessorInstance()
        register_preprocessor('inst', inst)
        pre = get_preprocessor('inst')
        self.assertIs(pre, inst)
        self.assertEqual(pre(3), 6)

    def test_register_and_get_class(self):
        register_preprocessor('class', DummyPreprocessor)
        pre = get_preprocessor('class', value=5)
        self.assertIsInstance(pre, DummyPreprocessor)
        self.assertEqual(pre(3), 8)

    def test_not_registered(self):
        with self.assertRaises(ValueError):
            get_preprocessor('not_exist')

    def test_kwargs_passed(self):
        register_preprocessor('class', DummyPreprocessor)
        pre = get_preprocessor('class', value=10)
        self.assertEqual(pre(1), 11)

if __name__ == '__main__':
    unittest.main()