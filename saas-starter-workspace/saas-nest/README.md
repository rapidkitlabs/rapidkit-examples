# saas-nest

Polyglot microservice demonstrating FastAPI/NestJS coexistence in production SaaS architecture. NestJS 11 service generated with [RapidKit](https://github.com/rapidkitlabs/rapidkit-core).

**Related:** Part of [saas-starter-workspace](../README.md) - Production SaaS architecture with 4 microservices.

---

## ⚡ Quick Start

> **Recommended Node version:** `20.19.6` (`.nvmrc` and `.node-version` included)

```bash
# Bootstrap dependencies
npx workspai init

# Copy env templates and install hooks
./bootstrap.sh

# Start development server on port 8002
npx workspai dev --port 8002
# Or: make dev

# Run tests
npx workspai test
# Or: make test

# Lint and type-check
make lint
make typecheck
```

**API running at:** http://localhost:8002

**Endpoints:**
- API Docs: http://localhost:8002/docs
- Health Check: http://localhost:8002/api/health
- Module Health: http://localhost:8002/api/health/module/*

---

## 🎯 Why This Service Exists

### Polyglot Microservices Pattern

**Demonstrates:**
- FastAPI and NestJS coexist in same workspace
- Shared authentication patterns across frameworks
- Framework-agnostic module design
- TypeScript + Python teams collaborate

**Real-world use cases:**
- Node.js team joins Python-based SaaS
- Migrate specific services to TypeScript
- Compare framework performance/DX
- Proof-of-concept for language migration

---

## 🏗️ Features

### Authentication (NestJS Implementation)

Same auth flow as `saas-api`, implemented in TypeScript:

- **Register/Login:**
  - `POST /auth/register` - Create user account
  - `POST /auth/login` - Get access token
  - `GET /auth/me` - Get current user profile

- **Password Hashing:**
  - SHA256 for demo (use bcrypt/argon2 in production)
  - In-memory user storage (swap with database)

- **Token Management:**
  - Bearer token authentication
  - Token-to-user mapping
  - Profile management

### User Profiles

- **Profile Operations:**
  - `GET /users/profile` - Get user profile
  - `PUT /users/profile` - Update profile fields
  - Timezone, display name, biography

### Health & Monitoring

- **Module-level health checks:**
  - `GET /api/health/module/auth-core`
  - `GET /api/health/module/users-core`
  - `GET /api/health/module/settings`

---

## 📦 Installed Modules

### RapidKit NestJS Modules

**`auth-core`** - Authentication module (NestJS)
- Password hashing and verification
- Token generation
- Health checks

**`users-core`** - User management (NestJS)
- User service with in-memory storage
- Profile management
- Health monitoring

**`settings`** - Configuration module (NestJS)
- Environment-based configuration
- Validation with Joi
- ConfigModule integration

---

## 📁 Project Structure

```
saas-nest/
├── src/
│   ├── main.ts              # Bootstrap application
│   ├── app.module.ts        # Root module with injection anchors
│   ├── app.controller.ts    # Root controller
│   ├── app.service.ts       # Root service
│   ├── auth/
│   │   ├── auth.module.ts
│   │   ├── auth.controller.ts  # Register, login, me
│   │   ├── auth.service.ts     # Auth logic (116 lines)
│   │   ├── users.controller.ts # Profile endpoints
│   │   └── entities/           # User/profile entities
│   ├── config/
│   │   ├── configuration.ts    # Settings loader
│   │   └── validation.ts       # Joi schema
│   ├── examples/
│   │   └── examples.module.ts  # Notes demo
│   ├── health/
│   │   └── health.controller.ts
│   └── modules/                # RapidKit NestJS modules
│       └── rapidkit/
│           ├── auth-core/
│           ├── users-core/
│           └── settings/
├── test/
│   ├── app.e2e-spec.ts
│   └── jest-e2e.json
├── docs/
│   └── README.md
├── nest-cli.json
├── package.json
├── tsconfig.json
└── eslint.config.cjs
```

### NestJS Architecture

- **Modules** – Feature-based organization
- **Controllers** – HTTP request handlers
- **Services** – Business logic
- **Providers** – Dependency injection

**Injection markers:**
```typescript
// <<<inject:module-imports>>> - Add module imports
// <<<inject:bootstrap-hooks>>> - Add startup hooks
```

---

## 🔧 Code Examples

### Authentication Service (TypeScript)

```typescript
@Injectable()
export class AuthService {
  private usersByEmail = new Map<string, UserRecord>();
  private tokens = new Map<string, string>();

  register(payload: { email: string; password: string }) {
    const email = payload.email.trim().toLowerCase();
    
    if (this.usersByEmail.has(email)) {
      throw new Error('Email already registered');
    }

    const user: UserRecord = {
      id: `user_${randomBytes(8).toString('hex')}`,
      email,
      passwordHash: this.hash(payload.password),
    };

    this.usersByEmail.set(email, user);
    const token = this.issueToken(user.id);

    return {
      user: this.publicUser(user),
      access_token: token,
      token_type: 'bearer'
    };
  }

  private hash(raw: string): string {
    return createHash('sha256').update(raw).digest('hex');
  }
}
```

**Compare with FastAPI (`saas-api`):**
- Same flow: hash → store → issue token
- TypeScript types vs Pydantic models
- NestJS DI vs FastAPI Depends()
- Both use service pattern

### Controller Pattern

```typescript
@Controller('auth')
export class AuthController {
  constructor(private readonly authService: AuthService) {}

  @Post('register')
  register(@Body() payload: { email: string; password: string }) {
    try {
      return this.authService.register(payload);
    } catch (error) {
      throw new HttpException(error.message, HttpStatus.CONFLICT);
    }
  }

  @Get('me')
  me(@Headers('authorization') authorization?: string) {
    const token = extractBearer(authorization);
    if (!token) {
      throw new HttpException('Auth required', HttpStatus.UNAUTHORIZED);
    }
    return this.authService.me(token);
  }
}
```

---

## 🧪 Usage Examples

### Register and Login

```bash
# Register user
curl -X POST http://localhost:8002/auth/register \
  -H 'Content-Type: application/json' \
  -d '{
    "email": "nest@example.com",
    "password": "SecurePass123!",
    "fullName": "NestJS User"
  }'

# Response:
# {
#   "user": {"id": "user_abc", "email": "nest@example.com"},
#   "access_token": "48_char_hex_token",
#   "token_type": "bearer"
# }

# Get profile
curl http://localhost:8002/auth/me \
  -H 'Authorization: Bearer 48_char_hex_token'
```

### Profile Management

```bash
# Get profile
curl http://localhost:8002/users/profile \
  -H 'Authorization: Bearer <token>'

# Update profile
curl -X PUT http://localhost:8002/users/profile \
  -H 'Authorization: Bearer <token>' \
  -H 'Content-Type: application/json' \
  -d '{
    "displayName": "Updated Name",
    "timezone": "America/New_York",
    "biography": "NestJS developer"
  }'
```

---

## 🚀 Add More Modules

```bash

# Add database (when available for NestJS)
npx workspai add module db_postgres

# Add Redis
npx workspai add module redis

# Add logging
npx workspai add module logging
```

---

## 🔐 Environment Configuration

**`.env` template:**
```bash
# Application
NODE_ENV=development
PORT=8002
HOST=0.0.0.0

# Auth
RAPIDKIT_AUTH_CORE_SALT_ROUNDS=10

# Swagger
RAPIDKIT_ENABLE_SWAGGER=1

# Settings Module
RAPIDKIT_SETTINGS_AUTO_RELOAD=true
```

---

## 🧪 Testing

```bash
# Run all tests
npx workspai test
# Or: yarn test

# E2E tests
yarn test:e2e

# Coverage
yarn test:cov

# Watch mode
yarn test:watch
```

**Test files:**
- `test/app.e2e-spec.ts` - E2E tests
- `src/**/*.spec.ts` - Unit tests

---

## 🏗️ Production Deployment

### Docker

```bash
# Build image
docker build -t saas-nest:latest .

# Run container
docker run -p 8002:8002 saas-nest:latest
```

### Environment

```bash
NODE_ENV=production
PORT=8002
RAPIDKIT_ENABLE_SWAGGER=0  # Disable in production
```

### Health Checks

Configure orchestrator:
- **Liveness:** `GET /api/health` (200 = alive)
- **Readiness:** `GET /api/health/readyz` (200 = ready)

---

## 🔍 Framework Comparison

### FastAPI (`saas-api`) vs NestJS (`saas-nest`)

| Feature | FastAPI | NestJS |
|---------|---------|--------|
| Language | Python | TypeScript |
| Async | Native async/await | RxJS observables |
| DI | Function dependencies | Class-based DI |
| Validation | Pydantic | class-validator |
| OpenAPI | Auto-generated | Decorators |
| Modules | File-based | Class decorators |

**Both frameworks:**
- Suitable for production-oriented architecture exercises; deployment still
  requires the hardening and evidence gates documented by this workspace
- Auto-generated API docs
- Type safety (Pydantic vs TypeScript)
- Health check patterns
- Module injection systems

---

## 📚 Learn More

**Architecture guides:**
- [Workspace Overview](../README.md)
- [Code Walkthrough (Dev.to)](https://dev.to/rapidkit/build-production-saas-code-walkthrough-13)

**Compare with FastAPI:**
- [saas-api](../saas-api/README.md) - Same features, Python implementation
- [saas-webhooks](../saas-webhooks/README.md) - FastAPI webhook processor

**NestJS resources:**
- [NestJS Documentation](https://docs.nestjs.com)
- [RapidKit NestJS Modules](https://www.workspai.dev/docs/cli/modules/nestjs)

---

## 🛠️ Troubleshooting

**Port conflict:**
```bash
# Always run on port 8002
npx workspai dev --port 8002
```

**Node version mismatch:**
```bash
# Use nvm/asdf
nvm use
# or
asdf install nodejs 20.19.6
```

**Module not found errors:**
```bash
# Reinstall dependencies
npx workspai init
# or
yarn install
```

**Need help?**
- Documentation: https://getrapidkit.com/docs
- GitHub Issues: https://github.com/rapidkitlabs/rapidkit-core/issues
- NestJS Discord: https://discord.gg/nestjs
