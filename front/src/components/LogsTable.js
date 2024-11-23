import { useState, useEffect } from 'react';

export default function LogsTable({ logs }) {
    return (
        <div className="overflow-hidden rounded-xl relative border border-white/10 bg-[#121212]">
            <div className="absolute inset-0">
                <div className="absolute inset-0 bg-gradient-to-tl from-[#00ff94] via-[#00ff9415] to-transparent opacity-20" />
                <div className="absolute inset-0 bg-gradient-to-tl from-[#00ff94] via-transparent to-transparent opacity-10" />
            </div>
            <div className="relative z-10 p-6 border-b border-white/10">
                <h2 className="text-white text-xl font-semibold">Attack Logs</h2>
            </div>
            <div className="relative z-10 overflow-x-auto">
                <table className="min-w-full divide-y divide-white/10">
                    <thead className="bg-black/40">
                        <tr>
                            <th className="px-6 py-4 text-left text-xs font-medium text-[#00ff94] uppercase tracking-wider">
                                Timestamp
                            </th>
                            <th className="px-6 py-4 text-left text-xs font-medium text-[#00ff94] uppercase tracking-wider">
                                IP
                            </th>
                            <th className="px-6 py-4 text-left text-xs font-medium text-[#00ff94] uppercase tracking-wider">
                                Type of Attack
                            </th>
                            <th className="px-6 py-4 text-left text-xs font-medium text-[#00ff94] uppercase tracking-wider">
                                Status
                            </th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-white/10">
                        {logs.map((log, index) => (
                            <tr
                                key={index}
                                className={`
                                    transition-colors duration-150
                                    ${log.blocked
                                        ? 'bg-red-900/20 hover:bg-red-900/30'
                                        : 'hover:bg-white'
                                    }
                                `}
                            >
                                <td className="px-6 py-4 whitespace-nowrap text-sm">
                                    <span className={log.blocked ? 'text-red-200' : 'text-gray-300'}>
                                        {new Date(log.timestamp).toLocaleString()}
                                    </span>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm font-mono">
                                    <span className={log.blocked ? 'text-red-200' : 'text-gray-300'}>
                                        {log.ip}
                                    </span>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm">
                                    <span className={log.blocked ? 'text-red-200' : 'text-gray-300'}>
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
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
} 