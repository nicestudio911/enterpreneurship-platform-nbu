#!/usr/bin/env python3
"""
Script to update competitions with custom prompts based on their specific requirements
"""
import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, init_db
from app.models.competition import Competition

# Initialize database
init_db()

# Competition-specific prompts based on their actual requirements
COMPETITION_PROMPTS = {
    "Hult Prize": {
        "advice_prompt": """The Hult Prize focuses on social entrepreneurship and solving global challenges. When describing your idea:

1. **Emphasize Social Impact**: Clearly articulate how your solution addresses a pressing global challenge (poverty, education, healthcare, environment, etc.)

2. **Scalability**: Explain how your solution can scale to impact millions of people globally

3. **Sustainability**: Describe a sustainable business model that can operate long-term

4. **Measurable Impact**: Include specific metrics and KPIs for measuring social impact

5. **Team Diversity**: Highlight diverse team backgrounds and relevant experience

6. **Market Understanding**: Demonstrate deep understanding of the problem and target beneficiaries

Focus on creating a compelling narrative that shows both social impact potential and business viability.""",
        
        "file_generation_prompt": """You are an expert consultant helping teams prepare for the Hult Prize, the world's largest student competition for social good.

Generate comprehensive competition materials for a Hult Prize application. The Hult Prize focuses on social entrepreneurship and solving global challenges. Based on the project idea provided, create the following files:

1. **Business Plan** (business_plan.md) - A complete social enterprise business plan including:
   - Executive Summary with clear social impact statement
   - Problem Statement (global challenge being addressed)
   - Solution Description (how it addresses the challenge)
   - Social Impact Metrics (measurable outcomes, beneficiaries)
   - Market Analysis (target beneficiaries, market size)
   - Business Model (revenue streams, sustainability)
   - Implementation Plan (rollout strategy, timeline)
   - Team & Organization (diverse team, advisors)
   - Financial Projections (3-5 years, including impact metrics)
   - Scaling Strategy (how to reach millions of beneficiaries)
   - Risk Analysis & Mitigation

2. **Pitch Deck** (pitch_deck.md) - A 10-12 slide pitch deck structured for Hult Prize:
   - Slide 1: Title - Project Name & Tagline
   - Slide 2: The Global Challenge (problem statement)
   - Slide 3: Our Solution (how it solves the challenge)
   - Slide 4: Social Impact (measurable outcomes, beneficiaries)
   - Slide 5: Market Opportunity (size, reach, scalability)
   - Slide 6: Business Model (sustainable revenue streams)
   - Slide 7: Traction & Validation (proof of concept, early results)
   - Slide 8: Implementation Plan (rollout strategy)
   - Slide 9: Team (diverse backgrounds, relevant experience)
   - Slide 10: Financial Projections (revenue & impact)
   - Slide 11: Scaling Strategy (path to millions)
   - Slide 12: The Ask (funding needs, partnership opportunities)

3. **Executive Summary** (executive_summary.txt) - A 1-2 page summary highlighting:
   - The global challenge being addressed
   - The innovative solution
   - Social impact potential
   - Business viability
   - Team strength
   - Funding needs

4. **Financial Plan** (financial_plan.md) - Detailed financial projections including:
   - Revenue Model (sustainable income streams)
   - Cost Structure (operational costs)
   - 5-Year Financial Projections
   - Social Impact Metrics (beneficiaries reached, outcomes achieved)
   - Break-even Analysis
   - Funding Requirements & Use of Funds
   - Key Financial Assumptions

Make all documents professional, data-driven, and focused on both social impact and business sustainability. Emphasize scalability, measurable impact, and long-term viability."""
    },
    
    "TechCrunch Disrupt Startup Battlefield": {
        "advice_prompt": """TechCrunch Disrupt Startup Battlefield is for early-stage tech startups. When describing your idea:

1. **Focus on Innovation**: Emphasize the technological innovation and unique value proposition

2. **Market Traction**: Highlight any early users, customers, or validation you have

3. **Scalability**: Explain how your tech solution can scale rapidly

4. **Team**: Showcase technical expertise and startup experience

5. **Demo-Ready**: Ensure your idea can be demonstrated clearly

6. **Market Size**: Emphasize the large addressable market

Focus on creating a compelling tech startup narrative that shows rapid growth potential.""",
        
        "file_generation_prompt": """You are an expert consultant helping startups prepare for TechCrunch Disrupt Startup Battlefield, the premier startup competition for early-stage tech companies.

Generate comprehensive competition materials for TechCrunch Disrupt. This competition focuses on innovative tech startups with high growth potential. Based on the project idea provided, create the following files:

1. **Pitch Deck** (pitch_deck.md) - A concise 10-12 slide pitch deck optimized for Startup Battlefield:
   - Slide 1: Title Slide - Company Name, Tagline, Founder Name
   - Slide 2: Problem (pain point you're solving)
   - Slide 3: Solution (your product/service)
   - Slide 4: Market Opportunity (TAM, SAM, SOM)
   - Slide 5: Business Model (how you make money)
   - Slide 6: Traction (users, revenue, key metrics)
   - Slide 7: Product Demo (key features, screenshots description)
   - Slide 8: Go-to-Market Strategy (customer acquisition)
   - Slide 9: Competitive Advantage (what makes you unique)
   - Slide 10: Team (founders, key hires)
   - Slide 11: Financials (revenue projections, unit economics)
   - Slide 12: The Ask (funding round, use of funds)

2. **Business Plan** (business_plan.md) - A comprehensive tech startup business plan:
   - Executive Summary
   - Problem & Solution
   - Product/Technology Description
   - Market Analysis (TAM/SAM/SOM, target customers)
   - Business Model & Revenue Streams
   - Go-to-Market Strategy
   - Traction & Milestones
   - Competitive Analysis
   - Team & Advisors
   - Financial Projections (3 years)
   - Funding Requirements

3. **Executive Summary** (executive_summary.txt) - A 1-page summary for quick review:
   - Problem statement
   - Solution overview
   - Market opportunity
   - Traction highlights
   - Team strength
   - Funding ask

4. **Financial Plan** (financial_plan.md) - Startup financial projections:
   - Revenue Model (SaaS, marketplace, etc.)
   - Unit Economics (CAC, LTV, payback period)
   - 3-Year Financial Projections
   - Key Metrics (MRR, ARR, growth rates)
   - Funding Requirements & Use of Funds
   - Key Assumptions

Make all documents concise, data-driven, and focused on rapid growth potential. Emphasize innovation, traction, and scalability."""
    },
    
    "MIT $100K Entrepreneurship Competition": {
        "advice_prompt": """MIT $100K focuses on innovative, technology-driven startups. When describing your idea:

1. **Technical Innovation**: Emphasize the technical/technological innovation

2. **IP & Research**: Highlight any intellectual property, patents, or research backing

3. **Market Validation**: Show proof of concept, prototypes, or early validation

4. **Team Credentials**: Emphasize technical expertise and academic/research background

5. **Scalability**: Demonstrate how the technology can scale

6. **Competitive Moat**: Explain technical barriers to entry

Focus on creating a compelling narrative that showcases deep technical innovation and strong market potential.""",
        
        "file_generation_prompt": """You are an expert consultant helping teams prepare for the MIT $100K Entrepreneurship Competition, one of the world's premier entrepreneurship competitions for innovative, technology-driven startups.

Generate comprehensive competition materials for MIT $100K. This competition emphasizes technical innovation, intellectual property, and strong market potential. Based on the project idea provided, create the following files:

1. **Business Plan** (business_plan.md) - A comprehensive technology startup business plan:
   - Executive Summary
   - Technology/Innovation Description (technical details, IP)
   - Problem Statement & Market Need
   - Solution & Product Description
   - Intellectual Property (patents, trade secrets, competitive moat)
   - Market Analysis (TAM/SAM/SOM, target segments)
   - Business Model & Revenue Streams
   - Go-to-Market Strategy
   - Traction & Validation (prototypes, pilots, early customers)
   - Competitive Analysis & Differentiation
   - Team & Advisors (technical expertise, research background)
   - Financial Projections (3-5 years)
   - Funding Requirements & Use of Funds
   - Risk Analysis

2. **Pitch Deck** (pitch_deck.md) - A 12-15 slide technical pitch deck:
   - Slide 1: Title - Company, Technology, Team
   - Slide 2: Problem (market need)
   - Slide 3: Technology/Innovation (technical solution)
   - Slide 4: Intellectual Property (patents, competitive advantage)
   - Slide 5: Solution & Product (features, capabilities)
   - Slide 6: Market Opportunity (size, segments)
   - Slide 7: Business Model (revenue streams)
   - Slide 8: Traction (validation, early customers)
   - Slide 9: Go-to-Market Strategy
   - Slide 10: Competitive Landscape & Differentiation
   - Slide 11: Team (technical expertise, credentials)
   - Slide 12: Financial Projections
   - Slide 13: Funding Ask & Use of Funds

3. **Executive Summary** (executive_summary.txt) - A 1-2 page technical summary:
   - Technology innovation
   - Market opportunity
   - Competitive advantage
   - Traction highlights
   - Team credentials
   - Funding needs

4. **Financial Plan** (financial_plan.md) - Technology startup financials:
   - Revenue Model
   - Cost Structure (R&D, operations)
   - 5-Year Financial Projections
   - Key Metrics (unit economics, growth rates)
   - Funding Requirements
   - Use of Funds (R&D, team, market expansion)
   - Key Assumptions

Make all documents technical yet accessible, emphasizing innovation, IP, and strong market potential."""
    },
    
    "MassChallenge": {
        "advice_prompt": """MassChallenge is a global accelerator program. When describing your idea:

1. **Scalability**: Emphasize how your startup can scale globally

2. **Team**: Highlight diverse, experienced team members

3. **Traction**: Show any early validation, customers, or revenue

4. **Market Opportunity**: Demonstrate large addressable market

5. **Innovation**: Show what makes your solution unique

6. **Commitment**: Express readiness for intensive accelerator program

Focus on creating a compelling startup narrative that shows readiness for acceleration and global scaling.""",
        
        "file_generation_prompt": """You are an expert consultant helping startups prepare for MassChallenge, a global zero-equity startup accelerator program.

Generate comprehensive application materials for MassChallenge. This accelerator focuses on high-growth startups across all industries. Based on the project idea provided, create the following files:

1. **Business Plan** (business_plan.md) - A comprehensive startup business plan:
   - Executive Summary
   - Problem & Solution
   - Product/Service Description
   - Market Analysis (TAM/SAM/SOM, target customers)
   - Business Model & Revenue Streams
   - Go-to-Market Strategy
   - Traction & Milestones (customers, revenue, key metrics)
   - Competitive Analysis
   - Team & Advisors
   - Financial Projections (3 years)
   - Funding Requirements
   - Scaling Strategy

2. **Pitch Deck** (pitch_deck.md) - A 10-12 slide accelerator pitch deck:
   - Slide 1: Title - Company, Tagline, Founders
   - Slide 2: Problem (pain point)
   - Slide 3: Solution (product/service)
   - Slide 4: Market Opportunity (size, growth)
   - Slide 5: Business Model (revenue streams)
   - Slide 6: Traction (customers, revenue, metrics)
   - Slide 7: Product Demo (key features)
   - Slide 8: Go-to-Market Strategy
   - Slide 9: Competitive Advantage
   - Slide 10: Team (founders, key hires)
   - Slide 11: Financials (projections, unit economics)
   - Slide 12: The Ask (funding, partnerships)

3. **Executive Summary** (executive_summary.txt) - A 1-page summary:
   - Problem & solution
   - Market opportunity
   - Traction highlights
   - Team strength
   - Funding needs

4. **Financial Plan** (financial_plan.md) - Startup financial projections:
   - Revenue Model
   - Unit Economics
   - 3-Year Financial Projections
   - Key Metrics (growth rates, retention)
   - Funding Requirements
   - Use of Funds

Make all documents professional, data-driven, and focused on scalability and growth potential."""
    },
    
    "IBM Call for Code": {
        "advice_prompt": """IBM Call for Code focuses on technology solutions for social and environmental challenges. When describing your idea:

1. **Social/Environmental Impact**: Clearly articulate the problem you're solving (climate change, disaster response, health, etc.)

2. **Technology Solution**: Emphasize how technology (AI, cloud, IoT, etc.) solves the problem

3. **Open Source**: Consider open-source approach (Call for Code encourages this)

4. **Scalability**: Explain how the solution can scale globally

5. **Team Technical Skills**: Highlight technical expertise in relevant technologies

6. **Measurable Impact**: Include metrics for measuring success

Focus on creating a compelling narrative that combines technical innovation with social/environmental impact.""",
        
        "file_generation_prompt": """You are an expert consultant helping teams prepare for IBM Call for Code, a global challenge that brings together developers to create practical, effective, and high-quality applications based on open source technologies.

Generate comprehensive competition materials for IBM Call for Code. This competition focuses on technology solutions for social and environmental challenges (climate change, disaster response, health, etc.). Based on the project idea provided, create the following files:

1. **Technical Proposal** (business_plan.md) - A comprehensive technical proposal:
   - Executive Summary
   - Problem Statement (social/environmental challenge)
   - Technology Solution (how tech solves the problem)
   - Technical Architecture (system design, technologies used)
   - Open Source Components (libraries, frameworks)
   - Implementation Plan (development phases, timeline)
   - Impact Metrics (measurable outcomes)
   - Scalability & Deployment Strategy
   - Team & Technical Expertise
   - Budget & Resource Requirements
   - Risk Analysis

2. **Pitch Deck** (pitch_deck.md) - A 10-12 slide technical pitch:
   - Slide 1: Title - Project Name, Challenge Area, Team
   - Slide 2: The Challenge (problem statement)
   - Slide 3: Our Solution (technology approach)
   - Slide 4: Technical Architecture (system design)
   - Slide 5: Key Features & Functionality
   - Slide 6: Technology Stack (open source tools)
   - Slide 7: Impact & Metrics (measurable outcomes)
   - Slide 8: Implementation Plan (phases, timeline)
   - Slide 9: Scalability & Deployment
   - Slide 10: Team (technical expertise)
   - Slide 11: Demo/Prototype (current state)
   - Slide 12: Next Steps & Support Needed

3. **Executive Summary** (executive_summary.txt) - A 1-2 page technical summary:
   - Challenge being addressed
   - Technology solution
   - Technical approach
   - Expected impact
   - Team capabilities
   - Support needed

4. **Technical Documentation** (financial_plan.md) - Technical implementation details:
   - System Architecture
   - Technology Stack Details
   - Development Roadmap
   - Resource Requirements
   - Deployment Strategy
   - Maintenance & Support Plan
   - Key Technical Assumptions

Make all documents technical yet accessible, emphasizing open source technologies, measurable impact, and scalability."""
    },
    
    "Startup World Cup": {
        "advice_prompt": """Startup World Cup is a global startup competition. When describing your idea:

1. **Global Scalability**: Emphasize how your startup can scale internationally

2. **Market Traction**: Highlight customers, revenue, or validation

3. **Innovation**: Show what makes your solution unique

4. **Team**: Showcase diverse, experienced team

5. **Market Size**: Demonstrate large addressable market

6. **Business Model**: Clearly explain revenue streams

Focus on creating a compelling global startup narrative.""",
        
        "file_generation_prompt": """You are an expert consultant helping startups prepare for Startup World Cup, a global startup competition connecting entrepreneurs worldwide.

Generate comprehensive competition materials for Startup World Cup. This competition focuses on innovative startups with global scaling potential. Based on the project idea provided, create the following files:

1. **Business Plan** (business_plan.md) - A comprehensive global startup business plan:
   - Executive Summary
   - Problem & Solution
   - Product/Service Description
   - Global Market Analysis (TAM/SAM/SOM across regions)
   - Business Model & Revenue Streams
   - Go-to-Market Strategy (international expansion)
   - Traction & Milestones
   - Competitive Analysis
   - Team & Advisors
   - Financial Projections (3 years, global expansion)
   - Funding Requirements
   - International Scaling Strategy

2. **Pitch Deck** (pitch_deck.md) - A 10-12 slide global pitch deck:
   - Slide 1: Title - Company, Tagline, Founders
   - Slide 2: Problem (global pain point)
   - Slide 3: Solution (product/service)
   - Slide 4: Global Market Opportunity
   - Slide 5: Business Model
   - Slide 6: Traction (customers, revenue, metrics)
   - Slide 7: Product Demo
   - Slide 8: International Go-to-Market
   - Slide 9: Competitive Advantage
   - Slide 10: Team
   - Slide 11: Financials (global projections)
   - Slide 12: The Ask (funding, partnerships)

3. **Executive Summary** (executive_summary.txt) - A 1-page global summary:
   - Problem & solution
   - Global market opportunity
   - Traction highlights
   - Team strength
   - Funding needs

4. **Financial Plan** (financial_plan.md) - Global startup financials:
   - Revenue Model
   - Unit Economics
   - 3-Year Financial Projections (by region)
   - Key Metrics
   - Funding Requirements
   - Use of Funds (international expansion)

Make all documents professional, data-driven, and focused on global scalability."""
    },
    
    "Global Student Entrepreneur Awards (GSEA)": {
        "advice_prompt": """GSEA is for student entrepreneurs. When describing your idea:

1. **Student Status**: Emphasize that you're a student entrepreneur

2. **Business Viability**: Show that your business is operational, not just an idea

3. **Revenue/Impact**: Highlight actual revenue, customers, or measurable impact

4. **Balanced Life**: Show how you balance academics and business

5. **Growth Potential**: Demonstrate scalability

6. **Personal Story**: Include your entrepreneurial journey

Focus on creating a compelling student entrepreneur narrative that shows both business success and personal growth.""",
        
        "file_generation_prompt": """You are an expert consultant helping student entrepreneurs prepare for the Global Student Entrepreneur Awards (GSEA), the premier competition for students who own and operate businesses.

Generate comprehensive competition materials for GSEA. This competition focuses on student entrepreneurs who run actual businesses (not just ideas). Based on the project idea provided, create the following files:

1. **Business Plan** (business_plan.md) - A comprehensive student business plan:
   - Executive Summary
   - Student Entrepreneur Story (your journey, motivation)
   - Problem & Solution
   - Product/Service Description
   - Market Analysis
   - Business Model & Revenue Streams
   - Traction & Results (actual revenue, customers, metrics)
   - Operations (how you run the business as a student)
   - Team & Support Network
   - Financial Statements (actual and projected)
   - Growth Strategy
   - Balancing Academics & Business

2. **Pitch Deck** (pitch_deck.md) - A 10-12 slide student entrepreneur pitch:
   - Slide 1: Title - Your Name, Business Name, Student Status
   - Slide 2: Your Story (entrepreneurial journey)
   - Slide 3: Problem (what you're solving)
   - Slide 4: Solution (your business)
   - Slide 5: Market Opportunity
   - Slide 6: Business Model
   - Slide 7: Traction (revenue, customers, results)
   - Slide 8: Operations (how you run it as a student)
   - Slide 9: Team & Support
   - Slide 10: Financials (actual and projected)
   - Slide 11: Growth Plan
   - Slide 12: Vision & Impact

3. **Executive Summary** (executive_summary.txt) - A 1-2 page student entrepreneur summary:
   - Your entrepreneurial story
   - Business overview
   - Traction and results
   - Growth potential
   - Personal impact

4. **Financial Plan** (financial_plan.md) - Student business financials:
   - Actual Financial Performance
   - Revenue Model
   - Cost Structure
   - 3-Year Projections
   - Key Metrics
   - Growth Investment Needs

Make all documents authentic, showing real business operations and the student entrepreneur journey."""
    },
    
    "Hello Tomorrow Global Challenge": {
        "advice_prompt": """Hello Tomorrow focuses on deep tech startups. When describing your idea:

1. **Deep Tech Innovation**: Emphasize breakthrough technology or scientific innovation

2. **Technical Depth**: Show deep technical/scientific expertise

3. **Market Application**: Connect technology to real-world applications

4. **IP & Research**: Highlight patents, research, or technical barriers

5. **Team Credentials**: Showcase scientific/technical team background

6. **Scalability**: Demonstrate how deep tech can scale

Focus on creating a compelling deep tech narrative that combines scientific innovation with market potential.""",
        
        "file_generation_prompt": """You are an expert consultant helping deep tech startups prepare for Hello Tomorrow Global Challenge, a competition for breakthrough technologies and scientific innovations.

Generate comprehensive competition materials for Hello Tomorrow. This competition focuses on deep tech startups with scientific/technical innovations. Based on the project idea provided, create the following files:

1. **Business Plan** (business_plan.md) - A comprehensive deep tech business plan:
   - Executive Summary
   - Technology/Innovation Description (scientific breakthrough, technical details)
   - Problem & Market Need
   - Solution & Product Description
   - Intellectual Property (patents, research, competitive moat)
   - Market Analysis (applications, market size)
   - Business Model & Revenue Streams
   - Go-to-Market Strategy
   - Traction & Validation (prototypes, pilots, partnerships)
   - Competitive Analysis & Technical Differentiation
   - Team & Scientific Advisors
   - Financial Projections (5 years)
   - Funding Requirements
   - Risk Analysis

2. **Pitch Deck** (pitch_deck.md) - A 12-15 slide deep tech pitch:
   - Slide 1: Title - Company, Technology, Team
   - Slide 2: The Breakthrough (scientific/technical innovation)
   - Slide 3: Problem (market need)
   - Slide 4: Technology Solution (how it works)
   - Slide 5: Intellectual Property (patents, research)
   - Slide 6: Market Applications (use cases)
   - Slide 7: Business Model
   - Slide 8: Traction & Validation
   - Slide 9: Competitive Advantage (technical moat)
   - Slide 10: Team (scientific expertise)
   - Slide 11: Financial Projections
   - Slide 12: Funding Ask

3. **Executive Summary** (executive_summary.txt) - A 1-2 page technical summary:
   - Technology innovation
   - Market applications
   - Competitive advantage
   - Team credentials
   - Funding needs

4. **Financial Plan** (financial_plan.md) - Deep tech financials:
   - Revenue Model
   - R&D Costs
   - 5-Year Financial Projections
   - Key Metrics
   - Funding Requirements
   - Use of Funds (R&D, team, commercialization)

Make all documents technical yet accessible, emphasizing scientific innovation, IP, and market applications."""
    },
    
    "Slush 100 Pitching Competition": {
        "advice_prompt": """Slush 100 is a fast-paced pitch competition. When describing your idea:

1. **Concise Value Prop**: Create a clear, concise value proposition

2. **Market Traction**: Highlight customers, revenue, or growth metrics

3. **Scalability**: Emphasize rapid growth potential

4. **Team**: Showcase strong founding team

5. **Market Size**: Demonstrate large opportunity

6. **Pitch-Ready**: Ensure your idea can be pitched in 3-5 minutes

Focus on creating a compelling, concise pitch narrative that captures attention quickly.""",
        
        "file_generation_prompt": """You are an expert consultant helping startups prepare for Slush 100 Pitching Competition, a fast-paced pitch competition at Europe's leading startup event.

Generate comprehensive competition materials for Slush 100. This is a fast-paced pitch competition - materials must be concise and impactful. Based on the project idea provided, create the following files:

1. **Pitch Deck** (pitch_deck.md) - A concise 8-10 slide pitch deck optimized for quick presentation:
   - Slide 1: Title - Company, Tagline, Founders
   - Slide 2: Problem (one clear pain point)
   - Slide 3: Solution (your product in one sentence)
   - Slide 4: Market Opportunity (TAM, growth)
   - Slide 5: Business Model (how you make money)
   - Slide 6: Traction (customers, revenue, key metrics)
   - Slide 7: Competitive Advantage (what makes you unique)
   - Slide 8: Team (founders, key hires)
   - Slide 9: Financials (revenue projections)
   - Slide 10: The Ask (funding, partnerships)

2. **Business Plan** (business_plan.md) - A concise business plan:
   - Executive Summary
   - Problem & Solution
   - Market Opportunity
   - Business Model
   - Traction & Metrics
   - Competitive Analysis
   - Team
   - Financial Projections (3 years)
   - Funding Requirements

3. **Executive Summary** (executive_summary.txt) - A 1-page summary:
   - Problem & solution
   - Market opportunity
   - Traction highlights
   - Team strength
   - Funding ask

4. **Financial Plan** (financial_plan.md) - Startup financials:
   - Revenue Model
   - Unit Economics
   - 3-Year Projections
   - Key Metrics
   - Funding Requirements

Make all documents concise, data-driven, and pitch-ready. Focus on clarity and impact."""
    },
    
    "Web Summit PITCH": {
        "advice_prompt": """Web Summit PITCH is for early-stage startups. When describing your idea:

1. **Innovation**: Emphasize what makes your solution unique

2. **Market Traction**: Highlight early users, customers, or validation

3. **Scalability**: Show rapid growth potential

4. **Team**: Showcase founding team strength

5. **Market Opportunity**: Demonstrate large addressable market

6. **Pitch-Ready**: Ensure clear, compelling pitch narrative

Focus on creating a compelling startup pitch that stands out in a competitive field.""",
        
        "file_generation_prompt": """You are an expert consultant helping startups prepare for Web Summit PITCH, one of the world's largest startup pitch competitions.

Generate comprehensive competition materials for Web Summit PITCH. This competition focuses on early-stage startups with innovative solutions. Based on the project idea provided, create the following files:

1. **Pitch Deck** (pitch_deck.md) - A 10-12 slide pitch deck:
   - Slide 1: Title - Company, Tagline, Founders
   - Slide 2: Problem (pain point)
   - Slide 3: Solution (product/service)
   - Slide 4: Market Opportunity (TAM/SAM/SOM)
   - Slide 5: Business Model
   - Slide 6: Traction (users, revenue, metrics)
   - Slide 7: Product Demo (key features)
   - Slide 8: Go-to-Market Strategy
   - Slide 9: Competitive Advantage
   - Slide 10: Team
   - Slide 11: Financials
   - Slide 12: The Ask

2. **Business Plan** (business_plan.md) - A comprehensive startup plan:
   - Executive Summary
   - Problem & Solution
   - Market Analysis
   - Business Model
   - Traction & Milestones
   - Competitive Analysis
   - Team
   - Financial Projections (3 years)
   - Funding Requirements

3. **Executive Summary** (executive_summary.txt) - A 1-page summary:
   - Problem & solution
   - Market opportunity
   - Traction highlights
   - Team strength
   - Funding needs

4. **Financial Plan** (financial_plan.md) - Startup financials:
   - Revenue Model
   - Unit Economics
   - 3-Year Projections
   - Key Metrics
   - Funding Requirements

Make all documents professional, data-driven, and focused on innovation and growth potential."""
    },
    
    "Startup Grind Global Pitch Competition": {
        "advice_prompt": """Startup Grind focuses on community and mentorship. When describing your idea:

1. **Community Impact**: Show how your startup benefits the community

2. **Mentorship Readiness**: Express openness to mentorship and learning

3. **Traction**: Highlight customers, revenue, or validation

4. **Team**: Showcase coachable, dedicated team

5. **Market Opportunity**: Demonstrate market potential

6. **Growth Mindset**: Show commitment to learning and growth

Focus on creating a compelling narrative that shows community engagement and growth mindset.""",
        
        "file_generation_prompt": """You are an expert consultant helping startups prepare for Startup Grind Global Pitch Competition, a competition focused on community, mentorship, and entrepreneurial growth.

Generate comprehensive competition materials for Startup Grind. This competition emphasizes community impact, mentorship readiness, and growth mindset. Based on the project idea provided, create the following files:

1. **Business Plan** (business_plan.md) - A comprehensive startup plan:
   - Executive Summary
   - Problem & Solution
   - Community Impact (how you benefit the community)
   - Market Analysis
   - Business Model
   - Traction & Milestones
   - Mentorship & Learning Journey
   - Competitive Analysis
   - Team (coachable, dedicated)
   - Financial Projections (3 years)
   - Funding Requirements
   - Growth Strategy

2. **Pitch Deck** (pitch_deck.md) - A 10-12 slide community-focused pitch:
   - Slide 1: Title - Company, Tagline, Founders
   - Slide 2: Problem
   - Slide 3: Solution
   - Slide 4: Community Impact
   - Slide 5: Market Opportunity
   - Slide 6: Business Model
   - Slide 7: Traction
   - Slide 8: Mentorship & Learning
   - Slide 9: Competitive Advantage
   - Slide 10: Team (growth mindset)
   - Slide 11: Financials
   - Slide 12: The Ask

3. **Executive Summary** (executive_summary.txt) - A 1-page summary:
   - Problem & solution
   - Community impact
   - Traction highlights
   - Team strength
   - Funding needs

4. **Financial Plan** (financial_plan.md) - Startup financials:
   - Revenue Model
   - Unit Economics
   - 3-Year Projections
   - Key Metrics
   - Funding Requirements

Make all documents professional, emphasizing community impact, mentorship readiness, and growth potential."""
    },
    
    "Microsoft Imagine Cup (tech-focused)": {
        "advice_prompt": """Microsoft Imagine Cup is for student tech teams. When describing your idea:

1. **Technology Innovation**: Emphasize innovative use of technology

2. **Microsoft Technologies**: Consider incorporating Microsoft tools/platforms

3. **Social Impact**: Show how tech solves real-world problems

4. **Team Technical Skills**: Highlight technical expertise

5. **Prototype/Demo**: Ensure you have a working prototype

6. **Scalability**: Demonstrate how solution can scale

Focus on creating a compelling tech innovation narrative with social impact.""",
        
        "file_generation_prompt": """You are an expert consultant helping student tech teams prepare for Microsoft Imagine Cup, the world's premier student technology competition.

Generate comprehensive competition materials for Microsoft Imagine Cup. This competition focuses on student teams using technology to solve real-world problems. Based on the project idea provided, create the following files:

1. **Technical Proposal** (business_plan.md) - A comprehensive technical proposal:
   - Executive Summary
   - Problem Statement (real-world problem)
   - Technology Solution (innovative tech approach)
   - Microsoft Technologies Used (Azure, AI, etc.)
   - Technical Architecture
   - Prototype/Demo Description
   - Social Impact (how it helps people)
   - Implementation Plan
   - Team & Technical Skills
   - Scalability & Future Plans
   - Budget & Resources

2. **Pitch Deck** (pitch_deck.md) - A 10-12 slide technical pitch:
   - Slide 1: Title - Project Name, Team, University
   - Slide 2: The Problem (real-world challenge)
   - Slide 3: Our Solution (technology approach)
   - Slide 4: Microsoft Technologies (tools/platforms used)
   - Slide 5: Technical Architecture
   - Slide 6: Prototype/Demo (current state)
   - Slide 7: Social Impact (who it helps)
   - Slide 8: Key Features
   - Slide 9: Implementation Plan
   - Slide 10: Team (technical skills)
   - Slide 11: Future Vision
   - Slide 12: Support Needed

3. **Executive Summary** (executive_summary.txt) - A 1-2 page technical summary:
   - Problem being solved
   - Technology solution
   - Microsoft technologies
   - Social impact
   - Team capabilities
   - Future plans

4. **Technical Documentation** (financial_plan.md) - Technical implementation details:
   - System Architecture
   - Technology Stack (Microsoft tools)
   - Development Roadmap
   - Resource Requirements
   - Deployment Strategy
   - Key Technical Assumptions

Make all documents technical yet accessible, emphasizing Microsoft technologies, social impact, and student innovation."""
    },
    
    "European Innovation Council (EIC) Accelerator": {
        "advice_prompt": """EIC Accelerator is for deep tech and high-risk innovations. When describing your idea:

1. **Deep Innovation**: Emphasize breakthrough technology or innovation

2. **Market Potential**: Show large market opportunity

3. **Technical Feasibility**: Demonstrate technical viability

4. **Team Expertise**: Highlight strong technical/scientific team

5. **IP & Competitive Moat**: Show intellectual property or barriers to entry

6. **EU Impact**: Consider EU market focus and impact

Focus on creating a compelling deep tech narrative with strong market potential.""",
        
        "file_generation_prompt": """You are an expert consultant helping startups prepare for the European Innovation Council (EIC) Accelerator, the EU's flagship program for deep tech and high-risk innovations.

Generate comprehensive application materials for EIC Accelerator. This program focuses on breakthrough technologies with high market potential. Based on the project idea provided, create the following files:

1. **Business Plan** (business_plan.md) - A comprehensive deep tech business plan:
   - Executive Summary
   - Innovation Description (breakthrough technology)
   - Problem & Market Need
   - Solution & Product
   - Intellectual Property (patents, competitive moat)
   - Market Analysis (EU and global market)
   - Business Model & Revenue Streams
   - Go-to-Market Strategy
   - Traction & Validation
   - Competitive Analysis
   - Team & Scientific Advisors
   - Financial Projections (5 years)
   - Funding Requirements
   - EU Impact & Alignment
   - Risk Analysis

2. **Pitch Deck** (pitch_deck.md) - A 12-15 slide EIC pitch:
   - Slide 1: Title - Company, Innovation, Team
   - Slide 2: The Innovation (breakthrough technology)
   - Slide 3: Problem (market need)
   - Slide 4: Solution (product/technology)
   - Slide 5: Intellectual Property
   - Slide 6: Market Opportunity (EU & global)
   - Slide 7: Business Model
   - Slide 8: Traction & Validation
   - Slide 9: Competitive Advantage
   - Slide 10: Team (technical expertise)
   - Slide 11: Financial Projections
   - Slide 12: EU Impact
   - Slide 13: Funding Ask

3. **Executive Summary** (executive_summary.txt) - A 1-2 page summary:
   - Innovation description
   - Market opportunity
   - Competitive advantage
   - Team credentials
   - EU impact
   - Funding needs

4. **Financial Plan** (financial_plan.md) - Deep tech financials:
   - Revenue Model
   - R&D Costs
   - 5-Year Financial Projections
   - Key Metrics
   - Funding Requirements
   - Use of Funds
   - Key Assumptions

Make all documents professional, emphasizing deep innovation, market potential, and EU impact."""
    },
    
    "ClimateLaunchpad (green startups)": {
        "advice_prompt": """ClimateLaunchpad focuses on climate solutions. When describing your idea:

1. **Climate Impact**: Clearly articulate the environmental/climate problem

2. **Solution Impact**: Show measurable environmental benefits

3. **Business Viability**: Demonstrate sustainable business model

4. **Scalability**: Explain how solution can scale globally

5. **Market Opportunity**: Show market demand for climate solutions

6. **Team Passion**: Highlight team commitment to climate action

Focus on creating a compelling climate solution narrative that combines environmental impact with business viability.""",
        
        "file_generation_prompt": """You are an expert consultant helping green startups prepare for ClimateLaunchpad, the world's largest green business idea competition.

Generate comprehensive competition materials for ClimateLaunchpad. This competition focuses on climate solutions and green startups. Based on the project idea provided, create the following files:

1. **Business Plan** (business_plan.md) - A comprehensive green business plan:
   - Executive Summary
   - Climate Problem (environmental challenge)
   - Solution Description (how it addresses climate)
   - Environmental Impact (measurable benefits, CO2 reduction)
   - Market Analysis (demand for climate solutions)
   - Business Model & Revenue Streams
   - Go-to-Market Strategy
   - Traction & Validation
   - Competitive Analysis
   - Team & Climate Commitment
   - Financial Projections (3-5 years)
   - Funding Requirements
   - Scaling Strategy (global climate impact)

2. **Pitch Deck** (pitch_deck.md) - A 10-12 slide climate-focused pitch:
   - Slide 1: Title - Company, Climate Solution, Team
   - Slide 2: The Climate Problem
   - Slide 3: Our Solution
   - Slide 4: Environmental Impact (metrics, CO2 reduction)
   - Slide 5: Market Opportunity
   - Slide 6: Business Model
   - Slide 7: Traction
   - Slide 8: Go-to-Market
   - Slide 9: Competitive Advantage
   - Slide 10: Team (climate commitment)
   - Slide 11: Financials
   - Slide 12: The Ask

3. **Executive Summary** (executive_summary.txt) - A 1-2 page climate summary:
   - Climate problem
   - Solution overview
   - Environmental impact
   - Market opportunity
   - Team strength
   - Funding needs

4. **Financial Plan** (financial_plan.md) - Green startup financials:
   - Revenue Model
   - Cost Structure
   - 5-Year Financial Projections
   - Environmental Impact Metrics
   - Funding Requirements
   - Use of Funds

Make all documents professional, emphasizing climate impact, environmental benefits, and business sustainability."""
    },
    
    "XPRIZE Challenges": {
        "advice_prompt": """XPRIZE focuses on breakthrough innovations for grand challenges. When describing your idea:

1. **Grand Challenge**: Clearly define the major challenge you're addressing

2. **Breakthrough Innovation**: Emphasize revolutionary approach

3. **Measurable Impact**: Include specific, measurable outcomes

4. **Technical Feasibility**: Demonstrate technical viability

5. **Team Expertise**: Highlight world-class team

6. **Scalability**: Show how solution can have global impact

Focus on creating a compelling narrative for solving a grand challenge with breakthrough innovation.""",
        
        "file_generation_prompt": """You are an expert consultant helping teams prepare for XPRIZE Challenges, competitions that incentivize breakthrough innovations to solve humanity's grand challenges.

Generate comprehensive competition materials for XPRIZE. This competition focuses on breakthrough innovations for grand challenges (climate, health, education, etc.). Based on the project idea provided, create the following files:

1. **Technical Proposal** (business_plan.md) - A comprehensive breakthrough innovation proposal:
   - Executive Summary
   - Grand Challenge (major problem being addressed)
   - Breakthrough Innovation (revolutionary approach)
   - Technical Solution (how it works)
   - Measurable Impact (specific, quantifiable outcomes)
   - Technical Feasibility (proof of concept, validation)
   - Implementation Plan (phases, timeline)
   - Scalability & Global Impact
   - Team & World-Class Expertise
   - Budget & Resource Requirements
   - Risk Analysis
   - Long-term Vision

2. **Pitch Deck** (pitch_deck.md) - A 12-15 slide breakthrough innovation pitch:
   - Slide 1: Title - Project, Grand Challenge, Team
   - Slide 2: The Grand Challenge
   - Slide 3: Breakthrough Innovation
   - Slide 4: Technical Solution
   - Slide 5: Measurable Impact (metrics, outcomes)
   - Slide 6: Technical Feasibility (proof, validation)
   - Slide 7: Implementation Plan
   - Slide 8: Scalability & Global Impact
   - Slide 9: Competitive Advantage
   - Slide 10: Team (world-class expertise)
   - Slide 11: Budget & Resources
   - Slide 12: Long-term Vision
   - Slide 13: Support Needed

3. **Executive Summary** (executive_summary.txt) - A 1-2 page breakthrough summary:
   - Grand challenge
   - Breakthrough innovation
   - Measurable impact
   - Technical feasibility
   - Team expertise
   - Support needed

4. **Technical Documentation** (financial_plan.md) - Technical implementation:
   - System Architecture
   - Technology Stack
   - Development Roadmap
   - Resource Requirements
   - Impact Metrics
   - Key Technical Assumptions

Make all documents professional, emphasizing breakthrough innovation, measurable impact, and global scalability."""
    },
    
    "Chivas Venture": {
        "advice_prompt": """Chivas Venture focuses on social entrepreneurs. When describing your idea:

1. **Social Impact**: Clearly articulate the social problem

2. **Sustainable Business**: Show sustainable business model

3. **Measurable Impact**: Include specific social impact metrics

4. **Scalability**: Explain how solution can scale

5. **Team Commitment**: Highlight team dedication to social mission

6. **Financial Sustainability**: Demonstrate long-term viability

Focus on creating a compelling social enterprise narrative that balances impact and sustainability.""",
        
        "file_generation_prompt": """You are an expert consultant helping social entrepreneurs prepare for Chivas Venture, a global competition for social entrepreneurs creating positive change.

Generate comprehensive competition materials for Chivas Venture. This competition focuses on social enterprises that balance social impact with business sustainability. Based on the project idea provided, create the following files:

1. **Business Plan** (business_plan.md) - A comprehensive social enterprise plan:
   - Executive Summary
   - Social Problem (challenge being addressed)
   - Solution Description (how it creates social impact)
   - Social Impact Metrics (measurable outcomes, beneficiaries)
   - Market Analysis
   - Sustainable Business Model (revenue streams)
   - Operations & Implementation
   - Traction & Results (impact achieved)
   - Competitive Analysis
   - Team & Social Mission Commitment
   - Financial Projections (3-5 years)
   - Funding Requirements
   - Scaling Strategy (social impact at scale)

2. **Pitch Deck** (pitch_deck.md) - A 10-12 slide social enterprise pitch:
   - Slide 1: Title - Company, Social Mission, Team
   - Slide 2: The Social Problem
   - Slide 3: Our Solution
   - Slide 4: Social Impact (metrics, beneficiaries)
   - Slide 5: Sustainable Business Model
   - Slide 6: Market Opportunity
   - Slide 7: Traction & Impact Results
   - Slide 8: Operations & Implementation
   - Slide 9: Competitive Advantage
   - Slide 10: Team (social mission commitment)
   - Slide 11: Financials (sustainable model)
   - Slide 12: The Ask

3. **Executive Summary** (executive_summary.txt) - A 1-2 page social impact summary:
   - Social problem
   - Solution overview
   - Social impact metrics
   - Business sustainability
   - Team commitment
   - Funding needs

4. **Financial Plan** (financial_plan.md) - Social enterprise financials:
   - Revenue Model (sustainable)
   - Cost Structure
   - 5-Year Financial Projections
   - Social Impact Metrics
   - Funding Requirements
   - Use of Funds

Make all documents professional, emphasizing social impact, measurable outcomes, and business sustainability."""
    },
    
    "Seedstars World Competition": {
        "advice_prompt": """Seedstars focuses on emerging market startups. When describing your idea:

1. **Emerging Market Focus**: Emphasize relevance to emerging markets

2. **Local Impact**: Show understanding of local context

3. **Scalability**: Demonstrate potential to scale regionally/globally

4. **Traction**: Highlight customers, revenue, or validation

5. **Team Local Knowledge**: Showcase local market expertise

6. **Market Opportunity**: Demonstrate large emerging market opportunity

Focus on creating a compelling emerging market startup narrative.""",
        
        "file_generation_prompt": """You are an expert consultant helping startups prepare for Seedstars World Competition, a global competition for emerging market startups.

Generate comprehensive competition materials for Seedstars. This competition focuses on startups from emerging markets with local impact and global scalability. Based on the project idea provided, create the following files:

1. **Business Plan** (business_plan.md) - A comprehensive emerging market startup plan:
   - Executive Summary
   - Problem & Solution (local context)
   - Market Analysis (emerging market opportunity)
   - Local Impact (how it helps local communities)
   - Business Model & Revenue Streams
   - Go-to-Market Strategy (local and regional)
   - Traction & Milestones
   - Competitive Analysis
   - Team & Local Market Expertise
   - Financial Projections (3 years)
   - Funding Requirements
   - Regional/Global Scaling Strategy

2. **Pitch Deck** (pitch_deck.md) - A 10-12 slide emerging market pitch:
   - Slide 1: Title - Company, Market, Founders
   - Slide 2: Problem (local/emerging market challenge)
   - Slide 3: Solution
   - Slide 4: Local Impact
   - Slide 5: Emerging Market Opportunity
   - Slide 6: Business Model
   - Slide 7: Traction
   - Slide 8: Go-to-Market (local & regional)
   - Slide 9: Competitive Advantage
   - Slide 10: Team (local expertise)
   - Slide 11: Financials
   - Slide 12: The Ask

3. **Executive Summary** (executive_summary.txt) - A 1-page emerging market summary:
   - Problem & solution
   - Local impact
   - Market opportunity
   - Traction highlights
   - Team strength
   - Funding needs

4. **Financial Plan** (financial_plan.md) - Emerging market startup financials:
   - Revenue Model
   - Unit Economics
   - 3-Year Projections
   - Key Metrics
   - Funding Requirements
   - Use of Funds (local & regional expansion)

Make all documents professional, emphasizing local impact, emerging market understanding, and regional scalability."""
    },
    
    "She Loves Tech Global Competition (female-led)": {
        "advice_prompt": """She Loves Tech supports female tech entrepreneurs. When describing your idea:

1. **Tech Innovation**: Emphasize technology-driven solution

2. **Female Leadership**: Highlight female founder/leadership

3. **Market Impact**: Show how solution addresses real problems

4. **Traction**: Highlight customers, revenue, or validation

5. **Team Diversity**: Showcase diverse team

6. **Scalability**: Demonstrate growth potential

Focus on creating a compelling female tech entrepreneur narrative that showcases innovation and leadership.""",
        
        "file_generation_prompt": """You are an expert consultant helping female tech entrepreneurs prepare for She Loves Tech Global Competition, the world's largest competition for women in tech.

Generate comprehensive competition materials for She Loves Tech. This competition focuses on female-led tech startups with innovative solutions. Based on the project idea provided, create the following files:

1. **Business Plan** (business_plan.md) - A comprehensive female-led tech startup plan:
   - Executive Summary
   - Problem & Solution (tech-driven)
   - Technology Innovation
   - Market Analysis
   - Business Model & Revenue Streams
   - Go-to-Market Strategy
   - Traction & Milestones
   - Competitive Analysis
   - Team & Female Leadership (diverse team)
   - Financial Projections (3 years)
   - Funding Requirements
   - Growth Strategy

2. **Pitch Deck** (pitch_deck.md) - A 10-12 slide female tech entrepreneur pitch:
   - Slide 1: Title - Company, Tech Solution, Female Founder
   - Slide 2: Problem
   - Slide 3: Tech Solution
   - Slide 4: Technology Innovation
   - Slide 5: Market Opportunity
   - Slide 6: Business Model
   - Slide 7: Traction
   - Slide 8: Product Demo
   - Slide 9: Competitive Advantage
   - Slide 10: Team (female leadership, diversity)
   - Slide 11: Financials
   - Slide 12: The Ask

3. **Executive Summary** (executive_summary.txt) - A 1-page tech summary:
   - Problem & tech solution
   - Innovation highlights
   - Traction highlights
   - Team strength (female leadership)
   - Funding needs

4. **Financial Plan** (financial_plan.md) - Tech startup financials:
   - Revenue Model
   - Unit Economics
   - 3-Year Projections
   - Key Metrics
   - Funding Requirements

Make all documents professional, emphasizing tech innovation, female leadership, and market impact."""
    },
    
    "Youth Entrepreneurship Challenge by JA Worldwide": {
        "advice_prompt": """JA Worldwide focuses on youth entrepreneurship education. When describing your idea:

1. **Youth Perspective**: Emphasize unique youth perspective

2. **Learning Journey**: Show entrepreneurial learning and growth

3. **Business Viability**: Demonstrate actual business operations

4. **Community Impact**: Highlight community benefit

5. **Team Collaboration**: Showcase teamwork and collaboration

6. **Future Potential**: Demonstrate growth and learning potential

Focus on creating a compelling youth entrepreneur narrative that shows learning, growth, and impact.""",
        
        "file_generation_prompt": """You are an expert consultant helping youth entrepreneurs prepare for the Youth Entrepreneurship Challenge by JA Worldwide, a competition focused on youth entrepreneurship education and development.

Generate comprehensive competition materials for JA Worldwide Youth Challenge. This competition focuses on young entrepreneurs (students/youth) with actual business operations. Based on the project idea provided, create the following files:

1. **Business Plan** (business_plan.md) - A comprehensive youth business plan:
   - Executive Summary
   - Youth Entrepreneur Story (learning journey, motivation)
   - Problem & Solution
   - Product/Service Description
   - Market Analysis
   - Business Model & Revenue Streams
   - Operations (how you run the business)
   - Traction & Results (actual revenue, customers)
   - Community Impact
   - Team & Collaboration
   - Financial Statements (actual and projected)
   - Growth Strategy
   - Learning & Development Journey

2. **Pitch Deck** (pitch_deck.md) - A 10-12 slide youth entrepreneur pitch:
   - Slide 1: Title - Your Name, Business, Age/Student Status
   - Slide 2: Your Story (entrepreneurial journey)
   - Slide 3: Problem
   - Slide 4: Solution
   - Slide 5: Market Opportunity
   - Slide 6: Business Model
   - Slide 7: Traction (revenue, customers)
   - Slide 8: Community Impact
   - Slide 9: Team & Collaboration
   - Slide 10: Financials
   - Slide 11: Growth Plan
   - Slide 12: Vision & Learning

3. **Executive Summary** (executive_summary.txt) - A 1-2 page youth summary:
   - Your entrepreneurial story
   - Business overview
   - Traction and results
   - Community impact
   - Learning journey
   - Future potential

4. **Financial Plan** (financial_plan.md) - Youth business financials:
   - Actual Financial Performance
   - Revenue Model
   - Cost Structure
   - 3-Year Projections
   - Key Metrics
   - Growth Investment Needs

Make all documents authentic, showing real business operations, learning journey, and youth perspective."""
    },
    
    "UN World Tourism Startup Competition": {
        "advice_prompt": """UN World Tourism focuses on sustainable tourism. When describing your idea:

1. **Tourism Innovation**: Emphasize innovation in tourism sector

2. **Sustainability**: Show environmental and social sustainability

3. **Local Impact**: Highlight benefit to local communities

4. **Scalability**: Demonstrate potential to scale

5. **Market Opportunity**: Show tourism market potential

6. **UN SDGs Alignment**: Connect to UN Sustainable Development Goals

Focus on creating a compelling sustainable tourism innovation narrative.""",
        
        "file_generation_prompt": """You are an expert consultant helping startups prepare for the UN World Tourism Startup Competition, focused on sustainable tourism innovations.

Generate comprehensive competition materials for UN World Tourism Competition. This competition focuses on innovative solutions for sustainable tourism. Based on the project idea provided, create the following files:

1. **Business Plan** (business_plan.md) - A comprehensive sustainable tourism business plan:
   - Executive Summary
   - Tourism Innovation (what makes it innovative)
   - Problem Statement (tourism challenges)
   - Solution Description (sustainable tourism approach)
   - Environmental Sustainability (environmental impact, benefits)
   - Social Sustainability (local community impact)
   - Market Analysis (tourism market opportunity)
   - Business Model & Revenue Streams
   - Go-to-Market Strategy
   - Traction & Validation
   - Competitive Analysis
   - Team & Tourism Expertise
   - Financial Projections (3-5 years)
   - Funding Requirements
   - UN SDGs Alignment (which goals it supports)
   - Scaling Strategy

2. **Pitch Deck** (pitch_deck.md) - A 10-12 slide sustainable tourism pitch:
   - Slide 1: Title - Company, Tourism Innovation, Team
   - Slide 2: Tourism Challenge
   - Slide 3: Our Innovation
   - Slide 4: Environmental Sustainability
   - Slide 5: Social Sustainability (local impact)
   - Slide 6: Market Opportunity
   - Slide 7: Business Model
   - Slide 8: Traction
   - Slide 9: UN SDGs Alignment
   - Slide 10: Team
   - Slide 11: Financials
   - Slide 12: The Ask

3. **Executive Summary** (executive_summary.txt) - A 1-2 page tourism summary:
   - Tourism innovation
   - Sustainability impact
   - Local community benefit
   - Market opportunity
   - UN SDGs alignment
   - Funding needs

4. **Financial Plan** (financial_plan.md) - Sustainable tourism financials:
   - Revenue Model
   - Cost Structure
   - 5-Year Financial Projections
   - Sustainability Metrics
   - Funding Requirements
   - Use of Funds

Make all documents professional, emphasizing tourism innovation, environmental and social sustainability, and UN SDGs alignment."""
    }
}

def update_competition_prompts():
    db = SessionLocal()
    try:
        updated_count = 0
        for comp_name, prompts in COMPETITION_PROMPTS.items():
            competition = db.query(Competition).filter(Competition.name == comp_name).first()
            if competition:
                if prompts.get("advice_prompt"):
                    competition.advice_prompt = prompts["advice_prompt"]
                if prompts.get("file_generation_prompt"):
                    competition.file_generation_prompt = prompts["file_generation_prompt"]
                updated_count += 1
                print(f"Updated: {comp_name}")
            else:
                print(f"Not found: {comp_name}")
        
        db.commit()
        print(f"\nSuccessfully updated {updated_count} competitions with custom prompts!")
        
    except Exception as e:
        db.rollback()
        print(f"Error updating competitions: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    update_competition_prompts()

