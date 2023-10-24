from main.scripts_for_parsing.contests.asia_wine_challenge import AsiaWineChallenge


class AsiaWineChallenge2020(AsiaWineChallenge):
    def get_contest_year(self):
        return 2020


def deep_parse():
    asia_wine_challenge2020 = AsiaWineChallenge2020("asia_wine_challenge2020")
    asia_wine_challenge2020.deep_parse()


def surface_parse():
    asia_wine_challenge2020 = AsiaWineChallenge2020("asia_wine_challenge2020")
    asia_wine_challenge2020.surface_parse()


def total_parse():
    asia_wine_challenge2020 = AsiaWineChallenge2020("asia_wine_challenge2020")
    asia_wine_challenge2020.total_parse()
