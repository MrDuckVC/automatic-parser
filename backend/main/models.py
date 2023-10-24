"""
Django models file
"""
import datetime
import json

from django.db import models


class ParserScript(models.Model):
    """
    Django model for storing scripts names.
    """
    parser_script = models.CharField(max_length=128, help_text="Parser script name")
    objects = models.Manager()

    def __str__(self):
        return str(self.parser_script)

    def get_last_parse(self, parsing_type: str, state: str):
        """
        Search last parse by type of parse and by script object in model "ParserScript" with.
        :param parsing_type: type of parse
        :param state: used for get last parsing job with concrete state or "any" if you need any state.
        :return: object in model "Parsing Job".
        """
        intermediate_result = ParsingJob.objects.filter(parser_script=self, type_of_parse=parsing_type)
        if state == "any": 
            return intermediate_result.last()
        return intermediate_result.filter(status=state).order_by('time_of_start').last()

    @staticmethod
    def get_script_obj(parser_script: str):
        """
        Return script object in model "ParserScript" by script name. Can create new, if not coincidences be select, create new.
        :param parser_script: name of script in model "ParserScript".
        :return: script object in model "ParserScript"
        """
        script_obj = ParserScript.objects.filter(parser_script=parser_script).first()
        if script_obj is None:
            script_obj = ParserScript(parser_script=parser_script)
            script_obj.save()
        return script_obj


class ParsingJob(models.Model):
    """
    Django model for storing history of the parsing jobs.
    """
    # FIXME - declare class constants for states and types.
    PARSING_TYPE_DEEP = "deep"
    PARSING_TYPE_SURFACE = "surface"
    PARSING_TYPE_TOTAL = "total"
    PARSING_TYPE_CHECK = "check"
    PARSING_TYPE = [("deep", PARSING_TYPE_DEEP), ("surface", PARSING_TYPE_SURFACE), ["total", PARSING_TYPE_TOTAL], ["check", PARSING_TYPE_CHECK]]
    STATE_IN_PROGRESS = "In progress"
    STATE_DONE = "Done"
    STATE_CANCELED = "Canceled"
    STATE_FAILED = "Failed"
    STATES = [("In progress", STATE_IN_PROGRESS), ("Done", STATE_DONE), ("Canceled", STATE_CANCELED), ("Failed", STATE_FAILED)]
    parser_script = models.ForeignKey(ParserScript, on_delete=models.DO_NOTHING, help_text="Script name")
    time_of_start = models.DateTimeField(auto_now_add=True, null=True, help_text="Date time of parsing start")
    type_of_parse = models.CharField(max_length=128, choices=PARSING_TYPE, help_text="Parsing type")
    status = models.CharField(max_length=128, help_text="Current job status", choices=STATES)
    objects = models.Manager()

    def __str__(self):
        return str(self.parser_script)

    def needed_parsing(self, period: int):
        """
        Check if you need to run parse.
        :param period: period of launching script in seconds.
        :return: boolean True is you need or False if not.
        """
        return self is None or (self.status != "In progress" and datetime.datetime.now().timestamp() - self.time_of_start.timestamp() >= period)


class ParsingResult(models.Model):
    """
    Django model for storing parsing results of parsing in json.
    """

    wine_json = models.JSONField()
    parsing_job_id = models.ManyToManyField(ParsingJob, help_text="Parser run Id")
    hash = models.CharField(max_length=40, unique=True)
    objects = models.Manager()

    def show_parsing_result(self):
        """
        Method for correct showing parsing result in django admin.
        :return: string.
        """
        # get values in dict.
        wine_json = json.loads(self.wine_json)
        wine_parameter_value = []
        # form list with parameters and their value.
        for parameter in wine_json:
            wine_parameter_value.append(f"{parameter}: {wine_json[parameter]}")
        return " || ".join(wine_parameter_value)

    show_parsing_result.help_text = ("Wine parameters",)

    class Meta:
        indexes = [
            models.Index(fields=['hash', ]),
        ]
