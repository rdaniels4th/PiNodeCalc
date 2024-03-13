import datetime
import numpy as np
import matplotlib.pyplot as plt

# Example usage
days_operational = 1 # 1 day operational
Y = 1.0  # 100% uptime yesterday
avg_CPU_cores = 32  # Available CPU cores
avg_ports_open = 1.0  # Assuming 100% of the ports open

# Hourly Pi Base Rate = 0.0073 Pi per hour (as of 2022-03-12)
# Having will take effect on every March 14
Base_Rate_23_24 = 0.0073
Base_Rate_24_25 = Base_Rate_23_24 / 2
Base_Rate_25_26 = Base_Rate_24_25 / 2
Base_Rate_26_27 = Base_Rate_25_26 / 2
Base_Rate_27_28 = Base_Rate_26_27 / 2

# Pi value per coin (Assuming Pi value at $104 as of 2022-03-12)
pi_value_per_coin = 104 # USD

# Boosters
Pioneer_Booster = 1
Num_Security_Circle = 5
Num_Security_Circle_Booster = 20
Security_Circle_Boost = Num_Security_Circle * Num_Security_Circle_Booster
Lockup_Reward = 386.46

# Rewards
Pioneer = 1
Referral_Team = 0
Utility_Usage_Bonus = 0

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

# Calculate the node factor based on operational days
node_factor = calculate_node_factor_based_on_days(days_operational, Y, avg_CPU_cores, avg_ports_open)
print("Final Calculations...")

Rewards = Pioneer + Referral_Team + Utility_Usage_Bonus + node_factor
print(f"Rewards: {Rewards}")

# Total Boosters
Boosters_Total_Percent = Pioneer_Booster + Security_Circle_Boost + Lockup_Reward
Boosters_Total_Factor = Boosters_Total_Percent / 100
print(f"Boosters Total Factor: {Boosters_Total_Factor}")

# Total Rewards
Hourly_minning_rate = Base_Rate_23_24 * Rewards * Boosters_Total_Factor
print(f"Hourly Minning Rate: {Hourly_minning_rate}")


# Calculate base rate based on year
def get_base_rate_by_year(year):
    if year == 2024:
        return Base_Rate_23_24
    elif year == 2025:
        return Base_Rate_24_25
    elif year == 2026:
        return Base_Rate_25_26
    elif year == 2027:
        return Base_Rate_26_27
    elif year == 2028:
        return Base_Rate_27_28
    elif year == 2029:
        return Base_Rate_27_28 / 2
    elif year == 2030:
        return Base_Rate_27_28 / 4
    elif year == 2031:
        return Base_Rate_27_28 / 8
    elif year == 2032:
        return Base_Rate_27_28 / 16
    elif year == 2033:
        return Base_Rate_27_28 / 32
    else:
        return 0

# Simulate daily earnings over a year considering halving
start_date = datetime.date(2024, 3, 12)
days_in_year = [start_date + datetime.timedelta(days=x) for x in range(365 * 10)]
daily_earnings = []

for day in days_in_year:
    base_rate = get_base_rate_by_year(day.year)
    hourly_mining_rate = base_rate * Rewards * Boosters_Total_Factor
    daily_earning = hourly_mining_rate * 24 * pi_value_per_coin
    daily_earnings.append(daily_earning)

# Calculate cumulative earnings
cumulative_earnings = np.cumsum(daily_earnings)

# Plotting
plt.figure(figsize=(12, 6))
plt.plot(days_in_year, cumulative_earnings, label='Cumulative Earnings', color='blue')
plt.xlabel('Date')
plt.ylabel('Cumulative Earnings ($)')
plt.title('Cumulative Earnings Considering Halving Periods')
plt.xticks(rotation=45)
plt.tight_layout()
plt.legend()
plt.show()
