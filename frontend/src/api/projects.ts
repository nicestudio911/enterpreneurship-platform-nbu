import apiClient from './client'

export interface Project {
  id: number
  name: string
  description: string
  createdAt: string
}

export interface CreateProjectRequest {
  name: string
  description: string
}

export const getProjects = async (): Promise<Project[]> => {
  const response = await apiClient.get<Project[]>('/projects')
  return response.data
}

export const createProject = async (project: CreateProjectRequest): Promise<Project> => {
  const response = await apiClient.post<Project>('/projects', project)
  return response.data
}
