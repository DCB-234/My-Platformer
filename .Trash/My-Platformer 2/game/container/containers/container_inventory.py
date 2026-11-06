# Container classes manages what happens when player has their ui open
from game.container.container_type import ContainerType
from game.container.inventory import Inventory

class ContainerInventory(Inventory):
    def __init__(self):
        self.container_type = ContainerType.INVENTORY
        super().__init__(INVENTORY_SIZE=36)