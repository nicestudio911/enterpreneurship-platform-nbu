import { useState, useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { getProjects, deleteProject } from '../api/projects'
import type { Project } from '../api/projects'
import './Dashboard.css'

function Dashboard() {
  const [projects, setProjects] = useState<Project[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [deleting, setDeleting] = useState<number | null>(null)
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

  const handleDeleteProject = async (projectId: number, e: React.MouseEvent) => {
    e.preventDefault()
    e.stopPropagation()
    
    if (!window.confirm('Are you sure you want to delete this project? This action cannot be undone.')) {
      return
    }

    setDeleting(projectId)
    try {
      await deleteProject(projectId)
      setProjects(projects.filter(p => p.id !== projectId))
    } catch (err) {
      console.error('Error deleting project:', err)
      setError('Failed to delete project. Please try again.')
    } finally {
      setDeleting(null)
    }
  }

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <div className="dashboard-header-content">
          <h1>Dashboard</h1>
          <p>Welcome back, {username}!</p>
        </div>
        <div className="dashboard-actions">
          <button className="btn-primary" onClick={handleCreateProject}>
            + Create New Project
          </button>
          <button className="btn-outline" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </div>
      
      {loading && (
        <div className="loading-state">
          <div className="spinner" style={{ margin: '0 auto' }}></div>
          <p style={{ marginTop: '1rem' }}>Loading projects...</p>
        </div>
      )}
      
      {error && <div className="alert alert-error">{error}</div>}
      
      {!loading && projects.length === 0 && (
        <div className="empty-state">
          <div className="empty-state-icon">📁</div>
          <h3>No projects yet</h3>
          <p>Get started by creating your first entrepreneurship project!</p>
          <button className="btn-primary" onClick={handleCreateProject}>
            Create Your First Project
          </button>
        </div>
      )}
      
      {!loading && projects.length > 0 && (
        <div className="projects-grid">
          {projects.map((project) => (
            <div key={project.id} className="project-card">
              <div className="project-card-header">
                <h3 className="project-card-title">
                  <Link to={`/project/${project.id}`}>
                    {project.name}
                  </Link>
                </h3>
              </div>
              <div className="project-card-body">
                {project.idea_description && (
                  <p className="project-card-description">
                    {project.idea_description}
                  </p>
                )}
              </div>
              <div className="project-card-footer">
                <span className="project-card-date">
                  Created: {new Date(project.created_at).toLocaleDateString()}
                </span>
                <div className="project-card-actions">
                  <Link to={`/project/${project.id}`}>
                    <button className="btn-sm btn-primary">View</button>
                  </Link>
                  <button 
                    className="btn-sm btn-danger"
                    onClick={(e) => handleDeleteProject(project.id, e)}
                    disabled={deleting === project.id}
                  >
                    {deleting === project.id ? 'Deleting...' : 'Delete'}
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default Dashboard
