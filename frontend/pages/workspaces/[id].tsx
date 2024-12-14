import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import axios from 'axios';

const WorkspaceDetails = () => {
  const [workspace, setWorkspace] = useState<{ id: number; name: string } | null>(null);
  const [url, setUrl] = useState('');
  const [scrapedContent, setScrapedContent] = useState<string>('');
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();
  const { id } = router.query;

  useEffect(() => {
    const fetchWorkspace = async () => {
      const token = localStorage.getItem('token');
      if (!token) {
        setError('Please log in to view the workspace.');
        return;
      }

      try {
        const res = await axios.get(`http://localhost:5000/workspaces/${id}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        setWorkspace(res.data);
      } catch (error) {
        setError('Error fetching workspace details.');
      }
    };

    if (id) {
      fetchWorkspace();
    }
  }, [id]);

  const handleScrape = async () => {
    const token = localStorage.getItem('token');
    if (!token) {
      setError('Please log in to scrape content.');
      return;
    }

    try {
      const res = await axios.post(
        `http://localhost:5000/workspaces/${id}/scrape`,
        { url },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setScrapedContent(res.data.content);
      setError(null);
    } catch (error) {
      setError('Error scraping content.');
    }
  };

  if (error) {
    return <p>{error}</p>;
  }

  if (!workspace) {
    return <p>Loading...</p>;
  }

  return (
    <div>
      <h1>Workspace Details</h1>
      <p>ID: {workspace.id}</p>
      <p>Name: {workspace.name}</p>

      <h2>Scrape Content</h2>
      <input
        type="text"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        placeholder="Enter URL to scrape"
      />
      <button onClick={handleScrape}>Scrape</button>
      {scrapedContent && (
        <div>
          <h3>Scraped Content:</h3>
          <pre>{scrapedContent}</pre>
        </div>
      )}
    </div>
  );
};

export default WorkspaceDetails;