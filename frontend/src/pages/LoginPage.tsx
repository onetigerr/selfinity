import { Link, useNavigate } from 'react-router-dom'
import LoginForm from '../components/LoginForm'
import { useAuth } from '../hooks/useAuth'
import { useEffect } from 'react'

export default function LoginPage() {
  const { user, loading } = useAuth()
  const navigate = useNavigate()

  useEffect(() => {
    if (!loading && user) navigate('/profile')
  }, [loading, user])

  return (
    <div>
      <LoginForm />
      <p style={{ textAlign: 'center' }}>
        No account? <Link to="/register">Register</Link>
      </p>
    </div>
  )
}

