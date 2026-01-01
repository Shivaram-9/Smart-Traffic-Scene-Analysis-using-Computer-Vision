import csv

csv_file = "outputs/traffic_log.csv"

previous_count = None
anomaly_detected = False

print("\n--- TRAFFIC ANOMALY DETECTION REPORT ---")

with open(csv_file, 'r') as file:
    reader = csv.DictReader(file)

    for row in reader:
        current_count = (
            int(row["Cars"]) +
            int(row["Motorcycles"]) +
            int(row["Buses"]) +
            int(row["Trucks"])
        )

        if previous_count is not None:
            if current_count - previous_count >= 8:
                print("⚠️ Sudden traffic surge detected!")
                anomaly_detected = True
                break

        previous_count = current_count

if anomaly_detected:
    print("⚠️ Possible traffic anomaly or incident detected.")
else:
    print("✅ Traffic flow appears normal.")

print("---------------------------------------")
