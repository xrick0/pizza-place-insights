import sqlalchemy as sa
from sqlalchemy.orm import as_declarative


@as_declarative()
class ModelBase(object):
    __table__: sa.schema.Table

    # Possibilita acesso ao "server_default"
    __mapper_args__ = {"eager_defaults": True}

    @property
    def _id_str(self) -> str:
        ids = sa.inspect(self).identity
        if ids:
            return "-".join([str(x) for x in ids]) if len(ids) > 1 else str(ids[0])
        else:
            return "None"

    def __repr__(self) -> str:
        # get id like '#123'
        id_str = ("#" + self._id_str) if self._id_str else ""
        # join class name, id and repr_attrs
        return f"<{self.__class__.__name__} {id_str}>"
