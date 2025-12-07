import { useState, useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { register } from '../api/auth'
import Logo from '../components/Logo'
import './Signup.css'

function Signup() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  useEffect(() => {
    // Check if user is already logged in
    const token = localStorage.getItem('token')
    if (token) {
      navigate('/dashboard')
      return
    }
  }, [navigate])

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

    // Validate username length
    if (username.length < 3) {
      setError('Username must be at least 3 characters long')
      return
    }

    setLoading(true)

    try {
      const result = await register({ username, password })
      console.log('Registration successful:', result)
      // After successful registration, redirect to login
      navigate('/login', { state: { message: 'Registration successful! Please login.' } })
    } catch (err: any) {
      console.error('Registration error:', err)
      
      // Handle different error types
      if (err.response) {
        // Server responded with an error
        const errorMessage = err.response.data?.detail || err.response.data?.message || 'Registration failed. Please try again.'
        setError(errorMessage)
      } else if (err.request) {
        // Request was made but no response received
        setError('Unable to connect to server. Please check your connection and try again.')
      } else {
        // Something else happened
        setError(err.message || 'Registration failed. Please try again.')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-logo">
          <Logo className="logo-blue" />
        </div>
        <div className="auth-header">
          <h1>Create Account</h1>
          <p>Sign up to get started with your entrepreneurship journey</p>
        </div>

        {error && (
          <div className="alert alert-error">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              minLength={3}
              disabled={loading}
              placeholder="Choose a username"
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
              disabled={loading}
              placeholder="Create a password"
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
              disabled={loading}
              placeholder="Confirm your password"
            />
          </div>

          <button 
            type="submit" 
            className="btn-primary btn-lg auth-submit-btn"
            disabled={loading}
          >
            {loading ? (
              <>
                <div className="spinner" style={{ width: '16px', height: '16px', borderWidth: '2px' }}></div>
                Creating account...
              </>
            ) : (
              'Sign Up'
            )}
          </button>
        </form>

        <div className="auth-footer">
          <p>
            Already have an account?{' '}
            <Link to="/login" className="auth-link">
              Sign in here
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}

export default Signup
