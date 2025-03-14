"use client"

import type React from "react"

import { useState } from "react"
import { useAuth } from "@/hooks/use-auth"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { AlertCircle } from "lucide-react"
import Link from "next/link"

export default function RegisterPage() {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    re_password: "",
    first_name: "",
    last_name: "",
  })
  const [errors, setErrors] = useState<Record<string, string>>({})
  const { register, loading, error } = useAuth()

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))

    // Очищаем ошибку для этого поля при изменении
    if (errors[name]) {
      setErrors((prev) => {
        const newErrors = { ...prev }
        delete newErrors[name]
        return newErrors
      })
    }
  }

  const validateForm = () => {
    const newErrors: Record<string, string> = {}

    if (!formData.username) {
      newErrors.username = "Имя пользователя обязательно"
    }

    if (!formData.email) {
      newErrors.email = "Email обязателен"
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = "Некорректный email"
    }

    if (!formData.password) {
      newErrors.password = "Пароль обязателен"
    } else if (formData.password.length < 8) {
      newErrors.password = "Пароль должен содержать не менее 8 символов"
    }

    if (formData.password !== formData.re_password) {
      newErrors.re_password = "Пароли не совпадают"
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!validateForm()) {
      return
    }

    await register(formData)
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-background">
      <Card className="w-full max-w-md">
        <CardHeader className="space-y-1">
          <CardTitle className="text-2xl font-bold">Регистрация</CardTitle>
          <CardDescription>Создайте аккаунт для доступа к CRM</CardDescription>
        </CardHeader>
        <form onSubmit={handleSubmit}>
          <CardContent className="space-y-4">
            {error && (
              <Alert variant="destructive">
                <AlertCircle className="h-4 w-4" />
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="first_name">Имя</Label>
                <Input id="first_name" name="first_name" value={formData.first_name} onChange={handleChange} />
              </div>
              <div className="space-y-2">
                <Label htmlFor="last_name">Фамилия</Label>
                <Input id="last_name" name="last_name" value={formData.last_name} onChange={handleChange} />
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="username">Имя пользователя*</Label>
              <Input
                id="username"
                name="username"
                value={formData.username}
                onChange={handleChange}
                required
                className={errors.username ? "border-red-500" : ""}
              />
              {errors.username && <p className="text-xs text-red-500">{errors.username}</p>}
            </div>

            <div className="space-y-2">
              <Label htmlFor="email">Email*</Label>
              <Input
                id="email"
                name="email"
                type="email"
                value={formData.email}
                onChange={handleChange}
                required
                className={errors.email ? "border-red-500" : ""}
              />
              {errors.email && <p className="text-xs text-red-500">{errors.email}</p>}
            </div>

            <div className="space-y-2">
              <Label htmlFor="password">Пароль*</Label>
              <Input
                id="password"
                name="password"
                type="password"
                value={formData.password}
                onChange={handleChange}
                required
                className={errors.password ? "border-red-500" : ""}
              />
              {errors.password && <p className="text-xs text-red-500">{errors.password}</p>}
            </div>

            <div className="space-y-2">
              <Label htmlFor="re_password">Подтверждение пароля*</Label>
              <Input
                id="re_password"
                name="re_password"
                type="password"
                value={formData.re_password}
                onChange={handleChange}
                required
                className={errors.re_password ? "border-red-500" : ""}
              />
              {errors.re_password && <p className="text-xs text-red-500">{errors.re_password}</p>}
            </div>
          </CardContent>
          <CardFooter className="flex flex-col space-y-4">
            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? "Регистрация..." : "Зарегистрироваться"}
            </Button>
            <div className="text-sm text-center">
              Уже есть аккаунт?{" "}
              <Link href="/login" className="text-primary hover:underline">
                Войти
              </Link>
            </div>
          </CardFooter>
        </form>
      </Card>
    </div>
  )
}

