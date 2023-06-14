import json
import os
from collections import Counter
import matplotlib.pyplot as plt

#inputs of program
input_file = 'data.json'
value_to_filter = 'europe-west'
output_file_filtered_data = value_to_filter + '.json'

#remove all other JSON files that are not the input file
directory = os.path.dirname(os.path.abspath(__file__))
files = os.listdir(directory)
for file in files:
    if file.endswith(".json") and file != input_file or file.endswith(".png"):
        os.remove(os.path.join(directory, file))

#filter input data to only selected region and output it as a JSON file
with open(input_file, 'r') as f:
    data = json.load(f)
filteredDataToWrite = [entry for entry in data if 'Region' in entry and entry['Region'] == value_to_filter]
with open(output_file_filtered_data, 'w') as f:
    json.dump(filteredDataToWrite, f, indent=4)

#graph data on time of day (hours)
with open(output_file_filtered_data, 'r') as filtered:
    filteredData = json.load(filtered)
timestamps = [entry["Timestamp (UTC)"] for entry in filteredData]
time_parts = [timestamp.split(" ")[1] for timestamp in timestamps]
hours = [timepart.split(":")[0] for timepart in time_parts]
hourRanges = [f"{hour}:00 - {hour}:59" for hour in hours]
hourRangesCounted = Counter(hourRanges)
hourRangesCountedSorted = sorted(hourRangesCounted.items())
labels = []
counts = []
left_coordinates = []
coordCounter = 1
for key, value in hourRangesCountedSorted:
    labels.append(key)
    counts.append(value)
    left_coordinates.append(coordCounter)
    coordCounter += 1
fig, ax = plt.subplots(figsize=(12, 6))  # Adjust the figure size as needed

ax.bar(left_coordinates, counts, tick_label=labels, width=0.6, color=['red', 'black'])
ax.set_xlabel('Uren van de dag')
ax.set_ylabel('Aantal keer in dataset')
ax.set_title("BeReal momenten (UTC)")

# Adjust the font size of the labels and title
ax.tick_params(axis='x', labelsize=8)  # Font size for x-axis labels
ax.tick_params(axis='y', labelsize=8)  # Font size for y-axis labels
ax.title.set_fontsize(12)  # Font size for the title

# Adjust the spacing between labels
ax.set_xticks(left_coordinates)  # Set the x-ticks at the desired positions
ax.set_xticklabels(labels, rotation=45, ha='right')  # Set the x-tick labels and rotate them if needed

plt.tight_layout()  # Ensures labels do not overlap

plt.savefig("plot.png")