import sys
from contextlib import contextmanager
from mvc.models import get_session


@contextmanager
def use_session(commit=False):
    session = get_session()
    try:
        yield session
        if commit:
            session.commit()
    except Exception as exc:
        session.rollback()
        # Registra o erro no stderr para depuração sem expor ao usuário
        print(f"[DB ERROR] {type(exc).__name__}: {exc}", file=sys.stderr)
        raise
    finally:
        session.close()
