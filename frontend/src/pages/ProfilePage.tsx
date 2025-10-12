import { useAuth } from '../hooks/useAuth'

export default function ProfilePage() {
  const { user, logout } = useAuth()

  return (
    <div style={{ maxWidth: 640, margin: '2rem auto' }}>
      <h2>Profile</h2>
      {user ? (
        <div>
          <p><strong>Email:</strong> {user.email}</p>
          <p><strong>Language:</strong> {user.language_preference}</p>
          <p><strong>User ID:</strong> {user.id}</p>
          <button onClick={logout}>Logout</button>
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  )
}

