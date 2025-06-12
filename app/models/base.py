from sqlalchemy.orm import declarative_base

Base = declarative_base()

class ReprMixin:
    def __repr__(self):
        classname = self.__class__.__name__
        field_pairs = []
        for key in self.__mapper__.c.keys():
            value = getattr(self, key, None)
            field_pairs.append(f"{key}={repr(value)}")
        return f"<{classname}({', '.join(field_pairs)})>"