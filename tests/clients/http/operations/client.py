import uuid

import allure
from httpx import Response

from tests.clients.http.client import HTTPTestClient, build_http_test_client
from tests.config import test_settings
from tests.schema.operations import (
    GetOperationsQueryTestSchema,
    GetOperationResponseTestSchema,
    GetOperationsResponseTestSchema
)
from tests.tools.fakers import fake
from tests.tools.logger import get_test_logger
from tests.tools.routes import APITestRoutes


class OperationsHTTPTestClient(HTTPTestClient):

    @allure.step("Get operations list")
    def get_operations_api(
        self,
        query: GetOperationsQueryTestSchema,
    ) -> Response:
        return self.get(
            f"{APITestRoutes.OPERATIONS}/operations",
            query=query,
        )

    @allure.step("Get operation")
    def get_operation_api(
        self,
        operation_id: uuid.UUID,
    ) -> Response:
        return self.get(
            f"{APITestRoutes.OPERATIONS}/operation/{operation_id}",
        )

    def get_operations(self) -> GetOperationsResponseTestSchema:
        response = self.get_operations_api(GetOperationsQueryTestSchema(user_id=fake.uuid(),account_id=fake.uuid(),card_id=fake.uuid()).model_dump(by_alias=True, exclude_none=True))
        response.raise_for_status()
        return GetOperationsResponseTestSchema.model_validate_json(response.text)

    def get_operation(self) -> GetOperationResponseTestSchema:
        response = self.get_operation_api(fake.uuid())
        response.raise_for_status()
        return GetOperationResponseTestSchema.model_validate_json(response.text)


def build_operations_http_test_client() -> OperationsHTTPTestClient:
    client = build_http_test_client(
        logger=get_test_logger("OPERATIONS_HTTP_TEST_CLIENT"),
        config=test_settings.operations_http_client,
    )
    return OperationsHTTPTestClient(client=client)
