import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { createProject } from '../api/projects'

function ProjectCreate() {
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      await createProject({ name, description })
      navigate('/dashboard')
    } catch (err) {
      setError('Failed to create project. Please try again.')
      console.error('Error creating project:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleCancel = () => {
    navigate('/dashboard')
  }

  return (
    <div className="container">
      <h1>Create New Project</h1>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="name">Project Name</label>
          <input
            type="text"
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="description">Description</label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            required
          />
        </div>
        {error && <div className="error">{error}</div>}
        <div>
          <button type="submit" disabled={loading}>
            {loading ? 'Creating...' : 'Create Project'}
          </button>
          <button type="button" onClick={handleCancel}>
            Cancel
          </button>
        </div>
      </form>
    </div>
  )
}

export default ProjectCreate
