from main.scripts_for_parsing.contests.asia_wine_challenge import AsiaWineChallenge


class AsiaWineChallenge2021(AsiaWineChallenge):
    def get_contest_year(self):
        return 2021


def deep_parse():
    asia_wine_challenge2021 = AsiaWineChallenge2021("asia_wine_challenge2021")
    asia_wine_challenge2021.deep_parse()


def surface_parse():
    asia_wine_challenge2021 = AsiaWineChallenge2021("asia_wine_challenge2021")
    asia_wine_challenge2021.surface_parse()


def total_parse():
    asia_wine_challenge2021 = AsiaWineChallenge2021("asia_wine_challenge2021")
    asia_wine_challenge2021.total_parse()
