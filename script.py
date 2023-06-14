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

#graph data on time of day (hours) (UTC)
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
fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(left_coordinates, counts, tick_label=labels, width=0.6, color=['#FECC00', 'black'])
ax.set_xlabel('Uren van de dag')
ax.set_ylabel('Aantal keer in dataset')
ax.set_title("BeReal momenten (UTC)")
ax.tick_params(axis='x', labelsize=8)
ax.tick_params(axis='y', labelsize=8)
ax.title.set_fontsize(12)
ax.set_xticks(left_coordinates)
ax.set_xticklabels(labels, rotation=45, ha='right')
plt.tight_layout()
plt.savefig("plot.png")