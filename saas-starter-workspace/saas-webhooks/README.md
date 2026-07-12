# saas-webhooks

Dedicated webhook processor with Stripe-style signature verification, event logging, and replay capability. Minimal FastAPI service generated with [RapidKit](https://github.com/rapidkitlabs/rapidkit-core).

**Related:** Part of [saas-starter-workspace](../README.md) - Production SaaS architecture with 4 microservices.

---

## ⚡ Quick Start

```bash
# Bootstrap dependencies
npx workspai init

# Copy env templates and install hooks
./bootstrap.sh

# Start development server on port 8003
npx workspai dev --port 8003
# Or: make dev

# Run tests
npx workspai test

# Lint and type-check
make lint
make typecheck
```

**API running at:** http://localhost:8003

**Endpoints:**
- API Docs: http://localhost:8003/docs
- Health Check: http://localhost:8003/health
- Webhook Ingestion: `POST /api/webhooks/stripe`
- Event Logs: `GET /api/webhooks/logs`
- Replay Event: `POST /api/webhooks/replay/{event_id}`

---

## 🎯 Why Dedicated Webhook Service?

### Architecture Benefits

**Isolation:**
- Webhook crashes don't affect product API
- Independent scaling for event volume
- Different retry policies than user requests

**Reliability:**
- Background processing doesn't block responses
- Event replay fixes billing errors
- Audit trail for financial events

**Security:**
- Signature verification prevents forgery
- Idempotency prevents duplicate processing
- Rate limiting per webhook source

---

## 🔐 Features

### 1. Stripe Signature Verification

**HMAC-SHA256 validation:**
```python
def _verify_signature(body: bytes, header: str, secret: str) -> bool:
    """Verify Stripe webhook signature."""
    timestamp, signature = _parse_signature_header(header)
    
    # Reconstruct signed payload
    signed_payload = f"{timestamp}.{body.decode()}"
    expected = hmac.new(
        secret.encode(),
        signed_payload.encode(),
        hashlib.sha256
    ).hexdigest()
    
    # Constant-time comparison (prevents timing attacks)
    return hmac.compare_digest(expected, signature)
```

**Security features:**
- HMAC prevents signature forgery
- Timestamp prevents replay attacks
- Constant-time comparison prevents timing side-channels

### 2. Event Logging

**Every webhook is persisted:**
```python
WebhookLogEntry(
    event_id="evt_123",
    event_type="customer.subscription.updated",
    status="queued",
    received_at="2026-02-16T10:23:45Z",
    attempts=0,
    metadata={"provider": "stripe", ...}
)
```

**Log fields:**
- `event_id` - Unique event identifier
- `event_type` - Event type (subscription.updated, etc.)
- `status` - queued, processed, failed, retry_scheduled
- `received_at` - Ingestion timestamp
- `processed_at` - Completion timestamp
- `attempts` - Retry counter
- `replay_count` - Manual replay counter
- `last_error` - Error message if failed

### 3. Background Processing

**FastAPI BackgroundTasks:**
```python
@router.post("/stripe")
async def receive_webhook(
    payload: StripeWebhookRequest,
    background_tasks: BackgroundTasks,
):
    # 1. Verify signature immediately
    # 2. Check idempotency
    # 3. Persist log entry
    # 4. Queue background processing
    background_tasks.add_task(_process_event, payload)
    
    # Return 202 immediately (don't block Stripe)
    return {"status": "accepted", "event_id": payload.id}
```

**Why background tasks:**
- Stripe expects 2xx response within 5 seconds
- Processing can take longer (database, notifications)
- Failures don't block webhook acceptance

### 4. Event Replay (Critical for Billing)

**When you need replay:**
- Handler had a bug → fix code, replay events
- Database was temporarily down
- Need to backfill subscription states after migration

**Replay endpoint:**
```python
@router.post("/replay/{event_id}")
async def replay_event(event_id: str):
    """Reprocess event without calling Stripe."""
    
    event = _EVENTS.get(event_id)
    event.replay_count += 1
    
    # Reconstruct payload from stored data
    replay_payload = StripeWebhookRequest(
        id=event.event_id,
        type=event.event_type,
        data=event.metadata,
    )
    
    background_tasks.add_task(_process_event, replay_payload)
    return {"status": "replay_accepted"}
```

**Replay benefits:**
- No external API calls to Stripe
- Use stored event data
- Track replay count for audit
- Fix billing errors retroactively

### 5. Retry Logic

```python
async def _process_event(event: StripeWebhookRequest):
    """Process with automatic retry."""
    
    record = _EVENTS[event.id]
    max_attempts = int(os.getenv("WEBHOOKS_MAX_RETRIES", "3"))
    record.attempts += 1
    
    try:
        # Process event (send notifications, update DB, etc.)
        await _dispatch_subscription_notifications(event)
        record.status = "processed"
        record.processed_at = _utc_now()
    except Exception as exc:
        record.last_error = str(exc)
        record.status = "failed"
        
        # Schedule retry if under max attempts
        if record.attempts < max_attempts:
            record.status = "retry_scheduled"
```

### 6. Idempotency

```python
# Check for duplicate events (Stripe sends duplicates)
existing = _EVENTS.get(payload.id)
if existing:
    return {
        "status": "duplicate",
        "event_id": payload.id,
        "attempts": existing.attempts
    }
```

**Why idempotency matters:**
- Stripe sends duplicate webhooks
- Network retries can duplicate requests
- Prevents double-charging customers

---

## 📁 Project Structure

```
saas-webhooks/
├── src/
│   ├── main.py              # FastAPI app
│   ├── routing/
│   │   ├── __init__.py
│   │   ├── webhooks.py      # Core logic (210 lines)
│   │   │                    # - Signature verification
│   │   │                    # - Event ingestion
│   │   │                    # - Replay endpoint
│   │   │                    # - Logs endpoint
│   │   ├── health.py
│   │   └── examples.py
│   ├── modules/             # RapidKit modules (optional)
│   └── health/
├── tests/
│   ├── test_webhooks.py     # Signature, ingestion, replay tests
│   └── conftest.py
├── config/
├── .env.example
├── docker-compose.yml
└── Makefile
```

---

## 🔧 Usage Examples

### 1. Send Webhook Event

```bash
# Send Stripe-style webhook (no signature for local testing)
curl -X POST http://localhost:8003/api/webhooks/stripe \
  -H 'Content-Type: application/json' \
  -d '{
    "id": "evt_test_123",
    "type": "customer.subscription.updated",
    "data": {
      "object": {
        "id": "sub_abc123",
        "status": "active",
        "customer": "cus_xyz789"
      }
    }
  }'

# Response:
# {
#   "status": "accepted",
#   "event_id": "evt_test_123"
# }
```

### 2. View Event Logs

```bash
# Get all events
curl http://localhost:8003/api/webhooks/logs | jq

# Response:
# {
#   "items": [
#     {
#       "event_id": "evt_test_123",
#       "event_type": "customer.subscription.updated",
#       "status": "processed",
#       "received_at": "2026-02-16T10:23:45Z",
#       "processed_at": "2026-02-16T10:23:46Z",
#       "attempts": 1,
#       "replay_count": 0
#     }
#   ],
#   "total": 1
# }
```

### 3. Replay Event

```bash
# Replay specific event
curl -X POST http://localhost:8003/api/webhooks/replay/evt_test_123

# Response:
# {
#   "status": "replay_accepted",
#   "event_id": "evt_test_123",
#   "replay_count": 1
# }
```

### 4. Production: Verify Signature

**Generate test signature:**
```python
import hmac, hashlib, json, time

secret = 'whsec_test'
payload = {"id": "evt_sig", "type": "customer.subscription.created"}
body = json.dumps(payload, separators=(',', ':'))
ts = str(int(time.time()))

sig = hmac.new(
    secret.encode(),
    f"{ts}.{body}".encode(),
    hashlib.sha256
).hexdigest()

print(f"Stripe-Signature: t={ts},v1={sig}")
```

**Send with signature:**
```bash
curl -X POST http://localhost:8003/api/webhooks/stripe \
  -H 'Content-Type: application/json' \
  -H 'Stripe-Signature: t=1645123456,v1=abc123...' \
  -d '{"id":"evt_sig","type":"customer.subscription.created",...}'
```

---

## 🔐 Environment Configuration

**`.env` template:**
```bash
# Stripe Configuration
STRIPE_WEBHOOK_SECRET="whsec_test_local_development"
# Get real secret from Stripe Dashboard → Webhooks

# Retry Configuration
WEBHOOKS_MAX_RETRIES=3
WEBHOOKS_RETRY_BACKOFF_BASE=0.5  # seconds

# Notification (optional)
WEBHOOKS_NOTIFY_EMAIL="billing@example.com"
```

**Generate webhook secret:**
```bash
# For local testing
export STRIPE_WEBHOOK_SECRET="whsec_test"

# Production: Get from Stripe Dashboard
# 1. Go to Developers → Webhooks
# 2. Create endpoint: https://yourdomain.com/api/webhooks/stripe
# 3. Copy signing secret (starts with whsec_)
```

---

## 🧪 Testing

```bash
# Run all tests
npx workspai test

# Test specific scenarios
pytest tests/test_webhooks.py::test_signature_verification -v
pytest tests/test_webhooks.py::test_idempotency -v
pytest tests/test_webhooks.py::test_replay -v

# With coverage
pytest --cov=src tests/
```

**Test scenarios covered:**
- ✅ Signature verification (valid/invalid)
- ✅ Idempotency checks
- ✅ Event ingestion and logging
- ✅ Background processing
- ✅ Replay functionality
- ✅ Retry logic
- ✅ Error handling

---

## 🏗️ Production Hardening

### 1. Replace In-Memory Storage

**Current (demo):**
```python
_EVENTS: dict[str, WebhookLogEntry] = {}
```

**Production:**
```python
# Add db_postgres module
npx workspai add module db_postgres

# Create webhooks table
CREATE TABLE webhook_events (
    event_id VARCHAR(255) PRIMARY KEY,
    event_type VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL,
    received_at TIMESTAMP NOT NULL,
    processed_at TIMESTAMP,
    attempts INTEGER DEFAULT 0,
    replay_count INTEGER DEFAULT 0,
    last_error TEXT,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

# Use async SQLAlchemy
async def store_webhook_event(db: AsyncSession, event: WebhookLogEntry):
    db_event = WebhookEvent(**event.model_dump())
    db.add(db_event)
    await db.commit()
```

### 2. Add Exponential Backoff

```python
async def _process_event_with_backoff(event: StripeWebhookRequest):
    """Process with exponential backoff retry."""
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            await _process_event(event)
            break
        except Exception as exc:
            if attempt == max_retries - 1:
                # Send to dead-letter queue
                await send_to_dlq(event)
                await notify_ops_team(event, exc)
                break
            
            # Exponential backoff: 0.5s, 1.5s, 3.5s
            wait = (2 ** attempt) + random.random()
            await asyncio.sleep(wait)
```

### 3. Implement Dead Letter Queue

```python
async def send_to_dlq(event: StripeWebhookRequest):
    """Send permanently failed events to DLQ."""
    
    # Option 1: Database table
    await db.execute(
        "INSERT INTO webhook_dlq (event_id, payload, failed_at) VALUES ($1, $2, NOW())",
        event.id, event.model_dump_json()
    )
    
    # Option 2: Message queue (SQS, RabbitMQ)
    await dlq_client.send(event.model_dump_json())
    
    # Option 3: Log to file for manual replay
    with open(f"dlq/{event.id}.json", "w") as f:
        f.write(event.model_dump_json())
```

### 4. Add Monitoring

```bash
# Add observability module
npx workspai add module observability.core

# Track metrics
webhook_ingested_total.inc()
webhook_processing_duration.observe(duration)
webhook_failed_total.labels(event_type).inc()
```

---

## 📊 Webhook Event Types

### Stripe Subscription Events

**Lifecycle events:**
- `customer.subscription.created`
- `customer.subscription.updated`
- `customer.subscription.deleted`
- `customer.subscription.trial_will_end`

**Payment events:**
- `invoice.paid`
- `invoice.payment_failed`
- `payment_intent.succeeded`
- `payment_intent.payment_failed`

**Customer events:**
- `customer.created`
- `customer.updated`
- `customer.deleted`

---

## 📚 Learn More

**Architecture guides:**
- [Workspace Overview](../README.md)
- [Building Production SaaS Architecture (Medium)](https://medium.com/@rapidkit/building-production-saas-architecture-13)
- [Code Walkthrough (Dev.to)](https://dev.to/rapidkit/build-production-saas-code-walkthrough-13)

**Related services:**
- [saas-api](../saas-api/README.md) - Product API with subscriptions
- [saas-admin](../saas-admin/README.md) - Admin operations
- [saas-nest](../saas-nest/README.md) - NestJS service

**Stripe documentation:**
- [Webhook Best Practices](https://stripe.com/docs/webhooks/best-practices)
- [Signature Verification](https://stripe.com/docs/webhooks/signatures)
- [Event Types](https://stripe.com/docs/api/events/types)

---

## 🛠️ Troubleshooting

**Signature verification fails:**
```bash
# Check webhook secret matches Stripe Dashboard
echo $STRIPE_WEBHOOK_SECRET

# For local testing, disable signature check
# (remove stripe-signature header from curl)
```

**Events not processing:**
```bash
# Check logs
curl http://localhost:8003/api/webhooks/logs | jq '.items[] | select(.status=="failed")'

# Replay failed event
curl -X POST http://localhost:8003/api/webhooks/replay/{event_id}
```

**Port already in use:**
```bash
# Run on different port
npx workspai dev --port 8003
```

**Need help?**
- Documentation: https://getrapidkit.com/docs
- GitHub Issues: https://github.com/rapidkitlabs/rapidkit-core/issues
- Stripe Support: https://support.stripe.com
