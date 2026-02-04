import sys

from db import ShitDB
from pkey import pkey_from_str, ProductKeyParseError
from verifier import verify_pkey, ProductKeyVerificationError


def repl(db: ShitDB) -> None:
    print("Enter your product key, or type \"exit\"")
    raw_key = input("> ")

    if (raw_key == "exit"):
        db.disconnect()
        sys.exit(0)
        return None

    try:
        key = pkey_from_str(raw_key)
    except ProductKeyParseError as ex:
        print(ex.msg)
        repl(db)
        return None

    try:
        if verify_pkey(key):
            print("That product key is valid")
            register_key(db, raw_key)
        else:
            print("That product key is invalid")
    except ProductKeyVerificationError as ex:
        print(ex.msg)


def verify_key(db: ShitDB, raw_key: str) -> [bool, str]:
    try:
        key = pkey_from_str(raw_key)
    except ProductKeyParseError as ex:
        return [False, ex.msg]

    try:
        if verify_pkey(key):
            register_key(db, raw_key)
            return [True, None]
        else:
            return [False, None]
    except ProductKeyVerificationError as ex:
        return [False, ex.msg]


def register_key(db: ShitDB, raw_key: str) -> [bool, str]:
    try:
        key = pkey_from_str(raw_key)
    except ProductKeyParseError as ex:
        return [False, ex.msg]

    if db.has_key(key):
        return [False, "Key already exists"]

    try:
        if verify_pkey(key):
            db.add_key(raw_key)
            return [True, None]
        else:
            return [False, None]
    except ProductKeyVerificationError as ex:
        return [False, ex.msg]


def main() -> None:
    db = ShitDB()
    db.connect()
    db.init()
    # db.add_key(ProductKey(UUID(int=0), UUID(int=0)))
    options = ["repl", "verify", "register", "clearkeys"]
    requires_key_options = ["verify", "register"]

    if len(sys.argv) < 2 or sys.argv[1] not in options:
        print(f"Usage: {sys.argv[0]} {'|'.join(options)} <optional:key>")
        sys.exit(1)
        return None

    if sys.argv[1] == "repl":
        repl(db)
        db.disconnect()
        return None
    elif sys.argv[1] == "clearkeys":
        db.clear_keys()
        db.disconnect()
        return None

    if len(sys.argv) < 3 or sys.argv[1] not in requires_key_options:
        print(f"Usage: {sys.argv[0]} {sys.argv[1]} <key>")
        sys.exit(1)
        return None

    if (sys.argv[1] == "verify"):
        valid, message = verify_key(db, sys.argv[2])

        if valid and message != None:
            print(message)
        elif valid and not message:
            print("That product key is valid")
        elif not valid and message != None:
            print(message)
        elif not valid and not message:
            print("That product key is invalid")
    elif (sys.argv[1] == "register"):
        registered, message = register_key(db, sys.argv[2])

        if registered and message != None:
            print(message)
        elif registered and not message:
            print("Registration successful")
        elif not registered and message != None:
            print(message)
        elif not registered and not message:
            print("Unknown error while registering")

    db.disconnect()


if __name__ == "__main__":
    main()
