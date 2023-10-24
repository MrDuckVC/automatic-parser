from selenium.webdriver.common.by import By

from main.main_functions import ParsingScriptWithSelenium


class RoseRocks(ParsingScriptWithSelenium):
    def check_new_parsing_result(self):
        super().check_new_parsing_result()
        self.activate_web_driver()
        self.web_driver.get("https://www.roserocks.co.za/")
        year_of_results = self.web_driver.find_elements(By.XPATH, "/html/body/div[6]/div[2]/ul/li")
        for year in year_of_results:
            if "2022" in year.text:
                self.add_info_dict({"new_results": True})
                self.finish_parsing()
                return True

        self.add_info_dict({"new_results": False})
        self.finish_parsing()
        return False


def check_new_parsing_result():
    rose_rocks = RoseRocks("rose_rocks")
    rose_rocks.check_new_parsing_result()
