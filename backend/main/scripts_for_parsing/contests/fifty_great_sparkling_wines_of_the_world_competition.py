from selenium.webdriver.common.by import By
import selenium.common.exceptions

from main.main_functions import ParsingScriptWithSelenium


class FiftyGreatSparklingWinesOfTheWorldCompetition(ParsingScriptWithSelenium):
    def get_contest_year(self):
        return 2022
    
    def surface_parse(self):
        super().surface_parse()
        self.activate_web_driver()
        self.web_driver.get(f"https://www.winepleasures.com/contest/50-great-sparkling-wines-of-the-world-{self.get_contest_year()}/")

        wines = self.web_driver.find_elements_by_css_selector("td.wine-contest-table > a")
        link = wines[0].get_attribute("href")

        self.web_driver.get(link)
        self.parse_wine()

        amount_of_wine = len(wines)
        self.add_info_dict({"amount_of_wine": amount_of_wine})

        self.finish_parsing()

    def deep_parse(self):
        super().deep_parse()
        self.activate_web_driver()
        self.web_driver.get(f"https://www.winepleasures.com/contest/50-great-sparkling-wines-of-the-world-{self.get_contest_year()}/")

        wines = self.web_driver.find_elements_by_css_selector("td.wine-contest-table > a")[0:10]
        links = [wine.get_attribute("href") for wine in wines]

        for link in links:
            self.web_driver.get(link)
            self.parse_wine()

        self.finish_parsing()

    def total_parse(self):
        super().total_parse()
        self.activate_web_driver()
        self.web_driver.get(f"https://www.winepleasures.com/contest/50-great-sparkling-wines-of-the-world-{self.get_contest_year()}/")

        wines = self.web_driver.find_elements_by_css_selector("td.wine-contest-table > a")
        links = [wine.get_attribute("href") for wine in wines]

        for link in links:
            self.web_driver.get(link)
            self.parse_wine()

        self.finish_parsing()

    def parse_wine(self):
        wine_name = self.web_driver.find_element_by_css_selector("div > h1").text
        country = self.web_driver.find_element_by_css_selector("div > div > div > div > strong:nth-child(1)").text
        region = self.web_driver.find_element_by_css_selector("div > div > div > div > strong:nth-child(2)").text
        vintage = self.web_driver.find_element_by_css_selector("tr:nth-child(1) > td.data").text
        ageing = self.web_driver.find_element_by_css_selector("tr:nth-child(2) > td.data").text
        prize = self.web_driver.find_element_by_css_selector("tr:nth-child(3) > td.data").text
        category = self.web_driver.find_element_by_css_selector("tr:nth-child(4) > td.data").text
        process = self.web_driver.find_element_by_css_selector("tr:nth-child(5) > td.data").text
        score = self.web_driver.find_element_by_css_selector("span.score-number").text
        medal = self.web_driver.find_element_by_css_selector("div > span.score-award").text
        company_name = self.web_driver.find_element_by_css_selector("div > h2").text
        try:
            wine_image = self.web_driver.find_element_by_css_selector("div > span > img").get_attribute("src")
        except selenium.common.exceptions.NoSuchElementException:
            wine_image = ""

        self.add_info_dict({
            "company_name": company_name, "country": country, "region": region, "vintage": vintage, "ageing": ageing,
            "prize": prize, "category": category, "process": process, "score": score, "medal": medal, "wine_name": wine_name,
            "wine_image": wine_image
        })

    def check_new_parsing_result(self):
        super().check_new_parsing_result()
        self.activate_web_driver()
        self.web_driver.get(f"https://www.winepleasures.com/contest/50-great-sparkling-wines-of-the-world-{self.get_contest_year()}/")

        try:
            self.web_driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div/div/div/div[1]/article/div/h1")
            self.add_info_dict({"new_results": False})
        except selenium.common.exceptions.NoSuchElementException:
            self.add_info_dict({"new_results": True})

        self.finish_parsing()


def check_new_parsing_result():
    fifty_great_sparkling_wines_of_the_world_competition = FiftyGreatSparklingWinesOfTheWorldCompetition("fifty_great_sparkling_wines_of_the_world_competition")
    fifty_great_sparkling_wines_of_the_world_competition.check_new_parsing_result()
