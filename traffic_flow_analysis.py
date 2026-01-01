import csv
from collections import Counter

csv_file = "outputs/traffic_log.csv"

vehicle_counts = []
traffic_states = []

with open(csv_file, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        total = int(row["Cars"]) + int(row["Motorcycles"]) + int(row["Buses"]) + int(row["Trucks"])
        vehicle_counts.append(total)
        traffic_states.append(row["Traffic_Status"])

if not vehicle_counts:
    print("No traffic data available.")
    exit()

average_vehicles = sum(vehicle_counts) / len(vehicle_counts)
max_vehicles = max(vehicle_counts)
most_common_state = Counter(traffic_states).most_common(1)[0][0]

print("\n--- TRAFFIC FLOW ANALYSIS REPORT ---")
print(f"Total Records Analysed : {len(vehicle_counts)}")
print(f"Average Vehicle Count  : {average_vehicles:.2f}")
print(f"Peak Vehicle Count     : {max_vehicles}")
print(f"Most Frequent Traffic  : {most_common_state}")
print("-----------------------------------")
