import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function AttackChart({ logs }) {
    const getHistogramData = () => {
        const hourlyBins = logs.reduce((acc, log) => {
            const hour = new Date(log.timestamp).getHours();
            acc[hour] = (acc[hour] || 0) + 1;
            return acc;
        }, {});

        return Array.from({ length: 24 }, (_, hour) => ({
            hour: hour,
            frequency: hourlyBins[hour] || 0,
            label: `${hour.toString().padStart(2, '0')}:00`
        }));
    };

    return (
        <div className="w-full p-6 rounded-xl relative overflow-hidden border border-white/10 bg-[#121212]">
            <div className="absolute inset-0">
                <div className="absolute inset-0 bg-gradient-to-tl from-[#00ff94] via-[#00ff9415] to-transparent opacity-20" />
                <div className="absolute inset-0 bg-gradient-to-tl from-[#00ff94] via-transparent to-transparent opacity-10" />
            </div>
            <div className="relative z-10">
                <div className="mb-6">
                    <h2 className="text-white text-xl font-semibold mb-2">Attack Frequency Distribution</h2>
                    <div className="flex gap-4 text-sm">
                        <div className="px-4 py-2 rounded-lg bg-black/40 backdrop-blur-sm border border-white/5">
                            <p className="text-gray-300 mb-1">Total Attacks</p>
                            <p className="text-white text-lg font-semibold">{logs.length}</p>
                        </div>
                        <div className="px-4 py-2 rounded-lg bg-black/40 backdrop-blur-sm border border-white/5">
                            <p className="text-gray-300 mb-1">Peak Hour</p>
                            <p className="text-white text-lg font-semibold">
                                {getHistogramData().reduce((max, curr) =>
                                    curr.frequency > max.frequency ? curr : max
                                ).label}
                            </p>
                        </div>
                    </div>
                </div>
                <div className="h-[300px]">
                    <ResponsiveContainer width="100%" height="100%">
                        <LineChart
                            data={getHistogramData()}
                            margin={{ top: 20, right: 30, left: 20, bottom: 20 }}
                        >
                            <defs>
                                <linearGradient id="lineGradient" x1="1" y1="1" x2="0" y2="0">
                                    <stop offset="0%" stopColor="#00ff94" stopOpacity={0.8} />
                                    <stop offset="100%" stopColor="#00ff94" stopOpacity={0.2} />
                                </linearGradient>
                                <linearGradient id="areaGradient" x1="1" y1="1" x2="0" y2="0">
                                    <stop offset="0%" stopColor="#00ff94" stopOpacity={0.2} />
                                    <stop offset="100%" stopColor="#00ff94" stopOpacity={0.05} />
                                </linearGradient>
                            </defs>
                            <CartesianGrid
                                strokeDasharray="3 3"
                                stroke="rgba(255,255,255,0.1)"
                                vertical={false}
                            />
                            <XAxis
                                dataKey="label"
                                stroke="#ffffff"
                                tick={{ fill: '#ffffff' }}
                                axisLine={{ stroke: '#ffffff40' }}
                            />
                            <YAxis
                                stroke="#ffffff"
                                tick={{ fill: '#ffffff' }}
                                axisLine={{ stroke: '#ffffff40' }}
                            />
                            <Tooltip
                                contentStyle={{
                                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                                    border: '1px solid rgba(255, 255, 255, 0.2)',
                                    borderRadius: '8px',
                                    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
                                }}
                                labelStyle={{ color: '#ffffff' }}
                                itemStyle={{ color: '#ffffff' }}
                            />
                            <Line
                                type="monotone"
                                dataKey="frequency"
                                stroke="url(#lineGradient)"
                                strokeWidth={3}
                                dot={{
                                    fill: '#000000',
                                    stroke: '#00ff94',
                                    strokeWidth: 2,
                                    r: 4
                                }}
                                activeDot={{
                                    fill: '#00ff94',
                                    stroke: '#000000',
                                    strokeWidth: 2,
                                    r: 6
                                }}
                                fill="url(#areaGradient)"
                            />
                        </LineChart>
                    </ResponsiveContainer>
                </div>
            </div>
        </div>
    );
} 