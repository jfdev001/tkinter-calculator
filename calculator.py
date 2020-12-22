"""Simple calculator implemented using tkinter.

Documentation:
https://tcl.tk/man/tcl8.6/TkCmd/contents.htm

https://docs.python.org/3/library/tkinter.html#tk-option-data-types

Notes:
--On passing function to kwarg 'command' for Button widget 
--Reason for using ' from functools import partial '
--Why does command lambda: button_click(ele) not work for buttonList?
https://stackoverflow.com/questions/6920302/how-to-pass-arguments-to-
a-button-command-in-tkinter
"""

from tkinter import *
from functools import partial


# Functions
def button_click(operand):
    """Insert args to Entry widget then eval if '='"""
    if (operand == "Clear"): # Clear the entry field
        expr.delete(0, END)
    elif (operand == "="):   # Calculate and display result
        expression_list = parse_expression(expr.get())
        result = parse_calculation(expression_list)
        expr.delete(0, END)
        expr.insert(0, result)
    else:                    # Get current length and insert next index
        cur_length = len(expr.get())
        expr.insert(cur_length+1, operand)


def parse_expression(expr):
    """Convert expr to int list then calculate based on PEMDAS"""
    expression_list = list()  # Stores infix int & str math expression
    operator_list = ["+", "-", "*", "/"]
    index = 0     # For iterating through str expression 
    num = ""      # Str which will be converted to float
    # Build expression_list
    while (index < len(expr)):
            if (expr[index] not in operator_list):
                num += expr[index]
            elif (expr[index] in operator_list):
                expression_list.append(float(num))
                num = "" 
                expression_list.append(expr[index])

            if (index == len(expr)-1):
                expression_list.append(float(num))

            index += 1    # Recurring operation
    return expression_list


def parse_calculation(expression_list):
    """Calculate result based on PE(MDAS) ignoring P & E."""
    has_operands = True
    # Search for indices of operands in MDAS and update expression_list
    while(has_operands):
        try:
            op_index = expression_list.index("*")
            expression_list[op_index-1] = (expression_list[op_index-1]   
                                          * expression_list[op_index+1])
            del(expression_list[op_index])
            del(expression_list[op_index])
        except:
            try:
                op_index = expression_list.index("/")
                expression_list[op_index-1] = (expression_list[op_index-1] 
                                            / expression_list[op_index+1])
                del(expression_list[op_index])
                del(expression_list[op_index])
            except:
                try:    
                    op_index = expression_list.index("+")
                    expression_list[op_index-1] = (expression_list[op_index-1] 
                                                + expression_list[op_index+1])
                    del(expression_list[op_index])
                    del(expression_list[op_index])
                except:
                    try:
                        op_index = expression_list.index("-")
                        expression_list[op_index-1] = (expression_list[op_index-1] 
                                          - expression_list[op_index+1])
                        del(expression_list[op_index])
                        del(expression_list[op_index])
                    except:
                         has_operands = False 
    return expression_list[0]


# Parent window
root = Tk()
root.title("My Calculator")

# Expression Entry widget
expr = Entry(root, width=35, borderwidth=3)
expr.grid(row=0, column=0, columnspan=3) # Splits below column to 3 part

# Define list of Button widgets for calculator
button_list = list() # The nth element of this list is the nth button
for ele in range (0,10):
    button_to_add = Button(root, text=f"{ele}", padx=40, pady=20, 
                         command=partial(button_click, ele))
    button_list.append(button_to_add)

# Display calculator buttons -- better way to do this?
for topButton in range (7, 10):
    button_list[topButton].grid(row=1, column=topButton-7)
for midButton in range (4, 7):
    button_list[midButton].grid(row=2, column=midButton-4)
for botButton in range (1, 4):
    button_list[botButton].grid(row=3, column=botButton-1)
button_list[0].grid(row=4, column = 0)

# Define operation Button widgets
button_clear = Button(root, text="Clear", padx=78,pady=20, 
                     command=lambda: button_click("Clear"))
button_plus = Button(root, text="+",padx=39,pady=20, 
                    command=lambda: button_click("+"))
button_minus = Button(root, text="-", padx=41, pady=20,
                      command=lambda: button_click("-"))
button_multiply = Button(root, text="*", padx=40, pady=20,
                      command=lambda: button_click("*"))                       
button_divide = Button(root, text="/", padx=40, pady=20,
                      command=lambda: button_click("/"))                                          
button_equal = Button(root, text="=", padx=86,pady=20, 
                     command=lambda: button_click("=")) 

# Display operation Button widgets
button_clear.grid(row=4, column=1, columnspan=2)
button_plus.grid(row=5, column=0)
button_minus.grid(row=6, column=0)
button_multiply.grid(row=6, column=1)
button_divide.grid(row=6, column=2)
button_equal.grid(row=5, column=1, columnspan=2) 

# Event loop
root.mainloop()

