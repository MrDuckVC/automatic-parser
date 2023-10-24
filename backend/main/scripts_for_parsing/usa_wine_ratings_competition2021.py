from main.scripts_for_parsing.contests.usa_wine_ratings_competition import UsaWineRatingsCompetition


class UsaWineRatingsCompetition2021(UsaWineRatingsCompetition):
    def get_url(self):
        return "https://usawineratings.com/en/competition-global-results/2021/"


def deep_parse():
    usa_wine_ratings_competition2021 = UsaWineRatingsCompetition2021("usa_wine_ratings_competition2021")
    usa_wine_ratings_competition2021.deep_parse()


def surface_parse():
    usa_wine_ratings_competition2021 = UsaWineRatingsCompetition2021("usa_wine_ratings_competition2021")
    usa_wine_ratings_competition2021.surface_parse()


def total_parse():
    usa_wine_ratings_competition2021 = UsaWineRatingsCompetition2021("usa_wine_ratings_competition2021")
    usa_wine_ratings_competition2021.total_parse()
