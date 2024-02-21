from customer1 import Customer
from typing import Optional

class Customer_BST:
    def __init__(self) -> None:
        self._root = None
    
    def add_customer(self,customer:Customer):
        if not self._root:
            self._root = customer
            return
        
        debt = customer.debt
        temp = self._root
        while True:
            temp_debt = temp.debt
            if debt <= temp_debt:
                if not temp._left_debt:
                    temp._left_debt = customer
                    return
                temp = temp._left_debt
            else:
                if not temp._right_debt:
                    temp._right_debt = customer
                    return
                temp = temp._right_debt
        
  
    
        
    