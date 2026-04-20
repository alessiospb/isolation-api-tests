import uuid
from pathlib import Path

from fastapi import APIRouter, Depends

from tests.context.scenario import Scenario
from tests.mock.http.tools import get_scenario_http
from tests.schema.accounts import GetAccountResponseTestSchema, GetAccountsResponseTestSchema
from tests.tools.logger import get_test_logger
from tests.tools.mock import MockLoader
from tests.tools.routes import APITestRoutes

# MockLoader — инфраструктурный компонент.
# Его ответственность строго ограничена:
# - загрузить мок-данные из файлов,
# - провалидировать их контрактом,
# - залогировать процесс загрузки.
#
# Loader не знает:
# - кто вызывает мок (gateway, тест, другой сервис),
# - зачем используется конкретный сценарий,
# - как устроена бизнес-логика системы.
loader = MockLoader(
    root=Path("./tests/mock/http/data/accounts"),
    logger=get_test_logger("ACCOUNTS_SERVICE_MOCK_LOADER")
)

# Роутер представляет HTTP-контракт accounts-service.
# Префикс и пути соответствуют контрактам тестового стенда,
# а не внутренней реализации мок-сервиса.
account_mock_router = APIRouter(
    prefix=APITestRoutes.ACCOUNTS,
    tags=[APITestRoutes.ACCOUNTS]
)

@account_mock_router.get("", response_model=GetAccountsResponseTestSchema)
async def get_accounts_view(
    scenario: Scenario = Depends(get_scenario_http),
):
    return await loader.load_http(
        file=f"get_accounts/{scenario}.json",
        model=GetAccountsResponseTestSchema
    )

@account_mock_router.get("/{account_id}", response_model=GetAccountResponseTestSchema)
async def get_account_view(
    account_id: uuid.UUID,
    scenario: Scenario = Depends(get_scenario_http),
):
    # account_id присутствует в сигнатуре,
    # чтобы полностью соответствовать контракту accounts-service.
    #
    # Важно: мок не использует account_id для вычислений.
    # Поведение мока определяется только сценарием,
    # что гарантирует детерминизм и воспроизводимость тестов.

    return await loader.load_http(
        # Имя файла формируется на основе сценария.
        # Это связывает внешний мир с тестовым сценарием,
        # а не с параметрами конкретного запроса.
        file=f"get_account/{scenario}.json",

        # Ответ валидируется тестовой схемой,
        # что гарантирует контрактную корректность мока.
        model=GetAccountResponseTestSchema
    )
