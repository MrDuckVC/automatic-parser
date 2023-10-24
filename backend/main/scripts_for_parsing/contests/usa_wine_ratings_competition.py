import re

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from main.main_functions import ParsingScriptWithSelenium


class UsaWineRatingsCompetition(ParsingScriptWithSelenium):

    def surface_parse(self):
        super().surface_parse()
        self.activate_web_driver()
        self.web_driver.get(self.get_url())
        wine_block = self.web_driver.find_elements(By.CSS_SELECTOR, "#filterContainer > div > div")[0]

        wine = wine_block.find_elements(By.CSS_SELECTOR, "article")[0]
        points = wine.find_element(By.CSS_SELECTOR, "div.imgContainer").text
        image_of_medal = wine.find_element(By.CSS_SELECTOR, "div.imgContainer > img").get_attribute("src")
        if "GoldMedal" in image_of_medal:
            medal = "Gold"
        elif "SilverMedal" in image_of_medal:
            medal = "Silver"
        elif "BronzeMedal" in image_of_medal:
            medal = "Bronze"
        else:
            medal = ""
        name_of_wine = wine.find_element(By.CSS_SELECTOR, "div.txt > h1").text
        tab_of_info = wine.find_element(By.CSS_SELECTOR, "div.txt > ul").text
        try:
            winery = re.findall("Producer Name: (.+)", tab_of_info)[0]
        except IndexError:
            winery = ""
        country = re.findall("Country: (.+)", tab_of_info)[0]
        try:
            vintage = re.findall("Vintage: (.+)", tab_of_info)[0]
        except IndexError:
            vintage = ""
        category = re.findall("Category: (.+)", tab_of_info)[0]
        varietal = re.findall("Varietal: (.+)", tab_of_info)[0]
        result_dict = {"points": points, "medal": medal, "name_of_wine": name_of_wine, "winery": winery,
                       "country": country, "vintage": vintage, "category": category, "varietal": varietal}
        self.add_info_dict(result_dict)

        self.finish_parsing()

    def get_url(self):
        return "https://usawineratings.com/en/competition-global-results/2022/"

    def deep_parse(self):
        super().deep_parse()
        self.activate_web_driver()
        self.web_driver.get(self.get_url())
        wine_block = self.web_driver.find_element(By.CSS_SELECTOR, "#filterContainer > div > div")

        wines = wine_block.find_elements(By.CSS_SELECTOR, "article")[0:15]
        for wine in wines:
            points = wine.find_element(By.CSS_SELECTOR, "div.imgContainer").text
            image_of_medal = wine.find_element(By.CSS_SELECTOR, "div.imgContainer > img").get_attribute("src")
            if "GoldMedal" in image_of_medal:
                medal = "Gold"
            elif "SilverMedal" in image_of_medal:
                medal = "Silver"
            elif "BronzeMedal" in image_of_medal:
                medal = "Bronze"
            else:
                medal = ""
            name_of_wine = wine.find_element(By.CSS_SELECTOR, "div.txt > h1").text
            tab_of_info = wine.find_element(By.CSS_SELECTOR, "div.txt > ul").text
            try:
                winery = re.findall("Producer Name: (.+)", tab_of_info)[0]
            except IndexError:
                winery = ""
            country = re.findall("Country: (.+)", tab_of_info)[0]
            try:
                vintage = re.findall("Vintage: (.+)", tab_of_info)[0]
            except IndexError:
                vintage = ""
            category = re.findall("Category: (.+)", tab_of_info)[0]
            varietal = re.findall("Varietal: (.+)", tab_of_info)[0]
            result_dict = {"points": points, "medal": medal, "name_of_wine": name_of_wine, "winery": winery,
                           "country": country, "vintage": vintage, "category": category, "varietal": varietal}
            self.add_info_dict(result_dict)

        self.finish_parsing()

    def total_parse(self):
        super().total_parse()
        self.activate_web_driver()
        self.web_driver.get(self.get_url())
        wine_blocks = self.web_driver.find_elements(By.CSS_SELECTOR, "#filterContainer > div > div")

        for wine_block in wine_blocks:
            try:
                trophy = wine_block.find_element(By.CSS_SELECTOR, "h2").text
            except NoSuchElementException:
                trophy = ""
            wines = wine_block.find_elements(By.CSS_SELECTOR, "article")
            for wine in wines:
                points = wine.find_element(By.CSS_SELECTOR, "div.imgContainer").text
                image_of_medal = wine.find_element(By.CSS_SELECTOR, "div.imgContainer > img").get_attribute("src")
                if "GoldMedal" in image_of_medal:
                    medal = "Gold"
                elif "SilverMedal" in image_of_medal:
                    medal = "Silver"
                elif "BronzeMedal" in image_of_medal:
                    medal = "Bronze"
                else:
                    medal = ""
                name_of_wine = wine.find_element(By.CSS_SELECTOR, "div.txt > h1").text
                tab_of_info = wine.find_element(By.CSS_SELECTOR, "div.txt > ul").text
                try:
                    winery = re.findall("Producer Name: (.+)", tab_of_info)[0]
                except IndexError:
                    winery = ""
                country = re.findall("Country: (.+)", tab_of_info)[0]
                try:
                    vintage = re.findall("Vintage: (.+)", tab_of_info)[0]
                except IndexError:
                    vintage = ""
                category = re.findall("Category: (.+)", tab_of_info)[0]
                varietal = re.findall("Varietal: (.+)", tab_of_info)[0]
                if medal != "":
                    result_dict = {"points": points, "medal": medal, "name_of_wine": name_of_wine,
                                   "winery": winery, "country": country, "vintage": vintage, "category": category,
                                   "varietal": varietal, "trophy": None}
                    self.add_info_dict(result_dict)
                elif trophy != "Winery Of The Year":
                    self.add_params_for_dict(additional_info={"trophy": trophy},
                                             filters={"name_of_wine": name_of_wine, "winery": winery, "country": country,
                                                      "category": category, "varietal": varietal})

        self.finish_parsing()

    def check_new_parsing_result(self):
        super().check_new_parsing_result()
        self.activate_web_driver()
        self.web_driver.get(self.get_url())
        year_of_results = self.web_driver.find_elements(By.XPATH, "/html/body/div[1]/header/div[3]/div/div[1]/nav/ul/li[4]/ul/li")

        for year in year_of_results:
            if "2022" in year.text:
                self.add_info_dict({"new_results": True})
                self.finish_parsing()
                return

        self.add_info_dict({"new_results": False})
        self.finish_parsing()


def check_new_parsing_result():
    usa_wine_ratings_competition = UsaWineRatingsCompetition("usa_wine_ratings_competition")
    usa_wine_ratings_competition.check_new_parsing_result()
