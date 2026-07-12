import path from 'node:path';
import { registerAs } from '@nestjs/config';

/* eslint-disable @typescript-eslint/no-require-imports */

// Dynamic vendor loader - resolves .rapidkit/vendor in project root or uses
// RAPIDKIT_VENDOR_ROOT if set. This avoids hard-coded relative imports into
// src/.rapidkit and makes generated projects robust and portable.
const VENDOR_ROOT_ENV = 'RAPIDKIT_VENDOR_ROOT';
const VENDOR_MODULE = 'settings';
const VENDOR_VERSION = '0.1.45';
const VENDOR_CONFIGURATION_RELATIVE = 'src/config/configuration';

function resolveVendorRoot(): string {
  const override = process.env[VENDOR_ROOT_ENV];
  if (override && override.trim().length > 0) {
    return path.resolve(override);
  }
  return path.resolve(process.cwd(), '.rapidkit', 'vendor');
}

function resolveVendorModule() {
  const vendorPath = path.join(
    resolveVendorRoot(),
    VENDOR_MODULE,
    VENDOR_VERSION,
    VENDOR_CONFIGURATION_RELATIVE,
  );
  // Attempt to dynamically load a vendor-provided configuration. If the
  // vendor snapshot is not present in .rapidkit/vendor (common when the
  // 'settings' module wasn't installed), fail gracefully instead of
  // allowing require() to throw and crash the application.
  try {
    // eslint-disable-next-line @typescript-eslint/no-var-requires, global-require
    return require(vendorPath);
  } catch (err: unknown) {
    const e = err as { code?: string } | undefined;
    // Only suppress MODULE_NOT_FOUND / ENOENT for the vendor path so other
    // unexpected errors still surface to the user.
    if (e && (e.code === 'MODULE_NOT_FOUND' || e.code === 'ENOENT')) {
      // eslint-disable-next-line no-console
      console.warn(`WARN: vendor settings not found at ${vendorPath} - continuing without vendor settings`);
      return null;
    }
    throw err;
  }
}

const _vendor = resolveVendorModule();

