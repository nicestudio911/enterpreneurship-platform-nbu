import { Link, useNavigate, useLocation } from 'react-router-dom'
import Logo from './Logo'
import './Navigation.css'

function Navigation() {
  const navigate = useNavigate()
  const location = useLocation()
  const username = localStorage.getItem('username')

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('username')
    navigate('/login')
  }

  // Don't show navigation on login/signup pages
  if (location.pathname === '/login' || location.pathname === '/signup') {
    return null
  }

  return (
    <nav className="main-navigation">
      <div className="nav-container">
        <div className="nav-brand">
          <Link to="/dashboard" className="brand-link">
            <Logo className="logo-white" />
          </Link>
        </div>
        <div className="nav-links">
          <Link to="/dashboard" className={location.pathname === '/dashboard' ? 'active' : ''}>
            Dashboard
          </Link>
          <Link to="/project/create" className={location.pathname === '/project/create' ? 'active' : ''}>
            Create Project
          </Link>
          {username && (
            <span className="nav-username">Hello, {username}</span>
          )}
          <button onClick={handleLogout} className="nav-logout-btn">
            Logout
          </button>
        </div>
      </div>
    </nav>
  )
}

export default Navigation


