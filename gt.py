import numpy as np
B_high = 10  
B_low = 5    
C_high = 6  
C_low = 3   
beta_H = 1   
beta_L = 1.5 
P_L_max = 6  
p = 0.2      
# Price range
P_values = np.linspace(0, 10, 101)  # Prices from 0 to 10

def unregulated_scenario():
    profits = []
    for q, B_q, C_q in [('Low', B_low, C_low), ('High', B_high, C_high)]:
        for P in P_values:
            # High-income patient decision
            U_H = B_q - beta_H * P
            accept_H = U_H >= 0

            # Low-income patient decision
            U_L = B_q - beta_L * P
            accept_L = U_L >= 0 and P <= P_L_max

            # Expected profit
            profit = (p * accept_H + (1 - p) * accept_L) * (P - C_q)

            profits.append({
                'Quality': q,
                'Price': P,
                'Profit': profit,
                'Accept_H': accept_H,
                'Accept_L': accept_L
            })

    max_profit = max(profits, key=lambda x: x['Profit'])
    return max_profit

def regulated_scenario():
    profits = []
    # Regulation: Minimum quality level is High
    q = 'High'
    B_q = B_high
    C_q = C_high

    # Government provides subsidy S to low-income patients
    S = 4  # Subsidy amount

    for P in P_values:
        # High-income patient decision
        U_H = B_q - beta_H * P
        accept_H = U_H >= 0

        # Low-income patient decision with subsidy
        net_price_L = P - S
        U_L = B_q - beta_L * net_price_L
        accept_L = U_L >= 0 and net_price_L <= P_L_max

        # Expected profit
        profit = (p * accept_H + (1 - p) * accept_L) * (P - C_q)

        profits.append({
            'Quality': q,
            'Price': P,
            'Profit': profit,
            'Accept_H': accept_H,
            'Accept_L': accept_L
        })

    # Find the maximum profit
    max_profit = max(profits, key=lambda x: x['Profit'])
    return max_profit

# Compute equilibria
unregulated_result = unregulated_scenario()
regulated_result = regulated_scenario()

# Display results
print("Unregulated Scenario:")
print(f"Quality Level: {unregulated_result['Quality']}")
print(f"Price: {unregulated_result['Price']}")
print(f"Maximum Profit: {unregulated_result['Profit']}")
print(f"High-Income Patient Accepts: {unregulated_result['Accept_H']}")
print(f"Low-Income Patient Accepts: {unregulated_result['Accept_L']}")

print("\nRegulated Scenario:")
print(f"Quality Level: {regulated_result['Quality']}")
print(f"Price: {regulated_result['Price']}")
print(f"Maximum Profit: {regulated_result['Profit']}")
print(f"High-Income Patient Accepts: {regulated_result['Accept_H']}")
print(f"Low-Income Patient Accepts: {regulated_result['Accept_L']}")
