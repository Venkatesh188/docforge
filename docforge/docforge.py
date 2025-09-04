#!/usr/bin/env python3
"""
DocForge - Open Source AI-Powered Documentation Generator

A self-contained tool for generating professional software documentation
from simple project ideas using AI agents.

Usage:
    python docforge.py generate "Your project idea here"
    python docforge.py generate "E-commerce platform" --docs srs,hld
    python docforge.py list-docs
    python docforge.py status my-project
"""

import argparse
import asyncio
import os
import sys
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any
import re

# Add the backend `app` package to Python path (works for source and installed wheel)
possible_backend_paths = [
    Path(__file__).parent / "backend",               # when backend is vendored under docforge/
    Path(__file__).parent.parent / "backend",        # when backend is installed at site-packages/backend
]
for p in possible_backend_paths:
    if p.exists() and str(p) not in sys.path:
        sys.path.insert(0, str(p))
        break

from app.core.simple_config import settings
from app.services.local_storage_service import LocalStorageService
from app.models import DocumentType

# Set environment variable to force simple config usage
os.environ["DOCFORGE_CLI_MODE"] = "true"

from app.services.document_agents import DocumentAgentService

class DocForgeCore:
    """Core DocForge functionality without authentication or external dependencies"""
    
    def __init__(self, base_dir: Optional[Path] = None):
        self.base_dir = base_dir or Path.cwd()
        self.generated_docs_dir = settings.generated_docs_path
        self.generated_docs_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize local storage service
        self.storage = LocalStorageService(base_dir=settings.storage_path)
        
        # Initialize document agent service without database
        self.doc_agent_service = DocumentAgentService(db=None)
    
    def _slugify(self, text: str) -> str:
        """Convert text to a URL-friendly slug"""
        # Convert to lowercase and replace spaces/special chars with hyphens
        slug = re.sub(r'[^\w\s-]', '', text.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug.strip('-')
    
    def _create_project_metadata(self, name: str, initial_idea: str, 
                                additional_context: str = None) -> Dict[str, Any]:
        """Create project metadata structure"""
        return {
            "id": str(uuid.uuid4()),
            "name": name,
            "slug": self._slugify(name),
            "initial_idea": initial_idea,
            "additional_context": additional_context,
            "created_at": datetime.now().isoformat(),
            "documents_generated": [],
            "generation_config": {
                "ai_model": getattr(settings, 'openai_model', 'gpt-4'),
                "custom_requirements": [],
                "additional_context": additional_context or ""
            }
        }
    
    async def generate_documents(self, 
                               idea: str,
                               document_types: Optional[List[str]] = None,
                               context: Optional[str] = None,
                               project_name: Optional[str] = None) -> Dict[str, Any]:
        """Generate documents from an idea"""
        
        print("🚀 Starting DocForge document generation...")
        
        # Validate configuration
        config_validation = settings.validate_config()
        if not config_validation["valid"]:
            return {
                "success": False,
                "error": f"Configuration error: {', '.join(config_validation['errors'])}"
            }
        
        # Extract project name from idea if not provided
        if not project_name:
            project_name = idea.split('.')[0].strip()
            if len(project_name) > 50:
                project_name = project_name[:50]
        
        # Create project in storage
        project_result = await self.storage.create_project(
            name=project_name,
            initial_idea=idea,
            additional_context=context
        )
        
        if not project_result["success"]:
            return {
                "success": False,
                "error": f"Failed to create project: {project_result['error']}"
            }
        
        project_metadata = project_result["project"]
        project_slug = project_metadata["slug"]
        project_id = project_metadata["id"]
        
        # Create project directory for generated docs (centralized path)
        project_dir = self.generated_docs_dir / project_slug
        project_dir.mkdir(exist_ok=True)
        
        print(f"📁 Created project: {project_name} ({project_id})")
        print(f"📁 Documents will be saved to: {project_dir}")
        
        # Determine document types to generate
        available_doc_types = list(DocumentType)
        if document_types:
            # Convert string names to DocumentType enums
            selected_types = []
            for doc_type_str in document_types:
                try:
                    doc_type = DocumentType(doc_type_str)
                    selected_types.append(doc_type)
                except ValueError:
                    print(f"⚠️  Unknown document type: {doc_type_str}")
                    print(f"Available types: {[dt.value for dt in available_doc_types]}")
                    continue
            doc_types_to_generate = selected_types
        else:
            # Generate core document types by default
            doc_types_to_generate = [
                DocumentType.PROJECT_CHARTER,
                DocumentType.SRS,
                DocumentType.ARCHITECTURE,
                DocumentType.TEST_SPECIFICATION
            ]
        
        if not doc_types_to_generate:
            return {
                "success": False,
                "error": "No valid document types specified"
            }
        
        print(f"📝 Generating {len(doc_types_to_generate)} document types...")
        
        # Create mock project object for document generation
        mock_project = {
            "id": project_metadata["id"],
            "name": project_metadata["name"],
            "initial_idea": idea,
            "expanded_concept": f"Expanded concept for {project_name}: {idea}",
            "status": "in_progress"
        }
        
        # Generate documents sequentially
        generated_documents = []
        for i, doc_type in enumerate(doc_types_to_generate, 1):
            try:
                print(f"🔄 [{i}/{len(doc_types_to_generate)}] Generating {doc_type.value}...")
                
                # Generate document using AI agents
                result = await self.doc_agent_service.generate_document(
                    document_type=doc_type,
                    project=mock_project,
                    additional_context=context,
                    custom_requirements=None
                )
                
                if result.get("success", True):
                    # Save document through storage service
                    doc_title = f"{project_metadata['name']} - {doc_type.value.replace('_', ' ').title()}"
                    doc_result = await self.storage.create_document(
                        project_id=project_id,
                        document_type=doc_type.value,
                        title=doc_title,
                        content=result["content"],
                        additional_context=context
                    )
                    
                    if doc_result["success"]:
                        # File already saved by storage service into the centralized folder
                        # Resolve filename for README and console output
                        filename = doc_result.get("markdown_file") or f"{i:02d}_{doc_type.value}.md"
                        print(f"✅ Generated: {filename}")
                        
                        # Update document metadata with generation info
                        await self.storage.update_document(
                            doc_result["document"]["id"],
                            {
                                "tokens_used": result.get("tokens_used", 0),
                                "agent_used": result.get("agent_used", "unknown"),
                                "status": "completed"
                            }
                        )
                        
                        # Track generated document
                        document_info = {
                            "id": doc_result["document"]["id"],
                            "type": doc_type.value,
                            "status": "completed",
                            "file": filename,
                            "generated_at": datetime.now().isoformat(),
                            "tokens_used": result.get("tokens_used", 0),
                            "agent_used": result.get("agent_used", "unknown")
                        }
                        
                        generated_documents.append(document_info)
                
                else:
                    print(f"❌ Failed to generate {doc_type.value}: {result.get('error', 'Unknown error')}")
                    
            except Exception as e:
                print(f"❌ Error generating {doc_type.value}: {str(e)}")
                continue
        
        # Update project with generated documents info
        await self.storage.update_project(project_id, {
            "status": "completed",
            "documents_generated": [doc["id"] for doc in generated_documents]
        })
        
        # Create README for the project
        additional_context_block = ""
        if context:
            additional_context_block = "## Additional Context\n" + str(context) + "\n"

        readme_content = f"""# {project_metadata['name']}

**Generated by DocForge** - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Project Overview
{idea}

{additional_context_block}

## Generated Documents
{chr(10).join([f"- [{doc['file']}](./{doc['file']}) - {doc['type'].replace('_', ' ').title()}" for doc in generated_documents])}

## Project Details
- **Project ID**: {project_metadata['id']}
- **Documents Generated**: {len(generated_documents)}
- **AI Model Used**: {project_metadata['generation_config']['ai_model']}

---
*Generated with ❤️ by DocForge - Open Source AI Documentation Generator*
"""
        
        readme_path = project_dir / "README.md"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print(f"\n🎉 Documentation generation complete!")
        print(f"📁 Location: {project_dir}")
        print(f"📄 Generated {len(generated_documents)} documents")
        print(f"🔗 View README: {readme_path}")
        
        return {
            "success": True,
            "project_dir": str(project_dir),
            "documents_generated": len(generated_documents),
            "project_metadata": project_metadata
        }
    
    def list_document_types(self) -> List[str]:
        """List available document types"""
        return [doc_type.value for doc_type in DocumentType]
    
    async def get_project_status(self, project_slug: str) -> Dict[str, Any]:
        """Get status of a generated project"""
        # Find project by slug
        projects_result = await self.storage.list_projects()
        if not projects_result["success"]:
            return {"success": False, "error": "Failed to list projects"}
        
        # Find project with matching slug
        project = None
        for p in projects_result["projects"]:
            if p.get("slug") == project_slug:
                project = p
                break
        
        if not project:
            return {"success": False, "error": f"Project '{project_slug}' not found"}
        
        # Get project documents
        docs_result = await self.storage.list_project_documents(project["id"])
        documents_count = docs_result["count"] if docs_result["success"] else 0
        
        project_dir = self.generated_docs_dir / project_slug
        
        return {
            "success": True,
            "project": project,
            "documents_count": documents_count,
            "location": str(project_dir)
        }
    
    async def list_projects(self) -> List[Dict[str, Any]]:
        """List all generated projects"""
        projects_result = await self.storage.list_projects()
        if not projects_result["success"]:
            return []
        
        projects_summary = []
        for project in projects_result["projects"]:
            # Get document count for each project
            docs_result = await self.storage.list_project_documents(project["id"])
            documents_count = docs_result["count"] if docs_result["success"] else 0
            
            projects_summary.append({
                "slug": project.get("slug", "unknown"),
                "name": project.get("name", "Unknown"),
                "created_at": project.get("created_at", "Unknown"),
                "documents_count": documents_count,
                "status": project.get("status", "unknown")
            })
        
        return sorted(projects_summary, key=lambda x: x["created_at"], reverse=True)


async def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="DocForge - Open Source AI-Powered Documentation Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  docforge.py generate "E-commerce platform for handmade crafts"
  docforge.py generate "Mobile app" --docs srs,hld --context "React Native, Node.js backend"
  docforge.py list-docs
  docforge.py status my-ecommerce-platform
  docforge.py list-projects
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Generate command
    generate_parser = subparsers.add_parser('generate', help='Generate documentation from an idea')
    generate_parser.add_argument('idea', help='Your project idea or description')
    generate_parser.add_argument('--docs', help='Comma-separated list of document types to generate')
    generate_parser.add_argument('--context', help='Additional context about your project')
    generate_parser.add_argument('--name', help='Custom project name (default: extracted from idea)')
    
    # List document types command
    subparsers.add_parser('list-docs', help='List available document types')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Get status of a project')
    status_parser.add_argument('project_slug', help='Project slug/directory name')
    
    # List projects command
    subparsers.add_parser('list-projects', help='List all generated projects')
    
    # Init command
    init_parser = subparsers.add_parser('init', help='Initialize DocForge in current directory')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize DocForge core only when needed
    docforge = None
    
    if args.command == 'generate':
        docforge = DocForgeCore()
        # Parse document types
        doc_types = None
        if args.docs:
            doc_types = [dt.strip() for dt in args.docs.split(',')]
        
        result = await docforge.generate_documents(
            idea=args.idea,
            document_types=doc_types,
            context=args.context,
            project_name=args.name
        )
        
        if not result["success"]:
            print(f"❌ Generation failed: {result['error']}")
            sys.exit(1)
    
    elif args.command == 'list-docs':
        from app.core.simple_config import get_available_document_types
        doc_types = get_available_document_types()
        print("📋 Available Document Types:")
        print("=" * 60)
        for i, doc_type in enumerate(doc_types, 1):
            print(f"{i:2d}. {doc_type['name']}")
            print(f"    Type: {doc_type['type']}")
            print(f"    Description: {doc_type['description']}")
            print()
        
        print("=" * 60)
        print(f"Total: {len(doc_types)} document types available")
        print("\nUsage examples:")
        print("  python docforge.py generate \"My project\" --docs project_charter,srs")
        print("  python docforge.py generate \"My project\" --docs architecture,test_specification")
        print("  python docforge.py generate \"My project\"  # Uses default document types")
    
    elif args.command == 'status':
        docforge = DocForgeCore()
        result = await docforge.get_project_status(args.project_slug)
        if result["success"]:
            project = result["project"]
            print(f"📊 Project Status: {project['name']}")
            print(f"  📁 Location: {result['location']}")
            print(f"  📄 Documents: {result['documents_count']}")
            print(f"  📅 Created: {project['created_at']}")
            print(f"  💡 Idea: {project['initial_idea']}")
            print(f"  🔄 Status: {project.get('status', 'unknown')}")
            
            if result['documents_count'] > 0:
                print("  📝 Generated Documents: Check the project directory for files")
        else:
            print(f"❌ {result['error']}")
            sys.exit(1)
    
    elif args.command == 'list-projects':
        docforge = DocForgeCore()
        projects = await docforge.list_projects()
        if projects:
            print("📁 Generated Projects:")
            for project in projects:
                print(f"  📂 {project['slug']}")
                print(f"     Name: {project['name']}")
                print(f"     Documents: {project['documents_count']}")
                print(f"     Status: {project['status']}")
                print(f"     Created: {project['created_at']}")
                print()
        else:
            print("📂 No projects found. Generate your first project with:")
            print("   python docforge.py generate \"Your project idea here\"")
    
    elif args.command == 'init':
        print("🚀 Initializing DocForge...")
        
        # Create only the generated-docs directory (storage will be created when needed)
        generated_docs_dir = Path("generated-docs")
        generated_docs_dir.mkdir(parents=True, exist_ok=True)
        
        # Create .env template if it doesn't exist
        env_path = Path('.env')
        if not env_path.exists():
            from app.core.simple_config import create_env_template
            create_env_template(str(env_path))
            print("✅ Created .env file template")
        else:
            print("✅ .env file already exists")
        
        # Show available document types
        from app.core.simple_config import get_available_document_types
        doc_types = get_available_document_types()
        
        print(f"\n📋 Available Document Types ({len(doc_types)}):")
        for i, doc_type in enumerate(doc_types, 1):
            print(f"  {i:2d}. {doc_type['name']}")
            print(f"      Type: {doc_type['type']}")
            print(f"      Description: {doc_type['description']}")
            print()
        
        # Check configuration
        from app.core.simple_config import check_configuration
        config_valid = check_configuration()
        
        if config_valid:
            print("✅ DocForge initialized and configured successfully!")
            print("\n🚀 You're ready to generate documents!")
            print("   python docforge.py generate \"Your project idea\"")
            print("   python docforge.py generate \"Your project idea\" --docs project_charter,srs")
        else:
            print("\n📝 Next steps:")
            print("1. Edit .env file and add your OpenAI API key")
            print("2. Get your API key from: https://platform.openai.com/api-keys")
            print("3. Run: python docforge.py generate \"Your project idea\"")


def cli():
    """Synchronous console entry point wrapper for asyncio main."""
    asyncio.run(main())


if __name__ == "__main__":
    cli()
