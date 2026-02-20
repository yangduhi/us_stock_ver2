'use client'

import { useQuery } from '@tanstack/react-query'
import { Card } from '@/components/ui/card'
import { Shield, AlertTriangle } from 'lucide-react'

export default function RiskPage() {
    const { data: risk, isLoading } = useQuery({
        queryKey: ['risk'],
        queryFn: async () => {
            const res = await fetch('http://localhost:8000/api/v1/market/risk')
            if (!res.ok) throw new Error('Failed to fetch risk data')
            return res.json()
        }
    })

    if (isLoading) return <div className="p-8 text-white">Loading Risk Analysis...</div>

    return (
        <div className="min-h-screen p-8 text-white">
            <h1 className="mb-8 text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-red-400 to-orange-300">
                포트폴리오 리스크 모니터
            </h1>

            <div className="grid gap-6 md:grid-cols-2">
                <Card className="border-zinc-800 bg-[#0f0f10] p-6">
                    <div className="flex items-center gap-4">
                        <div className="rounded-full bg-red-500/10 p-3 text-red-500">
                            <Shield className="h-8 w-8" />
                        </div>
                        <div>
                            <p className="text-sm font-medium text-zinc-400">포트폴리오 변동성 (연환산)</p>
                            <h2 className="text-3xl font-bold text-white">{risk?.volatility}%</h2>
                        </div>
                    </div>
                </Card>

                <Card className="border-zinc-800 bg-[#0f0f10] p-6">
                    <div className="flex items-center gap-2 mb-4">
                        <AlertTriangle className="h-5 w-5 text-yellow-500" />
                        <h3 className="text-lg font-semibold text-white">높은 상관관계 경고</h3>
                    </div>
                    <div className="space-y-3">
                        {risk?.high_correlations?.length === 0 ? (
                            <p className="text-zinc-500">위험한 상관관계가 감지되지 않았습니다.</p>
                        ) : (
                            risk?.high_correlations?.map((item: any, idx: number) => (
                                <div key={idx} className="flex justify-between items-center bg-zinc-900/50 p-3 rounded-lg border border-zinc-800">
                                    <span className="text-sm font-medium text-white">{item.asset1} ↔ {item.asset2}</span>
                                    <span className="text-sm font-bold text-red-400">{item.correlation}</span>
                                </div>
                            ))
                        )}
                    </div>
                </Card>
            </div>
        </div>
    )
}
