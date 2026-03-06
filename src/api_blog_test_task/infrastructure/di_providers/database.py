from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    async_sessionmaker
)

from api_blog_test_task.application.interfaces.database import ITransactionManager
from api_blog_test_task.infrastructure.settings import DatabaseSettings
from api_blog_test_task.infrastructure.database import (
    TransactionManager,
    create_sa_engine,
    create_sa_session_factory,
)

class DatabaseProvider(Provider):
    def __init__(
            self,
            database_settings: DatabaseSettings,
            scope=None,
            component=None
    ):
        super().__init__(scope, component)
        self._database_settings = database_settings

    @provide(scope=Scope.APP)
    def db_engine(self) -> AsyncEngine:
        return create_sa_engine(self._database_settings.url_obj)

    @provide(scope=Scope.APP)
    def db_session_factory(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return create_sa_session_factory(engine)

    @provide(scope=Scope.REQUEST)
    def transaction_manager(self, session_factory: async_sessionmaker[AsyncSession]) -> ITransactionManager:
        session = session_factory()
        return TransactionManager(session)
