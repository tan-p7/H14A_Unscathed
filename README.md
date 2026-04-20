# Despatch Advice API

Lambda-backed API for managing despatch advices (UBL XML) with JSON auth routes. The Lambda handler is invoked by API Gateway.

## API Endpoints

Configure the following routes in API Gateway to trigger this Lambda:

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/auth/register` | Register a user. JSON body: `email`, `password` (min 8 chars), `name`. Returns `userId`, `email`, `name` (201). |
| `POST` | `/api/auth/login` | Login. JSON body: `email`, `password`. Returns `accessToken`, `tokenType`, `expiresIn` (200). |
| `POST` | `/api/auth/logout` | Logout. Header `Authorization: Bearer <accessToken>`. Revokes token server-side if revocations table is configured (204). |
| `OPTIONS` | `/api/auth/*` or under `/api/despatch/*` | CORS preflight; returns 204 when `CORS_ALLOW_ORIGIN` is set (see below). |
| `GET`  | `/api/despatch/health` | Health check (public). |
| `POST` | `/api/despatch/despatch-advice` | Create despatch (requires `Authorization: Bearer`). |
| `GET`  | `/api/despatch/despatch-advice` | List all (requires Bearer). |
| `GET`  | `/api/despatch/despatch-advice/{despatch-id}` | Retrieve by ID (requires Bearer). |
| `PUT` | `/api/despatch/despatch-advice/{despatch-id}` | Update (requires Bearer). |
| `DELETE` | `/api/despatch/despatch-advice/{despatch-id}` | Delete (requires Bearer). |

## Authentication

- After **login**, send `Authorization: Bearer <accessToken>` on all despatch routes.
- JWT is signed with **HS256**. Set **`JWT_SECRET`** in Lambda (use **AWS Secrets Manager** in production; never commit real secrets).
- Optional **`JWT_EXPIRY_SECONDS`** (default `3600`).

## DynamoDB: Users table (create in AWS; not created by this repo)

| Attribute | Type | Role |
|-----------|------|------|
| `user_id` | String | Partition key (UUID). |
| `email` | String | Normalized lowercase; **GSI** `EmailIndex` partition key for login lookup. |
| `password_hash` | String | bcrypt hash. |
| `name` | String | Display name. |
| `created_at` | String | ISO8601 timestamp. |

- **GSI name:** `EmailIndex` on `email` (project all attributes or at least `user_id`, `password_hash`, `name`).

**Lambda environment (placeholders until infra exists):**

- `USERS_TABLE_NAME` — e.g. `TODO_USERS_TABLE` until you create the table.
- `USERS_EMAIL_GSI_NAME` — default `EmailIndex` if omitted.
- `JWT_SECRET` — **TODO:** set a strong secret in deployment.
- `REVOCATIONS_TABLE_NAME` — optional; for server-side logout. Table: partition key `jti` (String), numeric **`ttl`** attribute for [DynamoDB TTL](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html) (Unix epoch seconds).

**IAM:** Grant Lambda `dynamodb:Query` (Users + GSI), `dynamodb:PutItem` on Users, and if using revocations: `dynamodb:PutItem`, `dynamodb:GetItem` on that table.

## CORS (SPA)

Set **`CORS_ALLOW_ORIGIN`** to your frontend origin (e.g. `https://app.example.com`), or `*` for local dev only. Responses then include `Access-Control-Allow-Origin`, `-Headers`, and `-Methods`. Configure matching **OPTIONS** in API Gateway or rely on Lambda `OPTIONS` handling.

## API Gateway / Infrastructure

- **Lambda handler**: `lambda_function.lambda_handler` (or the module path matching your deployment).
- **POST despatch-advice:** body is UBL Order XML; include `Authorization: Bearer`.
- **Path parameter** `despatch-id` for GET, PUT, DELETE on `/api/despatch/despatch-advice/{despatch-id}`.

## Running tests

```bash
pip install boto3 pytest pytest-cov xmlschema PyJWT bcrypt
PYTHONPATH=. pytest src/tests -v
```

CI installs the same dependencies as in [`.github/workflows/ci.yml`](.github/workflows/ci.yml).
