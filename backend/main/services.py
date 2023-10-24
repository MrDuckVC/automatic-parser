import os
from importlib.machinery import SourceFileLoader

from django.contrib import messages

from .celery import app
from .models import ParsingJob, ParserScript
import main.tasks as tasks


def parse_by_type(parser_script: str, parsing_type: str):
    """
    Run deep parse by name.
    :param parser_script: parser name.
    :param parsing_type: parsing type
    """
    try:
        if parsing_type in [ParsingJob.PARSING_TYPE_DEEP, ParsingJob.PARSING_TYPE_SURFACE, ParsingJob.PARSING_TYPE_TOTAL]:
            module = SourceFileLoader(parser_script, f"main/scripts_for_parsing/{parser_script}.py").load_module()
            if parsing_type == ParsingJob.PARSING_TYPE_DEEP:
                module.deep_parse()
            elif parsing_type == ParsingJob.PARSING_TYPE_SURFACE:
                module.surface_parse()
            elif parsing_type == ParsingJob.PARSING_TYPE_TOTAL:
                module.total_parse()
            elif parsing_type == ParsingJob.PARSING_TYPE_CHECK:
                module.check_new_parsing_result()
        elif parsing_type == ParsingJob.PARSING_TYPE_CHECK:
            module = SourceFileLoader(parser_script, f"main/scripts_for_parsing/contests/{parser_script}.py").load_module()
            module.check_new_parsing_result()
    except Exception as e:
        print(f"{e} at {parser_script}, {parsing_type} parse.")
        script_obj = ParserScript.objects.filter(parser_script=parser_script).first()
        failed_parse = ParsingJob.objects.filter(parser_script=script_obj, type_of_parse=parsing_type, status="In progress").first()
        failed_parse.status = "Failed"
        failed_parse.save()


def script_availability(parser_script: str, script_type: str):
    """
    Check if file exists for parsing job functions.
    :param parser_script: script name in model "ParserScript".
    :param script_type: "contest" if check parse, "contest year" if deep, surface, total.
    :return: boolean True if file exists or False if not.
    """
    if script_type == "contest":
        return os.path.exists(f"main/scripts_for_parsing/contests/{parser_script}.py")
    elif script_type == "contest year":
        return os.path.exists(f"main/scripts_for_parsing/{parser_script}.py")
    return False


def run_parse_by_type(scripts_objects, parsing_type: str, request):
    """
    Run parse for one or more scripts by parsing type.
    :param scripts_objects: set of objects in model "ParserScript".
    :param parsing_type: type of parse.
    :param request: request object.
    """
    for script in scripts_objects:
        # Select script with state "In progress".
        parsing_job = ParsingJob.objects.filter(parser_script=script, type_of_parse=parsing_type, status="In progress").first()
        if parsing_job is not None:
            messages.error(request,
                           f"Script {script.parser_script} is already running {parsing_type} parse. Cancel parsing or wait for parsing result.")
        else:
            tasks.run_parse.delay(script.parser_script, parsing_type)


def cancel_parse_by_type(scripts_objects, parsing_type: str):
    """
    Cancel parse for one and more scripts by parsing type.
    :param scripts_objects: set of objects in model "ParserScript".
    :param parsing_type: type of parse.
    """
    for script in scripts_objects:
        # Get all active celery tasks.
        celery_worker = app.control.inspect().active()
        hostname = list(celery_worker.keys())[0]
        celery_tasks = [task["id"] for task in celery_worker[hostname]]
        for task in celery_tasks:
            task_info = tasks.check_for_last_parse.AsyncResult(task).info
            if task_info["script_in_progress"] == script.parser_script and task_info["type"] == parsing_type:
                # Canceling celery task.
                app.control.revoke(task, terminate=True)
                # Update parsing state.
                last_parse = ParsingJob.objects.filter(parser_script=script, type_of_parse=parsing_type, status="In progress")[0]
                last_parse.status = "Canceled"
                last_parse.save()
                break
