 'use client'

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { cn } from "@/lib/utils"

const data = [
    {
        name: 'Avoid',
        uv: 31.47,
        pv: 2400,
        fill: '#8884d8',
    },
    {
        name: 'Hold',
        uv: 26.69,
        pv: 4567,
        fill: '#83a6ed',
    },
    {
        name: 'Buy',
        uv: 15.69,
        pv: 1398,
        fill: '#8dd1e1',
    },
];

// Placeholder Gauge - Simply using a stylized Circle or Pie in S-Class design is better than RadialBar for gauges often
// But let's stick to simple efficient visual.
// Detailed Implementation: 0-100 Score.
const ScoreGauge = ({ score }: { score: number }) => {
    const isBullish = score > 60;
    const isBearish = score < 40;

    return (
        <div className="relative flex flex-col items-center justify-center p-6">
            <div className="relative h-44 w-44">
                {/* Background Ring */}
                <svg className="h-full w-full transform -rotate-90">
                    <circle
                        cx="88"
                        cy="88"
                        r="70"
                        stroke="#27272a"
                        strokeWidth="12"
                        fill="transparent"
                        strokeDasharray={2 * Math.PI * 70}
                        className="opacity-20"
                    />
                    {/* Progress Ring */}
                    <circle
                        cx="88"
                        cy="88"
                        r="70"
                        stroke={isBullish ? "#22c55e" : isBearish ? "#ef4444" : "#eab308"}
                        strokeWidth="12"
                        fill="transparent"
                        strokeDasharray={2 * Math.PI * 70}
                        strokeDashoffset={2 * Math.PI * 70 * (1 - score / 100)}
                        strokeLinecap="round"
                        className="transition-all duration-1000 ease-out"
                    />
                </svg>
                {/* Center Content */}
                <div className="absolute inset-0 flex flex-col items-center justify-center">
                    <span className="text-4xl font-extrabold text-white">{score}</span>
                    <span className="text-[10px] font-bold uppercase tracking-widest text-zinc-500">Sentiment</span>
                </div>
            </div>
            <div className={cn(
                "mt-6 px-4 py-1.5 rounded-full text-xs font-bold uppercase tracking-widest border transition-all",
                isBullish ? "bg-green-500/10 text-green-500 border-green-500/20" :
                    isBearish ? "bg-red-500/10 text-red-500 border-red-500/20" :
                        "bg-yellow-500/10 text-yellow-500 border-yellow-500/20"
            )}>
                {score > 70 ? "Extreme Greed" : score > 60 ? "Greed" : score < 30 ? "Extreme Fear" : score < 40 ? "Fear" : "Neutral"}
            </div>
        </div>
    )
}

export function PredictionGauge({ value = 50 }: { value?: number }) {
    return (
        <Card className="h-full border-zinc-800 bg-[#0f0f10]">
            <CardHeader className="pb-2">
                <CardTitle className="text-white">Market Sentiment Gauge</CardTitle>
            </CardHeader>
            <CardContent className="flex justify-center p-0">
                <ScoreGauge score={value} />
            </CardContent>
        </Card>
    )
}
