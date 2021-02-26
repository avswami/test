import unittest
from doc_test import add 

class Test_addmethods(unittest.TestCase):
  def test_can_add_num(self):
      self.assertEqual(add(8,4), 12)

  def test_can_add_negative_num(self):
      self.assertEqual(add(-2,-4), -6)


if __name__ == '__main__':
    unittest.main()