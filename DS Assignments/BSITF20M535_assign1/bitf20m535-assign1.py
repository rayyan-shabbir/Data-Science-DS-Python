# ASSIGNMENT # 01 (DATA SCIENCE)
# Name: Rayyan Ahmed
# Roll: BITF20M535


# Importing important libraries
import numpy as np
import sys


print("\nVM IMPLEMENTATION")
print("#######***************************************************************************########\n")

# VM Implementation (by executing tas1.bin)
# Loading VM Images
def load_program(fileName):
    
    # reading the program images file
    fhand = open(fileName, 'r')
    vm_images = fhand.readlines()
    # print(len(vm_images))
    # print(vm_images)
    
    
    # Step-01: Reading the size of the data array
    data_size = int(vm_images[0], 16)
    # print(data_size)
    
    
    # Step-02: Allocating the 'data' array
    # data = np.zeros(data_size)
    data = [0] * data_size
    # print(data)
    
    
    # Step-03: Reading the size of the vm images
    image_size = int(vm_images[1], 16)
    # print(image_size)
    
    # Step-04: Read the vm images values sequentially into the 'data' array
    for i in range(image_size):
        # data[i] = "{032b}".format((int(vm_images[i+2], 16)))                # can write vm images values in 32 bit binary form in array
        data[i] = int(vm_images[i+2], 16)                                   # can write vm images values in 32 bit integer form in array
    
    #returning 'data' array
    return data





# Calling load_program
data = load_program('task1.bin')

# print(data[49])



# Defining important signed variables (registers)
# Global variables
ip = 0
sp = len(data)
# print(ip, sp)



# Important Functions of 'f' & 'g' which are called by below instructions
def f_func(v):
    # declare ip & sp as global variables
    global ip
    global sp
    
    sp = sp - 1
    data[sp] = v

    
def g_func():
    # declare ip & sp as global variables
    global sp
    global ip
    
    v = data[sp]
    sp = sp + 1
    return v




