import random
#800x 600y
#paddle 150y, the paddle is 1/4 of the screen.

#given the predicted Y value that will hit the middle of the paddle, this function \
#will execute the moviment based of probabilities;
def countEqualBigger(lst:float, x):
    counter = 0
    for each in lst:
        if each >= x:
            counter += 1
    return counter

def botMoviment(deltaY : int, floor : int):
    dice = 20
    x = random.randint(1, dice)

    result = floor + (100 / dice) * x 
    return (int)(result)

values = []
num = 200000
movementSuccess = 150.0
movementMin = movementSuccess / 2

xFloor = []
ySuccess = []
for j in range(50):
    values = []
    for i in range(num):
        values.append(botMoviment(movementSuccess, j))
    blockrate = (100 * countEqualBigger(sorted(values), movementMin)) / num
    ySuccess.append(blockrate)
    xFloor.append(j)

# importing the required module
import matplotlib.pyplot as plt
  
# x axis values
x = range(num)
# corresponding y axis values
y = sorted(values)
# plotting the points 
plt.plot(xFloor, ySuccess)
y_value = movementMin

# Draw the vertical line on the y-axis
plt.axhline(y=y_value, color='red', linestyle='--', label=f'Horizontal Line at y={y_value}')

# naming the x axis
plt.xlabel('x - number of plays')
# naming the y axis
plt.ylabel('y - success %')

# giving a title to my graph
# blockrate = (100 * countEqualBigger(y, movementMin)) / num
# print(blockrate)
# sts = 'blockrate ' + (str)(blockrate) + '%'
plt.title("sts")
  
# function to show the plot
plt.show()