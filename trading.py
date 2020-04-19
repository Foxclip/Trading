import scenarios

if __name__ == "__main__":

    # amount = 7649335
    amount = 10**5

    # scenarios.save_balancerec(amount, plot_balance=True, diff=True)
    scenarios.save_balancerec_grid(amount)
    # scenarios.balancerec_strat_cmp(amount, plot_balance=True, diff=True)
    # scenarios.balancerec_strat_time(amount, plot_balance=True, diff=True)

    # scenarios.grid_search_mas(amount, 10, 10)
