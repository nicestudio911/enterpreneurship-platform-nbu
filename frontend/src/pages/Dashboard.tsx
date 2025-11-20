import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { getProjects } from '../api/projects'
import type { Project } from '../api/projects'

function Dashboard() {
  const [projects, setProjects] = useState<Project[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const navigate = useNavigate()
  const username = localStorage.getItem('username')

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) {
      navigate('/login')
      return
    }

    loadProjects()
  }, [navigate])

  const loadProjects = async () => {
    try {
      const data = await getProjects()
      setProjects(data)
    } catch (err) {
      setError('Failed to load projects')
      console.error('Error loading projects:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('username')
    navigate('/login')
  }

  const handleCreateProject = () => {
    navigate('/project/create')
  }

  return (
    <div className="container">
      <h1>Dashboard</h1>
      <p>Welcome, {username}!</p>
      <div>
        <button onClick={handleCreateProject}>Create New Project</button>
        <button onClick={handleLogout}>Logout</button>
      </div>
      
      {loading && <p>Loading projects...</p>}
      {error && <div className="error">{error}</div>}
      
      <h2>Your Projects</h2>
      {!loading && projects.length === 0 && (
        <p>No projects yet. Create your first project!</p>
      )}
      {projects.length > 0 && (
        <ul className="project-list">
          {projects.map((project) => (
            <li key={project.id}>
              <h3>{project.name}</h3>
              <p>{project.description}</p>
              <small>Created: {new Date(project.createdAt).toLocaleDateString()}</small>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

export default Dashboard
