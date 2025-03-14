"use client"

import { cn } from "@/lib/utils"
import Link from "next/link"
import { usePathname } from "next/navigation"

export function MainNav() {
  const pathname = usePathname()

  const navItems = [
    {
      label: "Overview",
      href: "/",
      active: pathname === "/",
    },
    {
      label: "Customers",
      href: "/customers",
      active: pathname === "/customers",
    },
    {
      label: "Deals",
      href: "/deals",
      active: pathname === "/deals",
    },
  ]

  return (
    <nav className="hidden md:flex items-center gap-6">
      {navItems.map((item) => (
        <Link
          key={item.href}
          href={item.href}
          className={cn(
            "text-sm font-medium transition-colors hover:text-primary",
            item.active ? "text-foreground" : "text-muted-foreground",
          )}
        >
          {item.label}
        </Link>
      ))}
    </nav>
  )
}

