import LogsTable from "../components/LogsTable";
import AttackChart from "../components/AttackChart";
import TitleHeader from "../components/TitleHeader";
import { useState, useEffect } from 'react';

export default function Home() {
  const [logs, setLogs] = useState([]);
  const [dataSource, setDataSource] = useState('sample');

  const fetchData = async () => {
    try {
      if (dataSource === 'sample') {
        const response = await fetch('/api/logs');
        const data = await response.json();
        const sortedLogs = data.logs.sort((a, b) =>
          new Date(b.timestamp) - new Date(a.timestamp)
        );
        setLogs(sortedLogs);
      } else {
        const response = await fetch(`${process.env.NEXT_PUBLIC_NGROK_URL}/attack-logs`, {
          headers: new Headers({
            "ngrok-skip-browser-warning": "69420",
          }),
        });
        const data = await response.json();
        console.log("DATA", data);
        const sortedLogs = data.logs.sort((a, b) =>
          new Date(b.timestamp) - new Date(a.timestamp)
        );
        setLogs(sortedLogs);
      }
    } catch (error) {
      console.error('Error loading logs:', error);
    }
  };

  useEffect(() => {
    fetchData();
  }, [dataSource]);

  const toggleDataSource = () => {
    setDataSource(prev => prev === 'sample' ? 'api' : 'sample');
  };

  return (
    <div className="min-h-screen bg-[#000000] text-white">
      <div className="container mx-auto p-6 space-y-6">
        <TitleHeader />
        <div className="flex justify-end mb-4">
          <button
            onClick={toggleDataSource}
            className="px-4 py-2 rounded-lg bg-[#00ff94] text-black font-medium hover:bg-[#00ff94]/90 transition-colors"
          >
            {dataSource === 'sample' ? 'Switch to Live Data' : 'Switch to Sample Data'}
          </button>
        </div>
        <AttackChart logs={logs} />
        <LogsTable logs={logs} />
      </div>
    </div>
  );
}