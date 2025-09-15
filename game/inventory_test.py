import unittest

from .inventory import Inventory
from .items import RustySword

class TestInventory(unittest.TestCase):

    def test_add(self):
        sword = RustySword()
        inventory = Inventory()
        inventory.add_item(sword)
        self.assertEqual(len(inventory._items), 1)
        self.assertEqual(inventory._items[0], sword)

    def test_remove(self):
        sword = RustySword()
        inventory = Inventory()
        inventory.add_item(sword)
        inventory.remove_item(sword)
        self.assertEqual(len(inventory._items), 0)

if __name__ == "__main__":
    unittest.main()