import LogsTable from "../components/LogsTable";
import AttackChart from "../components/AttackChart";
import TitleHeader from "../components/TitleHeader";
import { useState, useEffect } from 'react';

export default function Home() {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    fetch('/api/logs')
      .then(response => response.json())
      .then(data => {
        const sortedLogs = data.logs.sort((a, b) =>
          new Date(b.timestamp) - new Date(a.timestamp)
        );
        setLogs(sortedLogs);
      })
      .catch(error => console.error('Error loading logs:', error));
  }, []);

  return (
    <div className="min-h-screen bg-[#121212] text-white">
      <div className="container mx-auto p-6 space-y-6">
        <TitleHeader />
        <AttackChart logs={logs} />
        <LogsTable logs={logs} />
      </div>
    </div>
  );
}