from selenium.webdriver.common.by import By
import selenium.common.exceptions

from main.main_functions import ParsingScriptWithSelenium


class AsiaWineChallenge(ParsingScriptWithSelenium):

    def get_contest_year(self):
        return 2022

    def surface_parse(self):
        super().surface_parse()
        self.activate_web_driver()

        self.web_driver.get(f"https://results.wine-trophy.com/en?sf=trophy_name:Asia%20Wine%20Trophy&sf=trophy_year:{self.get_contest_year()}&size=1")
        amount_of_wines = int(self.web_driver.find_elements(By.XPATH, "/html/body/div[4]/div/div[2]/div[2]/div[2]/div/div[2]/a")[-1].text)

        link = self.web_driver.find_element(By.CSS_SELECTOR, "div > div > div > div.col-md-1.wine-photo > a").get_attribute("href")
        self.web_driver.get(link)

        self.parse_wine()

        self.add_info_dict({"amount_of_wines": amount_of_wines})

        self.finish_parsing()

    def deep_parse(self):
        super().deep_parse()
        self.activate_web_driver()

        self.web_driver.get(f"https://results.wine-trophy.com/en?sf=trophy_name:Asia%20Wine%20Trophy&sf=trophy_year:{self.get_contest_year()}&size=10")
        wine_info_boxes = self.web_driver.find_elements(By.CSS_SELECTOR, "div > div > div > div.col-md-1.wine-photo > a")
        links = [link.get_attribute("href") for link in wine_info_boxes]

        for link in links:
            self.web_driver.get(link)
            self.parse_wine()

        self.finish_parsing()

    def total_parse(self):
        super().total_parse()
        self.activate_web_driver()
        self.web_driver.get(f"https://results.wine-trophy.com/en?sf=trophy_name:Asia%20Wine%20Trophy&sf=trophy_year:{self.get_contest_year()}&size=1")
        amount_of_wines = int(self.web_driver.find_elements(By.XPATH, "/html/body/div[4]/div/div[2]/div[2]/div[2]/div/div[2]/a")[-1].text)

        self.web_driver.get(f"https://results.wine-trophy.com/en?sf=trophy_name:Asia%20Wine%20Trophy&sf=trophy_year:{self.get_contest_year()}&size={amount_of_wines}")
        wine_info_boxes = self.web_driver.find_elements(By.CSS_SELECTOR, "div > div > div > div.col-md-1.wine-photo > a")
        links = [link.get_attribute("href") for link in wine_info_boxes]

        for link in links:
            self.web_driver.get(link)
            self.parse_wine()

        self.finish_parsing()
    
    def parse_wine(self):
        name_of_wine = self.web_driver.find_element(By.CSS_SELECTOR, "div.col-md-8.wine-description-panel > h1").text
        medal = self.web_driver.find_element(By.CSS_SELECTOR, "div:nth-child(4) > div.col-md-8.wine-decription-value").text
        vintage = self.web_driver.find_element(By.CSS_SELECTOR, "div:nth-child(6) > div.col-md-8.wine-decription-value").text
        winery = self.web_driver.find_element(By.CSS_SELECTOR, "div:nth-child(7) > div.col-md-8.wine-decription-value").text
        country = self.web_driver.find_element(By.CSS_SELECTOR, "div:nth-child(9) > div.col-md-8.wine-decription-value").text
        region = self.web_driver.find_element(By.CSS_SELECTOR, "div:nth-child(10) > div.col-md-8.wine-decription-value").text
        category = self.web_driver.find_element(By.CSS_SELECTOR, "div:nth-child(12) > div.col-md-8.wine-decription-value").text
        flavour = self.web_driver.find_element(By.CSS_SELECTOR, "div:nth-child(13) > div.col-md-8.wine-decription-value").text
        vinification = self.web_driver.find_element(By.CSS_SELECTOR, "div:nth-child(14) > div.col-md-8.wine-decription-value").text
        type_of_wine = self.web_driver.find_element(By.CSS_SELECTOR, "div:nth-child(15) > div.col-md-8.wine-decription-value").text
        type_of_grape = self.web_driver.find_element(By.CSS_SELECTOR, "div:nth-child(16) > div.col-md-8.wine-decription-value > div").text
        alcohol_content = self.web_driver.find_element(By.CSS_SELECTOR, "div:nth-child(18) > div.col-md-8.wine-decription-value").text
        acidity = self.web_driver.find_element(By.CSS_SELECTOR, "div:nth-child(19) > div.col-md-8.wine-decription-value").text
        residual_sugar = self.web_driver.find_element(By.CSS_SELECTOR, "div:nth-child(20) > div.col-md-8.wine-decription-value").text
        total_sulfur = self.web_driver.find_element(By.CSS_SELECTOR, "div:nth-child(21) > div.col-md-8.wine-decription-value").text
        bio = self.web_driver.find_element(By.CSS_SELECTOR, "div:nth-child(22) > div.col-md-8.wine-decription-value").text
        image_of_wine = self.web_driver.find_element(By.CSS_SELECTOR, "#wine-photo > img").get_attribute("src")

        self.add_info_dict({
            "name_of_wine": name_of_wine, "medal": medal, "vintage": vintage, "winery": winery, "country": country,
            "region": region, "category": category, "flavour": flavour, "vinification": vinification, "type_of_wine": type_of_wine,
            "type_of_grape": type_of_grape, "alcohol_content(%)": alcohol_content, "acidity(g/l)": acidity,
            "residual_sugar(g/l)": residual_sugar, "total_sulfur(mg/l)": total_sulfur, "bio": bio, "image_of_wine": image_of_wine,
        })

    def check_new_parsing_result(self):
        super().check_new_parsing_result()
        self.activate_web_driver()
        self.web_driver.get(f"https://results.wine-trophy.com/en?sf=trophy_name:Asia%20Wine%20Trophy&sf=trophy_year:{self.get_contest_year()}&size=1")

        try:
            self.web_driver.find_element(By.XPATH, "/html/body/div[4]/div/div[2]/div[2]/div[2]/table/tbody/tr[2]/td/div/p")
            self.add_info_dict({"new_results": False})
        except selenium.common.exceptions.NoSuchElementException:
            self.add_info_dict({"new_results": True})

        self.finish_parsing()


def check_new_parsing_result():
    asia_wine_challenge = AsiaWineChallenge("asia_wine_challenge")
    asia_wine_challenge.check_new_parsing_result()
