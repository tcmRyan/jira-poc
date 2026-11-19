from typing import Any, Dict, Optional, Protocol


class AuthenticationQueries(Protocol):
    """The queries aiosql loads from authentications.sql."""

    def insert_authentication(
        self,
        conn: Any,
        *,
        key: Optional[str],
        client_key: Optional[str],
        shared_secret: Optional[str],
        plugins_version: Optional[str],
        base_url: Optional[str],
        product_type: Optional[str],
        description: Optional[str],
        service_entitlement_number: Optional[str],
        event_type: Optional[str],
        public_key: Optional[str],
        server_version: Optional[str],
        installed_by: Optional[str],
    ) -> None: ...

    def get_authentication_by_base_url(self, conn: Any, *, base_url: str) -> Optional[Dict[str, Any]]: ...

    def delete_authentications_by_client_key(self, conn: Any, *, client_key: str) -> None: ...
