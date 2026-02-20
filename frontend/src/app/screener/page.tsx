'use client'

import { useQuery } from '@tanstack/react-query'
import { Card } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

export default function ScreenerPage() {
    const { data: stocks, isLoading } = useQuery({
        queryKey: ['screener'],
        queryFn: async () => {
            const res = await fetch('http://localhost:8000/api/v1/market/screener/smart-money')
            if (!res.ok) throw new Error('Failed to fetch screener data')
            return res.json()
        }
    })

    if (isLoading) return <div className="p-8 text-white">Loading Smart Money Picks...</div>

    return (
        <div className="min-h-screen p-8 text-white">
            <h1 className="mb-8 text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-green-400 to-emerald-300">
                스마트 머니 스크리너 (Smart Money Screener)
            </h1>

            <Card className="border-zinc-800 bg-[#0f0f10] overflow-hidden">
                <div className="overflow-x-auto">
                    <table className="w-full text-left text-sm">
                        <thead className="bg-zinc-900 text-zinc-400">
                            <tr>
                                <th className="p-4">티커 (Ticker)</th>
                                <th className="p-4">점수 (Score)</th>
                                <th className="p-4">현재가 (Price)</th>
                                <th className="p-4">변동률 (Change)</th>
                                <th className="p-4">RSI</th>
                                <th className="p-4">PER</th>
                                <th className="p-4">투자의견 (Rating)</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-zinc-800">
                            {stocks?.map((stock: any) => (
                                <tr key={stock.ticker} className="hover:bg-zinc-900/50 transition-colors">
                                    <td className="p-4">
                                        <div className="font-bold text-white">{stock.ticker}</div>
                                        <div className="text-xs text-zinc-500">{stock.name}</div>
                                    </td>
                                    <td className="p-4">
                                        <span className={`font-bold ${stock.score >= 70 ? 'text-green-400' : 'text-yellow-400'}`}>
                                            {stock.score}
                                        </span>
                                    </td>
                                    <td className="p-4 text-white">${stock.price}</td>
                                    <td className={`p-4 ${stock.change >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                                        {stock.change > 0 ? '+' : ''}{stock.change}%
                                    </td>
                                    <td className="p-4 text-zinc-300">{stock.rsi}</td>
                                    <td className="p-4 text-zinc-300">{stock.pe}</td>
                                    <td className="p-4">
                                        <Badge variant="outline" className="border-zinc-700 text-zinc-300">
                                            {stock.recommendation}
                                        </Badge>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </Card>
        </div>
    )
}
