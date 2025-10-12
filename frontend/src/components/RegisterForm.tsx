import { useForm } from 'react-hook-form'
import { useAuth } from '../hooks/useAuth'

type FormValues = { email: string; password: string; confirm_password: string }

export default function RegisterForm() {
  const { register, handleSubmit, watch } = useForm<FormValues>()
  const auth = useAuth()

  const onSubmit = async (data: FormValues) => {
    if (data.password !== data.confirm_password) {
      alert('Passwords do not match')
      return
    }
    await auth.register(data.email, data.password)
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} style={{ maxWidth: 360, margin: '2rem auto' }}>
      <h2>Register</h2>
      <div>
        <label>Email</label>
        <input type="email" {...register('email', { required: true })} />
      </div>
      <div>
        <label>Password</label>
        <input type="password" {...register('password', { required: true, minLength: 6 })} />
      </div>
      <div>
        <label>Confirm Password</label>
        <input type="password" {...register('confirm_password', { required: true, minLength: 6 })} />
      </div>
      <button type="submit">Sign up</button>
    </form>
  )
}

