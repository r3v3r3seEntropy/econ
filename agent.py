import random
import matplotlib.pyplot as plt

class Actor:
    def __init__(self, actor_id, money, employer_index=0):
        self.id = actor_id
        self.money = money  # Non-negative endowment of paper money
        self.ei = employer_index  # Employer index
        self.employees = set()  # Set of employee IDs

def initialize_economy(N, M):
    actors = {}
    initial_money = M / N
    for i in range(1, N + 1):
        actors[i] = Actor(actor_id=i, money=initial_money)
    return actors

def get_class_sets(actors):
    C = set()  # Capitalists
    W = set()  # Workers
    U = set()  # Unemployed

    for actor in actors.values():
        if actor.employees and actor.ei == 0:
            C.add(actor.id)
        elif not actor.employees and actor.ei != 0:
            W.add(actor.id)
        elif not actor.employees and actor.ei == 0:
            U.add(actor.id)
    return C, W, U

def actor_selection_rule_S1(actors):
    return random.choice(list(actors.values()))

def hiring_rule_H1(a, actors, hwi):
    if a.ei == 0:  # If actor a is unemployed
        # Form the set of potential employers (C ∪ U)
        H = [actor for actor in actors.values() if actor.ei == 0 and actor.id != a.id]
        if not H:
            return
        # Weigh potential employers by their wealth
        total_money = sum([h.money for h in H])
        if total_money == 0:
            return
        probabilities = [h.money / total_money for h in H]
        c = random.choices(H, weights=probabilities, k=1)[0]
        if c.money > hwi:
            # c hires a
            a.ei = c.id
            c.employees.add(a.id)

def expenditure_rule_E1(a, actors, V):
    other_actors = [actor for actor in actors.values() if actor.id != a.id]
    if not other_actors:
        return V
    b = random.choice(other_actors)
    if b.money > 0:
        m = random.uniform(0, b.money)
        b.money -= m
        V += m
    return V

def market_sample_rule_M1(a, actors, V):
    if a.ei != 0 or a.employees:
        if V > 0:
            m = random.uniform(0, V)
            V -= m
            if a.ei != 0 and not a.employees:
                employer = actors[a.ei]
                employer.money += m
            elif a.employees:
                a.money += m
    return V

def firing_rule_F1(a, actors, hwi):
    if a.employees:
        u = max(len(a.employees) - int(a.money / hwi), 0)
        if u > 0:
            employees_to_fire = random.sample(list(a.employees), u)
            for emp_id in employees_to_fire:
                emp = actors[emp_id]
                emp.ei = 0  # Set employee as unemployed
                a.employees.remove(emp_id)
    return

def wage_payment_rule_W1(a, actors, wa, wb):
    if a.employees:
        for emp_id in a.employees.copy():
            w = random.uniform(wa, wb)
            if a.money >= w:
                a.money -= w
                actors[emp_id].money += w
            else:
                w = random.uniform(0, a.money)
                a.money -= w
                actors[emp_id].money += w

def simulation_rule_SR1(actors, V, wa, wb, hwi):
    a = actor_selection_rule_S1(actors)
    hiring_rule_H1(a, actors, hwi)
    V = expenditure_rule_E1(a, actors, V)
    V = market_sample_rule_M1(a, actors, V)
    firing_rule_F1(a, actors, hwi)
    wage_payment_rule_W1(a, actors, wa, wb)
    return V

def one_month_rule(actors, V, wa, wb, hwi):
    N = len(actors)
    for _ in range(N):
        V = simulation_rule_SR1(actors, V, wa, wb, hwi)
    return V

def one_year_rule(actors, V, wa, wb, hwi):
    for _ in range(12):
        V = one_month_rule(actors, V, wa, wb, hwi)
    return V

def collect_statistics(actors):
    C, W, U = get_class_sets(actors)
    total_money = sum([actor.money for actor in actors.values()])
    class_counts = {
        'Capitalists': len(C),
        'Workers': len(W),
        'Unemployed': len(U)
    }
    wealth_distribution = [actor.money for actor in actors.values()]
    return class_counts, wealth_distribution, total_money

def calculate_gini(wealth_distribution):
    sorted_wealth = sorted(wealth_distribution)
    n = len(sorted_wealth)
    cumulative_wealth = [0]
    for wealth in sorted_wealth:
        cumulative_wealth.append(cumulative_wealth[-1] + wealth)
    B = sum(cumulative_wealth) / (n * cumulative_wealth[-1])
    Gini = (n + 1 - 2 * B) / n
    return Gini

def plot_results(class_counts_over_time, gini_coefficients, num_years):
    years = list(range(1, num_years + 1))

    # Plot class counts over time
    capitalists = [counts['Capitalists'] for counts in class_counts_over_time]
    workers = [counts['Workers'] for counts in class_counts_over_time]
    unemployed = [counts['Unemployed'] for counts in class_counts_over_time]

    plt.figure(figsize=(12, 6))
    plt.plot(years, capitalists, label='Capitalists')
    plt.plot(years, workers, label='Workers')
    plt.plot(years, unemployed, label='Unemployed')
    plt.xlabel('Year')
    plt.ylabel('Number of Actors')
    plt.title('Class Counts Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Plot Gini coefficient over time
    plt.figure(figsize=(12, 6))
    plt.plot(years, gini_coefficients, marker='o')
    plt.xlabel('Year')
    plt.ylabel('Gini Coefficient')
    plt.title('Gini Coefficient Over Time')
    plt.grid(True)
    plt.show()

def main():
    # Parameters
    N = 100  # Number of actors
    M = 10000  # Total money supply
    wa = 10  # Minimum wage
    wb = 20  # Maximum wage
    hwi = (wa + wb) / 2  # Average wage
    V = 0  # Initial available market value
    num_years = 20  # Simulation duration

    # Initialize economy
    actors = initialize_economy(N, M)

    # Data collection
    class_counts_over_time = []
    gini_coefficients = []

    for year in range(num_years):
        V = one_year_rule(actors, V, wa, wb, hwi)
        class_counts, wealth_distribution, total_money = collect_statistics(actors)
        gini = calculate_gini(wealth_distribution)
        class_counts_over_time.append(class_counts)
        gini_coefficients.append(gini)

        print(f"Year {year + 1}:")
        print(f"  Class Counts: {class_counts}")
        print(f"  Total Money: {total_money:.2f}")
        print(f"  Gini Coefficient: {gini:.4f}")

    # Plot results
    plot_results(class_counts_over_time, gini_coefficients, num_years)

if __name__ == '__main__':
    main()
