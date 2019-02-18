type_castle = [[0,0,0,3,0,0,0],
               [2,0,2,2,2,0,2],
               [1,1,1,1,1,1,1]]

# The center point of each composite will allow the code to generate a 
# structure that covers the most area possible, by increasing the value 
# by 433 the next part of the structure will be aproximately at the next
# level upwards, and by increasing the x value by 250 aproximately at 
# the next column

# 1st position
# x = 750
# y = 0 (because when the xml is created a -350 is given to the base) 
# End position
# x = - 750
# y = 1050
# Increments
# x =  - 250
# y = composite height


def calculate_mask(individual, mask):
    # 
    # First
    height_list = []
    new_x_list = []
    x = 750
    el_height = -350
    el_height_cont = 0
    cumulative_height = 0
    for item in individual:
        for element in item:
            for obj in element:
                if len(obj) <= 2:
                    height_list.append(obj[1])

    print(height_list)

    for j in range(6, -1, -1):
        for i in range(2, -1, -1):
            print(mask[i][j])
            # set x value to the column value
            # get a piece and place it
            
            while cumulative_height <= (mask[i][j] * 150):
                # while the height of the current column is less than an estimated value continue adding pieces
                print(height_list[0])
                print(height_list)
                cumulative_height += height_list[0]
                new_x_list.append(x)
                el_height = el_height + (height_list[0]/2)
                el_height_cont = height_list[0]/2
                height_list.pop(0)
            
            #print("Line break")
            
            # Check if the next line requires adding pieces
            if mask[i-1][j] == 0 or (i-1)==-1:
                # reset the height value
                x += -250
                print(cumulative_height)
                print(height_list[0])
                cumulative_height = 0
                print("-----< Column break >-----")
                # Exit current iteration
                break
    for r in range(0, len(height_list)):
        new_x_list.append(1000)
    print("----< Re-Write Individual >----")
    print(new_x_list)            
    for item in individual:
        for element in item:
            for obj in element:
                if len(obj) <= 2:
                    obj[0] = new_x_list[0]
                    height_list.append(obj[1])
                    new_x_list.pop(0)
    return individual
