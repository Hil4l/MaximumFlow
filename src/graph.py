import numpy as np
import matplotlib.pyplot as plt
 
# set width of bar
barWidth = 0.25
fig = plt.subplots(figsize =(10, 5))

categories = ['100', '300', '700', '900', '1300', '1500']

# set height of bar
LP1 = [0.002, 0.02, 0.36, 0.1, 4.3, 3]
FF1 = [0.002, 0.02, 0.3, 0.6, 2.1, 3.3]

LP = [0.01, 0.01, 0.9, 2, 6.1, 8.8]
FF = [0.01, 0.01, 1.1, 3, 10.6, 12]

LP3 = [0.01, 0.1, 1.8, 3.4, 9, 15.1]
FF3 = [0.01, 0.1, 3.6, 8.5, 23.1, 31.4]

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
plt.xlabel('(0.2) Instance', fontweight ='bold')
plt.ylabel('Solving time (s)', fontweight ='bold')
plt.xticks([r + barWidth for r in range(len(LP))], categories)
 
plt.legend()
plt.title('Comparaison temps resolution: LP vs FF (0.2 densité)')

plt.show()