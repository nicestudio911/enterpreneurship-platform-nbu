import { useState, useEffect } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { login } from '../api/auth'

function Login() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()
  const location = useLocation()

  useEffect(() => {
    // Show success message if redirected from signup
    if (location.state?.message) {
      // You could show this as a success message instead of error
      // For now, we'll just clear any existing errors
    }
  }, [location])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const response = await login({ username, password })
      localStorage.setItem('token', response.token)
      localStorage.setItem('username', response.username)
      navigate('/dashboard')
    } catch (err) {
      setError('Login failed. Please check your credentials.')
      console.error('Login error:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <h1>Login</h1>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="username">Username</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        {error && <div className="error">{error}</div>}
        {location.state?.message && (
          <div style={{ color: 'green', marginBottom: '1rem' }}>{location.state.message}</div>
        )}
        <button type="submit" disabled={loading}>
          {loading ? 'Logging in...' : 'Login'}
        </button>
        <div style={{ marginTop: '1rem', textAlign: 'center' }}>
          <p>Don't have an account?</p>
          <button 
            type="button" 
            onClick={() => navigate('/signup')}
            style={{ marginTop: '0.5rem' }}
          >
            Sign Up
          </button>
        </div>
      </form>
    </div>
  )
}

export default Login
