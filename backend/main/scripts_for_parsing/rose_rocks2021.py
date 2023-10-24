import re

from main.scripts_for_parsing.contests.rose_rocks import RoseRocks


class RoseRocks2021(RoseRocks):
    def total_parse(self):
        super().total_parse()
        self.activate_web_driver()
        self.web_driver.get("https://www.roserocks.co.za/2021-results.html")
        tab = self.web_driver.find_element_by_css_selector("#wsite-content > div:nth-child(3)").text.split("\n")
        medal = ""
        for row in tab:
            if "Winners" in row:
                medal = row
            else:
                vintage = str(re.findall(r"\d{2}", row)).replace("[", "").replace("]", "").replace("'", "")
                name_of_wine = row.replace(f" {vintage}", "").replace(" NV", "")
                if len(vintage) > 0:
                    vintage = "20" + vintage
                if name_of_wine != "" and vintage != "":
                    self.add_info_dict({"name_of_wine": name_of_wine, "vintage": vintage, "medal": medal})

        self.finish_parsing()

    def deep_parse(self):
        super().deep_parse()
        self.activate_web_driver()
        self.web_driver.get("https://www.roserocks.co.za/2021-results.html")
        tab = self.web_driver.find_element_by_css_selector("#wsite-content > div:nth-child(3)").text.split("\n")[0:10]
        medal = ""
        for row in tab:
            if "Winners" in row:
                medal = row
            else:
                vintage = str(re.findall(r"\d{2}", row)).replace("[", "").replace("]", "").replace("'", "")
                name_of_wine = row.replace(f" {vintage}", "").replace(" NV", "")
                if len(vintage) > 0:
                    vintage = "20" + vintage
                if name_of_wine != "" and vintage != "":
                    self.add_info_dict({"name_of_wine": name_of_wine, "vintage": vintage, "medal": medal})

        self.finish_parsing()

    def surface_parse(self):
        super().surface_parse()
        self.activate_web_driver()
        self.web_driver.get("https://www.roserocks.co.za/2021-results.html")
        tab = self.web_driver.find_element_by_css_selector("#wsite-content > div:nth-child(3)").text.split("\n")
        amount_of_wines = len(tab)
        wine = tab[4]
        vintage = str(re.findall(r"\d{2}", wine)).replace("[", "").replace("]", "").replace("'", "")
        name_of_wine = wine.replace(f" {vintage}", "").replace(" NV", "")
        if len(vintage) > 0:
            vintage = "20" + vintage
        wine_info = {"name_of_wine": name_of_wine, "vintage": vintage}
        self.add_info_dict({"wine_info": wine_info, "amount_of_wines": amount_of_wines})

        self.finish_parsing()


def deep_parse():
    rose_rocks2021 = RoseRocks2021("rose_rocks2021")
    rose_rocks2021.deep_parse()


def surface_parse():
    rose_rocks2021 = RoseRocks2021("rose_rocks2021")
    rose_rocks2021.surface_parse()


def total_parse():
    rose_rocks2021 = RoseRocks2021("rose_rocks2021")
    rose_rocks2021.total_parse()
