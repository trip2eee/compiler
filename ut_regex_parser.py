import unittest
from src.regex_parser import RegExParser

class RegExParserTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_parser(self):
        
        rules = [
            "[_a-zA-Z]+[_a-zA-Z0-9]*",
            "if",
            "[0-9]+",        
        ]

        for regx in rules:
            parser = RegExParser()
            regx_parser = RegExParser()
            regx_parser.parse(regx)
            regx_parser.print()

if __name__ == '__main__':
    unittest.main()
