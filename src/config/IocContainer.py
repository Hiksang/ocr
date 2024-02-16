from enum import Enum, auto

class AppContext: 
    _instances = {}

    @classmethod
    def register(cls, key, instance):
        if isinstance(key, Enum):
            cls._instances[key] = instance
        else:
            raise TypeError("Key must be an Enum member")

    @classmethod
    def get(cls, key: Enum):
        if isinstance(key, Enum):
            return cls._instances.get(key)
        else:
            raise TypeError("Key must be an Enum member")
