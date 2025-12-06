import apiClient from './client'

export interface GeneratedFile {
  id: number
  project_id: number
  filename: string
  file_type: string
  status: string
  created_at: string
}

export interface FileContent {
  id: number
  filename: string
  file_type: string
  content: string
}

export interface GenerationLog {
  id: number
  project_id: number
  message: string
  log_type: string
  created_at: string
}

export const generateFiles = async (projectId: number): Promise<{ message: string; project_id: number; status: string }> => {
  const response = await apiClient.post(`/files/generate/${projectId}`)
  return response.data
}

export const getProjectFiles = async (projectId: number): Promise<GeneratedFile[]> => {
  const response = await apiClient.get<GeneratedFile[]>(`/files/project/${projectId}`)
  return response.data
}

export const getGenerationLogs = async (projectId: number): Promise<GenerationLog[]> => {
  const response = await apiClient.get<GenerationLog[]>(`/files/project/${projectId}/logs`)
  return response.data
}

export const downloadFile = async (fileId: number): Promise<Blob> => {
  const response = await apiClient.get(`/files/${fileId}/download`, {
    responseType: 'blob'
  })
  return response.data
}

export const downloadAllFiles = async (projectId: number): Promise<Blob> => {
  const response = await apiClient.get(`/files/project/${projectId}/download-all`, {
    responseType: 'blob'
  })
  return response.data
}

export const getFileContent = async (fileId: number): Promise<FileContent> => {
  const response = await apiClient.get<FileContent>(`/files/${fileId}/content`)
  return response.data
}

export const regenerateSingleFile = async (projectId: number, filename: string): Promise<{ message: string; project_id: number; filename: string; status: string }> => {
  const response = await apiClient.post(`/files/generate/${projectId}/file/${filename}`)
  return response.data
}
