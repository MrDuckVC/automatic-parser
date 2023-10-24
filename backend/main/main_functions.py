"""
File where is main class for parsers and their types.
"""
import json
import hashlib
from abc import abstractmethod, ABC

from django.core.mail import send_mail
from django.conf import settings
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver

from main.models import ParserScript, ParsingJob, ParsingResult


class ParsingScript:
    """
    General class for parsers.
    """
    def __init__(self, parser_script: str):
        """
        Init function.
        :param parser_script: name of script that parse concurs.
        """
        self.parsing_job_record = None
        self.parser_script = parser_script

    @abstractmethod
    def deep_parse(self):
        """
        Realise your deep parse method here.
        """
        self.create_parsing_job_record(ParsingJob.PARSING_TYPE_DEEP)

    @abstractmethod
    def surface_parse(self):
        """
        Realise your surface parse method here.
        """
        self.create_parsing_job_record(ParsingJob.PARSING_TYPE_SURFACE)

    @abstractmethod
    def total_parse(self):
        """
        Realise your parsing site.
        """
        self.create_parsing_job_record(ParsingJob.PARSING_TYPE_TOTAL)

    @abstractmethod
    def check_new_parsing_result(self):
        """
        Realise here your script for checking new event parsing result.
        """
        self.create_parsing_job_record(ParsingJob.PARSING_TYPE_CHECK)

    def add_info_dict(self, parsing_result_dict: dict):
        """
        Function for adding 1 json parsing result of info in db.
        :param parsing_result_dict: parameters of wine and their value.
        """
        info_json = json.dumps(parsing_result_dict)
        info_hash = hashlib.sha1(info_json.encode('utf-8')).hexdigest()
        same_result_in_db = ParsingResult.objects.filter(hash=info_hash)
        # If there is no same wine we will create new wine.
        if len(same_result_in_db) == 0:
            info = ParsingResult.objects.create(wine_json=info_json, hash=info_hash)
            info.parsing_job_id.add(self.parsing_job_record)
        # Else we will create links between the wine and parsing job.
        else:
            self.parsing_job_record.parsingresult_set.add(same_result_in_db[0])

    def create_parsing_job_record(self, parsing_type: str):
        """
        Function for creating parsing job record in db, status "In progress".
        :param parsing_type: can be "total", "check", "deep" or "surface".
        """
        script_object = ParserScript.objects.filter(parser_script=self.parser_script)[0]
        self.parsing_job_record = ParsingJob(status="In progress", parser_script=script_object, type_of_parse=parsing_type)
        self.parsing_job_record.save()
        print(f"Start parsing of {self.parser_script} by {self.parsing_job_record.type_of_parse} parse")

    def end_parsing_job_record(self):
        """
        Function for changing parsing job record status to "Done".
        """
        self.parsing_job_record.status = "Done"
        self.parsing_job_record.save()
        print(f"Ended parsing of {self.parser_script} by {self.parsing_job_record.type_of_parse} parse")

    def check_updates(self):
        """
        Function for checking updates in parsing result data of previous parse and current parse.
        :return: boolean that indicate if there were changes.
        """
        send_mail_to = settings.TO_EMAILS
        script = ParserScript.objects.filter(parser_script=self.parser_script).first()
        previous_parse = script.get_last_parse(self.parsing_job_record.type_of_parse, "Done")
        if previous_parse is not None:
            # Getting old and current parsing result.
            old_results = ParsingResult.objects.filter(parsing_job_id=previous_parse)
            current_results = ParsingResult.objects.filter(parsing_job_id=self.parsing_job_record)

            # Check for missing parsing_result.
            lost_wines = []
            for old_wine in old_results:
                if old_wine not in current_results:
                    lost_wines.append(json.loads(old_wine.wine_json))

            if lost_wines and self.parsing_job_record.type_of_parse != ParsingJob.PARSING_TYPE_CHECK:
                # Send email "Not found in new parsing result wine <lost_wines>. Parsing job time <parsing_job_time>.".
                send_mail(
                    "Not found in new parsing result wines",
                    f"Not found in new parsing result wines {lost_wines}. Parsing job {self.parsing_job_record.parser_script} time {self.parsing_job_record.time_of_start}.",
                    settings.EMAIL_HOST_USER,
                    send_mail_to,
                    fail_silently=False,
                )
                print(f"Not found in new parsing result wines {lost_wines}. Parsing job {self.parsing_job_record.parser_script} time {self.parsing_job_record.time_of_start}.")
            # Check for new parsing result.
            new_wines = []
            for current_wine in current_results:
                if current_wine not in old_results:
                    new_wines.append(json.loads(current_wine.wine_json))

            if new_wines and self.parsing_job_record.type_of_parse != ParsingJob.PARSING_TYPE_CHECK:
                # Send email "Found new wines in parsing result <new_wines>. Parsing job time <parsing_job_time>.".
                send_mail(
                    "Found new wines in parsing result",
                    f"Found new wines in parsing result {new_wines}. Parsing job {self.parsing_job_record.parser_script} time {self.parsing_job_record.time_of_start}.",
                    settings.EMAIL_HOST_USER,
                    send_mail_to,
                    fail_silently=False,
                )
                print(f"Found new wines in parsing result {new_wines}. Parsing job {self.parsing_job_record.parser_script} time {self.parsing_job_record.time_of_start}.")

            if lost_wines and new_wines and self.parsing_job_record.type_of_parse == ParsingJob.PARSING_TYPE_CHECK:
                # Send email "New contest year parsing result at concurs <concurs>. Parsing job time <parsing_job_time>.".
                send_mail(
                    "New contest year parsing result at concurs",
                    f"New contest year parsing result at concurs {str(self.parsing_job_record.parser_script)}. Parsing job {self.parsing_job_record.parser_script} time {self.parsing_job_record.time_of_start}.",
                    settings.EMAIL_HOST_USER,
                    send_mail_to,
                    fail_silently=False,
                )
                print(f"New contest year parsing result at concurs {str(self.parsing_job_record.parser_script)}. Parsing job {self.parsing_job_record.parser_script} time {self.parsing_job_record.time_of_start}.")

    def add_params_for_dict(self, additional_info: dict, filters: dict):
        """
        Function for adding parameters for wine that already is added in database.
        :param additional_info: parameters and their value that need to be added for wine.
        :param filters: parameters and their value that will be used as a filter for searching wine in database.
        :return: returns boolean, True is we have found needed wine and False if not.
        """
        # Getting all wines from current parsing job.
        wines = ParsingResult.objects.filter(parsing_job_id=self.parsing_job_record)
        for wine in wines:
            # Getting wine info in dict.
            wine_dict = json.loads(wine.wine_json)

            match = True
            for param in filters.keys():
                if param in wine_dict.keys() and wine_dict[param] == filters[param]:
                    pass
                else:
                    match = False
                    break

            if match is True:
                # Add additional information for wine.
                for param in additional_info:
                    if wine_dict.get(param) is None:
                        wine_dict[param] = additional_info[param]
                    elif isinstance(wine_dict[param], list):
                        wine_dict[param] = wine_dict[param].append(additional_info[param])
                    else:
                        wine_dict[param] = [additional_info[param], wine_dict[param]]

                print(wine_dict)
                self.add_info_dict(wine_dict)
                self.parsing_job_record.parsingresult_set.remove(wine)
                if len(wine.parsing_job_id.all()) == 0:
                    wine.delete()
                return True

        return False

    def finish_parsing(self):
        """
        Function for perform all parsing completion operations.
        """
        self.check_updates()
        self.end_parsing_job_record()


class ParsingScriptWithSelenium(ParsingScript):
    """
    This class for scripts, that use selenium for parse.
    """
    def __init__(self, parser_script: str):
        """
        Init function.
        :param parser_script: name of script that parse concurs.
        """
        super().__init__(parser_script)
        self.web_driver = None

    def activate_web_driver(self):
        """
        Function for activate selenium web driver.
        """
        self.web_driver = webdriver.Remote("http://webdriver:4444/wd/hub", desired_capabilities=DesiredCapabilities.CHROME)

    def close_web_driver(self):
        """
        Function for closing selenium web driver.
        """
        self.web_driver.close()

    def finish_parsing(self):
        super().finish_parsing()
        self.close_web_driver()
