import type { Metadata } from "next"
import DashboardPage from "@/components/dashboard-page"

export const metadata: Metadata = {
  title: "CRM Dashboard",
  description: "A minimalist CRM system with Apple-inspired design",
}

export default function Home() {
  return <DashboardPage />
}