export default registerAs('app', () => ({
  name: process.env.APP_NAME ?? "Saas Nest",
  env: process.env.NODE_ENV ?? 'development',
  host: process.env.HOST ?? '0.0.0.0',
  port: parseInt(process.env.PORT ?? '8000', 10),
  logLevel: (() => {
    const raw = (process.env.LOG_LEVEL ?? 'log').toLowerCase();
    if (raw === 'info') return 'log';
    if (raw === 'warning') return 'warn';
    return raw;
  })(),
  // <<<inject:configuration>>>
  // <<<inject:configuration:rate_limiting_settings_fields_nestjs:start>>>
    rateLimiting: {
      enabled: process.env.RATE_LIMIT_ENABLED === '1' || process.env.RATE_LIMIT_ENABLED?.toLowerCase() === 'true',
      backend: process.env.RATE_LIMIT_BACKEND ?? 'memory',
      redisUrl: process.env.RATE_LIMIT_REDIS_URL ?? null,
      redisPrefix: process.env.RATE_LIMIT_REDIS_PREFIX ?? 'rate-limit',
      trustForwardedFor:
        process.env.RATE_LIMIT_TRUST_FORWARDED_FOR === '1' ||
        process.env.RATE_LIMIT_TRUST_FORWARDED_FOR?.toLowerCase() === 'true',
      forwardedForHeader: process.env.RATE_LIMIT_FORWARDED_FOR_HEADER ?? 'X-Forwarded-For',
      identityHeader: process.env.RATE_LIMIT_IDENTITY_HEADER ?? 'X-RateLimit-Identity',
      defaultRuleName: process.env.RATE_LIMIT_DEFAULT_RULE_NAME ?? 'default',
      defaultLimit: Number.parseInt(process.env.RATE_LIMIT_DEFAULT_LIMIT ?? '120', 10),
      defaultWindow: Number.parseInt(process.env.RATE_LIMIT_DEFAULT_WINDOW ?? '60', 10),
      defaultScope: process.env.RATE_LIMIT_DEFAULT_SCOPE ?? 'identity',
      defaultPriority: Number.parseInt(process.env.RATE_LIMIT_DEFAULT_PRIORITY ?? '100', 10),
      defaultBlockSeconds:
        process.env.RATE_LIMIT_DEFAULT_BLOCK_SECONDS === undefined
          ? null
          : Number.parseInt(process.env.RATE_LIMIT_DEFAULT_BLOCK_SECONDS, 10),
      headerLimit: process.env.RATE_LIMIT_HEADER_LIMIT ?? 'X-RateLimit-Limit',
      headerRemaining: process.env.RATE_LIMIT_HEADER_REMAINING ?? 'X-RateLimit-Remaining',
      headerReset: process.env.RATE_LIMIT_HEADER_RESET ?? 'X-RateLimit-Reset',
      headerRetryAfter: process.env.RATE_LIMIT_HEADER_RETRY_AFTER ?? 'Retry-After',
      headerRule: process.env.RATE_LIMIT_HEADER_RULE ?? 'X-RateLimit-Rule',
      rulesJson: process.env.RATE_LIMIT_RULES_JSON ?? '',
    },
  // <<<inject:configuration:rate_limiting_settings_fields_nestjs:end>>>
  // <<<inject:configuration:redis_settings_fields_nestjs:start>>>
    redis: {
      url: process.env.REDIS_URL ?? "redis://localhost:6379/0",
      preconnect:
        process.env.REDIS_PRECONNECT !== undefined
          ? ["1", "true", "yes", "on"].includes(
              process.env.REDIS_PRECONNECT.toLowerCase(),
            )
          : false,
      retries: Number.parseInt(
        process.env.REDIS_CONNECT_RETRIES ?? "3",
        10,
      ),
      backoffBase: Number.parseFloat(
        process.env.REDIS_CONNECT_BACKOFF_BASE ?? "0.5",
      ),
      ttl: Number.parseInt(process.env.CACHE_TTL ?? "3600", 10),
    },
  // <<<inject:configuration:redis_settings_fields_nestjs:end>>>
  // <<<inject:configuration:db_postgres_settings_fields_nestjs:start>>>
  // PostgreSQL module configuration for NestJS kits
  dbPostgres: {
    url: process.env.DATABASE_URL ?? "postgresql://postgres:postgres@localhost:5432/myapp",
    testUrl: process.env.TEST_DATABASE_URL ?? "postgresql://postgres:postgres@localhost:5432/myapp_test",
    pool: {
      size: process.env.DB_POOL_SIZE ? Number(process.env.DB_POOL_SIZE) : 10,
      maxOverflow: process.env.DB_MAX_OVERFLOW ? Number(process.env.DB_MAX_OVERFLOW) : 20,
      timeoutSeconds: process.env.DB_POOL_TIMEOUT ? Number(process.env.DB_POOL_TIMEOUT) : 30,
      recycleSeconds: process.env.DB_POOL_RECYCLE ? Number(process.env.DB_POOL_RECYCLE) : 3600,
    },
    echo: process.env.DB_ECHO ? process.env.DB_ECHO === "true" : false,
    expireOnCommit: process.env.DB_EXPIRE_ON_COMMIT
      ? process.env.DB_EXPIRE_ON_COMMIT === "true"
      : false,
  },
  // <<<inject:configuration:db_postgres_settings_fields_nestjs:end>>>
  // <<<inject:configuration:oauth_settings_fields_nestjs:start>>>
    OAUTH_REDIRECT_BASE_URL: process.env.OAUTH_REDIRECT_BASE_URL,
  
    OAUTH_STATE_TTL_SECONDS:
      process.env.OAUTH_STATE_TTL_SECONDS == null
        ? undefined
        : Number.parseInt(process.env.OAUTH_STATE_TTL_SECONDS, 10),
  
    OAUTH_STATE_CLEANUP_INTERVAL:
      process.env.OAUTH_STATE_CLEANUP_INTERVAL == null
        ? undefined
        : Number.parseInt(process.env.OAUTH_STATE_CLEANUP_INTERVAL, 10),
  
    // Keep as raw string to avoid crashing on invalid JSON
    OAUTH_PROVIDERS: process.env.OAUTH_PROVIDERS,
  // <<<inject:configuration:oauth_settings_fields_nestjs:end>>>
}));

// Provide a safe default settingsConfiguration if no vendor snapshot is present
// so generated projects still boot even when the optional settings module
// hasn't been installed.
const defaultSettings = () => ({
  ENV: process.env.NODE_ENV ?? 'development',
  DEBUG: process.env.DEBUG === '1' || process.env.DEBUG?.toLowerCase() === 'true',
  PROJECT_NAME: process.env.APP_NAME ?? 'Saas Nest',
  SECRET_KEY: process.env.SECRET_KEY ?? 'development-only-change-me',
  VERSION: process.env.APP_VERSION ?? '0.0.1',
  ALLOWED_HOSTS: (process.env.ALLOWED_HOSTS ?? '*').split(',').map((s) => s.trim()).filter(Boolean),
  CONFIG_FILES: [],
  CONFIG_REFRESH_INTERVAL: Number.parseInt(process.env.CONFIG_REFRESH_INTERVAL ?? '60', 10),
  VAULT_URL: null,
  AWS_REGION: null,
  HOT_RELOAD_ENABLED:
    process.env.HOT_RELOAD_ENABLED === '1' || process.env.HOT_RELOAD_ENABLED?.toLowerCase() === 'true',
  HOT_RELOAD_ENV_ALLOWLIST: (process.env.HOT_RELOAD_ENV_ALLOWLIST ?? '').split(',').map((s) => s.trim()).filter(Boolean),
});

export const settingsConfiguration =
  _vendor?.settingsConfiguration ?? _vendor?.default?.settingsConfiguration ?? (() => defaultSettings());
