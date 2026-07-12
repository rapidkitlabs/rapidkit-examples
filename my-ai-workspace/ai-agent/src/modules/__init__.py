"""Module bootstrap namespace."""

from src.modules.free.essentials.settings import (
    BaseSettings,
    CustomConfigSource,
    Field,
    Settings,
    configure_fastapi_app,
    get_settings,
    settings,
    settings_dependency,
)
from src.modules.free.ai import ai_assistant as ai_assistant
from src.modules.free.essentials import deployment as deployment
from src.modules.free.essentials import logging as logging
from src.modules.free.essentials import middleware as middleware
from src.modules.free.essentials.settings import BaseSettings as BaseSettings, CustomConfigSource as CustomConfigSource, Field as Field, Settings as Settings, configure_fastapi_app as configure_fastapi_app, get_settings as get_settings, settings as settings, settings_dependency as settings_dependency
import src.modules.free.ai.ai_assistant
import src.modules.free.essentials.deployment
import src.modules.free.essentials.logging
import src.modules.free.essentials.middleware
# <<<inject:module-init>>>