import { useState } from 'react';

export default function Login({ account, onLogin }) {
  const [hasError, setHasError] = useState(false);

  function handleSubmit(event) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    setHasError(!onLogin(form.get('email'), form.get('password')));
  }

  return (
    <main className="login-screen">
      <div className="login-card">
        <div className="login-content">
          <div className="brand">
            <span className="brand-mark" aria-hidden="true" />
            <span>Agentic QA Tester</span>
          </div>
          <div className="login-heading">
            <h1>Sign in</h1>
            <p>Use the demo account to open your workspace.</p>
          </div>
          <form
            className="login-form"
            onSubmit={handleSubmit}
            onChange={() => setHasError(false)}
          >
            <div className="field">
              <label htmlFor="email">Email</label>
              <input
                id="email"
                name="email"
                type="email"
                autoComplete="username"
                placeholder="you@example.test"
                required
                data-testid="email-input"
              />
            </div>
            <div className="field">
              <label htmlFor="password">Password</label>
              <input
                id="password"
                name="password"
                type="password"
                autoComplete="current-password"
                required
                data-testid="password-input"
              />
            </div>
            {hasError && (
              <p className="login-error" role="alert" data-testid="login-error">
                Invalid email or password
              </p>
            )}
            <button className="button button-primary" type="submit" data-testid="login-button">
              Login
            </button>
          </form>
        </div>
        <aside className="demo-panel" aria-labelledby="demo-account-title">
          <div className="browser-illustration" aria-hidden="true">
            <div className="browser-toolbar"><span /><span /><span /></div>
            <div className="browser-body">
              <div className="browser-check"><span /></div>
              <div className="browser-line" />
              <div className="browser-line browser-line-short" />
            </div>
          </div>
          <div className="demo-details">
            <h2 id="demo-account-title">Demo account</h2>
            <p>Credentials for local testing only.</p>
            <dl className="demo-credentials">
              <div><dt>Email</dt><dd><code>{account.email}</code></dd></div>
              <div><dt>Password</dt><dd><code>{account.password}</code></dd></div>
            </dl>
          </div>
        </aside>
      </div>
    </main>
  );
}
