'use client'

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts"
import { useQuery } from '@tanstack/react-query'
import { fetchTickerHistory } from "@/lib/api"

export function StockChart({ ticker = "SPY" }: { ticker?: string }) {
    const { data, isLoading } = useQuery({
        queryKey: ['history', ticker],
        queryFn: () => fetchTickerHistory(ticker, "1y")
    })

    if (isLoading) return <div className="h-[300px] animate-pulse bg-muted/20" />

    return (
        <Card className="border-zinc-800 bg-[#0f0f10]">
            <CardHeader className="pb-2">
                <CardTitle className="text-white">Price Action ({ticker})</CardTitle>
            </CardHeader>
            <CardContent>
                <div className="h-[280px]">
                    <ResponsiveContainer width="100%" height="100%">
                        <AreaChart data={data || []}>
                            <defs>
                                <linearGradient id="colorPrice" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                                </linearGradient>
                            </defs>
                            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#27272a" opacity={0.5} />
                            <XAxis
                                dataKey="date"
                                stroke="#71717a"
                                fontSize={11}
                                tickLine={false}
                                axisLine={false}
                                minTickGap={30}
                            />
                            <YAxis
                                stroke="#71717a"
                                fontSize={11}
                                tickLine={false}
                                axisLine={false}
                                tickFormatter={(value) => `$${value}`}
                                domain={['auto', 'auto']}
                            />
                            <Tooltip
                                contentStyle={{
                                    backgroundColor: '#0f0f10',
                                    borderColor: '#27272a',
                                    borderRadius: '12px',
                                    fontSize: '12px',
                                    color: '#fff'
                                }}
                                itemStyle={{ color: '#3b82f6' }}
                            />
                            <Area
                                type="monotone"
                                dataKey="price"
                                stroke="#3b82f6"
                                strokeWidth={2}
                                fillOpacity={1}
                                fill="url(#colorPrice)"
                            />
                        </AreaChart>
                    </ResponsiveContainer>
                </div>
            </CardContent>
        </Card>
    )
}
