import { NextResponse } from "next/server"
import type { NextRequest } from "next/server"

// Этот middleware проверяет аутентификацию и перенаправляет на страницу входа, если пользователь не авторизован
export function middleware(request: NextRequest) {
  // Проверяем, является ли текущий путь публичным (не требующим авторизации)
  const isPublicPath = [
    "/login",
    "/register",
    "/forgot-password",
    "/reset-password",
    // Добавьте другие публичные пути при необходимости
  ].includes(request.nextUrl.pathname)

  // Получаем токен из localStorage (через cookies, так как middleware не имеет доступа к localStorage)
  const authToken = request.cookies.get("authToken")?.value

  // Если пользователь не авторизован и пытается получить доступ к защищенному маршруту
  if (!authToken && !isPublicPath) {
    // Перенаправляем на страницу входа
    const loginUrl = new URL("/login", request.url)
    // Сохраняем исходный URL для перенаправления после входа
    loginUrl.searchParams.set("callbackUrl", request.nextUrl.pathname)
    return NextResponse.redirect(loginUrl)
  }

  // Если пользователь авторизован и пытается получить доступ к странице входа
  if (authToken && isPublicPath) {
    // Перенаправляем на главную страницу
    return NextResponse.redirect(new URL("/", request.url))
  }

  return NextResponse.next()
}

// Указываем, для каких путей должен срабатывать middleware
export const config = {
  matcher: [
    // Исключаем статические файлы
    "/((?!api|_next/static|_next/image|favicon.ico).*)",
  ],
}

