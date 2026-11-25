# Agentic QA Tester Demo

A standalone React app for practicing browser automation against a predictable login flow. It runs independently of the FastAPI backend.

## Run locally

Use Node.js 20.19+ on the 20.x release line, or Node.js 22.12+.

From the project root:

```sh
cd demo-app
npm ci
npm run dev
```

Open [http://localhost:5173](http://localhost:5173). Vite exits if port 5173 is already in use.

To create a production build, run `npm run build` from `demo-app`.

## Demo credentials

These credentials are public and for local testing only. The app checks them in the browser and keeps sign-in state in React memory. Reloading the page clears that state.

| Field | Value |
| --- | --- |
| Email | `qa@example.test` |
| Password | `demo-password` |

## Routes and expected behavior

| Route | Behavior |
| --- | --- |
| `/` | Redirects to Login for guests and Dashboard for signed-in users. |
| `/login` | Correct credentials open Dashboard. Incorrect credentials show an alert with the text `Invalid email or password`. Native form validation blocks submission with empty fields or an invalid email format. Signed-in users are redirected to Dashboard. |
| `/dashboard` | Shows the welcome message and session details. Guests are redirected to Login. |
| `/settings` | Shows account details. Guests are redirected to Login. |

Use the workspace navigation to switch between Dashboard and Settings. The Logout button on either page clears the session and returns to Login.

## Playwright selectors

Use Python Playwright's `page.get_by_test_id("email-input")` syntax for these selectors.

| Test ID | Element |
| --- | --- |
| `email-input` | Email field |
| `password-input` | Password field |
| `login-button` | Login form submit button |
| `login-error` | Invalid credentials message with `role="alert"` |
| `dashboard-title` | Dashboard heading |
| `settings-title` | Settings heading |
| `dashboard-link` | Dashboard navigation link |
| `settings-link` | Settings navigation link |
| `logout-button` | Logout button on both protected pages |
