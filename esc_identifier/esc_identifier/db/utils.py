def db_model_repr(self):
    """Create a automatic meaningful repr for db.Model classes
    Usage example:
    class MyClass(Base):
        __repr__ = db_model_repr
    """
    fields = [
        str(column).split('.')[-1]
        for column
        in self.__table__.columns
    ]
    values = [
        f"{field}={getattr(self, field)}"
        for field
        in fields
    ]
    stringified_values = ', '.join(values)
    return f"{self.__class__.__name__}({stringified_values})"
