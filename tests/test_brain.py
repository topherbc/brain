import unittest
from src.brain import CognitiveCrew

class TestCognitiveCrew(unittest.TestCase):
    def setUp(self):
        """Set up test cases"""
        self.crew = CognitiveCrew(verbose=False)

    def test_basic_input_processing(self):
        """Test basic input processing"""
        input_text = "What is 2 + 2?"
        result = self.crew.process_input(input_text, domain="math")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)

    def test_none_input_handling(self):
        """Test handling of None input"""
        with self.assertRaises(ValueError):
            self.crew.process_input(None)

    def test_domain_specialization(self):
        """Test domain specialization affects processing"""
        input_text = "What causes rain?"
        
        # Process with physics domain
        physics_result = self.crew.process_input(input_text, domain="physics")
        
        # Process with literature domain
        literature_result = self.crew.process_input(input_text, domain="literature")
        
        # Results should be different due to domain specialization
        self.assertNotEqual(physics_result, literature_result)

    def test_empty_string_input(self):
        """Test handling of empty string input"""
        result = self.crew.process_input("")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)

    def test_long_input_handling(self):
        """Test handling of long input text"""
        long_input = "What is the meaning of life? " * 100
        result = self.crew.process_input(long_input)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)

if __name__ == '__main__':
    unittest.main()