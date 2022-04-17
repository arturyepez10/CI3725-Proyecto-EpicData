from matplotlib import pyplot as plt

# Set the figure size
plt.rcParams["figure.figsize"] = [7.00, 3.50]
plt.rcParams["figure.autolayout"] = True

# List of data points
data = [0, 1, 3, 2, 1, 5, 2, 1, 4, 2, 4, 0]

# Plot bar chart with data points
plt.bar(data, data)

# Display the plot
plt.show()