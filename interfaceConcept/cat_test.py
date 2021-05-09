from interfaceConcept.reporter import Reporter
from interfaceConcept.main import Cat
import unittest

class TestCatClass(unittest.TestCase):
    def test_run(self):
        cat = Cat(Reporter())
        self.assertEqual(cat.run(), "I've ran for 3 miles.")

    def test_shit(self):
        cat = Cat(Reporter())
        self.assertEqual(cat.shit(), "I've shit on your carpet, happy cleaning!!!")

    def test_eat(self):
        cat = Cat(Reporter())
        self.assertEqual(cat.eat(3), "I've eaten 3 cat food(s).")


if __name__ == '__main__':
    unittest.main()