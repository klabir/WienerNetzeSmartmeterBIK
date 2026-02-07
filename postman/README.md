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

## Bruno conversions
If you convert this collection to Bruno, import `bruno.env.sample.json` as a Bruno environment.
Bruno expects a `variables` array (not Postman’s `values` array), so the Postman `env.sample.json`
won’t load directly.

### Bruno pre-request script (PKCE)
If you want Bruno to auto-generate `code_verifier` and `code_challenge`:
1. Open any request in Bruno (or the collection).
2. Go to **Scripts → Pre Request**.
3. Paste the script below and run the request once to populate the environment.

```javascript
const crypto = require('crypto');

const base64UrlEncode = (buffer) => (
  buffer.toString('base64')
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=+$/g, '')
);

const codeVerifier = base64UrlEncode(crypto.randomBytes(32));
const codeChallenge = base64UrlEncode(
  crypto.createHash('sha256').update(codeVerifier).digest()
);

bru.setEnvVar('code_verifier', codeVerifier);
bru.setEnvVar('code_challenge', codeChallenge);
console.log('PKCE generated', { codeVerifier, codeChallenge });
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
