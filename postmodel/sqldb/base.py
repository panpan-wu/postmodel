
from typing import Any, List, Optional, Sequence, Tuple, Type, Union, Set
import copy

class BaseSQLDBClient:
    def __init__(self, name, connection) -> None:
        self.name = name
        self.connection = connection

    async def close(self) -> None:
        raise NotImplementedError()  # pragma: nocoverage

    def in_transaction(self):
        raise NotImplementedError()  # pragma: nocoverage

    async def execute_insert(self, query: str, values: list) -> Any:
        raise NotImplementedError()  # pragma: nocoverage

    async def execute_query(
        self, query: str, values: Optional[list] = None
    ) -> Tuple[int, Sequence[dict]]:
        raise NotImplementedError()  # pragma: nocoverage

    async def execute_script(self, query: str) -> None:
        raise NotImplementedError()  # pragma: nocoverage

    async def execute_many(self, query: str, values: List[list]) -> None:
        raise NotImplementedError()  # pragma: nocoverage

    async def execute_query_dict(self, query: str, values: Optional[list] = None) -> List[dict]:
        raise NotImplementedError()  # pragma: nocoverage


class BaseSQLDBMapper(object):
    def __init__(self, model, client):
        self.model = model
        self.client = client
    
    async def create_table(self):
        raise NotImplementedError()

    async def insert(self, data):
        raise NotImplementedError()


class BaseSQLDBEngine(object):
    mapper_class = BaseSQLDBMapper
    client_class = BaseSQLDBClient
    default_config = {}
    default_parameters = {}

    def __init__(self, name, config, parameters={}):
        self.name = name
        self.config = copy.deepcopy(self.default_config)
        self.config.update(config)
        self.parameters = copy.deepcopy(self.default_parameters)
        self.parameters.update(parameters)
    
    @property
    def client(self):
        return self._client

    async def init(self):
        pass
    
    async def close(self):
        if not self._client:
            return
        await self._client.close()
    
    async def db_create(self) -> None:
        raise NotImplementedError()  # pragma: nocoverage

    async def db_delete(self) -> None:
        raise NotImplementedError()  # pragma: nocoverage
    
    def acquire(self):
        raise NotImplementedError()  # pragma: nocoverage