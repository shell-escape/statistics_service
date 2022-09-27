"""
Нужно разработать микросервис для счетчиков статистики. Сервис должен уметь взаимодействовать с клиентом при помощи REST API. Также нужно реализовать валидацию входных данных.

API методы:
Метод сохранения статистики
Метод показа статистики
Метод сброса статистики
Метод сохранения статистики.
Принимает на вход:

date - дата события
views - количество показов
clicks - количество кликов
cost - стоимость кликов (в рублях с точностью до копеек)
Поля views, clicks и cost - опциональные. Статистика агрегируется по дате.

Метод показа статистики
Принимает на вход:

from - дата начала периода (включительно)
to - дата окончания периода (включительно)
Отвечает статистикой, отсортированной по дате. В ответе должны быть поля:

date - дата события
views - количество показов
clicks - количество кликов
cost - стоимость кликов
cpc = cost/clicks (средняя стоимость клика)
cpm = cost/views * 1000 (средняя стоимость 1000 показов)
Метод сброса статистики
Удаляет всю сохраненную статистику.

Критерии приемки:
язык программирования: Python/ Fast Api
можно использовать любое хранилище(PostgreSQL, MySQl, Redis и т.д.) или обойтись без него (in-memory). При использовании СУБД нужен файл с запросами на создание - - всех необходимых таблиц.
формат даты YYYY-MM-DD.
стоимость указывается в рублях с точностью до копеек.
в методе показа статистики можно выбрать сортировку по любому из полей ответа.
простая инструкция для запуска (в идеале — с возможностью запустить в docker).
Усложнения:
покрытие unit-тестами.
документация (достаточно структурированного описания методов, примеров их вызова в README.md).
"""


import datetime

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from src import execution, schemas
from src.db import service

app = FastAPI(title="stats_service")


# exception messages
NO_SORT_FIELD = "No such field to sort."


@app.post("/save_stat", status_code=200, response_model=dict[str, str])
def save_stat(
    day_stat: execution.DayStat, session: Session = Depends(service.get_session)
) -> dict[str, str]:
    """Save day statistic."""
    existing_day_stat = service.get_stat_by_date(session, day_stat.date)
    if existing_day_stat is None:
        day_stat.add_to_db(session)
        return {"result": f"Statistic for {day_stat.date} saved."}
    else:
        day_stat.update(session, existing_day_stat)
        return {"result": f"Statistic for {day_stat.date} updated."}


@app.get("/get_stat", status_code=200, response_model=list[schemas.StatOut])
def get_stat(
    from_: datetime.date,
    to_: datetime.date,
    sort_field: str = "date",
    session: Session = Depends(service.get_session),
) -> list[schemas.StatOut]:
    """Gets statistic sorted by 'sort_field' in [from_, to] date range."""
    stat = service.get_stat(session, from_, to_)
    stat_to_view = execution.get_stat_view(stat)
    try:
        return sorted(stat_to_view, key=lambda stat: getattr(stat, sort_field))
    except AttributeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=NO_SORT_FIELD
        )


@app.delete("/stat", status_code=200, response_model=dict[str, str])
def delete_stats(
    session: Session = Depends(service.get_session),
) -> dict[str, str]:
    """Deletes statistic."""
    service.delete_stat(session)
    return {"result": "Statistic deleted."}
