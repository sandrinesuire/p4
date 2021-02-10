"""File for chess models"""
import operator
from functools import reduce

from tinydb import TinyDB, where


class Manager:
    """Manager for DB"""

    indice = None
    db = TinyDB('chess.json')
    table_name = "default"
    table = db.table(table_name)

    def save(self):
        """Saving method"""
        pass

    @classmethod
    def get(cls, kwargs):
        """Method for getting element from kwargs informations"""
        my_filter = []
        for k, v in kwargs.items():
            my_filter.append((where(k) == v))

        data = cls.table.search(reduce(operator.and_, my_filter))
        data = data[0] if data else None
        return cls.deserialize(data)

    @classmethod
    def deserialize(cls, data):
        """Method converting db instance data in instance model"""
        if data:
            instance = cls(**data)
            instance.indice = data.doc_id
            return instance
        return

    @classmethod
    def get_n_first_instances(cls, instances_number: int):
        """Method getting n first instance from db"""
        instances = []
        instances_list = cls.table.all()
        if instances_list:
            for i, player_data in enumerate(instances_list[0:instances_number]):
                instance = cls.deserialize(player_data)
                instances.append(instance)
            return instances

    @classmethod
    def existing_n_instances(cls, instances_number: int):
        """Method checking if n instance existing in db"""
        instances_list = cls.table.all()
        return len(instances_list) >= instances_number

    def update(self, **kwargs):
        """Method updating model instance with kwargs informations"""
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.save()


