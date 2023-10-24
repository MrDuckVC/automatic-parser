import sys
import os

from django.conf import settings
from django.db.utils import OperationalError
from celery.decorators import periodic_task
from celery.schedules import crontab
from celery.signals import worker_ready

import main.services as services
from .celery import app
from .models import ParsingJob, ParserScript


@periodic_task(run_every=(crontab(minute="*/1", )), name="check_for_last_parse")
def check_for_last_parse(track_started=True):
    # Deep, surface and check parse period in seconds.
    deep_parse_period = settings.DEEP_PARSE_PERIOD
    surface_parse_period = settings.SURFACE_PARSE_PERIOD
    check_parse_period = settings.CHECK_PARSE_PERIOD
    try:
        # Getting names of scripts in dir "main/scripts_for_parsing" and "main/scripts_for_parsing/contests".
        contests_year = os.listdir("main/scripts_for_parsing")
        contests = os.listdir("main/scripts_for_parsing/contests")

        parser_files = [contests_year, contests]
        for parsers in parser_files:
            for script in parsers:
                # Ignoring file "__pycache__", "__init__.py" and "contests".
                if script not in ["__pycache__", "__init__.py", "contests"]:
                    script = script.replace(".py", "")

                    # Get script object.
                    script_obj = ParserScript.get_script_obj(script)

                    # Find out what kind of parser it is.
                    if parser_files.index(parsers) == 0:
                        parsing_types_period = {ParsingJob.PARSING_TYPE_DEEP: deep_parse_period, ParsingJob.PARSING_TYPE_SURFACE: surface_parse_period}
                    else:
                        parsing_types_period = {ParsingJob.PARSING_TYPE_CHECK: check_parse_period}

                    for parsing_type in parsing_types_period:
                        # Check for last deep parse.
                        last_parse = script_obj.get_last_parse(parsing_type, "any")
                        if last_parse is None or last_parse.needed_parsing(parsing_types_period[parsing_type]):
                            # Update celery task status.
                            check_for_last_parse.update_state(state='PROGRESS', meta={'script_in_progress': script, "type": parsing_type})
                            services.parse_by_type(script, parsing_type)
                            check_for_last_parse.update_state(state='PROGRESS', meta={})

    # If mysql db is not active yet, we will restart.
    except OperationalError:
        sys.exit(127)
    return True


@app.task
def run_parse(parser_script, type):
    run_parse.update_state(state='PROGRESS', meta={'script_in_progress': parser_script, "type": type})
    if type == ParsingJob.PARSING_TYPE_DEEP:
        if services.script_availability(parser_script, "contest year"):
            services.parse_by_type(parser_script, type)
    elif type == ParsingJob.PARSING_TYPE_SURFACE:
        if services.script_availability(parser_script, "contest year"):
            services.parse_by_type(parser_script, type)
    elif type == ParsingJob.PARSING_TYPE_TOTAL:
        if services.script_availability(parser_script, "contest year"):
            services.parse_by_type(parser_script, type)
    elif type == ParsingJob.PARSING_TYPE_CHECK:
        if services.script_availability(parser_script, "contest"):
            services.parse_by_type(parser_script, type)

    run_parse.update_state(state='PROGRESS', meta={})


@worker_ready.connect
def check_for_failure(sender, **k):
    failed_parsing_jobs = ParsingJob.objects.filter(status="In progress")
    for parsing_job in failed_parsing_jobs:
        parsing_job.status = "Failed"
        parsing_job.save()
