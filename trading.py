import scenarios
import time

if __name__ == "__main__":

    time1 = time.time()

    amount = 10**6

    # scenarios.save_balancerec(amount, plot_balance=True)
    # scenarios.balancerec_strat(amount)

    # scenarios.balancerec_strat_cmp(amount)

    scenarios.simple_ma(amount)
