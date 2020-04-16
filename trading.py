import scenarios

if __name__ == "__main__":

    amount = 10**5

    scenarios.save_balancerec(amount)
    # scenarios.balancerec_strat(amount)

    scenarios.balancerec_strat_cmp(amount)
