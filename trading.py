import scenarios

if __name__ == "__main__":

    # amount = 7649335
    amount = 10**6

    # scenarios.save_balancerec(amount, plot_balance=False)
    # scenarios.balancerec_strat_cmp(amount)

    scenarios.grid_search_mas(amount, 10, 10)
