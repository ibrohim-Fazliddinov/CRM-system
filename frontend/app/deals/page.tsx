"use client"

import type React from "react"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Label } from "@/components/ui/label"
import {
  Pagination,
  PaginationContent,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Textarea } from "@/components/ui/textarea"
import { Loader2, Plus, Search, Edit, Trash2, MoreHorizontal, DollarSign } from "lucide-react"
import { dealsService, clientsService } from "@/lib/api"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { toast } from "@/hooks/use-toast"

interface Deal {
  id: number
  title: string
  client: {
    id: number
    name: string
  }
  amount: number
  stage: string
  description: string
  created_at: string
}

interface Client {
  id: number
  name: string
}

export default function DealsPage() {
  const [deals, setDeals] = useState<Deal[]>([])
  const [clients, setClients] = useState<Client[]>([])
  const [loading, setLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState("")
  const [currentPage, setCurrentPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false)
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false)
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false)
  const [selectedDeal, setSelectedDeal] = useState<Deal | null>(null)
  const [formData, setFormData] = useState({
    title: "",
    client_id: "",
    amount: "",
    stage: "lead",
    description: "",
  })

  const fetchDeals = async (page = 1, search = "") => {
    setLoading(true)
    try {
      const params: Record<string, string> = {
        page: page.toString(),
        limit: "10",
      }

      if (search) {
        params.search = search
      }

      const response = await dealsService.getAll(params)
      setDeals(response.results)
      setTotalPages(Math.ceil(response.count / 10))
      setCurrentPage(page)
    } catch (error) {
      console.error("Ошибка при загрузке сделок:", error)
      toast({
        title: "Ошибка",
        description: "Не удалось загрузить список сделок",
        variant: "destructive",
      })
    } finally {
      setLoading(false)
    }
  }

  const fetchClients = async () => {
    try {
      const response = await clientsService.getAll({ limit: "100" })
      setClients(response.results)
    } catch (error) {
      console.error("Ошибка при загрузке клиентов:", error)
    }
  }

  useEffect(() => {
    fetchDeals(currentPage, searchQuery)
    fetchClients()
  }, [currentPage, searchQuery])

  const handleSearch = () => {
    setCurrentPage(1)
    fetchDeals(1, searchQuery)
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleStageChange = (value: string) => {
    setFormData((prev) => ({ ...prev, stage: value }))
  }

  const handleClientChange = (value: string) => {
    setFormData((prev) => ({ ...prev, client_id: value }))
  }

  const resetForm = () => {
    setFormData({
      title: "",
      client_id: "",
      amount: "",
      stage: "lead",
      description: "",
    })
  }

  const handleCreateDeal = async () => {
    try {
      await dealsService.create({
        ...formData,
        amount: Number.parseFloat(formData.amount),
      })
      setIsCreateDialogOpen(false)
      resetForm()
      fetchDeals(currentPage, searchQuery)
      toast({
        title: "Успешно",
        description: "Сделка успешно создана",
      })
    } catch (error) {
      console.error("Ошибка при создании сделки:", error)
      toast({
        title: "Ошибка",
        description: "Не удалось создать сделку",
        variant: "destructive",
      })
    }
  }

  const handleEditDeal = async () => {
    if (!selectedDeal) return

    try {
      await dealsService.update(selectedDeal.id, {
        ...formData,
        amount: Number.parseFloat(formData.amount),
      })
      setIsEditDialogOpen(false)
      fetchDeals(currentPage, searchQuery)
      toast({
        title: "Успешно",
        description: "Данные сделки обновлены",
      })
    } catch (error) {
      console.error("Ошибка при обновлении сделки:", error)
      toast({
        title: "Ошибка",
        description: "Не удалось обновить данные сделки",
        variant: "destructive",
      })
    }
  }

  const handleDeleteDeal = async () => {
    if (!selectedDeal) return

    try {
      await dealsService.delete(selectedDeal.id)
      setIsDeleteDialogOpen(false)
      fetchDeals(currentPage, searchQuery)
      toast({
        title: "Успешно",
        description: "Сделка удалена",
      })
    } catch (error) {
      console.error("Ошибка при удалении сделки:", error)
      toast({
        title: "Ошибка",
        description: "Не удалось удалить сделку",
        variant: "destructive",
      })
    }
  }

  const openEditDialog = (deal: Deal) => {
    setSelectedDeal(deal)
    setFormData({
      title: deal.title,
      client_id: deal.client.id.toString(),
      amount: deal.amount.toString(),
      stage: deal.stage,
      description: deal.description,
    })
    setIsEditDialogOpen(true)
  }

  const openDeleteDialog = (deal: Deal) => {
    setSelectedDeal(deal)
    setIsDeleteDialogOpen(true)
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("ru-RU")
  }

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat("ru-RU", {
      style: "currency",
      currency: "RUB",
      maximumFractionDigits: 0,
    }).format(amount)
  }

  const getStageBadgeClass = (stage: string) => {
    switch (stage.toLowerCase()) {
      case "lead":
        return "bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs"
      case "negotiation":
        return "bg-yellow-100 text-yellow-800 px-2 py-1 rounded-full text-xs"
      case "proposal":
        return "bg-purple-100 text-purple-800 px-2 py-1 rounded-full text-xs"
      case "won":
        return "bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs"
      case "lost":
        return "bg-red-100 text-red-800 px-2 py-1 rounded-full text-xs"
      default:
        return "bg-gray-100 text-gray-800 px-2 py-1 rounded-full text-xs"
    }
  }

  const getStageText = (stage: string) => {
    switch (stage.toLowerCase()) {
      case "lead":
        return "Лид"
      case "negotiation":
        return "Переговоры"
      case "proposal":
        return "Предложение"
      case "won":
        return "Выиграна"
      case "lost":
        return "Проиграна"
      default:
        return stage
    }
  }

  return (
    <div className="container py-10">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Сделки</h1>
        <Dialog open={isCreateDialogOpen} onOpenChange={setIsCreateDialogOpen}>
          <DialogTrigger asChild>
            <Button>
              <Plus className="mr-2 h-4 w-4" />
              Добавить сделку
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Добавить новую сделку</DialogTitle>
              <DialogDescription>Заполните информацию о новой сделке</DialogDescription>
            </DialogHeader>
            <div className="grid gap-4 py-4">
              <div className="space-y-2">
                <Label htmlFor="title">Название</Label>
                <Input id="title" name="title" value={formData.title} onChange={handleInputChange} required />
              </div>
              <div className="space-y-2">
                <Label htmlFor="client_id">Клиент</Label>
                <Select value={formData.client_id} onValueChange={handleClientChange}>
                  <SelectTrigger>
                    <SelectValue placeholder="Выберите клиента" />
                  </SelectTrigger>
                  <SelectContent>
                    {clients.map((client) => (
                      <SelectItem key={client.id} value={client.id.toString()}>
                        {client.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <Label htmlFor="amount">Сумма</Label>
                <div className="relative">
                  <DollarSign className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                  <Input
                    id="amount"
                    name="amount"
                    type="number"
                    className="pl-8"
                    value={formData.amount}
                    onChange={handleInputChange}
                  />
                </div>
              </div>
              <div className="space-y-2">
                <Label htmlFor="stage">Этап</Label>
                <Select value={formData.stage} onValueChange={handleStageChange}>
                  <SelectTrigger>
                    <SelectValue placeholder="Выберите этап" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="lead">Лид</SelectItem>
                    <SelectItem value="negotiation">Переговоры</SelectItem>
                    <SelectItem value="proposal">Предложение</SelectItem>
                    <SelectItem value="won">Выиграна</SelectItem>
                    <SelectItem value="lost">Проиграна</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <Label htmlFor="description">Описание</Label>
                <Textarea
                  id="description"
                  name="description"
                  value={formData.description}
                  onChange={handleInputChange}
                  rows={3}
                />
              </div>
            </div>
            <DialogFooter>
              <Button variant="outline" onClick={() => setIsCreateDialogOpen(false)}>
                Отмена
              </Button>
              <Button onClick={handleCreateDeal}>Создать</Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      </div>

      <Card className="mb-6">
        <CardHeader>
          <div className="flex items-center gap-4">
            <div className="relative flex-1">
              <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
              <Input
                type="search"
                placeholder="Поиск сделок..."
                className="pl-8"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleSearch()}
              />
            </div>
            <Button variant="outline" onClick={handleSearch}>
              Поиск
            </Button>
          </div>
        </CardHeader>
      </Card>

      <Card>
        <CardContent className="p-0">
          {loading ? (
            <div className="flex justify-center items-center py-10">
              <Loader2 className="h-8 w-8 animate-spin text-primary" />
            </div>
          ) : deals.length === 0 ? (
            <div className="text-center py-10 text-muted-foreground">Сделки не найдены</div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Название</TableHead>
                  <TableHead>Клиент</TableHead>
                  <TableHead>Сумма</TableHead>
                  <TableHead>Этап</TableHead>
                  <TableHead>Дата создания</TableHead>
                  <TableHead className="text-right">Действия</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {deals.map((deal) => (
                  <TableRow key={deal.id}>
                    <TableCell className="font-medium">{deal.title}</TableCell>
                    <TableCell>{deal.client.name}</TableCell>
                    <TableCell>{formatCurrency(deal.amount)}</TableCell>
                    <TableCell>
                      <span className={getStageBadgeClass(deal.stage)}>{getStageText(deal.stage)}</span>
                    </TableCell>
                    <TableCell>{formatDate(deal.created_at)}</TableCell>
                    <TableCell className="text-right">
                      <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                          <Button variant="ghost" size="icon">
                            <MoreHorizontal className="h-4 w-4" />
                            <span className="sr-only">Действия</span>
                          </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end">
                          <DropdownMenuItem onClick={() => openEditDialog(deal)}>
                            <Edit className="mr-2 h-4 w-4" />
                            Редактировать
                          </DropdownMenuItem>
                          <DropdownMenuItem onClick={() => openDeleteDialog(deal)} className="text-red-600">
                            <Trash2 className="mr-2 h-4 w-4" />
                            Удалить
                          </DropdownMenuItem>
                        </DropdownMenuContent>
                      </DropdownMenu>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}

          {totalPages > 1 && (
            <div className="py-4 border-t">
              <Pagination>
                <PaginationContent>
                  <PaginationItem>
                    <PaginationPrevious
                      onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
                      className={currentPage === 1 ? "pointer-events-none opacity-50" : ""}
                    />
                  </PaginationItem>

                  {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
                    <PaginationItem key={page}>
                      <PaginationLink onClick={() => setCurrentPage(page)} isActive={currentPage === page}>
                        {page}
                      </PaginationLink>
                    </PaginationItem>
                  ))}

                  <PaginationItem>
                    <PaginationNext
                      onClick={() => setCurrentPage((prev) => Math.min(prev + 1, totalPages))}
                      className={currentPage === totalPages ? "pointer-events-none opacity-50" : ""}
                    />
                  </PaginationItem>
                </PaginationContent>
              </Pagination>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Диалог редактирования */}
      <Dialog open={isEditDialogOpen} onOpenChange={setIsEditDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Редактировать сделку</DialogTitle>
            <DialogDescription>Обновите информацию о сделке</DialogDescription>
          </DialogHeader>
          <div className="grid gap-4 py-4">
            <div className="space-y-2">
              <Label htmlFor="edit-title">Название</Label>
              <Input id="edit-title" name="title" value={formData.title} onChange={handleInputChange} required />
            </div>
            <div className="space-y-2">
              <Label htmlFor="edit-client_id">Клиент</Label>
              <Select value={formData.client_id} onValueChange={handleClientChange}>
                <SelectTrigger>
                  <SelectValue placeholder="Выберите клиента" />
                </SelectTrigger>
                <SelectContent>
                  {clients.map((client) => (
                    <SelectItem key={client.id} value={client.id.toString()}>
                      {client.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>
          <div className="space-y-2">
            <Label htmlFor="edit-amount">Сумма</Label>
            <div className="relative">
              <DollarSign className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
              <Input
                id="edit-amount"
                name="amount"
                type="number"
                className="pl-8"
                value={formData.amount}
                onChange={handleInputChange}
              />
            </div>
          </div>
          <div className="space-y-2">
            <Label htmlFor="edit-stage">Этап</Label>
            <Select value={formData.stage} onValueChange={handleStageChange}>
              <SelectTrigger>
                <SelectValue placeholder="Выберите этап" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="lead">Лид</SelectItem>
                <SelectItem value="negotiation">Переговоры</SelectItem>
                <SelectItem value="proposal">Предложение</SelectItem>
                <SelectItem value="won">Выиграна</SelectItem>
                <SelectItem value="lost">Проиграна</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div className="space-y-2">
            <Label htmlFor="edit-description">Описание</Label>
            <Textarea
              id="edit-description"
              name="description"
              value={formData.description}
              onChange={handleInputChange}
              rows={3}
            />
          </div>
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={() => setIsEditDialogOpen(false)}>
            Отмена
          </Button>
          <Button onClick={handleEditDeal}>Сохранить</Button>
        </DialogFooter>
      </Dialog>

      {/* Диалог удаления */}
      <Dialog open={isDeleteDialogOpen} onOpenChange={setIsDeleteDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Удалить сделку</DialogTitle>
            <DialogDescription>
              Вы уверены, что хотите удалить сделку "{selectedDeal?.title}"? Это действие нельзя отменить.
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button variant="outline" onClick={() => setIsDeleteDialogOpen(false)}>
              Отмена
            </Button>
            <Button variant="destructive" onClick={handleDeleteDeal}>
              Удалить
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}

