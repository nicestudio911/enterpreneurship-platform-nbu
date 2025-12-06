import apiClient from './client'

export interface Project {
  id: number
  name: string
  description: string
  competition_id: number | null
  idea_description: string | null
  created_at: string
}

export interface CreateProjectRequest {
  name: string
  description: string
  competition_id?: number | null
  idea_description?: string | null
}

export interface UpdateProjectRequest {
  name?: string
  description?: string
  idea_description?: string
}

export const getProjects = async (): Promise<Project[]> => {
  const response = await apiClient.get<Project[]>('/projects')
  return response.data
}

export const getProject = async (id: number): Promise<Project> => {
  const response = await apiClient.get<Project>(`/projects/${id}`)
  return response.data
}

export const createProject = async (project: CreateProjectRequest): Promise<Project> => {
  const response = await apiClient.post<Project>('/projects', project)
  return response.data
}

export const updateProject = async (id: number, project: UpdateProjectRequest): Promise<Project> => {
  const response = await apiClient.put<Project>(`/projects/${id}`, project)
  return response.data
}

export const deleteProject = async (id: number): Promise<void> => {
  await apiClient.delete(`/projects/${id}`)
}
