"use client"

import { cn } from "@/lib/utils"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { MainNav } from "@/components/main-nav"
import { UserNav } from "@/components/user-nav"
import { Plus, Search } from "lucide-react"
import { Input } from "@/components/ui/input"

export function DashboardHeader() {
  const [searchFocused, setSearchFocused] = useState(false)

  return (
    <header className="sticky top-0 z-10 border-b bg-background/95 backdrop-blur">
      <div className="flex h-14 items-center gap-4 px-4 md:px-6 lg:px-8">
        <MainNav />
        <div
          className={cn(
            "relative ml-auto flex-1 max-w-sm transition-all duration-300 ease-in-out",
            searchFocused ? "max-w-xl" : "max-w-sm",
          )}
        >
          <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
          <Input
            type="search"
            placeholder="Search..."
            className="w-full rounded-full bg-muted pl-8 md:w-[300px] lg:w-[440px]"
            onFocus={() => setSearchFocused(true)}
            onBlur={() => setSearchFocused(false)}
          />
        </div>
        <Button size="sm" className="rounded-full">
          <Plus className="mr-2 h-4 w-4" />
          New
        </Button>
        <UserNav />
      </div>
    </header>
  )
}

