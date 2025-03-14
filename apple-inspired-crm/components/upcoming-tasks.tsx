"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Checkbox } from "@/components/ui/checkbox"
import { Badge } from "@/components/ui/badge"
import { tasksService } from "@/lib/api"

interface Task {
  id: number
  title: string
  due_date: string
  priority: "High" | "Medium" | "Low"
  completed: boolean
}

export function UpcomingTasks() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const data = await tasksService.getAll({ limit: 5, upcoming: "true" })
        setTasks(data.results)
      } catch (error) {
        console.error("Ошибка при загрузке задач:", error)
      } finally {
        setLoading(false)
      }
    }

    fetchTasks()
  }, [])

  const handleTaskComplete = async (taskId: number, completed: boolean) => {
    try {
      if (completed) {
        await tasksService.complete(taskId)
      } else {
        await tasksService.update(taskId, { completed: false })
      }

      // Обновляем состояние задачи локально
      setTasks(tasks.map((task) => (task.id === taskId ? { ...task, completed } : task)))
    } catch (error) {
      console.error("Ошибка при обновлении задачи:", error)
    }
  }

  const formatDueDate = (dateString: string) => {
    const date = new Date(dateString)
    const today = new Date()
    const tomorrow = new Date(today)
    tomorrow.setDate(tomorrow.getDate() + 1)

    if (date.toDateString() === today.toDateString()) {
      return `Сегодня, ${date.toLocaleTimeString("ru-RU", { hour: "2-digit", minute: "2-digit" })}`
    } else if (date.toDateString() === tomorrow.toDateString()) {
      return `Завтра, ${date.toLocaleTimeString("ru-RU", { hour: "2-digit", minute: "2-digit" })}`
    } else {
      return date.toLocaleString("ru-RU", {
        day: "numeric",
        month: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      })
    }
  }

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case "High":
        return "bg-red-100 text-red-800 hover:bg-red-100/80"
      case "Medium":
        return "bg-amber-100 text-amber-800 hover:bg-amber-100/80"
      case "Low":
        return "bg-green-100 text-green-800 hover:bg-green-100/80"
      default:
        return "bg-blue-100 text-blue-800 hover:bg-blue-100/80"
    }
  }

  const getPriorityText = (priority: string) => {
    switch (priority) {
      case "High":
        return "Высокий"
      case "Medium":
        return "Средний"
      case "Low":
        return "Низкий"
      default:
        return priority
    }
  }

  if (loading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Предстоящие задачи</CardTitle>
          <CardDescription>Задачи, требующие вашего внимания</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="flex items-start gap-3 animate-pulse">
              <div className="h-4 w-4 mt-1 rounded bg-muted"></div>
              <div className="space-y-2 flex-1">
                <div className="h-4 w-3/4 bg-muted rounded"></div>
                <div className="flex items-center gap-2">
                  <div className="h-3 w-1/3 bg-muted rounded"></div>
                  <div className="h-5 w-16 bg-muted rounded-full"></div>
                </div>
              </div>
            </div>
          ))}
        </CardContent>
      </Card>
    )
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Предстоящие задачи</CardTitle>
        <CardDescription>Задачи, требующие вашего внимания</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {tasks.length > 0 ? (
          tasks.map((task) => (
            <div key={task.id} className="flex items-start gap-3">
              <Checkbox
                id={`task-${task.id}`}
                checked={task.completed}
                onCheckedChange={(checked) => handleTaskComplete(task.id, checked as boolean)}
              />
              <div className="grid gap-1">
                <label
                  htmlFor={`task-${task.id}`}
                  className={`text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 ${
                    task.completed ? "line-through text-muted-foreground" : ""
                  }`}
                >
                  {task.title}
                </label>
                <div className="flex items-center gap-2">
                  <p className="text-xs text-muted-foreground">{formatDueDate(task.due_date)}</p>
                  <Badge variant="outline" className={getPriorityColor(task.priority)}>
                    {getPriorityText(task.priority)}
                  </Badge>
                </div>
              </div>
            </div>
          ))
        ) : (
          <p className="text-sm text-muted-foreground">Нет предстоящих задач</p>
        )}
      </CardContent>
    </Card>
  )
}

