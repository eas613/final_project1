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
        
    def _print_ordered_by_debt(self,customer):
        if not customer:
            return
        self._print_ordered_by_debt(customer._right_debt)
        print(customer)
        self._print_ordered_by_debt(customer._left_debt)

    def print_ordered_by_debt(self):
        self._print_ordered_by_debt(self._root)
        print("")
    
    @property
    def root(self):
        return self._root 
    
    def find_max_debt(self,customer:Customer)->Customer|None:
        if not customer:
            return

    def find_max_debt(self,customer:Customer)-> Customer|None:
        if not customer:
            return
        if not customer._right_debt:
            return customer
        return self.find_max_debt(customer._right_debt)

    def _remove_customer(self,customer:Customer,current:Customer,prev):
        if not current:
            print("Error , not found.")
            return
        if customer is current: # if removing the root
            if not customer._left_debt :
                self.remove_no_left(customer,prev)
            elif not customer._right_debt :
                self.remove_no_right(customer,prev)
            else:
                self.remove_two_child(customer,prev)
        elif customer._debt <= current._debt:
            self._remove_customer(customer,current._left_debt,current)
        elif customer._debt > current._debt:
            self._remove_customer(customer,current._right_debt,current)
    

    def remove_customer(self,customer:Customer):
        self._remove_customer(customer,self.root,self.root)

    def remove_no_left(self,customer:Customer,prev:Customer):   
        if customer is self.root:
            self._root = customer._right_debt
        elif prev._left_debt is customer:
            prev._left_debt = customer._right_debt
        elif prev._right_debt is customer:
            prev._right_debt = customer._right_debt
        customer.reset_left_right_debt()

    def remove_no_right(self,customer:Customer,prev:Customer):
        if customer is self.root:
                self._root = customer._left_debt
        elif prev._left_debt is customer:
            prev._left_debt = customer._left_debt
        elif prev._right_debt is customer:
            prev._right_debt = customer._left_debt
        customer.reset_left_right_debt()

    def remove_two_child(self,customer:Customer,prev:Customer):
        max_customer = self.find_max_debt(customer._left_debt)
        self.remove_customer(max_customer) 
        max_customer._right_debt = customer._right_debt
        max_customer._left_debt = customer._left_debt
        if customer is self._root:
            self._root = max_customer
        elif prev._left_debt is customer:
            prev._left_debt = max_customer
        elif prev._right_debt is customer:
            prev._right_debt = max_customer
        customer.reset_left_right_debt()
        return


    def _find_first_name(self,first:str,customer:Customer,found = None):
        if found is None:
            found = []
        if not customer:
            return found
        self._find_first_name(first,customer._right_debt,found)
        if customer._first.lower() == first:
            print(customer)
            found.append(True)
        self._find_first_name(first,customer._left_debt,found)
        return found
    
    def _find_last_name(self,last:str,customer:Customer,found = None):
        if found is None:
            found = []
        if not customer:
            return found
        self._find_last_name(last,customer._right_debt,found)
        if customer._last.lower() == last:
            print(customer)
            found.append(True)
        self._find_last_name(last,customer._left_debt,found)
        return found
        
    def find_by_name(self,attr,name:str):
        if attr == "first":
            return self._find_first_name(name,self.root)
        if attr == "last":
            return self._find_last_name(name,self.root)
        
    def _find_phone(self,phone:str,customer:Customer,found = None):
        if found is None:
            found = []
        if not customer:
            return found
        self._find_phone(phone,customer._right_debt,found)
        if customer._phone == phone:
            print(customer)
            found.append(True)
        self._find_phone(phone,customer._left_debt,found)
        return found
    
    def find_by_phone(self,phone:str):
            return self._find_phone(phone,self.root)

        
    