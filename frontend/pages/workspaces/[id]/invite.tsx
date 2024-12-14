import { useState } from 'react';
import { useRouter } from 'next/router';
import axios from 'axios';

const InvitePage = () => {
  const [email, setEmail] = useState('');
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();
  const { id } = router.query;

  const sendInvite = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const token = localStorage.getItem('token');
    if (!token) {
      setError('Please log in to send an invite.');
      return;
    }

    try {
      await axios.post(
        `http://localhost:5000/workspaces/${id}/invite`,
        { email },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setEmail('');
      setError(null);
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.status === 401) {
        setError('Unauthorized. Please log in again.');
        localStorage.removeItem('token');
      } else {
        setError('An error occurred while sending the invite.');
      }
    }
  };

  return (
    <div>
      <h1>Invite to Workspace</h1>
      <form onSubmit={sendInvite}>
        <input
          type="email"
          placeholder="Team Member's Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <button type="submit">Send Invite</button>
      </form>
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
};

export default InvitePage;
