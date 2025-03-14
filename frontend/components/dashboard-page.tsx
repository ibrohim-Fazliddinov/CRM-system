"use client"

import { useState } from "react"
import { Sidebar } from "@/components/sidebar"
import { DashboardHeader } from "@/components/dashboard-header"
import { DashboardCards } from "@/components/dashboard-cards"
import { RecentActivity } from "@/components/recent-activity"
import { UpcomingTasks } from "@/components/upcoming-tasks"
import { Button } from "@/components/ui/button"
import { Menu } from "lucide-react"

export default function DashboardPage() {
  const [sidebarOpen, setSidebarOpen] = useState(false)

  return (
    <div className="flex min-h-screen bg-background">
      <Sidebar open={sidebarOpen} onOpenChange={setSidebarOpen} />
      <div className="flex-1">
        <div className="flex items-center md:hidden border-b h-14 px-4">
          <Button variant="ghost" size="icon" onClick={() => setSidebarOpen(true)}>
            <Menu className="h-5 w-5" />
            <span className="sr-only">Toggle sidebar</span>
          </Button>
          <div className="ml-3 font-medium">CRM</div>
        </div>
        <div className="flex flex-col">
          <DashboardHeader />
          <main className="flex-1 p-4 md:p-6 lg:p-8 pt-0">
            <div className="mx-auto max-w-7xl space-y-8">
              <DashboardCards />
              <div className="grid gap-8 md:grid-cols-2">
                <RecentActivity />
                <UpcomingTasks />
              </div>
            </div>
          </main>
        </div>
      </div>
    </div>
  )
}

