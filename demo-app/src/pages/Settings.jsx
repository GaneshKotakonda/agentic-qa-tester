export default function Settings({ email }) {
  return (
    <main className="workspace-main" aria-labelledby="settings-title">
      <div className="page-heading">
        <h1 id="settings-title" data-testid="settings-title">Settings</h1>
        <p>View your demo account details.</p>
      </div>
      <section className="content-card" aria-labelledby="account-title">
        <h2 id="account-title">Account settings</h2>
        <dl className="account-details">
          <div><dt>Email</dt><dd>{email}</dd></div>
          <div><dt>Account type</dt><dd>Demo account</dd></div>
        </dl>
      </section>
    </main>
  );
}
