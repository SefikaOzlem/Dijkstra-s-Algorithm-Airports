import os

print("\nHello, you will be shown the most suitable transfers,the total cost to be paid \nand the total distance according to the flight type you choose.\n")
print("1- Show by minimum distance")
print("2- Show by minimum cost")
print("3- Show by minimum transfer")
option = input("\nPlease!! Enter the option you want: ")

if str(option)=="1":
    print("\n-- MINIMUM DISTANCE --")
    os.system('python dijkstra_min_distance.py')
elif str(option)=="2":
    print("\n-- MINIMUM COST --")
    os.system('python dijkstra_min_cost.py')
elif str(option)=="3":
    print("\n-- MINIMUM VERTEX --")
    os.system('python dijkstra_min_vertex.py')
else:
    print("\n-- !! WRONG INPUT !! --")

    '''
    Enter from airport name: Nanping Wuyishan Airport
Enter to airport name: Frankfurt Hahn
    '''