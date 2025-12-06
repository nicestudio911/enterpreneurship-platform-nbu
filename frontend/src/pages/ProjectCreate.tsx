import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { createProject } from '../api/projects'
import { getCompetitions, type Competition } from '../api/competitions'
import './ProjectCreate.css'

function ProjectCreate() {
  const [name, setName] = useState('')
  const [competitionId, setCompetitionId] = useState<number | null>(null)
  const [ideaDescription, setIdeaDescription] = useState('')
  const [competitions, setCompetitions] = useState<Competition[]>([])
  const [selectedCompetition, setSelectedCompetition] = useState<Competition | null>(null)
  const [showAdvice, setShowAdvice] = useState(false)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [loadingCompetitions, setLoadingCompetitions] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    loadCompetitions()
  }, [])

  useEffect(() => {
    if (competitionId) {
      const competition = competitions.find(c => c.id === competitionId)
      setSelectedCompetition(competition || null)
    } else {
      setSelectedCompetition(null)
    }
  }, [competitionId, competitions])

  const loadCompetitions = async () => {
    try {
      const data = await getCompetitions()
      setCompetitions(data)
    } catch (err) {
      console.error('Error loading competitions:', err)
      setError('Failed to load competitions. Please refresh the page.')
    } finally {
      setLoadingCompetitions(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    
    if (!name.trim()) {
      setError('Please enter a project name')
      return
    }

    if (!ideaDescription.trim()) {
      setError('Please describe your idea')
      return
    }

    setLoading(true)

    try {
      const createdProject = await createProject({
        name,
        description: '', // No longer used, but kept for API compatibility
        competition_id: competitionId,
        idea_description: ideaDescription
      })
      // Navigate to project view page
      navigate(`/project/${createdProject.id}`)
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

  const defaultAdvice = "Describe your idea clearly and concisely. Include:\n- The problem you're solving\n- Your solution\n- Target market\n- Unique value proposition\n- How it's different from existing solutions"

  return (
    <div className="project-create-container">
      <div className="project-create-header">
        <h1>Create New Project</h1>
        <p>Start your entrepreneurship journey by creating a new project</p>
      </div>
      
      <div className="form-card">
        <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="name">Project Name</label>
          <input
            type="text"
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
            placeholder="Enter your project name"
          />
        </div>

        <div className="form-group">
          <label htmlFor="competition">Entrepreneur Competition (Optional)</label>
          {loadingCompetitions ? (
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', padding: '1rem' }}>
              <div className="spinner"></div>
              <span>Loading competitions...</span>
            </div>
          ) : (
            <select
              id="competition"
              value={competitionId || ''}
              onChange={(e) => setCompetitionId(e.target.value ? parseInt(e.target.value) : null)}
            >
              <option value="">None - Use default template</option>
              {competitions.map((competition) => (
                <option key={competition.id} value={competition.id}>
                  {competition.name}
                </option>
              ))}
            </select>
          )}
          {selectedCompetition?.description && (
            <div className="competition-description">{selectedCompetition.description}</div>
          )}
          <small style={{ display: 'block', marginTop: '0.5rem', color: 'var(--color-text-tertiary)' }}>
            Selecting a competition will use competition-specific templates and prompts. If no competition is selected, a default template will be used.
          </small>
        </div>

        <div className="form-group">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
            <label htmlFor="ideaDescription" style={{ marginBottom: 0 }}>
              Describe Your Idea *
            </label>
            <button
              type="button"
              onClick={() => setShowAdvice(!showAdvice)}
              className="advice-toggle-btn"
            >
              {showAdvice ? 'Hide' : 'Show'} Writing Tips
            </button>
          </div>
          
          {showAdvice && (
            <div className="advice-panel">
              <h4>How to Describe Your Idea Best</h4>
              <div className="advice-content">
                {selectedCompetition?.advice_prompt ? (
                  <div className="competition-specific-advice">
                    <strong>Competition-specific guidance:</strong>
                    <pre>{selectedCompetition.advice_prompt}</pre>
                  </div>
                ) : (
                  <div className="default-advice">
                    <pre>{defaultAdvice}</pre>
                  </div>
                )}
              </div>
            </div>
          )}

          <textarea
            id="ideaDescription"
            value={ideaDescription}
            onChange={(e) => setIdeaDescription(e.target.value)}
            required
            placeholder="Describe your entrepreneurial idea in detail. Include the problem, solution, target market, and unique value proposition."
            rows={12}
            className="idea-description-textarea"
          />
          <small style={{ display: 'block', marginTop: '0.5rem', color: 'var(--color-text-tertiary)' }}>
            This description will be used to generate the required files for the competition.
          </small>
        </div>

          {error && <div className="alert alert-error">{error}</div>}
          <div className="form-actions">
            <button type="submit" className="btn-primary" disabled={loading || loadingCompetitions}>
              {loading ? 'Creating...' : 'Create Project'}
            </button>
            <button type="button" className="btn-outline" onClick={handleCancel} disabled={loading}>
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default ProjectCreate
