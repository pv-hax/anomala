import LogsTable from "../components/LogsTable";
import AttackChart from "../components/AttackChart";
import TitleHeader from "../components/TitleHeader";
import { useState, useEffect } from "react";

// Helper to format dates consistently
const formatLogs = (logs) => {
  return logs.map((log) => ({
    ...log,
    timestamp: new Date(log.timestamp).toISOString(),
    formattedDate: new Date(log.timestamp).toUTCString()
  }));
};

export const getServerSideProps = async () => {
  const response = await fetch(
    "http://ec2-100-26-197-252.compute-1.amazonaws.com:8000/attack-logs"
  );
  const data = await response.json();
  const formattedLogs = formatLogs(data.logs);

  return { props: { initialLogs: formattedLogs } };
};

export default function Home({ initialLogs }) {
  const [logs, setLogs] = useState(initialLogs);
  const [dataSource, setDataSource] = useState("live");

  const fetchSampleLogs = async () => {
    try {
      const response = await fetch('/api/logs');
      const data = await response.json();
      const formattedLogs = formatLogs(data.logs);
      setLogs(formattedLogs);
    } catch (error) {
      console.error('Error fetching sample logs:', error);
    }
  };

  const toggleDataSource = () => {
    const newSource = dataSource === "live" ? "sample" : "live";
    setDataSource(newSource);

    if (newSource === "sample") {
      fetchSampleLogs();
    } else {
      setLogs(initialLogs);
    }
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
            {dataSource === "live" ? "Switch to Sample Data" : "Switch to Live Data"}
          </button>
        </div>
        <AttackChart logs={logs} />
        <LogsTable logs={logs} />
      </div>
    </div>
  );
}
