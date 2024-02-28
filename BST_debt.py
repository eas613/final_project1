from customer1 import Customer
from typing import Optional
from datetime import datetime

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


    def _find_first_name(self,first:str,operator:str,customer:Customer,found = None):
        if found is None:
            found = []
        if not customer:
            return found
        self._find_first_name(first,operator,customer._right_debt,found)
        if operator == "=":
            if customer._first.lower() == first:
                print(customer)
                found.append(True)
        elif operator == "!=":
            if customer._first.lower() !=  first:
                print(customer)
                found.append(True)
        if operator == "<":
            if customer._first.lower() < first:
                print(customer)
                found.append(True)
        if operator == ">":
            if customer._first.lower() > first:
                print(customer)
                found.append(True)
        self._find_first_name(first,operator,customer._left_debt,found)
        return found
    
    def _find_last_name(self,last:str,operator:str,customer:Customer,found = None):
        if found is None:
            found = []
        if not customer:
            return found
        self._find_last_name(last,operator,customer._right_debt,found)
        if operator == "=":
            if customer._last.lower() == last:
                print(customer)
                found.append(True)
        elif operator == "!":
            if customer._last.lower() !=  last:
                print(customer)
                found.append(True)
        if operator == "<":
            if customer._last.lower() < last:
                print(customer)
                found.append(True)
        if operator == ">":
            if customer._last.lower() > last:
                print(customer)
                found.append(True)  
        self._find_last_name(last,operator,customer._left_debt,found)
        return found
        
    def find_by_name(self,attr:str,operator,name:str):
        if attr == "first":
            return self._find_first_name(name,operator,self.root)
        if attr == "last":
            return self._find_last_name(name,operator,self.root)

    def _find_by_id(self,id:str,operator:str,customer:Customer,found = None):
        if found is None:
            found = []
        if not customer:
            return found
        self._find_by_id(id,operator,customer._right_debt,found)
        if operator == "!":
            if customer._id !=  id:
                print(customer)
                found.append(True)
        if operator == "<":
            if customer._id < id:
                print(customer)
                found.append(True)
        if operator == ">":
            if customer._id > id:
                print(customer)
                found.append(True)  
        self._find_by_id(id,operator,customer._left_debt,found)
        return found
  
    def find_by_id(self,operator:str,id:str):
            return self._find_by_id(id,operator,self.root)

    def _find_by_phone(self,phone:str,operator:str,customer:Customer,found = None):
        if found is None:
            found = []
        if not customer:
            return found
        self._find_by_phone(phone,operator,customer._right_debt,found)
        if operator == "=":
            if customer._phone ==  phone:
                print(customer)
                found.append(True)
        if operator == "!":
            if customer._phone !=  phone:
                print(customer)
                found.append(True)
        if operator == "<":
            if customer._phone < phone:
                print(customer)
                found.append(True)
        if operator == ">":
            if customer._phone > phone:
                print(customer)
                found.append(True)  
        self._find_by_phone(phone,operator,customer._left_debt,found)
        return found
  
    def find_by_phone(self,operator:str,phone:str):
            return self._find_by_phone(phone,operator,self.root)
    
    def find_by_debt(self,operator:str,debt:float):
            return self._find_by_debt(operator,debt,self.root)

    def _find_by_debt(self,operator,debt:float,customer:Customer,found = None):
        if found is None:
            found = []
        if not customer:
            return
        operator = eval(operator)
        if operator == "!=":
            self._find_by_debt(operator,debt,customer._right_debt,found)
            if customer._debt != debt:
                print(customer)
                found.append(True)
            self._find_by_debt(operator,debt,customer._left_debt,found)
            return found
        elif operator == "=":
            self._find_by_debt(operator,debt,customer._right_debt,found)
            if customer._debt == debt:
                print(customer)
                found.append(True)
            self._find_by_debt(operator,debt,customer._left_debt,found)
            return found
        elif operator == "<":
            self._find_by_debt(operator,debt,customer._right_debt,found)
            if customer._debt < debt:
                print(customer)
                found.append(True)
            self._find_by_debt(operator,debt,customer._left_debt,found)
            return found
        elif operator == ">":
            self._find_by_debt(operator,debt,customer._right_debt,found)
            if customer._debt > debt:
                print(customer)
                found.append(True)
            self._find_by_debt(operator,debt,customer._left_debt,found)
            return found
    
    def find_by_date(self,operator,date:datetime):
            return self._find_by_date(operator,date,self.root)
    
    def _find_by_date(self,operator,date:datetime,customer:Customer,found = None):
        if found is None:
            found = []
        if not customer:
            return
        if operator == "!=":
            self._find_by_date(operator,date,customer._right_debt,found)
            if customer._date != date:
                print(customer)
                found.append(True)
            self._find_by_date(operator,date,customer._left_debt,found)
            return found
        elif operator == "=":
            self._find_by_date(operator,date,customer._right_debt,found)
            if customer._date == date:
                print(customer)
                found.append(True)
            self._find_by_date(operator,date,customer._left_debt,found)
            return found
        elif operator == "<":
            self._find_by_date(operator,date,customer._right_debt,found)
            if customer._date < date:
                print(customer)
                found.append(True)
            self._find_by_date(operator,date,customer._left_debt,found)
            return found
        elif operator == ">":
            self._find_by_date(operator,date,customer._right_debt,found)
            if customer._date > date:
                print(customer)
                found.append(True)
            self._find_by_date(operator,date,customer._left_debt,found)
            return found
    
    