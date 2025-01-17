from openbb_terminal.rich_config import console
from openbb_terminal.session import (
    local_model as Local,
    session_model,
)
from openbb_terminal.session.user import User


def get_session(email: str, password: str, token: str, save: bool):
    session = ""

    if token:
        console.print("Creating session from token.")
        session = session_model.create_session_from_token(token, save)

    if not session:
        console.print("Creating session from email and password.")
        session = session_model.create_session(email, password, save)

    if not (isinstance(session, dict) and session):
        raise Exception("Failed to create session.")

    return session


def login(
    email: str = "", password: str = "", token: str = "", keep_session: bool = False
):
    """
    Login and load user info.
    If there is a saved session it will be used (this can be achieved by `keep_session=True`).
    If there's not a local session,
    the user can use either email and password or the OpenBB Personal Access Token.

    Parameters
    ----------
    email : str
        The email.
    password : str
        The password.
    token : str
        The OpenBB Personal Access Token.
    keep_session : bool
        Keep the session, i.e., next time the user logs in,
        there is no need to enter the email and password or the token.

    Examples
    --------
    >>> from openbb_terminal.sdk import openbb
    >>> openbb.login(email="your_email", password="your_password")
    """

    session = Local.get_session()

    if not session:
        session = get_session(email, password, token, keep_session)
    else:
        console.print("Using saved session to login.")

    if session_model.login(session) in [
        session_model.LoginStatus.FAILED,
        session_model.LoginStatus.NO_RESPONSE,
    ]:
        raise Exception("Login failed.")

    console.print("[green]Login successful.[/green]")


def logout():
    """
    Logout and clear session.

    Examples
    --------
    >>> from openbb_terminal.sdk import openbb
    >>> openbb.logout()
    """
    session_model.logout(
        auth_header=User.get_auth_header(),
        token=User.get_token(),
        guest=User.is_guest(),
    )


def whoami():
    """
    Display user info.

    Examples
    --------
    >>> from openbb_terminal.sdk import openbb
    >>> openbb.whoami()
    """
    User.whoami()
