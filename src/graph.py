import numpy as np
import matplotlib.pyplot as plt
 
# set width of bar
barWidth = 0.25
fig = plt.subplots(figsize =(10, 5))

categories = ['100', '300', '700', '900', '1300', '1500']

# set height of bar
LP = [0.001, 0.1, 0.3, 0.6, 2.1, 3.3]
FF = [0.01, 0.2, 2.44, 3.8, 17.1, 13.2]

# Calculate the difference between the heights of the two bars
diff = np.divide(FF, LP)
 
# Set position of bar on X axis
br1 = np.arange(len(LP))
br2 = [x + barWidth for x in br1]
 
# Make the plot
plt.bar(br1, LP, width = barWidth, label ='LP')
plt.bar(br2, FF, width = barWidth, label ='FF')
 
# Add a line representing the growing difference
plt.axhline(0, color='black')  # Baseline at y=0
plt.plot(br2, diff, linestyle='-', color='g', label='Diff (facteur)')

# Adding Xticks
plt.xlabel('(0.1) Instance', fontweight ='bold')
plt.ylabel('Solving time (s)', fontweight ='bold')
plt.xticks([r + barWidth for r in range(len(LP))], categories)
 
plt.legend()
plt.title('Comparaison temps resolution: LP vs FF (0.1 densité)')

plt.show()