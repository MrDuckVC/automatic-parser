from main.scripts_for_parsing.contests.usa_wine_ratings_competition import UsaWineRatingsCompetition


class UsaWineRatingsCompetition2020(UsaWineRatingsCompetition):
    def get_url(self):
        return "https://usawineratings.com/en/competition-global-results/2020/"


def deep_parse():
    usa_wine_ratings_competition2020 = UsaWineRatingsCompetition2020("usa_wine_ratings_competition2020")
    usa_wine_ratings_competition2020.deep_parse()


def surface_parse():
    usa_wine_ratings_competition2020 = UsaWineRatingsCompetition2020("usa_wine_ratings_competition2020")
    usa_wine_ratings_competition2020.surface_parse()


def total_parse():
    usa_wine_ratings_competition2020 = UsaWineRatingsCompetition2020("usa_wine_ratings_competition2020")
    usa_wine_ratings_competition2020.total_parse()
