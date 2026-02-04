from uuid import UUID


class ProductKey:
    app: UUID
    key: UUID

    def __init__(self, app: UUID, key: UUID):
        self.app = app
        self.key = key

    def __str__(self) -> str:
        return f"{str(self.app)}|{str(self.key)}"


def pkey_from_str(raw: str) -> ProductKey:
    if "|" not in raw:
        raise ProductKeyParseError(f"Attempted to parse invalid product key! {raw}")

    app, key = raw.split("|", 2)

    if not app.strip() or not key.strip():
        raise ProductKeyParseError(f"Attempted to parse invalid product key! {raw}")

    try:
        return ProductKey(UUID(app), UUID(key))
    except ValueError:
        raise ProductKeyParseError(f"Attempted to parse invalid product key! {raw}")


class ProductKeyParseError(SyntaxError):
    pass
