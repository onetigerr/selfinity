import { useForm } from 'react-hook-form'
import { useAuth } from '../hooks/useAuth'

type FormValues = { email: string; password: string }

export default function LoginForm() {
  const { register, handleSubmit } = useForm<FormValues>()
  const auth = useAuth()

  const onSubmit = async (data: FormValues) => {
    await auth.login(data.email, data.password)
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} style={{ maxWidth: 360, margin: '2rem auto' }}>
      <h2>Login</h2>
      <div>
        <label>Email</label>
        <input type="email" {...register('email', { required: true })} />
      </div>
      <div>
        <label>Password</label>
        <input type="password" {...register('password', { required: true, minLength: 6 })} />
      </div>
      <button type="submit">Sign in</button>
    </form>
  )
}

