export default function StatsCard() {
    const stats = {
        total_attacks: 2847,
        blocked_attacks: 1963,
        types_of_attacks: {
            sqlinjection: 45,
            xss: 30,
            bruteforce: 15,
            ddos: 10
        }
    };

    return (
        <div className="w-full p-6 rounded-xl relative overflow-hidden border border-white/10 backdrop-blur-md bg-[#121212]/80">
            <div className="relative z-10">
                <div className="grid grid-cols-2 gap-6 mb-8">
                    <div>
                        <h3 className="text-sm text-gray-400 mb-2">Total Attacks</h3>
                        <p className="font-inter font-light text-3xl text-white">{stats.total_attacks}</p>
                    </div>

                    <div>
                        <h3 className="text-sm text-gray-400 mb-2">Blocked Attacks</h3>
                        <p className="font-inter font-light text-3xl text-white">{stats.blocked_attacks}</p>
                    </div>
                </div>

                <div>
                    <h3 className="text-sm text-gray-400 mb-4">Attack Types Distribution</h3>
                    <div className="flex h-4 rounded-full overflow-hidden bg-white/5">
                        <div
                            className="bg-[#00ff94]/80 transition-all duration-500"
                            style={{ width: `${stats.types_of_attacks.sqlinjection}%` }}
                        />
                        <div
                            className="bg-[#00ff94]/50 transition-all duration-500"
                            style={{ width: `${stats.types_of_attacks.xss}%` }}
                        />
                        <div
                            className="bg-[#00ff94]/20 transition-all duration-500"
                            style={{ width: `${stats.types_of_attacks.bruteforce}%` }}
                        />
                        <div
                            className="bg-[#00ff94]/10 transition-all duration-500"
                            style={{ width: `${stats.types_of_attacks.ddos}%` }}
                        />
                    </div>
                    <div className="flex justify-between mt-2 text-xs">
                        <div className="flex items-center">
                            <div className="w-2 h-2 rounded-full bg-[#00ff94]/80 mr-2" />
                            <span className="text-gray-400">SQL ({stats.types_of_attacks.sqlinjection}%)</span>
                        </div>
                        <div className="flex items-center">
                            <div className="w-2 h-2 rounded-full bg-[#00ff94]/50 mr-2" />
                            <span className="text-gray-400">XSS ({stats.types_of_attacks.xss}%)</span>
                        </div>
                        <div className="flex items-center">
                            <div className="w-2 h-2 rounded-full bg-[#00ff94]/20 mr-2" />
                            <span className="text-gray-400">Bruteforce ({stats.types_of_attacks.bruteforce}%)</span>
                        </div>
                        <div className="flex items-center">
                            <div className="w-2 h-2 rounded-full bg-[#00ff94]/10 mr-2" />
                            <span className="text-gray-400">DDoS ({stats.types_of_attacks.ddos}%)</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
} 