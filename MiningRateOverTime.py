def calculate_node_factor_based_on_days(days_operational, Y, avg_CPU_cores, avg_ports_open):
    """
    Calculate the node factor (F) dynamically based on the number of operational days,
    yesterday's uptime (Y), average CPU cores, and average ports open.

    Args:
        days_operational (int): Number of days the node has been operational.
        Y (float): Yesterday's uptime as a decimal (e.g., 0.95 for 95%).
        avg_CPU_cores (int): Average number of CPU cores during operational period.
        avg_ports_open (float): Average percentage of ports open during operational period.

    Returns:
        float: The dynamically calculated node factor.
    """
    # Adjust uptime and port open factors for operational days
    U_90 = days_operational / 90 if days_operational < 90 else 1
    U_360 = days_operational / 360 if days_operational < 360 else 1
    U_2_years = days_operational / (2 * 365) if days_operational < 2 * 365 else 1
    U_10_years = days_operational / (10 * 365) if days_operational < 10 * 365 else 1

    # Adjust port open factors for operational days
    P_90 = avg_ports_open * (days_operational / 90 if days_operational < 90 else 1)
    P_360 = avg_ports_open * (days_operational / 360 if days_operational < 360 else 1)
    P_2_years = avg_ports_open * (days_operational / (2 * 365) if days_operational < 2 * 365 else 1)
    P_10_years = avg_ports_open * (days_operational / (10 * 365) if days_operational < 10 * 365 else 1)

    C_90 = avg_CPU_cores * (days_operational / 90 if days_operational < 90 else 1)
    C_360 = avg_CPU_cores * (days_operational / 360 if days_operational < 360 else 1)
    C_2_years = avg_CPU_cores * (days_operational / (2 * 365) if days_operational < 2 * 365 else 1)
    C_10_years = avg_CPU_cores * (days_operational / (10 * 365) if days_operational < 10 * 365 else 1)

    # Calculate the dynamic factors
    U = U_90 + 1.5*U_360 + 2*U_2_years + 3*U_10_years
    P = 1 + P_90 + 1.5*P_360 + 2*P_2_years + 3*P_10_years
    C = (1 + C_90 + 1.5*C_360 + 2*C_2_years + 3*C_10_years) / 4

    print(f"U: {U}, P: {P}, C: {C}")

    # Calculate node factor F
    F = Y * U * P * C

    return F

# Adjusting the initial setup to ensure days_operational changes with the years and correctly calculating node factor

import datetime
import numpy as np
import matplotlib.pyplot as plt

# Setup for halving and initial values
base_rate_annual_changes = {
    2024: 0.0073,
    2025: 0.0073 / 2,  # Halving every March 14th
    2026: 0.0073 / 4,
    2027: 0.0073 / 8,
    2028: 0.0073 / 16,
    2029: 0.0073 / 32,
    2030: 0.0073 / 64
}

pi_value_per_coin = 104  # USD
pioneer_booster = 1
num_security_circle = 5
num_security_circle_booster = 20
security_circle_boost = num_security_circle * num_security_circle_booster
lockup_reward = 386.46
boosters_total_factor = (pioneer_booster + security_circle_boost + lockup_reward) / 100
y = 1.0  # 100% uptime
avg_cpu_cores = 32
avg_ports_open = 1.0

# Function to calculate days operational based on the date
def days_since_start(start_date, current_date):
    return (current_date - start_date).days + 1

# Start and end dates for the simulation
start_date = datetime.date(2024, 3, 12)
end_date = datetime.date(2030, 3, 11)

# Generate dates for simulation
dates = [start_date + datetime.timedelta(days=x) for x in range((end_date - start_date).days + 1)]

# Calculate node factor and effective mining rate over time
node_factors = []
hourly_mining_rates = []
for current_date in dates:
    days_operational = days_since_start(start_date, current_date)
    node_factor = calculate_node_factor_based_on_days(days_operational, y, avg_cpu_cores, avg_ports_open)  # Assuming a constant node factor for simplicity
    base_rate = base_rate_annual_changes.get(current_date.year, list(base_rate_annual_changes.values())[-1])
    effective_rate = base_rate * node_factor * boosters_total_factor
    node_factors.append(node_factor)
    hourly_mining_rates.append(effective_rate)

# Plotting the effective hourly mining rate over time
plt.figure(figsize=(14, 7))
plt.plot(dates, hourly_mining_rates, label='Hourly Mining Rate')
plt.title('Effective Hourly Mining Rate Over Time with Dynamic Node Factor')
plt.xlabel('Date')
plt.ylabel('Rate (Pi/hour)')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

