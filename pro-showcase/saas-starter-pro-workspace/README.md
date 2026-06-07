# SaaS Starter Pro

Production SaaS backend starter built with RapidKit + Workspai.

This is the public showcase page for the private Pro workspace. The full implementation, customer archive, release evidence, and buyer documentation live in the private `rapidkit-examples-pro` repository.

## Who It Is For

Teams building SaaS backends that need a faster path to:

- Auth, sessions, OAuth, users, teams, and profiles
- Billing and Stripe-oriented workflows
- Admin operations
- Webhook ingestion and replay-oriented processing
- Worker/service separation
- Release evidence and customer-ready handoff documentation

## Free vs Pro

| Area | Free SaaS Starter | SaaS Starter Pro |
| --- | --- | --- |
| Source access | Public example workspace | Private customer package |
| Scope | Learning/reference scaffold | Buyer-ready SaaS foundation |
| Services | API, admin, NestJS parity, webhooks | API, admin, workers, webhooks, hardened docs and gates |
| Evidence | Open-source docs and code | Gate evidence, customer archive, checksum, buyer docs |
| Best for | Evaluation and learning | Saving implementation time on commercial products |

## Start Free

Use the public SaaS Starter Workspace first:

```bash
git clone https://github.com/rapidkitlabs/rapidkit-examples.git
cd rapidkit-examples/saas-starter-workspace
npx rapidkit doctor --workspace
```

## Pro Delivery Standard

The Pro product is only eligible for sale when it has:

- a private release manifest linked from `products.json`
- `README.customer.md`
- a customer archive and SHA-256 checksum under the private release lane
- `make factory-validate`
- `make release-check PRODUCT=saas-starter-pro-workspace`
- documented setup, smoke checks, and support boundaries

Until then, this page is a public product showcase and upgrade path, not a source release.
