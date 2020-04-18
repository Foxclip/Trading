import simulation
import templates


def startup(skip, amount, filename):
    simulation.init()
    simulation.global_settings.precision = 5
    simulation.global_settings.skip = skip
    simulation.global_settings.amount = amount
    simulation.load_file(filename)


def smallfile(amount):
    skip = 1000000 - amount
    startup(skip, amount, "EURUSD_i_M1_201706131104_202002240839.csv")


def bigfile(amount):
    skip = 7649335 - amount
    startup(skip, amount, "EURUSD_M1_199901041022_202004171116.csv")


def simple_ma(amount):
    bigfile(amount)
    simulation.sim_list([templates.ma])
    print()


def grid_search_mas(amount, count1, count2):

    bigfile(amount)
    main_template = templates.ma

    def create_sim(ma1, ma2):
        template = main_template.copy()
        template["name"] = f"{ma1} {ma2}"
        template["ma1"] = ma1
        template["ma2"] = ma2
        simulation.add_from_template(template)

    simulation.grid_search(
        create_sim,
        [list(range(1, count1 + 1)), list(range(1, count2 + 1))],
        "ma1", "ma2",
        sorted_count=10
    )


def balancerec_strat(amount):
    bigfile(amount)
    simulation.sim_list([templates.balancerec])
    print()


def save_balancerec(amount, plot_balance=False):
    bigfile(amount)
    pairs_list = [
        [1, 10],
        [9, 10],
        [15, 30],
        [17, 37],
        [4, 8],
    ]
    main_template = templates.ma
    template_list = []
    for pair in pairs_list:
        template = main_template.copy()
        template["ma1"] = pair[0]
        template["ma2"] = pair[1]
        template["name"] = f"ma {pair[0]} {pair[1]}"
        template_list.append(template)
        template = main_template.copy()
        template["ma1"] = pair[1]
        template["ma2"] = pair[0]
        template["name"] = f"ma {pair[1]} {pair[0]}"
        template_list.append(template)
    plotting = ["balance"] if plot_balance else []
    simulation.sim_list(template_list, save_filename="balance.txt",
                        plotting=plotting)
    print()


def balancerec_strat_cmp(amount):
    bigfile(amount)
    template = templates.balancerec
    brlens = [i * 1000 for i in range(5, 21)]
    template_list = []
    for brlen in brlens:
        template = template.copy()
        template["brlen"] = brlen
        template["name"] = f"{brlen}"
        template_list.append(template)
    simulation.sim_list(template_list)
    print()
