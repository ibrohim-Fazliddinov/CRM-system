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
import { Loader2, Plus, Search, Edit, Trash2, MoreHorizontal } from "lucide-react"
import { clientsService } from "@/lib/api"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { toast } from "@/hooks/use-toast"

interface Client {
  id: number
  name: string
  email: string
  phone: string
  company: string
  status: string
  created_at: string
}

export default function ClientsPage() {
  const [clients, setClients] = useState<Client[]>([])
  const [loading, setLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState("")
  const [currentPage, setCurrentPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false)
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false)
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false)
  const [selectedClient, setSelectedClient] = useState<Client | null>(null)
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    phone: "",
    company: "",
    status: "active",
  })

  const fetchClients = async (page = 1, search = "") => {
    setLoading(true)
    try {
      const params: Record<string, string> = {
        page: page.toString(),
        limit: "10",
      }

      if (search) {
        params.search = search
      }

      const response = await clientsService.getAll(params)
      setClients(response.results)
      setTotalPages(Math.ceil(response.count / 10))
      setCurrentPage(page)
    } catch (error) {
      console.error("Ошибка при загрузке клиентов:", error)
      toast({
        title: "Ошибка",
        description: "Не удалось загрузить список клиентов",
        variant: "destructive",
      })
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchClients(currentPage, searchQuery)
  }, [currentPage])

  const handleSearch = () => {
    setCurrentPage(1)
    fetchClients(1, searchQuery)
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleStatusChange = (value: string) => {
    setFormData((prev) => ({ ...prev, status: value }))
  }

  const resetForm = () => {
    setFormData({
      name: "",
      email: "",
      phone: "",
      company: "",
      status: "active",
    })
  }

  const handleCreateClient = async () => {
    try {
      await clientsService.create(formData)
      setIsCreateDialogOpen(false)
      resetForm()
      fetchClients(currentPage, searchQuery)
      toast({
        title: "Успешно",
        description: "Клиент успешно создан",
      })
    } catch (error) {
      console.error("Ошибка при создании клиента:", error)
      toast({
        title: "Ошибка",
        description: "Не удалось создать клиента",
        variant: "destructive",
      })
    }
  }

  const handleEditClient = async () => {
    if (!selectedClient) return

    try {
      await clientsService.update(selectedClient.id, formData)
      setIsEditDialogOpen(false)
      fetchClients(currentPage, searchQuery)
      toast({
        title: "Успешно",
        description: "Данные клиента обновлены",
      })
    } catch (error) {
      console.error("Ошибка при обновлении клиента:", error)
      toast({
        title: "Ошибка",
        description: "Не удалось обновить данные клиента",
        variant: "destructive",
      })
    }
  }

  const handleDeleteClient = async () => {
    if (!selectedClient) return

    try {
      await clientsService.delete(selectedClient.id)
      setIsDeleteDialogOpen(false)
      fetchClients(currentPage, searchQuery)
      toast({
        title: "Успешно",
        description: "Клиент удален",
      })
    } catch (error) {
      console.error("Ошибка при удалении клиента:", error)
      toast({
        title: "Ошибка",
        description: "Не удалось удалить клиента",
        variant: "destructive",
      })
    }
  }

  const openEditDialog = (client: Client) => {
    setSelectedClient(client)
    setFormData({
      name: client.name,
      email: client.email,
      phone: client.phone,
      company: client.company,
      status: client.status,
    })
    setIsEditDialogOpen(true)
  }

  const openDeleteDialog = (client: Client) => {
    setSelectedClient(client)
    setIsDeleteDialogOpen(true)
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("ru-RU")
  }

  const getStatusBadgeClass = (status: string) => {
    switch (status.toLowerCase()) {
      case "active":
        return "bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs"
      case "inactive":
        return "bg-gray-100 text-gray-800 px-2 py-1 rounded-full text-xs"
      case "lead":
        return "bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs"
      default:
        return "bg-gray-100 text-gray-800 px-2 py-1 rounded-full text-xs"
    }
  }

  const getStatusText = (status: string) => {
    switch (status.toLowerCase()) {
      case "active":
        return "Активный"
      case "inactive":
        return "Неактивный"
      case "lead":
        return "Лид"
      default:
        return status
    }
  }

  return (
    <div className="container py-10">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Клиенты</h1>
        <Dialog open={isCreateDialogOpen} onOpenChange={setIsCreateDialogOpen}>
          <DialogTrigger asChild>
            <Button>
              <Plus className="mr-2 h-4 w-4" />
              Добавить клиента
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Добавить нового клиента</DialogTitle>
              <DialogDescription>Заполните информацию о новом клиенте</DialogDescription>
            </DialogHeader>
            <div className="grid gap-4 py-4">
              <div className="space-y-2">
                <Label htmlFor="name">Имя</Label>
                <Input id="name" name="name" value={formData.name} onChange={handleInputChange} required />
              </div>
              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input id="email" name="email" type="email" value={formData.email} onChange={handleInputChange} />
              </div>
              <div className="space-y-2">
                <Label htmlFor="phone">Телефон</Label>
                <Input id="phone" name="phone" value={formData.phone} onChange={handleInputChange} />
              </div>
              <div className="space-y-2">
                <Label htmlFor="company">Компания</Label>
                <Input id="company" name="company" value={formData.company} onChange={handleInputChange} />
              </div>
              <div className="space-y-2">
                <Label htmlFor="status">Статус</Label>
                <Select value={formData.status} onValueChange={handleStatusChange}>
                  <SelectTrigger>
                    <SelectValue placeholder="Выберите статус" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="active">Активный</SelectItem>
                    <SelectItem value="inactive">Неактивный</SelectItem>
                    <SelectItem value="lead">Лид</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
            <DialogFooter>
              <Button variant="outline" onClick={() => setIsCreateDialogOpen(false)}>
                Отмена
              </Button>
              <Button onClick={handleCreateClient}>Создать</Button>
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
                placeholder="Поиск клиентов..."
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
          ) : clients.length === 0 ? (
            <div className="text-center py-10 text-muted-foreground">Клиенты не найдены</div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Имя</TableHead>
                  <TableHead>Email</TableHead>
                  <TableHead>Телефон</TableHead>
                  <TableHead>Компания</TableHead>
                  <TableHead>Статус</TableHead>
                  <TableHead>Дата создания</TableHead>
                  <TableHead className="text-right">Действия</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {clients.map((client) => (
                  <TableRow key={client.id}>
                    <TableCell className="font-medium">{client.name}</TableCell>
                    <TableCell>{client.email}</TableCell>
                    <TableCell>{client.phone}</TableCell>
                    <TableCell>{client.company}</TableCell>
                    <TableCell>
                      <span className={getStatusBadgeClass(client.status)}>{getStatusText(client.status)}</span>
                    </TableCell>
                    <TableCell>{formatDate(client.created_at)}</TableCell>
                    <TableCell className="text-right">
                      <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                          <Button variant="ghost" size="icon">
                            <MoreHorizontal className="h-4 w-4" />
                            <span className="sr-only">Действия</span>
                          </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end">
                          <DropdownMenuItem onClick={() => openEditDialog(client)}>
                            <Edit className="mr-2 h-4 w-4" />
                            Редактировать
                          </DropdownMenuItem>
                          <DropdownMenuItem onClick={() => openDeleteDialog(client)} className="text-red-600">
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
            <DialogTitle>Редактировать клиента</DialogTitle>
            <DialogDescription>Обновите информацию о клиенте</DialogDescription>
          </DialogHeader>
          <div className="grid gap-4 py-4">
            <div className="space-y-2">
              <Label htmlFor="edit-name">Имя</Label>
              <Input id="edit-name" name="name" value={formData.name} onChange={handleInputChange} required />
            </div>
            <div className="space-y-2">
              <Label htmlFor="edit-email">Email</Label>
              <Input id="edit-email" name="email" type="email" value={formData.email} onChange={handleInputChange} />
            </div>
            <div className="space-y-2">
              <Label htmlFor="edit-phone">Телефон</Label>
              <Input id="edit-phone" name="phone" value={formData.phone} onChange={handleInputChange} />
            </div>
            <div className="space-y-2">
              <Label htmlFor="edit-company">Компания</Label>
              <Input id="edit-company" name="company" value={formData.company} onChange={handleInputChange} />
            </div>
            <div className="space-y-2">
              <Label htmlFor="edit-status">Статус</Label>
              <Select value={formData.status} onValueChange={handleStatusChange}>
                <SelectTrigger>
                  <SelectValue placeholder="Выберите статус" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="active">Активный</SelectItem>
                  <SelectItem value="inactive">Неактивный</SelectItem>
                  <SelectItem value="lead">Лид</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setIsEditDialogOpen(false)}>
              Отмена
            </Button>
            <Button onClick={handleEditClient}>Сохранить</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Диалог удаления */}
      <Dialog open={isDeleteDialogOpen} onOpenChange={setIsDeleteDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Удалить клиента</DialogTitle>
            <DialogDescription>
              Вы уверены, что хотите удалить клиента {selectedClient?.name}? Это действие нельзя отменить.
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button variant="outline" onClick={() => setIsDeleteDialogOpen(false)}>
              Отмена
            </Button>
            <Button variant="destructive" onClick={handleDeleteClient}>
              Удалить
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}

