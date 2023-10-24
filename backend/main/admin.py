"""
Django admin file.
"""
import zipfile
import tempfile
import json

import openpyxl
from django.contrib import admin, messages
from django.http import HttpResponse

from .models import ParsingJob, ParserScript, ParsingResult
from .services import run_parse_by_type, script_availability, cancel_parse_by_type


@admin.action
def run_deep_parse(modeladmin, request, scripts_objects):
    """
    Admin action for parsing job deep parse.
    :param modeladmin: model admin object.
    :param request: request object.
    :param scripts_objects: objects in model "ParserScript".
    """
    run_parse_by_type(scripts_objects, ParsingJob.PARSING_TYPE_DEEP, request)


@admin.action
def run_surface_parse(modeladmin, request, scripts_objects):
    """
    Admin action for parsing job surface parse.
    :param modeladmin: model admin object.
    :param request: request object.
    :param scripts_objects: objects in model "ParserScript".
    """
    run_parse_by_type(scripts_objects, ParsingJob.PARSING_TYPE_SURFACE, request)


@admin.action
def run_total_parse(modeladmin, request, scripts_objects):
    """
    Admin action for parsing job total parse.
    :param modeladmin: model admin object.
    :param request: request object.
    :param scripts_objects: objects in model "ParserScript".
    """
    run_parse_by_type(scripts_objects, ParsingJob.PARSING_TYPE_TOTAL, request)


@admin.action
def run_check_parse(modeladmin, request, scripts_objects):
    """
    Admin action for parsing job check parse.
    :param modeladmin: model admin object.
    :param request: request object.
    :param scripts_objects: objects in model "ParserScript".
    """
    run_parse_by_type(scripts_objects, ParsingJob.PARSING_TYPE_CHECK, request)


@admin.action
def download_parsing_result(modeladmin, request, scripts_objects):
    """
    Download zip file with parsing result by app user.
    :param modeladmin: model admin object.
    :param request: request object.
    :param scripts_objects: objects in model "ParserScript".
    """
    with tempfile.NamedTemporaryFile(dir='/tmp') as tmp:
        with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as archive:
            for script in scripts_objects:
                is_contest_year = script_availability(script.parser_script, "contest year")
                if is_contest_year is False:
                    messages.error(request,
                                   f"Script {script.parser_script} contest or does not exists.")
                    continue
                # Getting last total parse.
                last_run = script.get_last_parse(ParsingJob.PARSING_TYPE_TOTAL, "Done")
                if last_run is None:
                    messages.error(request,
                                   f"Parsing job total parse for {script.parser_script} for downloading file with parsing result.")
                    continue
                with tempfile.NamedTemporaryFile() as tmp_xlsx:
                    workbook = openpyxl.Workbook()
                    sheet1 = workbook.active

                    parsing_results = last_run.parsingresult_set.all()
                    # Add headers for MS Excel table.
                    parameters = list(json.loads(parsing_results[0].wine_json))
                    sheet1.append(parameters)
                    for parsing_result in parsing_results:
                        parsing_result_dict = json.loads(parsing_result.wine_json)
                        parameters_value_list = []
                        for parameter in parameters:
                            if isinstance(parsing_result_dict[parameter], list):
                                ", ".join(parsing_result_dict[parameter])
                            parameters_value_list.append(str(parsing_result_dict[parameter]))
                        for value in parameters_value_list:
                            if value == "None":
                                parameters_value_list[parameters_value_list.index(value)] = ""
                        sheet1.append(parameters_value_list)
                    workbook.save(tmp_xlsx.name)
                    archive.write(tmp_xlsx.name, arcname=f"{script.parser_script}.xlsx")
        tmp.seek(0)
        response = HttpResponse()
        while True:
            chunk = tmp.read(4096)
            if not chunk:
                break
            response.write(chunk)
        response['Content-Type'] = 'application/zip'
        response['Content-Disposition'] = 'attachment; filename=parsing_result.zip'
        return response


@admin.action
def cancel_deep_parse(modeladmin, request, scripts_objects):
    """
    Canceling deep parse.
    :param modeladmin: model admin object.
    :param request: request object.
    :param scripts_objects: objects in model "ParserScript".
    """
    cancel_parse_by_type(scripts_objects, ParsingJob.PARSING_TYPE_DEEP)


@admin.action
def cancel_surface_parse(modeladmin, request, scripts_objects):
    """
    Canceling surface parse.
    :param modeladmin: model admin object.
    :param request: request object.
    :param scripts_objects: objects in model "ParserScript".
    """
    cancel_parse_by_type(scripts_objects, ParsingJob.PARSING_TYPE_SURFACE)


@admin.action
def cancel_total_parse(modeladmin, request, scripts_objects):
    """
    Canceling total parse.
    :param modeladmin: model admin object.
    :param request: request object.
    :param scripts_objects: objects in model "ParserScript".
    """
    cancel_parse_by_type(scripts_objects, ParsingJob.PARSING_TYPE_TOTAL)


@admin.action
def cancel_check_parse(modeladmin, request, scripts_objects):
    """
    Canceling check parse.
    :param modeladmin: model admin object.
    :param request: request object.
    :param scripts_objects: objects in model "ParserScript".
    """
    cancel_parse_by_type(scripts_objects, ParsingJob.PARSING_TYPE_CHECK)


class ParserScriptAdmin(admin.ModelAdmin):
    """
    Django admin model for showing scripts names and controlling parsing jobs.
    """
    list_display = ("parser_script",)
    actions = [
        run_deep_parse, run_surface_parse, run_total_parse, run_check_parse, download_parsing_result,
        cancel_deep_parse, cancel_surface_parse, cancel_total_parse, cancel_check_parse
    ]


class ParsingJobAdmin(admin.ModelAdmin):
    """
    Django admin model for showing parsing jobs.
    """
    list_display = ("parser_script", "type_of_parse", "time_of_start", "status")


class ParsingResultAdmin(admin.ModelAdmin):
    """
    Django admin model for showing parsing result of parsing.
    """
    list_display = ("show_parsing_result",)


admin.site.register(ParserScript, ParserScriptAdmin)
admin.site.register(ParsingJob, ParsingJobAdmin)
admin.site.register(ParsingResult, ParsingResultAdmin)
