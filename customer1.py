from datetime import date

class Customer:
    def __init__(self,first:str,last:str,id:int,phone:str,debt:float,date:date) -> None:
        self._first = first 
        self._last = last
        self._id =id 
        self._phone = phone
        self._debt = float(debt)
        self._date  = date
        self._left_id = None
        self._right_id = None
        self._left_debt = None
        self._right_debt = None
    
    @property
    def id(self)->str:
        return self._id
    
    @property
    def debt(self)->float:
        return self._debt

    def add_debt(self,debt:float|int):
        self._debt += float(debt) 

    def reset_left_right_debt(self):
        self._right_debt = None
        self._left_debt = None
    
    def __str__(self) :
        return f"name:{self._first} {self._last} id:{self._id} phone:{self._phone} debt:{self._debt} date:{self._date}"

    
