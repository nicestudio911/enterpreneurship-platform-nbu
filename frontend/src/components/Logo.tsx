import './Logo.css'

interface LogoProps {
  className?: string
}

function Logo({ className = '' }: LogoProps) {
  return (
    <svg 
      width="300" 
      height="150" 
      viewBox="0 0 300 150" 
      xmlns="http://www.w3.org/2000/svg"
      className={`logo-svg ${className}`}
    >
      {/* Stylized X with curved, overlapping elements */}
      <g transform="translate(150, 50)" className="logo-x">
        {/* Left stroke of X - curves inward from top left, outward to bottom right */}
        <path 
          d="M -35 -30 Q -10 -5 0 0 Q 10 5 35 30" 
          strokeWidth="12" 
          fill="none" 
          strokeLinecap="round"
          opacity="0.9"
          className="logo-x-stroke"
        />
        
        {/* Right stroke of X - curves inward from top right, outward to bottom left */}
        <path 
          d="M 35 -30 Q 10 -5 0 0 Q -10 5 -35 30" 
          strokeWidth="12" 
          fill="none" 
          strokeLinecap="round"
          opacity="0.9"
          className="logo-x-stroke"
        />
        
        {/* Overlapping center section - darker for depth */}
        <path 
          d="M -15 -10 Q 0 0 15 10" 
          strokeWidth="14" 
          fill="none" 
          strokeLinecap="round"
          opacity="0.8"
          className="logo-x-stroke-center"
        />
        <path 
          d="M 15 -10 Q 0 0 -15 10" 
          strokeWidth="14" 
          fill="none" 
          strokeLinecap="round"
          opacity="0.8"
          className="logo-x-stroke-center"
        />
      </g>
      
      {/* InnovateX text */}
      <text 
        x="150" 
        y="110" 
        fontFamily="Arial, 'Helvetica Neue', sans-serif" 
        fontSize="32" 
        fontWeight="600" 
        className="logo-text"
        textAnchor="middle" 
        letterSpacing="1"
      >
        InnovateX
      </text>
    </svg>
  )
}

export default Logo

