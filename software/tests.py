_num_rows = 7
_num_cols = 21
#print(math.ceil(17/8)-1)
for y in range(7):
    for x in range(21):
        serial_data = 0
        # state = 1
        serial_data = serial_data | (1 << y)  # set row
        serial_data = serial_data | (1 << (x + 24 + (8 * (x // 8))))  # set col
        print("( , ,  ) :   7654321076543210765432107654321076543210765432107654321076543210")
        print(f"({x},{y},ON) :{" "*(2-((x-10>=0) + (y-10>=0)))} {serial_data:064b}")
        print(serial_data)
        for i in range(64):
            print(serial_data&1, end="")
            serial_data >>= 1
        print("")