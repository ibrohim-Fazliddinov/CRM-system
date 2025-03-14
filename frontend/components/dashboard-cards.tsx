"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ArrowUpRight, DollarSign, Users, LineChart, Clock } from "lucide-react"
import { analyticsService } from "@/lib/api"

interface DashboardStats {
  totalRevenue: number
  revenueChange: number
  activeCustomers: number
  customersChange: number
  conversionRate: number
  conversionChange: number
  responseTime: number
  responseTimeChange: number
}

export function DashboardCards() {
  const [stats, setStats] = useState<DashboardStats | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchStats = async () => {
      try {
        // Получаем данные аналитики с бэкенда
        const data = await analyticsService.getDashboardStats()

        // Преобразуем данные в нужный формат
        // Предполагаем, что API возвращает данные в другом формате
        // и нам нужно их адаптировать для нашего интерфейса
        const formattedData: DashboardStats = {
          totalRevenue: data.total_revenue || 0,
          revenueChange: data.revenue_change || 0,
          activeCustomers: data.active_customers || 0,
          customersChange: data.customers_change || 0,
          conversionRate: data.conversion_rate || 0,
          conversionChange: data.conversion_change || 0,
          responseTime: data.response_time || 0,
          responseTimeChange: data.response_time_change || 0,
        }

        setStats(formattedData)
      } catch (error) {
        console.error("Ошибка при загрузке статистики:", error)
      } finally {
        setLoading(false)
      }
    }

    fetchStats()
  }, [])

  if (loading) {
    return (
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {[...Array(4)].map((_, i) => (
          <Card key={i} className="animate-pulse">
            <CardHeader className="pb-2">
              <div className="h-4 w-24 bg-muted rounded"></div>
            </CardHeader>
            <CardContent>
              <div className="h-7 w-32 bg-muted rounded mb-2"></div>
              <div className="h-3 w-24 bg-muted rounded"></div>
            </CardContent>
          </Card>
        ))}
      </div>
    )
  }

  // Если данные не загрузились, показываем заглушку
  if (!stats) {
    return (
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Общий доход</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">Нет данных</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Активные клиенты</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">Нет данных</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Конверсия</CardTitle>
            <LineChart className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">Нет данных</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Среднее время ответа</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">Нет данных</div>
          </CardContent>
        </Card>
      </div>
    )
  }

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat("ru-RU", {
      style: "currency",
      currency: "RUB",
      maximumFractionDigits: 0,
    }).format(value)
  }

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      <Card>
        <CardHeader className="flex flex-row items-center justify-between pb-2">
          <CardTitle className="text-sm font-medium">Общий доход</CardTitle>
          <DollarSign className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{formatCurrency(stats.totalRevenue)}</div>
          <div className="flex items-center text-xs text-muted-foreground">
            {stats.revenueChange > 0 ? (
              <ArrowUpRight className="mr-1 h-3 w-3 text-emerald-500" />
            ) : (
              <ArrowUpRight className="mr-1 h-3 w-3 text-red-500 rotate-90" />
            )}
            <span className={stats.revenueChange > 0 ? "text-emerald-500" : "text-red-500"}>
              {stats.revenueChange > 0 ? "+" : ""}
              {stats.revenueChange}%
            </span>
            <span className="ml-1">с прошлого месяца</span>
          </div>
        </CardContent>
      </Card>
      <Card>
        <CardHeader className="flex flex-row items-center justify-between pb-2">
          <CardTitle className="text-sm font-medium">Активные клиенты</CardTitle>
          <Users className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">+{stats.activeCustomers}</div>
          <div className="flex items-center text-xs text-muted-foreground">
            {stats.customersChange > 0 ? (
              <ArrowUpRight className="mr-1 h-3 w-3 text-emerald-500" />
            ) : (
              <ArrowUpRight className="mr-1 h-3 w-3 text-red-500 rotate-90" />
            )}
            <span className={stats.customersChange > 0 ? "text-emerald-500" : "text-red-500"}>
              {stats.customersChange > 0 ? "+" : ""}
              {stats.customersChange}%
            </span>
            <span className="ml-1">с прошлого месяца</span>
          </div>
        </CardContent>
      </Card>
      <Card>
        <CardHeader className="flex flex-row items-center justify-between pb-2">
          <CardTitle className="text-sm font-medium">Конверсия</CardTitle>
          <LineChart className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{stats.conversionRate}%</div>
          <div className="flex items-center text-xs text-muted-foreground">
            {stats.conversionChange > 0 ? (
              <ArrowUpRight className="mr-1 h-3 w-3 text-emerald-500" />
            ) : (
              <ArrowUpRight className="mr-1 h-3 w-3 text-red-500 rotate-90" />
            )}
            <span className={stats.conversionChange > 0 ? "text-emerald-500" : "text-red-500"}>
              {stats.conversionChange > 0 ? "+" : ""}
              {stats.conversionChange}%
            </span>
            <span className="ml-1">с прошлого месяца</span>
          </div>
        </CardContent>
      </Card>
      <Card>
        <CardHeader className="flex flex-row items-center justify-between pb-2">
          <CardTitle className="text-sm font-medium">Среднее время ответа</CardTitle>
          <Clock className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{stats.responseTime} ч.</div>
          <div className="flex items-center text-xs text-muted-foreground">
            {stats.responseTimeChange < 0 ? (
              <ArrowUpRight className="mr-1 h-3 w-3 text-emerald-500" />
            ) : (
              <ArrowUpRight className="mr-1 h-3 w-3 text-red-500 rotate-90" />
            )}
            <span className={stats.responseTimeChange < 0 ? "text-emerald-500" : "text-red-500"}>
              {stats.responseTimeChange > 0 ? "+" : ""}
              {stats.responseTimeChange}%
            </span>
            <span className="ml-1">с прошлого месяца</span>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

