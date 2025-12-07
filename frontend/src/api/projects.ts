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
  if (response.status !== 200) {
    throw new Error(`Failed to fetch projects: ${response.status}`)
  }
  return response.data
}

export const getProject = async (id: number): Promise<Project> => {
  const response = await apiClient.get<Project>(`/projects/${id}`)
  if (response.status !== 200) {
    throw new Error(`Failed to fetch project: ${response.status}`)
  }
  return response.data
}

export const createProject = async (project: CreateProjectRequest): Promise<Project> => {
  const response = await apiClient.post<Project>('/projects', project)
  if (response.status !== 200 && response.status !== 201) {
    throw new Error(`Failed to create project: ${response.status}`)
  }
  return response.data
}

export const updateProject = async (id: number, project: UpdateProjectRequest): Promise<Project> => {
  const response = await apiClient.put<Project>(`/projects/${id}`, project)
  if (response.status !== 200) {
    throw new Error(`Failed to update project: ${response.status}`)
  }
  return response.data
}

export const deleteProject = async (id: number): Promise<void> => {
  const response = await apiClient.delete(`/projects/${id}`)
  if (response.status !== 200 && response.status !== 204) {
    throw new Error(`Failed to delete project: ${response.status}`)
  }
}
