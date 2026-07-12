<!-- <<<inject:module-snippet>>> -->
<!-- <<<inject:module-snippet:auth_core_quickstart:start>>>
# Auth Core module quick actions
<!-- <<<inject:module-snippet:auth_core_quickstart:end>>>
<!-- <<<inject:module-snippet:redis_quickstart:start>>>
# Redis module quick actions
rapidkit module validate redis
rapidkit module info redis
<!-- <<<inject:module-snippet:redis_quickstart:end>>>
<!-- <<<inject:module-snippet:security_headers_quickstart:start>>>

# Security Headers FastAPI Setup Snippet
# This snippet demonstrates how to register the Security Headers middleware

from fastapi import FastAPI

from src.modules.free.security.security_headers.security_headers import (
	SecurityHeadersSettings,
	register_fastapi,
)

app = FastAPI()

security_headers_config = SecurityHeadersSettings(
	content_security_policy="default-src 'self'; img-src 'self' data:; object-src 'none'",
	permissions_policy={
		"geolocation": [],
		"camera": [],
		"microphone": [],
	},
)

register_fastapi(app, config=security_headers_config)
<!-- <<<inject:module-snippet:security_headers_quickstart:end>>>
