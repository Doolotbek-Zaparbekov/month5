import random
from django.core.cache import cache

def generate_confirmation_code() -> str:
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])


def set_confirmation_code(user_id: int, code: str):
    key = f"confirmation_code:{user_id}"
    cache.set(key, code, timeout=300)


def get_confirmation_code(user_id: int) -> str | None:
    key = f"confirmation_code:{user_id}"
    return cache.get(key)


def delete_confirmation_code(user_id: int):
    key = f"confirmation_code:{user_id}"
    cache.delete(key)
