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
import src.modules.free.essentials.logging
import src.modules.free.essentials.deployment
import src.modules.free.essentials.middleware
import src.modules.free.database.db_postgres
import src.modules.free.auth.core
from src.modules.free.cache.redis import (
    AsyncRedis,
    DEFAULTS,
    RedisClient,
    RedisSyncClient,
    SyncRedis,
    build_redis_url,
    check_redis_connection,
    describe_cache,
    get_redis,
    get_redis_metadata,
    get_redis_sync,
    list_features,
    redis_dependency,
    refresh_vendor_module,
    register_redis,
)
from src.modules.free.auth import core as core
from src.modules.free.cache.redis import AsyncRedis as AsyncRedis, DEFAULTS as DEFAULTS, RedisClient as RedisClient, RedisSyncClient as RedisSyncClient, SyncRedis as SyncRedis, build_redis_url as build_redis_url, check_redis_connection as check_redis_connection, describe_cache as describe_cache, get_redis as get_redis, get_redis_metadata as get_redis_metadata, get_redis_sync as get_redis_sync, list_features as list_features, redis_dependency as redis_dependency, refresh_vendor_module as refresh_vendor_module, register_redis as register_redis
from src.modules.free.database import db_postgres as db_postgres
from src.modules.free.essentials import deployment as deployment
from src.modules.free.essentials import logging as logging
from src.modules.free.essentials import middleware as middleware
from src.modules.free.essentials.settings import BaseSettings as BaseSettings, CustomConfigSource as CustomConfigSource, Field as Field, Settings as Settings, configure_fastapi_app as configure_fastapi_app, get_settings as get_settings, settings as settings, settings_dependency as settings_dependency
from src.modules.free.security import security_headers as security_headers
import src.modules.free.security.security_headers
# <<<inject:module-init>>>