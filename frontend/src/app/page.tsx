'use client'

import { useQuery } from '@tanstack/react-query'
import { fetchDashboardOverview, fetchAIIntelligence } from '@/lib/api'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Newspaper } from 'lucide-react'
import { cn } from '@/lib/utils'
import { StockChart } from '@/components/dashboard/StockChart'
import { SectorHeatmap } from '@/components/dashboard/SectorHeatmap'
import { PredictionGauge } from '@/components/dashboard/PredictionGauge'

export default function Dashboard() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['dashboard'],
    queryFn: fetchDashboardOverview,
    refetchInterval: 30000 // Auto-refresh every 30s
  })

  const { data: aiData, isLoading: isAiLoading } = useQuery({
    queryKey: ['ai-intelligence'],
    queryFn: fetchAIIntelligence,
    refetchInterval: 300000 // Refresh every 5 mins
  })

  // Loading State
  if (isLoading) {
    return (
      <div className="flex h-screen items-center justify-center bg-background text-foreground">
        <div className="flex flex-col items-center gap-4">
          <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent"></div>
          <p className="animate-pulse text-muted-foreground">퀀트 엔진 초기화 중...</p>
        </div>
      </div>
    )
  }

  // Error State
  if (error) {
    return (
      <div className="flex h-screen items-center justify-center bg-background">
        <div className="text-destructive">
          <h1 className="text-xl font-bold">시스템 오류 발생</h1>
          <p>{(error as Error).message}</p>
          <p className="text-sm">백엔드 서버(포트 8000)가 실행 중인지 확인해주세요.</p>
        </div>
      </div>
    )
  }

  const { indices, sectors, market_status, fear_greed } = data || {}

  return (
    <div className="min-h-screen p-8">
      {/* Header */}
      <header className="mb-10 flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-300">
            원스톱 대시보드 (One-Stop Dashboard)
          </h1>
          <p className="mt-1 text-sm font-medium tracking-wider text-zinc-400 uppercase">
            실시간 S-Class 시장 분석
          </p>
        </div>
        <div className="flex gap-4">
          <Card className="w-44 border-zinc-800 bg-[#0f0f10]">
            <CardContent className="flex flex-col items-center justify-center p-4">
              <span className="text-[10px] font-bold uppercase tracking-widest text-zinc-500">시장 상태 (Market Status)</span>
              <span className="mt-1 text-lg font-extrabold text-blue-500">{market_status === 'Open' ? '개장 (Open)' : '폐장 (Closed)'}</span>
            </CardContent>
          </Card>
          <Card className="w-44 border-zinc-800 bg-[#0f0f10]">
            <CardContent className="flex flex-col items-center justify-center p-4">
              <span className="text-[10px] font-bold uppercase tracking-widest text-zinc-500">공포 & 탐욕 지수</span>
              <div className="flex items-baseline gap-2">
                <span className={cn("text-2xl font-black", fear_greed?.value > 60 ? "text-green-500" : "text-yellow-500")}>
                  {fear_greed?.value || 50}
                </span>
                <span className="text-[10px] font-bold text-zinc-400 uppercase">{fear_greed?.label || "Neutral"}</span>
              </div>
            </CardContent>
          </Card>
        </div>
      </header>

      <div className="grid gap-6 lg:grid-cols-12">
        {/* Top Row: AI & Key Gauges (Bento Style) */}
        <div className="col-span-12 lg:col-span-8 flex flex-col gap-6">
          <Card className="flex-1 border-zinc-800 bg-[#0f0f10]">
            <CardHeader className="pb-2">
              <CardTitle className="flex items-center gap-2 text-white">
                <Newspaper className="h-5 w-5 text-blue-400" />
                AI 시장 브리핑 ({aiData?.ticker || 'Market'})
              </CardTitle>
            </CardHeader>
            <CardContent>
              {isAiLoading ? (
                <div className="flex flex-col items-center gap-2 py-8 text-zinc-500">
                  <div className="h-4 w-4 animate-spin rounded-full border-2 border-blue-500 border-t-transparent"></div>
                  <p className="text-sm font-medium">Quant AI가 패턴을 분석 중입니다...</p>
                </div>
              ) : (
                <div className="prose prose-sm prose-invert max-w-none">
                  {aiData?.summary && (
                    <div className="whitespace-pre-wrap leading-relaxed text-zinc-300">
                      {aiData.summary}
                    </div>
                  )}
                  {aiData?.error && <p className="text-red-500 font-semibold">시스템 알림: {aiData.error}</p>}
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        <div className="col-span-12 lg:col-span-4 flex flex-col gap-6">
          <PredictionGauge value={fear_greed?.value} />
        </div>

        {/* Row 2: Sector Heatmap & Indices */}
        <div className="col-span-12 lg:col-span-7">
          <SectorHeatmap sectors={sectors} />
        </div>

        <div className="col-span-12 lg:col-span-5">
          <Card className="h-full border-zinc-800 bg-[#0f0f10]">
            <CardHeader><CardTitle className="text-white">글로벌 지수 (Global Indices)</CardTitle></CardHeader>
            <CardContent className="space-y-4">
              {indices && Object.entries(indices).map(([symbol, change]: [string, any]) => (
                <div key={symbol} className="flex justify-between border-b border-zinc-800/50 pb-3 last:border-0 hover:bg-zinc-800/20 transition-colors px-2 rounded-lg">
                  <span className="font-bold text-white">{symbol}</span>
                  <span className={cn("font-mono font-bold", change >= 0 ? "text-green-500" : "text-red-500")}>
                    {change > 0 ? "+" : ""}{change}%
                  </span>
                </div>
              ))}
            </CardContent>
          </Card>
        </div>

        {/* Row 3: Charts */}
        <div className="col-span-12 lg:col-span-6">
          <StockChart ticker="SPY" />
        </div>
        <div className="col-span-12 lg:col-span-6">
          <StockChart ticker="QQQ" />
        </div>
      </div>
    </div>
  )
}
