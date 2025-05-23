import os
import random
import string
from configparser import BasicInterpolation, ConfigParser

from office365.runtime.auth.client_credential import ClientCredential
from office365.runtime.auth.user_credential import UserCredential


def create_unique_name(prefix):
    # type: (str) -> str
    return prefix + "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(8)
    )


def create_unique_file_name(prefix, ext):
    return ".".join([create_unique_name(prefix), ext])


class SecEnvInterpolation(BasicInterpolation):
    secure_vars_env = os.environ.get("office365_python_sdk_securevars", None)
    if not secure_vars_env:
        raise EnvironmentError(
            "The environment variable 'office365_python_sdk_securevars' is not set."
        )

    secure_vars = secure_vars_env.split(";")

    def before_get(self, parser, section, option, value, defaults):
        value = super(SecEnvInterpolation, self).before_get(
            parser, section, option, value, defaults
        )
        if option == "password":
            return self.secure_vars[1]
        elif option == "client_secret":
            return self.secure_vars[3]
        else:
            return value


def load_settings():
    cp = ConfigParser(interpolation=SecEnvInterpolation())
    root_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(root_dir, "settings.cfg")
    cp.read(config_file)
    return cp


settings = load_settings()

# shortcuts
test_tenant_name = settings.get("default", "tenant_prefix")
test_tenant = settings.get("default", "tenant")

test_client_id = settings.get("client_credentials", "client_id")
test_client_secret = settings.get("client_credentials", "client_secret")


test_client_credentials = ClientCredential(
    settings.get("client_credentials", "client_id"),
    settings.get("client_credentials", "client_secret"),
)

test_user_credentials = UserCredential(
    settings.get("user_credentials", "username"),
    settings.get("user_credentials", "password"),
)

test_admin_credentials = UserCredential(
    settings.get("user_credentials", "username"),
    settings.get("user_credentials", "password"),
)

test_site_url = settings.get("default", "site_url")
test_root_site_url = settings.get("default", "root_site_url")
test_team_site_url = settings.get("default", "team_site_url")
test_admin_site_url = settings.get("default", "admin_site_url")

test_user_principal_name = settings.get("users", "test_user1")
test_user_principal_name_alt = settings.get("users", "test_user2")
test_admin_principal_name = settings.get("users", "test_user3")

test_cert_thumbprint = settings.get("certificate_credentials", "thumbprint")
test_cert_path = "{0}/selfsigncert.pem".format(os.path.dirname(__file__))

test_username = settings.get("user_credentials", "username")
test_password = settings.get("user_credentials", "password")
