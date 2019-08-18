from unittest import TestCase

from game.tablescript import eval
from game.tablescript.datatypes import IntegerBox
from game.tablescript.datatypes import FloatingBox

import math

class TypeTest(TestCase):

    def setUp(self):
        return

    def tearDown(self):
        return

    def test_Numbers(self):

        try:

            for i in range(0, 10):
                if IntegerBox(i).value != eval(str(i), {}).value.value:
                    self.fail()

            if FloatingBox(math.inf).value != eval(str(float(math.inf)), {}).value.value:
                self.fail()

        except Exception as e:
            self.fail()

