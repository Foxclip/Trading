import simulation

if __name__ == "__main__":

    simulation.init()

    # settings
    simulation.global_settings.precision = 5
    simulation.global_settings.amount = 10**5

    # loading file
    simulation.load_file("EURUSD_i_M1_201706131104_202002240839.csv")

    # creating simulations
    import templates
    main_template = templates.balance_records

    simulation.sim_list([main_template])

    # pairs_list = [
    #     [1, 10],
    #     [9, 10],
    #     [15, 30],
    #     [17, 37],
    #     [4, 8],
    # ]
    # simulation.save_mas(main_template, pairs_list)

    # simulation.grid_search_mas(main_template, 10, 10)
