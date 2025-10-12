import { Link, useNavigate } from 'react-router-dom'
import RegisterForm from '../components/RegisterForm'
import { useAuth } from '../hooks/useAuth'
import { useEffect } from 'react'

export default function RegisterPage() {
  const { user, loading } = useAuth()
  const navigate = useNavigate()

  useEffect(() => {
    if (!loading && user) navigate('/profile')
  }, [loading, user])

  return (
    <div>
      <RegisterForm />
      <p style={{ textAlign: 'center' }}>
        Already have an account? <Link to="/login">Login</Link>
      </p>
    </div>
  )
}

