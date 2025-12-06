import os
import json
from typing import List, Dict
from openai import OpenAI
from sqlalchemy.orm import Session
from app.models.project import Project
from app.models.competition import Competition
from app.models.generated_file import GeneratedFile
from app.models.generation_log import GenerationLog
from app.repositories.file_repository import FileRepository
from app.repositories.log_repository import LogRepository


class FileGenerationService:
    def __init__(self, db: Session):
        self.db = db
        self.file_repository = FileRepository(db)
        self.log_repository = LogRepository(db)
        # Initialize OpenAI client - API key should be in environment variable
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            self.client = OpenAI(api_key=api_key)
        else:
            self.client = None
            print("Warning: OPENAI_API_KEY not set. File generation will not work.")

    def _log(self, project_id: int, message: str, log_type: str = "info"):
        """Helper method to log messages"""
        log = GenerationLog(project_id=project_id, message=message, log_type=log_type)
        self.log_repository.save(log)
        try:
            self.db.commit()  # Commit immediately so logs are visible
        except Exception:
            self.db.rollback()
            # Don't fail the whole process if logging fails

    def generate_files_for_project(self, project_id: int) -> List[GeneratedFile]:
        """Generate files for a project based on its competition requirements"""
        # Clear previous logs and files (for regeneration) - MUST happen first
        self._log(project_id, "🗑️ Clearing previous files and logs...", "info")
        self.log_repository.clear_project_logs(project_id)
        self.file_repository.delete_by_project_id(project_id)
        # Ensure deletion is committed before proceeding
        self.db.commit()
        self._log(project_id, "🚀 Starting file generation process...", "info")
        
        # Get project and competition
        self._log(project_id, "📋 Loading project information...", "info")
        project = self.db.query(Project).filter(Project.id == project_id).first()
        if not project:
            self._log(project_id, f"❌ Error: Project {project_id} not found", "error")
            raise ValueError(f"Project {project_id} not found")

        if not self.client:
            self._log(project_id, "❌ Error: OpenAI API key not configured", "error")
            raise ValueError("OpenAI API key not configured")

        # Handle competition (optional)
        competition = None
        if project.competition_id:
            self._log(project_id, f"🏆 Loading competition details...", "info")
            competition = self.db.query(Competition).filter(Competition.id == project.competition_id).first()
            if competition:
                self._log(project_id, f"✅ Found competition: {competition.name}", "success")
            else:
                self._log(project_id, f"⚠️ Competition {project.competition_id} not found, using default prompt", "warning")
        else:
            self._log(project_id, "ℹ️ No competition selected, using default prompt", "info")

        # Use competition-specific prompt if available, otherwise use default
        if competition and competition.file_generation_prompt:
            system_prompt = competition.file_generation_prompt
            self._log(project_id, "✅ Using competition-specific prompt", "success")
        else:
            if competition:
                self._log(project_id, "⚠️ Competition has no custom prompt, using default prompt", "warning")
            system_prompt = """You are an expert business consultant helping entrepreneurs prepare competition materials.

Generate comprehensive, professional documents for an entrepreneurship competition. These are the ESSENTIAL files needed for most startup competitions. Based on the project idea provided, create the following files:

1. **Pitch Deck** (pitch_deck.md) - A complete pitch deck outline (10-12 slides) including:
   - Problem Statement (What problem are you solving?)
   - Solution (Your product/service)
   - Market Opportunity (Market size, TAM/SAM/SOM)
   - Business Model (How you make money)
   - Traction/Milestones (What you've achieved)
   - Team (Key team members and their expertise)
   - Financials (Revenue projections, key metrics)
   - Ask/Next Steps (What you need, funding ask)

2. **Business Plan** (business_plan.md) - A comprehensive business plan including:
   - Executive Summary
   - Company Description & Vision
   - Market Analysis (Industry, competitors, target market)
   - Organization & Management (Team structure, advisors)
   - Product/Service Line (Detailed description)
   - Marketing & Sales Strategy
   - Financial Projections (3-5 years)
   - Funding Request & Use of Funds

3. **Executive Summary** (executive_summary.txt) - A concise 1-2 page summary that can be used for:
   - Quick overview for judges
   - Email introductions
   - Application forms
   - Investor outreach

4. **Financial Plan** (financial_plan.md) - Detailed financial projections including:
   - Revenue Model (How you generate revenue)
   - Cost Structure (Fixed and variable costs)
   - 3-Year Financial Projections (Income statement, cash flow)
   - Break-even Analysis
   - Funding Requirements & Use of Funds
   - Key Financial Assumptions

These 4 files cover the core requirements for most entrepreneurship competitions. Make all documents professional, well-structured, data-driven, and tailored to the specific project idea provided. Use realistic numbers and clear explanations."""

        # Build the prompt for OpenAI
        self._log(project_id, "📝 Preparing prompt for AI generation...", "info")
        user_prompt = f"""
Project Name: {project.name}
Project Description: {project.description or 'N/A'}
Idea Description: {project.idea_description}

Please generate the required files for this competition. Return a JSON object with the following structure:
{{
    "files": [
        {{
            "filename": "filename.ext",
            "content": "file content here",
            "file_type": "txt"
        }}
    ]
}}
"""

        try:
            # Call OpenAI API
            self._log(project_id, "🤖 Sending request to OpenAI API...", "info")
            self._log(project_id, "⏳ Waiting for AI response (this may take 30-60 seconds)...", "info")
            self.db.commit()  # Commit logs before API call
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Using gpt-4o-mini as it's more accessible
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
            )
            self._log(project_id, "✅ Received response from OpenAI", "success")
            self.db.commit()  # Commit success log

            # Parse response
            self._log(project_id, "📄 Parsing AI response...", "info")
            content = response.choices[0].message.content
            
            # Try to extract JSON from the response
            # Sometimes the response might have markdown code blocks
            files_data = None
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
                files_data = json.loads(content)
            elif "```" in content:
                # Try to find JSON in code blocks
                parts = content.split("```")
                for i, part in enumerate(parts):
                    if i % 2 == 1:  # Code blocks are on odd indices
                        try:
                            files_data = json.loads(part.strip())
                            break
                        except:
                            continue
                if not files_data:
                    # If no code block worked, try the whole content
                    files_data = json.loads(content)
            else:
                files_data = json.loads(content)
            
            self._log(project_id, f"✅ Successfully parsed response. Found {len(files_data.get('files', []))} file(s)", "success")
            
            # Create GeneratedFile records
            generated_files = []
            files_list = files_data.get("files", [])
            for idx, file_data in enumerate(files_list, 1):
                filename = file_data.get("filename", "unknown.txt")
                self._log(project_id, f"💾 Creating file {idx}/{len(files_list)}: {filename}", "info")
                file = GeneratedFile(
                    project_id=project_id,
                    filename=filename,
                    content=file_data.get("content", ""),
                    file_type=file_data.get("file_type", "txt"),
                    status="completed"
                )
                saved_file = self.file_repository.save(file)
                generated_files.append(saved_file)
                self._log(project_id, f"✅ File created: {filename}", "success")

            self._log(project_id, f"🎉 File generation completed! Generated {len(generated_files)} file(s)", "success")
            self.db.commit()  # Final commit
            return generated_files

        except json.JSONDecodeError as e:
            error_msg = f"❌ Error: Failed to parse JSON response from AI. {str(e)}"
            self._log(project_id, error_msg, "error")
            self._log(project_id, "💡 Tip: The AI response may not be in the expected format", "warning")
            # Create a failed file record
            error_file = GeneratedFile(
                project_id=project_id,
                filename="error.txt",
                content=f"Error generating files: {str(e)}\n\nAI Response (first 500 chars):\n{content[:500] if 'content' in locals() else 'N/A'}",
                file_type="txt",
                status="failed"
            )
            self.file_repository.save(error_file)
            self.db.commit()
            raise
        except Exception as e:
            import traceback
            error_msg = f"❌ Error: {str(e)}"
            self._log(project_id, error_msg, "error")
            self._log(project_id, f"📋 Traceback: {traceback.format_exc()[:500]}", "error")
            # Create a failed file record
            error_file = GeneratedFile(
                project_id=project_id,
                filename="error.txt",
                content=f"Error generating files: {str(e)}\n\n{traceback.format_exc()}",
                file_type="txt",
                status="failed"
            )
            self.file_repository.save(error_file)
            self.db.commit()
            raise

    def generate_single_file_for_project(self, project_id: int, filename: str) -> GeneratedFile:
        """Generate a single specific file for a project"""
        # Clear logs for this regeneration
        self.log_repository.clear_project_logs(project_id)
        self._log(project_id, f"🔄 Regenerating file: {filename}...", "info")
        
        # Get project and competition
        project = self.db.query(Project).filter(Project.id == project_id).first()
        if not project:
            self._log(project_id, f"❌ Error: Project {project_id} not found", "error")
            raise ValueError(f"Project {project_id} not found")

        if not self.client:
            self._log(project_id, "❌ Error: OpenAI API key not configured", "error")
            raise ValueError("OpenAI API key not configured")

        # Handle competition (optional)
        competition = None
        if project.competition_id:
            self._log(project_id, f"🏆 Loading competition details...", "info")
            competition = self.db.query(Competition).filter(Competition.id == project.competition_id).first()
            if competition:
                self._log(project_id, f"✅ Found competition: {competition.name}", "success")
            else:
                self._log(project_id, f"⚠️ Competition {project.competition_id} not found, using default prompt", "warning")
        else:
            self._log(project_id, "ℹ️ No competition selected, using default prompt", "info")

        # Use competition-specific prompt if available, otherwise use default
        if competition and competition.file_generation_prompt:
            system_prompt = competition.file_generation_prompt
            self._log(project_id, "✅ Using competition-specific prompt", "success")
        else:
            if competition:
                self._log(project_id, "⚠️ Competition has no custom prompt, using default prompt", "warning")
            system_prompt = """You are an expert business consultant helping entrepreneurs prepare competition materials.

Generate comprehensive, professional documents for an entrepreneurship competition. These are the ESSENTIAL files needed for most startup competitions. Based on the project idea provided, create the following files:

1. **Pitch Deck** (pitch_deck.md) - A complete pitch deck outline (10-12 slides) including:
   - Problem Statement (What problem are you solving?)
   - Solution (Your product/service)
   - Market Opportunity (Market size, TAM/SAM/SOM)
   - Business Model (How you make money)
   - Traction/Milestones (What you've achieved)
   - Team (Key team members and their expertise)
   - Financials (Revenue projections, key metrics)
   - Ask/Next Steps (What you need, funding ask)

2. **Business Plan** (business_plan.md) - A comprehensive business plan including:
   - Executive Summary
   - Company Description & Vision
   - Market Analysis (Industry, competitors, target market)
   - Organization & Management (Team structure, advisors)
   - Product/Service Line (Detailed description)
   - Marketing & Sales Strategy
   - Financial Projections (3-5 years)
   - Funding Request & Use of Funds

3. **Executive Summary** (executive_summary.txt) - A concise 1-2 page summary that can be used for:
   - Quick overview for judges
   - Email introductions
   - Application forms
   - Investor outreach

4. **Financial Plan** (financial_plan.md) - Detailed financial projections including:
   - Revenue Model (How you generate revenue)
   - Cost Structure (Fixed and variable costs)
   - 3-Year Financial Projections (Income statement, cash flow)
   - Break-even Analysis
   - Funding Requirements & Use of Funds
   - Key Financial Assumptions

These 4 files cover the core requirements for most entrepreneurship competitions. Make all documents professional, well-structured, data-driven, and tailored to the specific project idea provided. Use realistic numbers and clear explanations."""

        self._log(project_id, "📝 Preparing prompt for AI generation...", "info")
        user_prompt = f"""
Project Name: {project.name}
Project Description: {project.description or 'N/A'}
Idea Description: {project.idea_description}

Please generate ONLY the file: {filename}

Return a JSON object with the following structure:
{{
    "files": [
        {{
            "filename": "{filename}",
            "content": "file content here",
            "file_type": "{filename.split('.')[-1] if '.' in filename else 'txt'}"
        }}
    ]
}}
"""

        try:
            self._log(project_id, "🤖 Sending request to OpenAI API...", "info")
            self._log(project_id, "⏳ Waiting for AI response...", "info")
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
            )
            self._log(project_id, "✅ Received response from OpenAI", "success")

            content = response.choices[0].message.content
            
            # Parse JSON response
            files_data = None
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
                files_data = json.loads(content)
            elif "```" in content:
                parts = content.split("```")
                for i, part in enumerate(parts):
                    if i % 2 == 1:
                        try:
                            files_data = json.loads(part.strip())
                            break
                        except:
                            continue
                if not files_data:
                    files_data = json.loads(content)
            else:
                files_data = json.loads(content)
            
            self._log(project_id, f"✅ Successfully parsed response", "success")
            
            # Find the specific file in the response
            files_list = files_data.get("files", [])
            target_file = None
            for file_data in files_list:
                if file_data.get("filename") == filename:
                    target_file = file_data
                    break
            
            if not target_file:
                raise ValueError(f"File {filename} not found in AI response")
            
            # Delete old file if exists
            existing_files = self.file_repository.find_by_project_id(project_id)
            for existing_file in existing_files:
                if existing_file.filename == filename:
                    self.file_repository.delete(existing_file)
                    break
            
            # Create new file
            self._log(project_id, f"💾 Creating file: {filename}", "info")
            file = GeneratedFile(
                project_id=project_id,
                filename=filename,
                content=target_file.get("content", ""),
                file_type=target_file.get("file_type", filename.split('.')[-1] if '.' in filename else 'txt'),
                status="completed"
            )
            saved_file = self.file_repository.save(file)
            self._log(project_id, f"✅ File regenerated: {filename}", "success")
            return saved_file

        except json.JSONDecodeError as e:
            error_msg = f"❌ Error: Failed to parse JSON response from AI. {str(e)}"
            self._log(project_id, error_msg, "error")
            # Create a failed file record
            error_file = GeneratedFile(
                project_id=project_id,
                filename=filename,
                content=f"Error generating file: {str(e)}",
                file_type=filename.split('.')[-1] if '.' in filename else 'txt',
                status="failed"
            )
            self.file_repository.save(error_file)
            raise
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            self._log(project_id, error_msg, "error")
            # Create a failed file record
            error_file = GeneratedFile(
                project_id=project_id,
                filename=filename,
                content=f"Error generating file: {str(e)}",
                file_type=filename.split('.')[-1] if '.' in filename else 'txt',
                status="failed"
            )
            self.file_repository.save(error_file)
            raise

