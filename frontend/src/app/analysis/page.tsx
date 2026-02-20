'use client'

import { useQuery } from '@tanstack/react-query'
import { Card } from '@/components/ui/card'
import { ArrowUp, ArrowDown, Activity, TrendingUp, DollarSign } from 'lucide-react'
import { Area, AreaChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'

export default function MacroAnalysisPage() {
    const { data: macro, isLoading } = useQuery({
        queryKey: ['macro'],
        queryFn: async () => {
            const res = await fetch('http://localhost:8000/api/v1/market/macro')
            if (!res.ok) throw new Error('Failed to fetch macro data')
            return res.json()
        }
    })

    if (isLoading) return <div className="p-8 text-white">Loading Macro Data...</div>

    const indicators = [
        { label: "인플레이션 (CPI)", value: macro?.CPI?.value + "%", icon: Activity, color: "text-rose-400" },
        { label: "GDP 성장률", value: macro?.GDP?.value + "B", icon: TrendingUp, color: "text-emerald-400" },
        { label: "실업률", value: macro?.Unemployment?.value + "%", icon: ArrowDown, color: "text-amber-400" },
        { label: "M2 통화량", value: macro?.M2?.value + "B", icon: DollarSign, color: "text-blue-400" },
    ]

    return (
        <div className="min-h-screen p-8 text-white">
            <h1 className="mb-8 text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-300">
                거시경제 분석 (Macro Analysis)
            </h1>

            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
                {indicators.map((item) => (
                    <Card key={item.label} className="border-zinc-800 bg-[#0f0f10] p-6">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm font-medium text-zinc-400">{item.label}</p>
                                <p className="mt-2 text-2xl font-bold text-white">{item.value}</p>
                            </div>
                            <div className={`rounded-full bg-zinc-900 p-3 ${item.color}`}>
                                <item.icon className="h-6 w-6" />
                            </div>
                        </div>
                    </Card>
                ))}
            </div>

            <div className="mt-8 grid gap-6 md:grid-cols-2">
                <Card className="border-zinc-800 bg-[#0f0f10] p-6">
                    <h3 className="mb-4 text-lg font-semibold text-white">장단기 금리차 (10Y - 2Y)</h3>
                    <div className="flex items-center gap-4">
                        <div className="text-4xl font-bold text-white">
                            {macro?.Yield_Spread_10Y_2Y?.value?.toFixed(2)}%
                        </div>
                        <span className={`px-2 py-1 rounded text-xs font-bold ${macro?.Yield_Spread_10Y_2Y?.status === 'Inverted' ? 'bg-red-500/20 text-red-400' : 'bg-green-500/20 text-green-400'
                            }`}>
                            {macro?.Yield_Spread_10Y_2Y?.status === 'Inverted' ? '역전됨 (Inverted)' : '정상 (Normal)'}
                        </span>
                    </div>
                    <p className="mt-2 text-sm text-zinc-500">
                        장단기 금리차 역전은 역사적으로 경기 침체의 선행 지표로 여겨집니다.
                    </p>
                </Card>
            </div>
        </div>
    )
}
