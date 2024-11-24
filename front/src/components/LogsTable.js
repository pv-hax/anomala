import { useState, useEffect } from 'react';

export default function LogsTable({ logs }) {
    const [sortConfig, setSortConfig] = useState({
        key: 'timestamp',
        direction: 'desc'
    });
    const [sortedLogs, setSortedLogs] = useState(logs);

    // Sort function
    const sortLogs = (key) => {
        let direction = 'asc';
        if (sortConfig.key === key && sortConfig.direction === 'asc') {
            direction = 'desc';
        }

        const sorted = [...logs].sort((a, b) => {
            if (key === 'timestamp') {
                return direction === 'asc'
                    ? new Date(a[key]) - new Date(b[key])
                    : new Date(b[key]) - new Date(a[key]);
            }

            if (a[key] < b[key]) return direction === 'asc' ? -1 : 1;
            if (a[key] > b[key]) return direction === 'asc' ? 1 : -1;
            return 0;
        });

        setSortedLogs(sorted);
        setSortConfig({ key, direction });
    };

    // Update sorted logs when props change
    useEffect(() => {
        setSortedLogs(logs);
    }, [logs]);

    // Sort indicator component
    const SortIndicator = ({ columnKey }) => {
        if (sortConfig.key !== columnKey) return <span className="ml-1">↕</span>;
        return <span className="ml-1">{sortConfig.direction === 'asc' ? '↑' : '↓'}</span>;
    };

    const handleUnban = async (ip) => {
        try {
            const response = await fetch('http://ec2-100-26-197-252.compute-1.amazonaws.com:8000/unban-all', {
                method: 'POST',
            });
            if (!response.ok) throw new Error('Failed to unban IP');
            // You might want to add some success feedback here
        } catch (error) {
            console.error('Error unbanning IP:', error);
            // You might want to add some error feedback here
        }
    };

    return (
        <div className="overflow-hidden rounded-xl relative border border-white/10 bg-black">
            <div className="absolute inset-0">
                <div className="absolute inset-0 bg-gradient-to-bl from-white via-white/10 to-transparent opacity-[0.02]" />
                <div className="absolute inset-0 bg-gradient-to-bl from-white via-transparent to-transparent opacity-[0.03]" />
                <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-white via-white/10 to-transparent opacity-[0.08]" />
            </div>
            <div className="relative z-10 p-6 border-b border-white/10">
                <h2 className="font-inter font-light text-2xl text-white mb-2">Logs</h2>
            </div>
            <div className="relative z-10 overflow-x-auto">
                <table className="min-w-full divide-y divide-white/10">
                    <thead className="bg-black/40">
                        <tr>
                            <th
                                className="px-6 py-4 text-left text-xs font-medium text-white uppercase tracking-wider cursor-pointer hover:text-white/80"
                                onClick={() => sortLogs('timestamp')}
                            >
                                Timestamp
                                <SortIndicator columnKey="timestamp" />
                            </th>
                            <th
                                className="px-6 py-4 text-left text-xs font-medium text-white uppercase tracking-wider cursor-pointer hover:text-white/80"
                                onClick={() => sortLogs('ip')}
                            >
                                IP
                                <SortIndicator columnKey="ip" />
                            </th>
                            <th
                                className="px-6 py-4 text-left text-xs font-medium text-white uppercase tracking-wider cursor-pointer hover:text-white/80"
                                onClick={() => sortLogs('type_of_attack')}
                            >
                                Type of Attack
                                <SortIndicator columnKey="type_of_attack" />
                            </th>
                            <th
                                className="px-6 py-4 text-left text-xs font-medium text-white uppercase tracking-wider cursor-pointer hover:text-white/80"
                                onClick={() => sortLogs('blocked')}
                            >
                                Status
                                <SortIndicator columnKey="blocked" />
                            </th>
                            <th className="px-6 py-4 text-left text-xs font-medium text-white uppercase tracking-wider">
                                Actions
                            </th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-white/10">
                        {sortedLogs.map((log, index) => (
                            <tr
                                key={index}
                                className="transition-colors duration-150 hover:bg-white/5"
                            >
                                <td className="px-6 py-4 whitespace-nowrap text-sm">
                                    <span className="text-gray-300">
                                        {log.formattedDate}
                                    </span>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm font-mono">
                                    <span className="text-gray-300">
                                        {log.ip}
                                    </span>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm">
                                    <span className="text-gray-300">
                                        {log.type_of_attack}
                                    </span>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm">
                                    <span className={`
                                        px-3 py-1 rounded-full text-xs font-medium
                                        ${log.blocked
                                            ? 'bg-red-900/50 text-red-200 border border-red-700'
                                            : 'bg-[#00ff9415] text-[#00ff94] border border-[#00ff94]/20'
                                        }
                                    `}>
                                        {log.blocked ? 'Blocked' : 'Not Blocked'}
                                    </span>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm">
                                    {log.blocked && (
                                        <button
                                            onClick={() => handleUnban(log.ip)}
                                            className="px-3 py-1 rounded-lg bg-red-900/30 text-red-200 border border-red-700/30 hover:bg-red-900/50 hover:border-red-700/50 transition-colors duration-200"
                                        >
                                            Unban
                                        </button>
                                    )}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
} 