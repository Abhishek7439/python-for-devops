# ---------------------------
#  System Health Check Script
#  Day 01 - Python for DevOps
# ---------------------------

import psutil


def get_threshold(label):
    """Safely get a percentage threshold from the user."""
    try:
        value = int(input(f"{label} threshold (%): "))
        if 0 <= value <= 100:
            return value
        print("Please enter a value between 0–100.")
    except ValueError:
        print("Invalid input. Please enter a number.")
    return None


def system_health_check():
    """Main system health check logic."""

    try:
        cpu_usage_threshold = get_threshold("CPU")
        disk_usage_threshold = get_threshold("Disk")
        memory_usage_threshold = get_threshold("Memory")

        # Stop script if invalid input
        if None in ( cpu_usage_threshold, disk_usage_threshold, memory_usage_threshold ):
            print("\nStopping script — invalid input received.")
            return

        print("\nSystem health check running...\n")

        current_cpu_usage = psutil.cpu_percent(interval=1)
        current_disk_usage = psutil.disk_usage("/").percent
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
            print(f"Memory usage exceeded threshold:{memory_usage_threshold}%\n")

    except Exception as error:
        print(f"Unexpected error occurred: {error}")


if __name__ == "__main__":
    system_health_check()
