import { useEffect, useState } from 'react';
import Link from 'next/link';

export default function Home() {
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    const storedToken = localStorage.getItem('token');
    setToken(storedToken);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    setToken(null);
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>Welcome to the App</h1>

      {token ? (
        <>
          <p>You are logged in!</p>
          <nav>
            <ul>
              <li>
                <Link href="/scrape">Scrape a Website</Link>
              </li>
              <li>
                <button onClick={handleLogout} style={{ marginTop: '10px' }}>
                  Logout
                </button>
              </li>
            </ul>
          </nav>
        </>
      ) : (
        <>
          <p>Please log in to access the features.</p>
          <nav>
            <ul>
              <li>
                <Link href="/login">Login</Link>
              </li>
              <li>
                <Link href="/signup">Signup</Link>
              </li>
            </ul>
          </nav>
        </>
      )}
    </div>
  );
}
