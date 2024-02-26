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
  
    def _print_ordered_by_id(self,customer):
            if not customer:
                return
            self._print_ordered_by_id(customer._left_id)
            print(customer)
            self._print_ordered_by_id(customer._right_id)

    def print_ordered_by_id(self):
        self._print_ordered_by_id(self._root)
        print("")

    @property
    def root(self):
        return self._root 

    def _find_customer(self,id:str,customer:Customer):
        if not customer:
            return False
        if id == customer.id:
            return customer
        if id < customer.id:
            return self._find_customer(id,customer._left_id)
        if id > customer.id:
            return self._find_customer(id,customer._right_id)
    
    def find_customer_by_id(self,id:str)->Customer:
        return self._find_customer(id,self.root)
    
    def _find_first_name(self,first:str,customer:Customer,found = None):
        if found is None:
            found = []
        if not customer:
            return found
        if customer._first.lower() == first:
            print(customer)
            found.append(True)
        self._find_first_name(first,customer._left_id,found)
        self._find_first_name(first,customer._right_id,found)
        return found
    
    def _find_last_name(self,last:str,customer:Customer,found = None):
        if found is None:
            found = []
        if not customer:
            return found
        if customer._last.lower() == last:
            print(customer)
            found.append(True)
        self._find_last_name(last,customer._left_id,found)
        self._find_last_name(last,customer._right_id,found)
        return found
        
    def find_by_name(self,attr,name:str):
        if attr == "first":
            return self._find_first_name(name,self.root)
        if attr == "last":
            return self._find_last_name(name,self.root)
