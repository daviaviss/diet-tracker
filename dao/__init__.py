from contextlib import contextmanager
from mvc.models import get_session


@contextmanager
def use_session(commit=False):
    session = get_session()
    try:
        yield session
        if commit:
            session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
