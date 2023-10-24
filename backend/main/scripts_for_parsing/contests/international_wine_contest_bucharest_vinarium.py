from selenium.webdriver.common.by import By

from main.main_functions import ParsingScriptWithSelenium


class InternationalWineContestBucharestVinarium(ParsingScriptWithSelenium):

    def get_contest_year(self):
        return 2022

    def surface_parse(self):
        super().surface_parse()
        self.activate_web_driver()
        self.web_driver.get(f"https://www.iwcb.ro/registration/results.php?sort_by=&sort_order=&edition={self.get_contest_year()}&country=All&category=All&medal=All&producer_importer=&commercial_brand=")

        wines = self.web_driver.find_elements(By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div/div/article/div/div[4]/div/table/tbody/tr")
        wines.pop(0)
        self.parse_wine(wines[0])

        self.add_info_dict({"amount_of_wine": len(wines)})

        self.finish_parsing()

    def deep_parse(self):
        super().deep_parse()
        self.activate_web_driver()
        self.web_driver.get(f"https://www.iwcb.ro/registration/results.php?sort_by=&sort_order=&edition={self.get_contest_year()}&country=All&category=All&medal=All&producer_importer=&commercial_brand=")

        wines = self.web_driver.find_elements(By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div/div/article/div/div[4]/div/table/tbody/tr")
        wines.pop(0)
        for i in range(10):
            self.parse_wine(wines[i])

        self.finish_parsing()

    def total_parse(self):
        super().total_parse()
        self.activate_web_driver()
        self.web_driver.get(f"https://www.iwcb.ro/registration/results.php?sort_by=&sort_order=&edition={self.get_contest_year()}&country=All&category=All&medal=All&producer_importer=&commercial_brand=")

        wines = self.web_driver.find_elements(By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div/div/article/div/div[4]/div/table/tbody/tr")
        wines.pop(0)
        for wine in wines:
            self.parse_wine(wine)

        self.finish_parsing()

    def parse_wine(self, wine):
        wine_name = wine.find_element(By.XPATH, "td[2]").text
        varietal = wine.find_element(By.XPATH, "td[3]").text
        vintage = wine.find_element(By.XPATH, "td[4]").text
        country = wine.find_element(By.XPATH, "td[5]").text
        winery = wine.find_element(By.XPATH, "td[6]").text
        medal_img = wine.find_element(By.XPATH, "td[7]/img").get_attribute("src")
        if "_au.png" in medal_img:
            medal = "Gold"
        else:
            medal = "Silver"
        
        self.add_info_dict({"wine_name": wine_name, "varietal": varietal, "vintage": vintage, "country": country, "winery": winery, "medal": medal})

    def check_new_parsing_result(self):
        super().check_new_parsing_result()
        self.activate_web_driver()
        self.web_driver.get(f"https://www.iwcb.ro/registration/results.php?sort_by=&sort_order=&edition={self.get_contest_year()}&country=All&category=All&medal=All&producer_importer=&commercial_brand=")

        if self.web_driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div/div/article/div/div[1]/p").text == "Alert: No match for your selection":
            self.add_info_dict({"new_results": False})
        else:
            self.add_info_dict({"new_results": True})

        self.finish_parsing()


def check_new_parsing_result():
    international_wine_contest_bucharest_vinarium = InternationalWineContestBucharestVinarium("international_wine_contest_bucharest_vinarium")
    international_wine_contest_bucharest_vinarium.check_new_parsing_result()
