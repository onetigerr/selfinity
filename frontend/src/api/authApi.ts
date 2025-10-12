import { apiClient } from './apiClient'

export type UserResponse = {
  id: string
  email: string
  language_preference: 'ru' | 'en'
  created_at: string
}

export type TokenResponse = {
  access_token: string
  token_type: string
}

export const registerUser = async (email: string, password: string): Promise<UserResponse> => {
  const { data } = await apiClient.post<UserResponse>('/auth/register', { email, password })
  return data
}

export const loginUser = async (email: string, password: string): Promise<TokenResponse> => {
  const { data } = await apiClient.post<TokenResponse>('/auth/login', { email, password })
  return data
}

export const getCurrentUser = async (): Promise<UserResponse> => {
  const { data } = await apiClient.get<UserResponse>('/auth/me')
  return data
}

