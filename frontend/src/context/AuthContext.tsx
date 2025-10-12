import React, { createContext, useContext, useEffect, useMemo, useState } from 'react'
import { getCurrentUser, loginUser, registerUser } from '../api/authApi'

type User = {
  id: string
  email: string
  language_preference: 'ru' | 'en'
  created_at: string
}

type AuthContextType = {
  user: User | null
  token: string | null
  login: (email: string, password: string) => Promise<void>
  register: (email: string, password: string) => Promise<void>
  logout: () => void
  loading: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [token, setToken] = useState<string | null>(() => localStorage.getItem('token'))
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState<boolean>(true)

  useEffect(() => {
    const bootstrap = async () => {
      if (token) {
        try {
          const me = await getCurrentUser()
          setUser(me)
        } catch {
          localStorage.removeItem('token')
          setToken(null)
        }
      }
      setLoading(false)
    }
    bootstrap()
  }, [])

  const login = async (email: string, password: string) => {
    const { access_token } = await loginUser(email, password)
    localStorage.setItem('token', access_token)
    setToken(access_token)
    const me = await getCurrentUser()
    setUser(me)
  }

  const register = async (email: string, password: string) => {
    await registerUser(email, password)
    await login(email, password)
  }

  const logout = () => {
    localStorage.removeItem('token')
    setToken(null)
    setUser(null)
  }

  const value = useMemo(() => ({ user, token, login, register, logout, loading }), [user, token, loading])

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export const useAuthContext = () => {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuthContext must be used within AuthProvider')
  return ctx
}

