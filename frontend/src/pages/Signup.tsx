import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { register } from '../api/auth'

function Signup() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')

    // Validate passwords match
    if (password !== confirmPassword) {
      setError('Passwords do not match')
      return
    }

    // Validate password length
    if (password.length < 3) {
      setError('Password must be at least 3 characters long')
      return
    }

    setLoading(true)

    try {
      console.log('Attempting registration with:', { username })
      
      // Test the connection first
      console.log('Testing API connection...')
      const testURL = '/api/auth/register'
      console.log('Full URL will be:', window.location.origin + testURL)
      
      const result = await register({ username, password })
      console.log('Registration successful:', result)
      // After successful registration, redirect to login
      navigate('/login', { state: { message: 'Registration successful! Please login.' } })
    } catch (err: any) {
      console.error('Registration error details:', {
        error: err,
        message: err.message,
        code: err.code,
        response: err.response,
        request: err.request,
        config: err.config,
        stack: err.stack,
      })
      
      // Handle different error types
      if (err.response) {
        // Server responded with an error
        const errorMessage = err.response.data?.detail || err.response.data?.message || 'Registration failed. Please try again.'
        console.error('Server error response:', err.response.status, errorMessage)
        setError(errorMessage)
      } else if (err.request) {
        // Request was made but no response received
        console.error('No response received. Request details:', {
          url: err.config?.url,
          baseURL: err.config?.baseURL,
          fullURL: (err.config?.baseURL || '') + (err.config?.url || ''),
          method: err.config?.method,
          timeout: err.config?.timeout,
        })
        setError(`Unable to connect to server. Please check your connection and try again. (Error: ${err.message || 'Network error'})`)
      } else if (err.code === 'ECONNABORTED') {
        setError('Request timeout. Please try again.')
      } else {
        // Something else happened
        console.error('Unknown error:', err)
        setError(err.message || 'Registration failed. Please try again.')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <h1>Sign Up</h1>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="username">Username</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            minLength={3}
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
            minLength={3}
          />
        </div>
        <div className="form-group">
          <label htmlFor="confirmPassword">Confirm Password</label>
          <input
            type="password"
            id="confirmPassword"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
            minLength={3}
          />
        </div>
        {error && <div className="error">{error}</div>}
        <button type="submit" disabled={loading}>
          {loading ? 'Creating account...' : 'Sign Up'}
        </button>
        <p style={{ marginTop: '1rem', textAlign: 'center' }}>
          Already have an account? <Link to="/login">Login here</Link>
        </p>
      </form>
    </div>
  )
}

export default Signup

