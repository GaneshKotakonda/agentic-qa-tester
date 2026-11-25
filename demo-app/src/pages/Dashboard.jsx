export default function Dashboard({ email }) {
  return (
    <main className="workspace-main" aria-labelledby="dashboard-title">
      <div className="page-heading">
        <h1 id="dashboard-title" data-testid="dashboard-title">Dashboard</h1>
        <p>Welcome to the demo workspace.</p>
      </div>
      <section className="content-card" aria-labelledby="session-title">
        <h2 id="session-title">Your session</h2>
        <p className="session-status"><span aria-hidden="true" /> Signed in</p>
        <p className="session-email">{email}</p>
      </section>
    </main>
  );
}
