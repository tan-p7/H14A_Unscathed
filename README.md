# Despatch Advice API

Lambda-backed API for managing despatch advices (UBL XML). The Lambda handler is invoked by API Gateway.

## API Endpoints

Configure the following routes in API Gateway to trigger this Lambda:

| Method | Path | Description |
|--------|------|-------------|
| `GET`  | `/api/despatch/health` | Health check; returns 200 when the service and DynamoDB table are operational. |
| `POST` | `/api/despatch/despatch-advice` | Create a despatch advice. Request body must be a valid UBL Order XML (2.4). Returns the generated Despatch Advice XML and stores it in DynamoDB. |
| `GET`  | `/api/despatch/despatch-advice/{despatch-id}` | Retrieve a despatch advice by ID. |
| `PUT` / `PATCH` | `/api/despatch/despatch-advice/{despatch-id}` | Update a despatch advice by ID. Request body: JSON with optional `deliveredQuantity`, `backorderQuantity`, `backorderReason`, `note`. |
| `DELETE` | `/api/despatch/despatch-advice/{despatch-id}` | Delete a despatch advice by ID. |

## API Gateway / Infrastructure

- **Lambda handler**: `lambda_function.lambda_handler` (or the module path matching your deployment).
- **POST `/api/despatch/despatch-advice`**:  
  - Integration: Lambda proxy integration.  
  - Request body: raw UBL Order XML (e.g. `Content-Type: application/xml` or `text/xml`).  
  - Ensure the Lambda receives the body (e.g. “Use Lambda Proxy integration” or map the body to `event.body`).
- **Path parameter** for GET, PUT, PATCH, DELETE: `despatch-id` (e.g. resource path `/api/despatch/despatch-advice/{despatch-id}`).
- **DynamoDB**: Table name `Despatch-Advices`, partition key `despatch_id` (String). Stored attribute for the XML: `despatch_ubl` (String).

## Running tests

```bash
pip install boto3 pytest pytest-cov xmlschema
pytest src/tests -v
```
