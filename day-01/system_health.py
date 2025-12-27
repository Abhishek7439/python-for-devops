# ---------------------------
#  System Health Check Script
#  Day 01 - Python for DevOps
# ---------------------------

import psutil

def system_health_check():

    cpu_usage_threshold = int(input("CPU threshold (%): "))
    disk_usage_threshold = int(input("Disk threshold (%): "))
    memory_usage_threshold = int(input("Memory threshold (%): "))

    print("\nSystem health check running...\n")

    current_cpu_usage = psutil.cpu_percent(interval=1)
    current_disk_usage = psutil.disk_usage('/').percent
    current_memory_usage = psutil.virtual_memory().percent

    if current_cpu_usage > cpu_usage_threshold:
        print("CPU USAGE")
        print(f"Current CPU usage: {current_cpu_usage}%")
        print(f"CPU usage exceeded threshold: {cpu_usage_threshold}%\n")

    if current_disk_usage > disk_usage_threshold:
        print("DISK USAGE")
        print(f"Current Disk usage: {current_disk_usage}%")
        print(f"Disk usage exceeded threshold: {disk_usage_threshold}%\n")

    if current_memory_usage > memory_usage_threshold:
        print("MEMORY USAGE")
        print(f"Current Memory usage: {current_memory_usage}%")
        print(f"Memory usage exceeded threshold: {memory_usage_threshold}%\n")


system_health_check()
