# Postman collection (Wiener Netze Smartmeter)

This folder contains a Postman collection and a sample environment that mirror the API calls used by the integration.

## Files
- `WienerNetzeSmartmeter.postman_collection.json`: Postman collection with all API calls and auth steps.
- `env.sample.json`: Sample Postman environment with default URLs and placeholder values.
- `bruno.env.sample.json`: Sample Bruno environment (JSON) with the same variables, for Bruno conversions.

## Quick start
1. Import `WienerNetzeSmartmeter.postman_collection.json` into Postman.
2. Import `env.sample.json` as an environment and fill in the placeholders (username, password, tokens, IDs, dates).
3. Run the requests in the **Auth** folder to obtain an access token and API keys.
4. Call the B2C/B2B/ALT endpoints using the same environment.

## Step-by-step auth + consumption flow (with outputs)
Use this order to obtain a bearer token and then fetch daily consumption. Each step lists the
variables you must provide and the values you should extract for the next step.

1. **Auth Login Page** (GET `{{auth_url}}/auth?...`)
   - Provide: `client_id`, `redirect_uri`, `response_type`, `response_mode`, `scope`,
     `code_challenge`, `code_challenge_method`.
   - Result: HTML login page with a form action URL.
   - Extract: set `auth_action_url` (the `<form action="...">` value).
2. **Auth Login Action** (POST `{{auth_action_url}}`)
   - Provide: `username`, `login`.
   - Result: advances to the password step (typically another login form response).
3. **Auth Login Submit** (POST `{{auth_action_url}}`)
   - Provide: `username`, `password`.
   - Result: redirect response containing an authorization `code` in the URL fragment.
   - Extract: set `auth_code` (the `code` value from the redirect).
4. **Auth Token** (POST `{{auth_url}}/token`)
   - Provide: `grant_type`, `client_id`, `redirect_uri`, `code` (`auth_code`), `code_verifier`.
   - Result: JSON with `access_token` and `refresh_token`.
   - Extract: set `access_token`.
5. **App Config** (GET `https://smartmeter-web.wienernetze.at/assets/app-config.json`)
   - Provide: `Authorization: Bearer {{access_token}}`.
   - Result: JSON with `b2cApiKey` and `b2bApiKey`.
   - Extract: set `b2c_api_key`, `b2b_api_key`.
6. **Zaehlpunkte** (GET `{{b2c_api_url}}/zaehlpunkte`)
   - Provide: `Authorization: Bearer {{access_token}}`,
     `X-Gateway-APIKey: {{b2c_api_key}}`.
   - Result: list of meters (zaehlpunkte) and customer IDs.
   - Extract: set `customer_id`, `zaehlpunktnummer`.
7. **Daily consumption** (choose one)
   - **B2C verbrauchRaw**: GET
     `{{b2c_api_url}}/messdaten/{{customer_id}}/{{zaehlpunktnummer}}/verbrauchRaw`
     with `dateFrom`, `dateTo`, `granularity=DAY`.
   - **B2B messwerte**: GET
     `{{b2b_api_url}}/zaehlpunkte/{{customer_id}}/{{zaehlpunktnummer}}/messwerte`
     with `datumVon`, `datumBis`, `wertetyp=DAY`.
   - Both use `Authorization: Bearer {{access_token}}` and the matching `X-Gateway-APIKey`.

## Bruno conversions
If you convert this collection to Bruno, import `bruno.env.sample.json` as a Bruno environment.
Bruno expects a `variables` array (not Postman’s `values` array), so the Postman `env.sample.json`
won’t load directly.

### Bruno pre-request script (PKCE)
If you want Bruno to auto-generate `code_verifier` and `code_challenge`:
1. Open any request in Bruno (or the collection).
2. Go to **Scripts → Pre Request**.
3. Paste the script below and run the request once to populate the environment.
   (This uses the Web Crypto API available in Bruno scripting.)
4. The values are written into the active environment as `code_verifier` and `code_challenge`.
   You can view them in the environment editor and the script logs them in the console.

```javascript
const base64UrlEncode = (bytes) => {
  let binary = '';
  bytes.forEach((b) => {
    binary += String.fromCharCode(b);
  });
  return btoa(binary)
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=+$/g, '');
};

const randomBytes = (length) => {
  const bytes = new Uint8Array(length);
  crypto.getRandomValues(bytes);
  return bytes;
};

const sha256 = async (value) => {
  const encoder = new TextEncoder();
  const data = encoder.encode(value);
  const digest = await crypto.subtle.digest('SHA-256', data);
  return new Uint8Array(digest);
};

(async () => {
  const verifierBytes = randomBytes(32);
  const codeVerifier = base64UrlEncode(verifierBytes);
  const challengeBytes = await sha256(codeVerifier);
  const codeChallenge = base64UrlEncode(challengeBytes);

  bru.setEnvVar('code_verifier', codeVerifier);
  bru.setEnvVar('code_challenge', codeChallenge);
  console.log('PKCE generated', { codeVerifier, codeChallenge });
})();
```

## Auth notes
- **Auth login page** and **token exchange** use **no auth** (form-encoded body only).
- All API calls use **Bearer** authentication with `{{access_token}}`.
- B2C/B2B endpoints additionally require `X-Gateway-APIKey` headers.

## PKCE helper (Postman pre-request script)

Paste this into a **collection** or **request** pre-request script to auto-generate
`code_verifier` and `code_challenge` and store them in the active environment:

```javascript
const randomBytes = (size) => {
  const bytes = new Uint8Array(size);
  for (let i = 0; i < size; i += 1) {
    bytes[i] = Math.floor(Math.random() * 256);
  }
  return bytes;
};

const base64UrlEncode = (bytes) => {
  const base64 = btoa(String.fromCharCode(...bytes));
  return base64.replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/g, "");
};

const sha256 = async (data) => {
  const encoder = new TextEncoder();
  const digest = await crypto.subtle.digest("SHA-256", encoder.encode(data));
  return new Uint8Array(digest);
};

(async () => {
  const verifierBytes = randomBytes(32);
  const codeVerifier = base64UrlEncode(verifierBytes);
  const challengeBytes = await sha256(codeVerifier);
  const codeChallenge = base64UrlEncode(challengeBytes);

  pm.environment.set("code_verifier", codeVerifier);
  pm.environment.set("code_challenge", codeChallenge);
  console.log("PKCE generated", { codeVerifier, codeChallenge });
})();
```
