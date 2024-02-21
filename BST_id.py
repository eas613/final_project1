from customer1 import Customer
from typing import Optional

class Customer_BST_id:
    def __init__(self) -> None:
        self._root = None
    
    def add_customer(self,customer:Customer):
        if not self._root:
            self._root = customer
            return
        
        id = customer.id
        temp = self._root
        while True:
            temp_id = temp.id
            if id <= temp_id:
                if not temp._left_id:
                    temp._left_id = customer
                    return
                temp = temp._left_id
            else:
                if not temp._right_id:
                    temp._right_id = customer
                    return
                temp = temp._right_id