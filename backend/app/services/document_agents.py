from crewai import Agent, Task, Crew
from typing import Optional, Dict, Any, List
import os
import json

# Check if we're in CLI mode
if os.getenv("DOCFORGE_CLI_MODE") == "true":
    from ..core.simple_config import settings
else:
    try:
        # Try to import from original config (for web version)
        from ..core.simple_config import settings
    except ImportError:
        # Fallback to simple config
        from ..core.simple_config import settings

from ..models import DocumentType

# Import OpenAI service (optional)
try:
    from .openai_service import OpenAIService
except ImportError:
    # If OpenAI service not available, we'll handle this in the class
    OpenAIService = None

class DocumentAgentService:
    def __init__(self, db=None, user_api_key: Optional[str] = None):
        self.db = db  # Database instance (optional - for backwards compatibility)
        
        # Set up OpenAI API key for document generation
        api_key = user_api_key or settings.openai_api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OpenAI API key is required. Set OPENAI_API_KEY environment variable "
                "or pass user_api_key parameter."
            )
        
        # Initialize OpenAI service with provided or environment API key (if available)
        if OpenAIService:
            self.openai_service = OpenAIService(api_key=api_key)
        else:
            self.openai_service = None
        
        # Ensure CrewAI can access the API key
        os.environ["OPENAI_API_KEY"] = api_key
        
        # Agent configurations mapping document types to their settings
        self.agent_configs = {
            DocumentType.PROJECT_CHARTER: {
                "role": "Senior Program Manager",
                "goal": "Create board-grade project charters that secure funding and kickoff execution",
                "prompt_file": "charter.md",
                "max_tokens": int(os.getenv("PROJECT_CHARTER_MAX_TOKENS", "2000"))
            },
            DocumentType.SRS: {
                "role": "Lead Solution Architect", 
                "goal": "Generate comprehensive Software Requirements Specifications with epics and user stories",
                "prompt_file": "requirements.md",
                "max_tokens": int(os.getenv("SRS_MAX_TOKENS", "3000"))
            },
            DocumentType.ARCHITECTURE: {
                "role": "Principal Systems Architect",
                "goal": "Create security-first, enterprise-grade High-Level Design documents",
                "prompt_file": "architecture.md",
                "max_tokens": int(os.getenv("ARCHITECTURE_MAX_TOKENS", "2500"))
            },
            DocumentType.LOW_LEVEL_DESIGN: {
                "role": "Senior Software Architect",
                "goal": "Create detailed Low-Level Design with API specifications",
                "prompt_file": "design.md",
                "max_tokens": int(os.getenv("LLD_MAX_TOKENS", "3500"))
            },
            DocumentType.TEST_SPECIFICATION: {
                "role": "QA Lead",
                "goal": "Generate comprehensive test specifications and acceptance criteria",
                "prompt_file": "testing.md",
                "max_tokens": int(os.getenv("TEST_SPEC_MAX_TOKENS", "2500"))
            },
            DocumentType.DEPLOYMENT_GUIDE: {
                "role": "DevOps Lead",
                "goal": "Create enterprise-grade deployment and release guides",
                "prompt_file": "deployment.md",
                "max_tokens": int(os.getenv("DEPLOYMENT_GUIDE_MAX_TOKENS", "2800"))
            },
            DocumentType.OPERATIONS_MANUAL: {
                "role": "Operations Manager",
                "goal": "Generate comprehensive operations and maintenance documentation",
                "prompt_file": "operations.md",
                "max_tokens": int(os.getenv("OPERATIONS_MANUAL_MAX_TOKENS", "3000"))
            },
            DocumentType.BUSINESS_CASE: {
                "role": "Business Analyst",
                "goal": "Create compelling business case documents with ROI analysis",
                "prompt_file": "business_case.md",
                "max_tokens": int(os.getenv("BUSINESS_CASE_MAX_TOKENS", "2000"))
            },
            DocumentType.MARKET_REQUIREMENTS: {
                "role": "Product Manager",
                "goal": "Generate market requirements documents with competitive analysis",
                "prompt_file": "market_requirements.md",
                "max_tokens": int(os.getenv("MARKET_REQUIREMENTS_MAX_TOKENS", "1500"))
            },
            DocumentType.VISION_BRIEF: {
                "role": "Product Strategist",
                "goal": "Create vision and opportunity briefs for stakeholder alignment",
                "prompt_file": "vision_brief.md",
                "max_tokens": int(os.getenv("VISION_BRIEF_MAX_TOKENS", "1800"))
            }
        }
    
    def _load_prompt(self, prompt_file: str) -> str:
        """Load prompt from the prompts directory"""
        # Try multiple candidate locations for the prompts directory
        current_dir = os.path.dirname(__file__)
        backend_dir = os.path.dirname(os.path.dirname(current_dir))  # backend/app/services -> backend
        repo_root_dir = os.path.dirname(backend_dir)  # -> repo root

        candidate_prompt_dirs = [
            os.path.join(repo_root_dir, "prompts"),     # <repo-root>/prompts
            os.path.join(backend_dir, "prompts"),       # <repo-root>/backend/prompts (fallback if used)
        ]

        for prompts_dir in candidate_prompt_dirs:
            prompt_path = os.path.join(prompts_dir, prompt_file)
            try:
                with open(prompt_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except FileNotFoundError:
                continue

        return self._get_fallback_prompt(prompt_file)
    
    def _get_fallback_prompt(self, prompt_file: str) -> str:
        """Fallback prompt if file not found"""
        return f"""
        You are a professional document generator. Create a high-quality {prompt_file.replace('.md', '')} document.
        
        Requirements:
        - Use clean markdown formatting
        - No emojis or icons
        - Professional tone
        - Complete sections with no placeholders
        - Include relevant technical details
        
        Generate a comprehensive document based on the project context provided.
        """
    
    def _create_agent(self, document_type: DocumentType) -> Agent:
        """Create a specialized agent for the given document type"""
        config = self.agent_configs.get(document_type)
        
        if not config:
            # Default configuration for unknown document types
            config = {
                "role": "Technical Writer",
                "goal": f"Generate professional {document_type.value} documentation",
                "prompt_file": None,
                "max_tokens": int(os.getenv("DEFAULT_DOCUMENT_MAX_TOKENS", "2000"))
            }
        
        # Choose LLM provider
        llm_provider = None
        if self.openai_service is not None:
            llm_provider = self.openai_service.get_llm()
        else:
            # Fallback: construct CrewAI-compatible OpenAI LLM from env
            from crewai import LLM
            model_name = settings.openai_model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
            llm_provider = LLM(model=model_name)

        return Agent(
            role=config["role"],
            goal=config["goal"],
            backstory=f"""You are an experienced {config["role"]} who specializes in creating 
            high-quality technical documentation. You understand industry best practices and 
            ensure all documents are professional, comprehensive, and actionable.""",
            verbose=True,
            allow_delegation=False,
            llm=llm_provider
        )
    
    def _build_context(self, project: Dict[str, Any]) -> Dict[str, Any]:
        """Build context from project and existing documents"""
        context = {
            "project_name": project.get("name", "Unknown Project"),
            "initial_idea": project.get("initial_idea", ""),
            "expanded_concept": project.get("expanded_concept", ""),
            "project_status": project.get("status", "created")
        }
        
        # Note: For now, we skip existing documents context since we're using Supabase
        # This could be enhanced later to fetch related documents from Supabase
        
        return context
    
    def _create_generation_task(
        self,
        agent: Agent,
        document_type: DocumentType,
        project: Dict[str, Any],
        additional_context: Optional[str] = None,
        custom_requirements: Optional[List[str]] = None
    ) -> Task:
        """Create a document generation task"""
        
        config = self.agent_configs.get(document_type, {})
        prompt = self._load_prompt(config.get("prompt_file", ""))
        
        context = self._build_context(project)
        
        # Build the task description
        task_description = f"""
        {prompt}
        
        PROJECT CONTEXT:
        {json.dumps(context, indent=2)}
        
        ADDITIONAL REQUIREMENTS:
        """
        
        if additional_context:
            task_description += f"\nAdditional Context: {additional_context}"
        
        if custom_requirements:
            task_description += f"\nCustom Requirements: {', '.join(custom_requirements)}"
        
        task_description += """
        
        CRITICAL OUTPUT REQUIREMENTS:
        1. Generate ONLY the document content in clean markdown format
        2. NO emojis, icons, or decorative elements
        3. NO placeholders, TODOs, or incomplete sections
        4. Professional technical writing tone
        5. Follow the exact template structure provided in the prompt
        6. Include all required sections completely populated
        """
        
        return Task(
            description=task_description,
            agent=agent,
            expected_output=f"A complete, professional {document_type.value} document in markdown format"
        )
    
    async def generate_document(
        self,
        document_type: DocumentType,
        project: Dict[str, Any],
        additional_context: Optional[str] = None,
        custom_requirements: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Generate a document using AI agents"""
        
        # Validate OpenAI API key is available (from user settings or env)
        if self.openai_service and not self.openai_service.is_configured():
            raise ValueError("OpenAI API key is not configured. Please add it in Settings.")
        elif not self.openai_service:
            # For CLI version, we rely on the environment variable check above
            pass
        
        # Validate document type is configured
        if document_type not in self.agent_configs:
            raise ValueError(f"Document type '{document_type.value}' not configured for AI generation.")
        
        try:
            agent = self._create_agent(document_type)
            task = self._create_generation_task(
                agent=agent,
                document_type=document_type,
                project=project,
                additional_context=additional_context,
                custom_requirements=custom_requirements
            )
            
            crew = Crew(
                agents=[agent],
                tasks=[task],
                verbose=True
            )
            
            result = crew.kickoff()
            cleaned_result = self._clean_output(str(result))
            
            # Validate document quality
            validation_results = self._validate_document_quality(cleaned_result, document_type)
            
            return {
                "content": cleaned_result,
                "agent_used": f"{document_type.value}_agent",
                "tokens_used": getattr(crew.usage_metrics, 'total_tokens', 0) if hasattr(crew, 'usage_metrics') and crew.usage_metrics else 0,
                "success": True,
                "validation": validation_results
            }
        except Exception as e:
            print(f"Error generating document {document_type.value}: {str(e)}")
            raise ValueError(f"Failed to generate document: {str(e)}")
    
    def _clean_output(self, content: str) -> str:
        """Clean the generated content to ensure it meets formatting requirements"""
        import re
        
        # Remove common emoji patterns
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251"
                                   "]+", flags=re.UNICODE)
        
        content = emoji_pattern.sub('', content)
        
        # Remove excessive newlines
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        # Remove any remaining placeholder text
        placeholders = ['TODO', 'PLACEHOLDER', 'TBD', '...', 'INSERT_HERE', '[TO BE FILLED]', 
                       '[INSERT]', '[ADD]', '[UPDATE]', '{{', '}}', 'XXXX', 'YYY']
        for placeholder in placeholders:
            content = content.replace(placeholder, '')
        
        # Clean up markdown formatting issues
        content = self._validate_and_fix_markdown(content)
        
        return content.strip()
    
    def _validate_and_fix_markdown(self, content: str) -> str:
        """Validate and fix markdown structure"""
        import re
        
        lines = content.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Fix heading hierarchy - ensure proper spacing
            if line.strip().startswith('#'):
                # Ensure space after # symbols
                line = re.sub(r'^(#+)([^\s])', r'\1 \2', line.strip())
                # Add to cleaned lines with proper spacing
                if cleaned_lines and cleaned_lines[-1].strip():
                    cleaned_lines.append('')  # Add blank line before heading
                cleaned_lines.append(line)
            # Fix list formatting
            elif line.strip().startswith(('-', '*', '+')):
                # Ensure proper list formatting
                line = re.sub(r'^(\s*)[-*+]\s*', r'\1- ', line)
                cleaned_lines.append(line)
            # Fix numbered lists
            elif re.match(r'^\s*\d+\.', line.strip()):
                cleaned_lines.append(line)
            # Regular content
            else:
                cleaned_lines.append(line)
        
        content = '\n'.join(cleaned_lines)
        
        # Remove multiple consecutive blank lines
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        # Ensure document starts with a heading
        if not content.strip().startswith('#'):
            content = f"# Document\n\n{content}"
        
        return content
    
    def _validate_document_quality(self, content: str, document_type: DocumentType) -> Dict[str, Any]:
        """Validate document quality and completeness"""
        import re
        
        validation_results = {
            "is_valid": True,
            "issues": [],
            "warnings": [],
            "metrics": {}
        }
        
        # Check for minimum content length
        if len(content) < 500:
            validation_results["issues"].append("Document too short (< 500 characters)")
            validation_results["is_valid"] = False
        
        # Check for proper markdown structure
        headings = re.findall(r'^#+\s+.+$', content, re.MULTILINE)
        if len(headings) < 3:
            validation_results["warnings"].append("Document has fewer than 3 headings")
        
        # Check for placeholder text that shouldn't be there
        problematic_phrases = [
            'lorem ipsum', 'sample text', 'example content', 
            'insert here', 'add content', 'to be determined'
        ]
        
        for phrase in problematic_phrases:
            if phrase.lower() in content.lower():
                validation_results["issues"].append(f"Contains placeholder phrase: {phrase}")
                validation_results["is_valid"] = False
        
        # Check for proper sections based on document type
        required_sections = self._get_required_sections(document_type)
        missing_sections = []
        
        for section in required_sections:
            if not re.search(rf"#{1,6}\s+.*{re.escape(section)}", content, re.IGNORECASE):
                missing_sections.append(section)
        
        if missing_sections:
            validation_results["warnings"].extend([f"Missing section: {section}" for section in missing_sections])
        
        # Calculate metrics
        validation_results["metrics"] = {
            "character_count": len(content),
            "word_count": len(content.split()),
            "heading_count": len(headings),
            "section_count": len(re.findall(r'^##\s+', content, re.MULTILINE))
        }
        
        return validation_results
    
    def _get_required_sections(self, document_type: DocumentType) -> List[str]:
        """Get required sections for each document type"""
        required_sections_map = {
            DocumentType.PROJECT_CHARTER: ["Executive Summary", "Business Justification", "Scope", "Timeline"],
            DocumentType.SRS: ["Introduction", "Overall Description", "System Features", "Non-functional Requirements"],
            DocumentType.ARCHITECTURE: ["System Overview", "Architecture Design", "Components", "Security"],
            DocumentType.LOW_LEVEL_DESIGN: ["API Specifications", "Database Design", "Component Details"],
            DocumentType.TEST_SPECIFICATION: ["Test Strategy", "Test Cases", "Acceptance Criteria"],
            DocumentType.DEPLOYMENT_GUIDE: ["Prerequisites", "Installation", "Configuration", "Verification"],
            DocumentType.OPERATIONS_MANUAL: ["Operations Overview", "Monitoring", "Maintenance", "Troubleshooting"],
            DocumentType.BUSINESS_CASE: ["Executive Summary", "Problem Statement", "Solution", "ROI Analysis"],
            DocumentType.MARKET_REQUIREMENTS: ["Market Analysis", "User Requirements", "Competitive Analysis"],
            DocumentType.VISION_BRIEF: ["Vision Statement", "Objectives", "Success Criteria"]
        }
        
        return required_sections_map.get(document_type, [])