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
    if file.endswith(".json") and file != input_file:
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
plt.bar(left_coordinates,counts,tick_label=labels,width=0.6,color=['red','black'])
plt.xlabel('uren van de dag')
plt.ylabel('aantal keer in dataset')
plt.title("BeReal momenten (UTC)")
mng = plt.get_current_fig_manager()
mng.full_screen_toggle()
plt.show()