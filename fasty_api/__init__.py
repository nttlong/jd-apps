import fasty
import fasty.JWT
fasty.JWT.set_connection_string(fasty.config.db.connection_string())
from . import api_files
from . import api_files_content
from . import api_file_thumb
# from . import api_system_config
from . import api_apps_register
from . import api_apps_edit
from . import api_apps_list
from . import api_apps_update
from . import api_accounts_register
from . import api_accounts_login
from . import api_accounts_current_user
from fastapi_jwt_auth import AuthJWT
from fastapi import FastAPI, HTTPException, Depends, Request
import fasty

import db_connection
