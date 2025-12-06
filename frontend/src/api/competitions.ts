import apiClient from './client'

export interface Competition {
  id: number
  name: string
  description: string | null
  advice_prompt: string | null
  file_generation_prompt: string | null
  created_at: string
}

export const getCompetitions = async (): Promise<Competition[]> => {
  const response = await apiClient.get<Competition[]>('/competitions')
  return response.data
}

export const getCompetition = async (id: number): Promise<Competition> => {
  const response = await apiClient.get<Competition>(`/competitions/${id}`)
  return response.data
}

