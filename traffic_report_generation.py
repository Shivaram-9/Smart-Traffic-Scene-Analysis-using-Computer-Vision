import csv
from collections import Counter

csv_file = "outputs/traffic_log.csv"
report_file = "outputs/traffic_report.txt"

vehicle_counts = []
traffic_states = []

with open(csv_file, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        total = (
            int(row["Cars"]) +
            int(row["Motorcycles"]) +
            int(row["Buses"]) +
            int(row["Trucks"])
        )
        vehicle_counts.append(total)
        traffic_states.append(row["Traffic_Status"])

if not vehicle_counts:
    print("No data available to generate report.")
    exit()

avg_vehicles = sum(vehicle_counts) / len(vehicle_counts)
peak_vehicles = max(vehicle_counts)
common_state = Counter(traffic_states).most_common(1)[0][0]

with open(report_file, "w") as report:
    report.write("SMART TRAFFIC SCENE ANALYSIS REPORT\n")
    report.write("---------------------------------\n")
    report.write(f"Total Records Analysed : {len(vehicle_counts)}\n")
    report.write(f"Average Vehicle Count  : {avg_vehicles:.2f}\n")
    report.write(f"Peak Vehicle Count     : {peak_vehicles}\n")
    report.write(f"Most Frequent Traffic  : {common_state}\n\n")

    if common_state == "HEAVY":
        conclusion = "Heavy congestion observed. Traffic control measures recommended."
    elif common_state == "MODERATE":
        conclusion = "Moderate traffic flow observed. Monitor peak hours."
    else:
        conclusion = "Traffic flow is normal."

    report.write("Conclusion:\n")
    report.write(conclusion)

print("✅ Traffic report generated successfully.")
print(f"📄 Report saved at: {report_file}")
