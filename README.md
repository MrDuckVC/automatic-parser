Для развёртывания проекта требуется совершить несколько действий:
1. Создать файл `docker-compose.override.yml` и заполнить его по образцу `docker-compose.override-dev.yml`.
2. Создать файл `.env` и заполнить его по образцу `.env.dev`.
3. Запустить докер с помощью команды `docker-compose up -d --build`. Параметры `-d` нужен чтоб не отображать логи в термине, а `--build` нужен для пере сборки образов, если вдруг были изменения в `Dockerfile`.
4. Запустить миграции `docker-compose run backend python manage.py migrate`.
5. Собрать статику `docker-compose run backend python manage.py collectstatic`.
6. Создать суперпользователя `docker-compose run backend python manage.py createsuperuser`.
7. Перезапустить `backend` контейнер `docker-compose restart backend`.
8. Ещё некоторое время понадобится для того, чтоб `celery` запустился и начал выполнять задачи.

Перед добавлением конкурсов надо понять какие есть проверки и как это работает:
1. `surface parse` - быстрая проверка, того или иного конкурса на наличие изменений результатов.
2. `deep parse` - детальная проверка предназначена для более глубокой проверки. Она не должна проверять то что проверяла `surface parse`.
3. `total parse` - эта проверка парсит все вина на сайте, данную проверку может запустить только пользователь для скачивания результатов.
4. `check parse` - проверка, если появились результаты за новый год.

`surface parse`, `deep parse`, `total parse` - могут применять только к конкретному году конкурса.
`check parse` - применяется к конкурсу в целом.

В файле `backend/main/main_functions.py` представлен базовый класс `ParsingScript` для проверок.
Могут наследоваться класс использующие специфические методы парсинга, например, `ParsingScriptWithSelenium`, где определены и переопределены методы для парсинга используя библиотеку `selenium`.

При добавлении конкурса мы наследуемся от одного из основных классов описанных в `backend/main/main_functions.py` и называем файл и класс в честь конкурса в соответствии с правилами наименования. С начало мы описываем ключевой класс конкурса в папке `backend/main/scripts_for_parsing/contests/`. Здесь мы переопределяем абстрактный метод `check_new_results`, который представляет собой `check parse`.
Так же здесь мы уже можем переопределять `surface parse`, `deep parse`, `total parse` и реализовывать свои, если того требует ситуация. Как пример можно привести `backend/main/scripts_for_parsing/contests/asia_wine_challenge.py`. У данного конкурса есть 1 важная деталь - каждый год можно спарсить при помощи 1 скрипка поменяв лишь сам год в параметрах ссылки. Для этого был добавлен метод `get_contest_year`, которая возвращает нужный год. Ещё быа добавлен метод `parse_wine`, который судя по названии парсит 1 вино на текущей странице в браузере.
Можно только переопределить метод `check_new_results` как в файле `backend/main/scripts_for_parsing/contests/rose_rocks.py`. Так каждый год парситься по-своему.

После того как мы переопредели метод `check_new_results` и добавили или переопределили требуемые нам методы мы можем приступать к конкретным годам у конкурса. Мы добавляем к названию конкурса год проведения, например, `backend/main/scripts_for_parsing/asia_wine_challenge2021.py` или `backend/main/scripts_for_parsing/rose_rocks2021.py`.
Здесь нам надо переопределить абстрактные методы `surface_parse`, `deep_parse`, `total_parse` как в `backend/main/scripts_for_parsing/rose_rocks2021.py` или `backend/main/scripts_for_parsing/asia_wine_challenge2021.py`.

Так же в конце каждого файла в не зависимости от того это конкурс или конкретный год его проведения мы должны создать функции, где мы запускаем ту или иную проверку. У конкурса это `check_new_results`, а у конкретных годов проведения это `surface_parse`, `deep_parse`, `total_parse`.

Перед переопределением любой проверки вызываем метод `super().<метод, который мы переопределяем>()`, а в конце мы всегда пишем `self.finish_parsing()`.

Советую сами файлы подготовить заранее в другой директории, так как все файлы в `backend/main/scripts_for_parsing/` и `backend/main/scripts_for_parsing/contests` при появлении там в течение минуты попадают в систему.

В конце остаётся проверить работает ли это всё, пишем в терминал команду `docker-compose logs backend` и ищем надпись `{error_name} at {script_name}, {parsing type} parse.`.

Скрипты которые надо переносить находятся в [GitLab репозитории](https://gitlab.deeplace.md/winetaste/medal-data-parse/-/tree/issue19751_ValentinCunev).
Там есть скрипты, которые обрабатывают некий файл `файл.txt`, их не трогаем, они обрабатывают файлы формата `pdf`.
Все скрипты при запуске полностью спарсят сайт и сохранят файл в `Excel` формате. Это чем-то напоминает `total parse`.
Метод `check_new_results` надо писать полностью самостоятельно, а методы `surface_parse`, `deep_parse` зачастую исходят из `total_parse` с некими изменениями.