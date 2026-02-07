# Postman collection (Wiener Netze Smartmeter)

This folder contains a Postman collection and a sample environment that mirror the API calls used by the integration.

## Files
- `WienerNetzeSmartmeter.postman_collection.json`: Postman collection with all API calls and auth steps.
- `env.sample.json`: Sample Postman environment with default URLs and placeholder values.

## Quick start
1. Import `WienerNetzeSmartmeter.postman_collection.json` into Postman.
2. Import `env.sample.json` as an environment and fill in the placeholders (username, password, tokens, IDs, dates).
3. Run the requests in the **Auth** folder to obtain an access token and API keys.
4. Call the B2C/B2B/ALT endpoints using the same environment.

## Auth notes
- **Auth login page** and **token exchange** use **no auth** (form-encoded body only).
- All API calls use **Bearer** authentication with `{{access_token}}`.
- B2C/B2B endpoints additionally require `X-Gateway-APIKey` headers.
