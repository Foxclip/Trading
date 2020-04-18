import scenarios

if __name__ == "__main__":

    # amount = 7649335
    amount = 10**5

    scenarios.save_balancerec(amount, plot_balance=False)
    # scenarios.balancerec_strat(amount)

    scenarios.balancerec_strat_cmp(amount)

    # scenarios.simple_ma(amount)
