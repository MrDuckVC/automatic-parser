from main.scripts_for_parsing.contests.international_wine_contest_bucharest_vinarium import InternationalWineContestBucharestVinarium


class InternationalWineContestBucharestVinarium2021(InternationalWineContestBucharestVinarium):
    def get_contest_year(self):
        return 2021


def deep_parse():
    international_wine_contest_bucharest_vinarium2021 = InternationalWineContestBucharestVinarium2021("international_wine_contest_bucharest_vinarium2021")
    international_wine_contest_bucharest_vinarium2021.deep_parse()


def surface_parse():
    international_wine_contest_bucharest_vinarium2021 = InternationalWineContestBucharestVinarium2021("international_wine_contest_bucharest_vinarium2021")
    international_wine_contest_bucharest_vinarium2021.surface_parse()


def total_parse():
    international_wine_contest_bucharest_vinarium2021 = InternationalWineContestBucharestVinarium2021("international_wine_contest_bucharest_vinarium2021")
    international_wine_contest_bucharest_vinarium2021.total_parse()
