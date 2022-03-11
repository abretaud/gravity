from enum import Enum
from typing import (
    Any,
    Dict,
    Optional,
)
from pydantic import (
    BaseModel,
    BaseSettings,
    Field,
)


class LogLevel(str, Enum):
    debug = "DEBUG"
    info = "INFO"
    warning = "WARNING"
    error = "ERROR"


class AppServer(str, Enum):
    gunicorn = "gunicorn"
    unicornherder = "unicornherder"


class CelerySettings(BaseModel):

    concurrency: int = Field(2, ge=0, description="Number of Celery Workers to start.")
    loglevel: LogLevel = Field(LogLevel.debug, description="Log Level to use for Celery Worker.")
    extra_args: str = Field(default="", description="Extra arguments to pass to Celery command line.")

    class Config:
        use_enum_values = True


class GunicornSettings(BaseModel):
    bind: str = Field(default="localhost:8080", description="The socket to bind. A string of the form: ``HOST``, ``HOST:PORT``, ``unix:PATH``, ``fd://FD``. An IP is a valid HOST.")
    workers: int = Field(default=1, ge=1, description=" Controls the number of Galaxy application processes Gunicorn will spawn. Increased web performance can be attained by increasing this value. If Gunicorn is the only application on the server, a good starting value is the number of CPUs * 2 + 1. 4-12 workers should be able to handle hundreds if not thousands of requests per second.")
    timeout: int = Field(default=300, ge=0, description="Gunicorn workers silent for more than this many seconds are killed and restarted. Value is a positive number or 0. Setting it to 0 has the effect of infinite timeouts by disabling timeouts for all workers entirely. If you disable the ``preload`` option workers need to have finished booting within the timeout.")
    extra_args: str = Field(default="", description="Extra arguments to pass to Gunicorn command line.")
    preload: bool = Field(default=True, description="Use Gunicorn's --preload option to fork workers after loading the Galaxy Application. Consumes less memory when multiple processes are configured.")


class GxItProxySettings(BaseModel):
    enable: bool = Field(default=False, description="Set to true to start gx-it-proxy")
    ip: str = Field(default="localhost", description="Public-facing IP of the proxy")
    port: int = Field(default=4002, description="Public-facing port of the proxy")
    sessions: str = Field(default="database/interactivetools_map.sqlite", description="Routes file to monitor. Should be set to the same path as ``interactivetools_map`` in the ``galaxy:`` section.")
    verbose: bool = Field(default=True, description="Include verbose messages in gx-it-proxy")
    forward_ip: Optional[str] = Field(default=None, description="Forward all requests to IP. This is an advanced option that is only needed when proxying to remote interactive tool container that cannot be reached through the local network.")
    forward_port: Optional[int] = Field(default=None, description="Forward all requests to port. This is an advanced option that is only needed when proxying to remote interactive tool container that cannot be reached through the local network.")
    reverse_proxy: Optional[bool] = Field(default=False, description="Cause the proxy to rewrite location blocks with its own port. This is an advanced option that is only needed when proxying to remote interactive tool container that cannot be reached through the local network.")


class Settings(BaseSettings):
    """
    Configuration for gravity process manager. Configure gravity in this section. ``uwsgi:`` section will be ignored if Galaxy is started via gravity commands (e.g ``./run.sh``, ``galaxy`` or ``galaxyctl``).
    """
    galaxy_root: Optional[str] = Field(None, description="Specify Galaxy's root directory. gravity will attempt to find the root directory, but you can set the directory explicitly with this option.")
    log_dir: Optional[str] = Field(None, description="Set to a directory that should contain log files for the processes controlled by gravity. If not specified defaults to ``<state_dir>/logs``.")
    virtualenv: Optional[str] = Field(None, description="Set to Galaxy's virtualenv directory. If not specified, gravity assumes all processes are on PATH.")
    app_server: AppServer = Field(AppServer.gunicorn, description="Select the application server. ``gunicorn`` is the default application server. ``unicornherder`` is a production-oriented manager for (G)unicorn servers that automates zero-downtime Galaxy server restarts, similar to uWSGI Zerg Mode used in the past.")
    instance_name: str = Field(default="_default_", description="Override the default instance name, this is hidden from you when running a single instance.")
    gunicorn: GunicornSettings = Field(default={}, description="Configuration for Gunicorn.")
    celery: CelerySettings = Field(default={}, description="Configuration for Celery Processes.")
    gx_it_proxy: GxItProxySettings = Field(default={}, description="Configuration for gx-it-proxy.")
    handlers: Dict[str, Dict[str, Any]] = Field(default={}, description="Configure dynamic handlers in this section. See https://docs.galaxyproject.org/en/latest/admin/scaling.html#dynamically-defined-handlers for details.")

    class Config:
        env_prefix = "gravity_"
        env_nested_delimiter = "."
        case_sensitive = False
        use_enum_values = True
