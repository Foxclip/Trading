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
    simulation.save_mas(templates.ma, pairs_list, plot_balance=plot_balance)
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
