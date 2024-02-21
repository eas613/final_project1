import sys 
import os
from customer1 import Customer
from datetime import datetime
from BST_debt import Customer_BST
# from BST_id import Customer_BST_id

if len(sys.argv) < 2 :
    print ("Error: missing csv file name.")
    quit()

bst = Customer_BST()

csv_file = sys.argv[1]
if not os.path.exists(csv_file):
    with open(csv_file, "w"):
        pass

with open(csv_file, "r") as fd:
    for line in fd.readlines():
        fields = line.strip().split(",")

        