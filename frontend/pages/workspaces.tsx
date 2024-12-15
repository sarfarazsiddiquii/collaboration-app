import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import axios from 'axios';

const Workspaces = () => {
  const [workspaces, setWorkspaces] = useState<{ id: number; name: string }[]>([]);
  const [name, setName] = useState('');
  const [code, setCode] = useState('');
  const router = useRouter();

  const fetchWorkspaces = async () => {
    const token = localStorage.getItem('token');
    try {
      const res = await axios.get('http://localhost:5000/workspaces', {
        headers: { Authorization: `Bearer ${token}` },
      });
      setWorkspaces(res.data);
    } catch (error) {
      console.error('Error fetching workspaces:', error);
    }
  };

  const createWorkspace = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const token = localStorage.getItem('token');
    try {
      const res = await axios.post(
        'http://localhost:5000/workspaces',
        { name, code },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setName('');
      setCode('');
      fetchWorkspaces();
      router.push(`/workspaces/${res.data.workspace_id}`);
    } catch (error) {
      console.error('Error creating workspace:', error);
    }
  };

  useEffect(() => {
    fetchWorkspaces();
  }, []);

  return (
    <div>
      <h1>Workspaces</h1>
      <form onSubmit={createWorkspace}>
        <input
          type="text"
          placeholder="Workspace Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Workspace Code"
          value={code}
          onChange={(e) => setCode(e.target.value)}
          required
        />
        <button type="submit">Create Workspace</button>
      </form>

      <ul>
        {workspaces.map((ws) => (
          <li key={ws.id}>
            <a href={`/workspaces/${ws.id}`}>{ws.name}</a>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Workspaces;
