import simpy
import matplotlib.pyplot as plt
import random
from tabulate import tabulate

# Simulation parameters
num_customers = 100

# Generate random interarrival times (uniform between 1 and 8)
interarrival_times = [random.uniform(1, 8) for _ in range(num_customers)]

# Generate random service times based on the given distribution
service_time_options = [1, 2, 3, 4, 5, 6]
service_time_probabilities = [0.10, 0.20, 0.30, 0.25, 0.10, 0.05]
random_service_times = [random.choices(service_time_options, service_time_probabilities)[
    0] for _ in range(num_customers)]

# Function to calculate the previous customer's service end time


def prev_service_end_time(customer_data, name):
    if name == 0:
        return 0
    else:
        return customer_data[name - 1][6]

# Function to calculate customer's arrival time


def calculate_arrival_times(interarrival_times):
    arrival_times = [0]
    for i in range(1, len(interarrival_times)):
        arrival_times.append(arrival_times[i - 1] + interarrival_times[i])
    return arrival_times

# Simulation function


def customer(env, name, arrival_time, service_time):
    yield env.timeout(arrival_time)

    prev_end_time = prev_service_end_time(data, name)
    service_start_time = max(arrival_time, prev_end_time)
    service_end_time = service_start_time + service_time

    waiting_time_in_queue = service_start_time - arrival_time

    data[name] = [
        name + 1,
        interarrival_times[name],
        arrival_time,
        service_time,
        service_start_time,
        waiting_time_in_queue,
        service_end_time,
        time_customer_spends[name],
        0  # Idle time of server, to be filled later
    ]


# Initialize simulation environment
env = simpy.Environment()

# Create array to store customer data
data = [[] for _ in range(num_customers)]

# Calculate arrival times using interarrival times
arrival_times = calculate_arrival_times(interarrival_times)

# Create and start customers
for i in range(num_customers):
    env.process(customer(env, i, arrival_times[i], random_service_times[i]))

# Run the simulation
env.run()

# Initialize time_customer_spends
time_customer_spends = [0] * num_customers

# Calculate time customer spends in the system
for i in range(num_customers):
    time_customer_spends[i] = data[i][6] - data[i][2]

# Calculate idle time of server
for i in range(num_customers):
    prev_end_time = prev_service_end_time(data, i)
    if i == 0 or arrival_times[i] > prev_end_time:
        data[i][8] = arrival_times[i] - prev_end_time

# Print output table
headers = ["Customer", "Interarrival time", "Arrival time", "Service time (min)",
           "Time service begins", "Waiting time in queue (min)",
           "Time service ends", "Time customer spends in system", "Idle time of server"]

print(tabulate(data, headers=headers, tablefmt="grid"))

# Plot histograms
plt.figure(figsize=(10, 6))

# Plot histogram for waiting time in queue
plt.subplot(2, 1, 1)
waiting_time_in_queue = [row[5] for row in data]
plt.hist(waiting_time_in_queue, bins=20, alpha=0.7,
         color='blue', label='Queue Time')
plt.axvline(x=sum(waiting_time_in_queue) / num_customers, color='blue',
            linestyle='dashed', linewidth=2, label='Average Queue Time')
plt.xlabel('Time')
plt.ylabel('Frequency')
plt.title('Histogram of Queue Time')
plt.legend()
plt.grid(True)

# Plot histogram for time customer spends in the system
plt.subplot(2, 1, 2)
plt.hist(time_customer_spends, bins=20, alpha=0.7,
         color='green', label='System Time')
plt.axvline(x=sum(time_customer_spends) / num_customers, color='green',
            linestyle='dashed', linewidth=2, label='Average System Time')
plt.xlabel('Time')
plt.ylabel('Frequency')
plt.title('Histogram of System Time')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

average_queue_time = sum(waiting_time_in_queue) / num_customers
average_system_time = sum(time_customer_spends) / num_customers
print(f"Average time customer spends in the queue: {average_queue_time:.2f}")
print(f"Average time customer spends in the system: {average_system_time:.2f}")
