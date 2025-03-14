"use client"

import { createContext, useContext, useEffect, useState, type ReactNode } from "react"
import { authService, removeAuthToken } from "@/lib/api"
import { useRouter } from "next/navigation"

interface User {
  id: number
  username: string
  email: string
  first_name?: string
  last_name?: string
  is_staff?: boolean
}

interface AuthContextType {
  user: User | null
  loading: boolean
  error: string | null
  login: (username: string, password: string) => Promise<void>
  logout: () => Promise<void>
  register: (userData: any) => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const router = useRouter()

  useEffect(() => {
    // Проверяем авторизацию при загрузке
    const checkAuth = async () => {
      try {
        // Проверяем, есть ли токен в localStorage
        const token = localStorage.getItem("authToken")
        if (!token) {
          setUser(null)
          setLoading(false)
          return
        }

        // Если токен есть, получаем данные пользователя
        const userData = await authService.getCurrentUser()
        setUser(userData)
      } catch (err) {
        // Если не авторизован или токен недействителен, удаляем его
        removeAuthToken()
        setUser(null)
      } finally {
        setLoading(false)
      }
    }

    checkAuth()
  }, [])

  const login = async (username: string, password: string) => {
    setLoading(true)
    setError(null)

    try {
      const response = await authService.login(username, password)
      setUser(response.user)
      router.push("/")
    } catch (err) {
      setError(err instanceof Error ? err.message : "Ошибка при входе")
    } finally {
      setLoading(false)
    }
  }

  const logout = async () => {
    setLoading(true)

    try {
      await authService.logout()
      setUser(null)
      router.push("/login")
    } catch (err) {
      setError(err instanceof Error ? err.message : "Ошибка при выходе")
    } finally {
      setLoading(false)
    }
  }

  const register = async (userData: any) => {
    setLoading(true)
    setError(null)

    try {
      await authService.register(userData)
      router.push("/login")
    } catch (err) {
      setError(err instanceof Error ? err.message : "Ошибка при регистрации")
    } finally {
      setLoading(false)
    }
  }

  return (
    <AuthContext.Provider value={{ user, loading, error, login, logout, register }}>{children}</AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider")
  }
  return context
}

