import unittest
from src.regex_parser import RegExParser

class RegExParserTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_parser(self):
        
        rules = [
            "/\*[.\n]*\*/",
            "[_a-zA-Z]+[_a-zA-Z0-9]*",
            "if",
            "[0-9]+[.]?[0-9]*[fF]?",
        ]

        regx_parser = RegExParser()

        for regx in rules:            
            regx_parser.parse(regx)
            regx_parser.print()

if __name__ == '__main__':
    unittest.main()