# Interpreting VM Images (Instructions)
def interpreting(data):
    # declare ip & sp as global variables
    count = 0
    global ip
    global sp
    result_output = ""
    

    while True:

        current_instruction = data[ip]
        ip = ip + 1
        
        
        # DECODE Instruction
        binop = (current_instruction >> 31)                         # 32nd bit represents binop (applying bitwise righ-shift to get this bit)
        operation = (current_instruction >> 24) & 0x7f              # 25-31 bits represents operation (applying bitwise righ-shift to get these bits)
        optional_data = current_instruction & 0xffffff              # First 24 bits represents optional data (applying bitwise righ-shift to get these bits)
        
        # print(binop)
        # print(operation)
        # print(optional_data)
        
        
        # VM Instructions (Action to be performed)
        # Checking binop bit
        if binop == 0:
            # Checking operation bits to do action
            if operation == 0 or operation == 0x00:
                # print("\nPOP")
                pop = data[sp]
                data[sp] = None
                sp = sp + 1
                print("Poped value = ", pop)
                
            elif operation == 1 or operation == 0x01:
                # print("\nPUSH <const>")
                f_func(optional_data)
                
            elif operation == 2 or operation == 0x02:
                # print("\nPUSH ip")
                f_func(ip)
                
            elif operation == 3 or operation == 0x03:
                # print("\nPUSH sp")
                f_func(sp)
                
            elif operation == 4 or operation == 0x04:
                # print("\nLOAD")
                addr = g_func()
                if addr >= 0 and addr <= (len(data) - 1):
                    f_func(data[addr])
                else:
                    print("LOAD :: Cannot add value in array because Index is out of range.")
                
            elif operation == 5 or operation == 0x05:
                # print("\nSTORE")
                st_data = g_func()
                addr = g_func()
                if addr >= 0 and addr <= (len(data) - 1):
                    data[addr] = st_data
                else:
                    print("STORE :: Cannot add value in array because Index is out of range.")
                
            elif operation == 6 or operation == 0x06:
                # print("\nJMP")
                cond = g_func()
                addr = g_func()
                
                if cond != 0:
                    ip = addr
                    
            elif operation == 7 or operation == 0x07:
                # print("\nNOT")
                
                if not(g_func()):
                    f_func(1)
                else:
                    f_func(0)
                    
            elif operation == 8 or operation == 0x08:
                # print("\nPUTC")

                result_output += chr(int(g_func() & 0xff))              # converting 1 byte (integer) into it's appropriate ASCII text
                # print("One byte stream output is ", output)
                
            elif operation == 9 or operation == 0x09:
                # print("GETC")
                # reading 1 byte from stdin
                char_x = input("Enter 1 byte: ")[0]
                char_int = ord(char_x)                      # convert this 1 byte value to its sepcified unicode
                
                # casting input to 32 bits
                cast_x = "{032b}".format(char_int)
                
                # calling function
                f_func(cast_x & 0xff)
                
                
            elif operation == 10 or operation == 0x0A:
                # print("HALT")

                return result_output
                sys.exit()              # terminating program

            else:
                print("Operation bits (value) does not match.")
                
                
        elif binop == 1:
            # getting values 'a' & 'b' by calling g()
            b = g_func()
            a = g_func()
            
            # Checking operation bits to do action
            if operation == 0 or operation == 0x00:
                # print("\nADD")
                op_res = (a + b)
                f_func(op_res)
                
            elif operation == 1 or operation == 0x01:
                # print("\nSUBTRACT")
                op_res = (a - b)
                f_func(op_res)
                
            elif operation == 2 or operation == 0x02:
                # print("\nMULTIPLY")
                op_res = (a * b)
                f_func(op_res)
                
            elif operation == 3 or operation == 0x03:
                # print("\nDIVIDE")
                
                # checking denominator
                if b != 0:
                    op_res = int(a / b)
                else:
                    print("Division is not possible because denominator is 0.")
                    op_res = 0
                    
                f_func(op_res)
                
            elif operation == 4 or operation == 0x04:
                # print("\nAND")
                op_res = (a & b)
                f_func(op_res)
            
            elif operation == 5 or operation == 0x05:
                # print("\nOR")
                op_res = (a | b)
                f_func(op_res)
                
            elif operation == 6 or operation == 0x06:
                # print("\nXOR")
                op_res = (a ^ b)
                f_func(op_res)
                
            elif operation == 7 or operation == 0x07:
                # print("EQUAVALENT")
                op_res = int(a == b)
                f_func(op_res)
                
            elif operation == 8 or operation == 0x08:
                # print("LESS THAN")
                op_res = int(a < b)
                f_func(op_res)

            else:
                print("Operation bits (value) does not match.")
                
    print("I will Never Execute...")





# Calling interpreting function
print("*** Instructions that are performing ***")
result_output = interpreting(data)


print("\n\n*** Resultant Output ***\n")
print(result_output)



# Writing output into result.txt & dataArray.txt file
# opening result.txt file in append mode
fhand_r = open('result.txt', 'a')               # this file contains resultant output
# opening dataArray.txt file in append mode
fhand_d = open('dataArray.txt', 'a')            # this file contains 'data' array values

fhand_r.write(result_output)


array_size = len(data)
# iterating array and write its contents into file line by line
for i in range(array_size):
    fhand_d.write(str(data[i]) + '\n')
    # fhand.write(chr(array[i]))


print("\n\n---> *** Successfully written into file...***")



print("\n\n#######***************************************************************************########")


# *** TEST CASE ***
def Test_Case():
    print("\n*** Test Suite ***")

    total_test = 25
    global ip
    global sp

    for i in range(1, 26):

        if i < 10:
            # Calling load_program
            test_data = load_program('test0' + str(i) + '.bin')
            
        elif i >= 10:
            # Calling load_program
            test_data = load_program('test' + str(i) + '.bin')
        
        ip = 0
        sp = len(test_data)

        # Calling interpreting function
        test_array = interpreting(test_data)

        print("Output of test " + str(i) + ":\t"  , test_array)




# calling Test Case function
Test_Case()
