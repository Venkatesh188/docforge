#!/usr/bin/env python3
"""
DocForge - Open Source AI-Powered Documentation Generator

A self-contained tool for generating professional software documentation
from simple project ideas using AI agents.

Usage:
    docforge-ai generate "Your project idea here" --docs srs
    docforge-ai generate "E-commerce platform" --docs srs,architecture
    docforge-ai list-docs
    docforge-ai status my-project
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

# Add the backend app to Python path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

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
    
    def _get_document_type_aliases(self) -> Dict[str, str]:
        """Get mapping of common document type aliases to actual DocumentType values"""
        return {
            # Common aliases
            "PRD": "srs",  # Product Requirements Document -> Software Requirements Specification
            "PR": "srs",   # Product Requirements -> Software Requirements Specification
            "SRS": "srs",  # Software Requirements Specification
            "ARCH": "architecture",
            "ARC": "architecture",  # Architecture
            "ARCHITECTURE": "architecture",
            "HLD": "architecture",  # High Level Design -> Architecture
            "LLD": "low_level_design",  # Low Level Design
            "DESIGN": "low_level_design",
            "TEST": "test_specification",  # Test Specification
            "TESTING": "test_specification",
            "DEPLOY": "deployment_guide",  # Deployment Guide
            "DEPLOYMENT": "deployment_guide",
            "OPS": "operations_manual",  # Operations Manual
            "OPERATIONS": "operations_manual",
            "BUSINESS": "business_case",  # Business Case
            "MARKET": "market_requirements",  # Market Requirements
            "VISION": "vision_brief",  # Vision Brief
            "CHARTER": "project_charter",  # Project Charter
            "PROJECT": "project_charter",
            "CONCEPT": "concept_expansion",  # Concept Expansion
        }
    
    def _resolve_document_type(self, doc_type_input: str) -> Optional[str]:
        """Resolve document type from user input (handles aliases and case variations)"""
        # Normalize input
        normalized_input = doc_type_input.upper().strip()
        
        # Check aliases first
        aliases = self._get_document_type_aliases()
        if normalized_input in aliases:
            return aliases[normalized_input]
        
        # Check if it's already a valid DocumentType value (case-insensitive)
        for doc_type in DocumentType:
            if doc_type.value.upper() == normalized_input:
                return doc_type.value
        
        return None
    
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
        
        # Create project directory for generated docs
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
                        # Save document to project directory as well
                        filename = f"{i:02d}_{doc_type.value}.md"
                        file_path = project_dir / filename
                        
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(result["content"])
                        
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
        readme_content = f"""# {project_metadata['name']}

**Generated by DocForge** - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Project Overview
{idea}

{f"## Additional Context\n{context}\n" if context else ""}

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
    
    async def find_project_prd(self, project_slug: str) -> Optional[Dict[str, Any]]:
        """Find PRD document for a project"""
        # Find project by slug
        projects_result = await self.storage.list_projects()
        if not projects_result["success"]:
            return None
        
        project = None
        for p in projects_result["projects"]:
            if p.get("slug") == project_slug:
                project = p
                break
        
        if not project:
            return None
        
        # Get project documents
        docs_result = await self.storage.list_project_documents(project["id"])
        if not docs_result["success"]:
            return None
        
        # Find PRD document (SRS is our PRD)
        for doc in docs_result["documents"]:
            if doc.get("document_type") == "srs":
                return {
                    "project": project,
                    "document": doc,
                    "content": doc.get("content", "")
                }
        
        return None
    
    async def revise_prd(self, project_slug: str, additional_specs: str) -> Dict[str, Any]:
        """Revise existing PRD with additional specifications"""
        print(f"Revising PRD for project: {project_slug}")
        
        # Find existing PRD
        prd_info = await self.find_project_prd(project_slug)
        if not prd_info:
            return {
                "success": False,
                "error": f"No PRD found for project '{project_slug}'. Generate a PRD first."
            }
        
        project = prd_info["project"]
        existing_prd = prd_info["document"]
        existing_content = prd_info["content"]
        
        print(f"Found existing PRD: {existing_prd['title']}")
        print(f"Adding specifications: {additional_specs}")
        
        # Create enhanced context for revision
        revision_context = f"""
EXISTING PRD CONTENT:
{existing_content}

ADDITIONAL SPECIFICATIONS TO INCORPORATE:
{additional_specs}

Please revise the PRD by incorporating the additional specifications while maintaining the existing structure and improving the overall document quality.
"""
        
        # Generate revised PRD
        try:
            result = await self.doc_agent_service.generate_document(
                document_type=DocumentType.SRS,
                project={
                    "id": project["id"],
                    "name": project["name"],
                    "initial_idea": project["initial_idea"],
                    "expanded_concept": f"Revised concept for {project['name']}: {project['initial_idea']}",
                    "status": "revision"
                },
                additional_context=revision_context,
                custom_requirements=["Incorporate additional specifications", "Maintain existing structure", "Improve user stories"]
            )
            
            if result.get("success", True):
                # Update existing document
                update_result = await self.storage.update_document(
                    existing_prd["id"],
                    {
                        "content": result["content"],
                        "additional_context": additional_specs,
                        "status": "revised",
                        "revision_notes": f"Revised with additional specifications: {additional_specs[:100]}..."
                    }
                )
                
                if update_result["success"]:
                    # Update the markdown file
                    project_dir = self.generated_docs_dir / project["slug"]
                    prd_files = list(project_dir.glob("*_srs.md"))
                    if prd_files:
                        prd_file = prd_files[0]  # Take the first SRS file
                        with open(prd_file, 'w', encoding='utf-8') as f:
                            f.write(result["content"])
                        print(f"Updated PRD file: {prd_file}")
                    
                    return {
                        "success": True,
                        "message": f"PRD revised successfully for project '{project_slug}'",
                        "file_path": str(prd_files[0]) if prd_files else None,
                        "tokens_used": result.get("tokens_used", 0)
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to update PRD: {update_result['error']}"
                    }
            else:
                return {
                    "success": False,
                    "error": f"Failed to generate revised PRD: {result.get('error', 'Unknown error')}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Error revising PRD: {str(e)}"
            }
    
    async def generate_from_prd(self, project_slug: str, document_types: List[str]) -> Dict[str, Any]:
        """Generate additional documents based on existing PRD"""
        print(f"Generating documents from PRD for project: {project_slug}")
        
        # Find existing PRD
        prd_info = await self.find_project_prd(project_slug)
        if not prd_info:
            return {
                "success": False,
                "error": f"No PRD found for project '{project_slug}'. Generate a PRD first with: docforge-ai generate \"your idea\" --docs srs"
            }
        
        project = prd_info["project"]
        prd_content = prd_info["content"]
        
        print(f"Using PRD as base: {prd_info['document']['title']}")
        
        # Convert string document types to DocumentType enums
        selected_types = []
        available_doc_types = list(DocumentType)
        
        for doc_type_str in document_types:
            resolved_type = self._resolve_document_type(doc_type_str)
            if resolved_type:
                try:
                    doc_type = DocumentType(resolved_type)
                    if doc_type != DocumentType.SRS:  # Don't regenerate the PRD itself
                        selected_types.append(doc_type)
                except ValueError:
                    print(f"Warning: Unknown document type: {doc_type_str}")
                    continue
        
        if not selected_types:
            return {
                "success": False,
                "error": "No valid document types specified (excluding PRD which already exists)"
            }
        
        print(f"Generating {len(selected_types)} document types based on PRD...")
        
        # Create enhanced context with PRD content
        prd_context = f"""
EXISTING PRODUCT REQUIREMENTS DOCUMENT (PRD):
{prd_content}

Use the above PRD as the primary source of requirements and specifications. Ensure consistency with the PRD while expanding on the specific aspects relevant to this document type.
"""
        
        # Create project directory
        project_dir = self.generated_docs_dir / project["slug"]
        project_dir.mkdir(exist_ok=True)
        
        # Generate documents sequentially
        generated_documents = []
        for i, doc_type in enumerate(selected_types, 1):
            try:
                print(f"[{i}/{len(selected_types)}] Generating {doc_type.value} based on PRD...")
                
                # Generate document using AI agents with PRD context
                result = await self.doc_agent_service.generate_document(
                    document_type=doc_type,
                    project={
                        "id": project["id"],
                        "name": project["name"],
                        "initial_idea": project["initial_idea"],
                        "expanded_concept": f"Based on validated PRD for {project['name']}",
                        "status": "prd_based_generation"
                    },
                    additional_context=prd_context,
                    custom_requirements=["Base on existing PRD", "Maintain consistency with PRD requirements"]
                )
                
                if result.get("success", True):
                    # Save document through storage service
                    doc_title = f"{project['name']} - {doc_type.value.replace('_', ' ').title()}"
                    doc_result = await self.storage.create_document(
                        project_id=project["id"],
                        document_type=doc_type.value,
                        title=doc_title,
                        content=result["content"],
                        additional_context="Generated from validated PRD"
                    )
                    
                    if doc_result["success"]:
                        # Find the next available sequence number
                        existing_docs = list(project_dir.glob("*.md"))
                        sequence = len(existing_docs) + 1
                        
                        # Save document to project directory
                        filename = f"{sequence:02d}_{doc_type.value}.md"
                        file_path = project_dir / filename
                        
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(result["content"])
                        
                        print(f"Generated: {filename}")
                        
                        # Update document metadata
                        await self.storage.update_document(
                            doc_result["document"]["id"],
                            {
                                "tokens_used": result.get("tokens_used", 0),
                                "agent_used": result.get("agent_used", "unknown"),
                                "status": "completed",
                                "generation_source": "prd_based"
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
                    print(f"Failed to generate {doc_type.value}: {result.get('error', 'Unknown error')}")
                    
            except Exception as e:
                print(f"Error generating {doc_type.value}: {str(e)}")
                continue
        
        # Update project with new documents
        current_docs = project.get("documents_generated", [])
        new_doc_ids = [doc["id"] for doc in generated_documents]
        
        await self.storage.update_project(project["id"], {
            "documents_generated": current_docs + new_doc_ids,
            "last_generation_type": "prd_based"
        })
        
        print(f"\nGenerated {len(generated_documents)} additional documents based on PRD!")
        print(f"Location: {project_dir}")
        
        return {
            "success": True,
            "project_dir": str(project_dir),
            "documents_generated": len(generated_documents),
            "generated_documents": generated_documents,
            "base_prd": prd_info["document"]["title"]
        }


async def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="DocForge - Open Source AI-Powered Documentation Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # PRD-First Workflow (Recommended):
  # 1. Generate a PRD first
  docforge-ai generate "AI-powered chatbot for customer service" --docs srs
  
  # 2. Review and optionally revise the PRD
  docforge-ai revise ai-powered-chatbot-for-customer-service -s "Add multi-language support and integration with Slack"
  
  # 3. Generate additional documents based on validated PRD
  docforge-ai continue ai-powered-chatbot-for-customer-service ARCH TEST DEPLOY
  
  # Alternative: Generate all documents at once (legacy)
  docforge-ai generate "E-commerce platform for handmade crafts"
  docforge-ai generate "Mobile app" --docs srs,architecture --context "React Native, Node.js backend"
  
  # Other commands
  docforge-ai list-docs
  docforge-ai status my-ecommerce-platform
  docforge-ai list-projects
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Generate command
    generate_parser = subparsers.add_parser('generate', help='Generate documentation from an idea')
    generate_parser.add_argument('doc_type_or_idea', help='Document type (PRD, SRS, ARCHITECTURE, etc.) or project idea for full generation')
    generate_parser.add_argument('idea', nargs='?', help='Your project idea or description (required when specifying document type)')
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
    
    # Revise PRD command
    revise_parser = subparsers.add_parser('revise', help='Revise existing PRD with additional specifications')
    revise_parser.add_argument('project_slug', help='Project slug/directory name')
    revise_parser.add_argument('-s', '--specs', required=True, help='Additional specifications to incorporate into the PRD')
    
    # Continue command (generate additional documents from PRD)
    continue_parser = subparsers.add_parser('continue', help='Generate additional documents based on existing PRD')
    continue_parser.add_argument('project_slug', help='Project slug/directory name')
    continue_parser.add_argument('document_types', nargs='+', help='Document types to generate (ARCH, TEST, DEPLOY, etc.)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize DocForge core
    docforge_core = DocForgeCore()
    
    if args.command == 'generate':
        # Handle legacy syntax: docforge-ai generate "idea" --docs type
        if args.idea:
            # This syntax is currently not working - use legacy syntax instead
            resolved_doc_type = docforge_core._resolve_document_type(args.doc_type_or_idea)
            if resolved_doc_type:
                # Single document generation
                print(f"Generating {resolved_doc_type} document...")
                result = await docforge_core.generate_documents(
                    idea=args.idea,
                    document_types=[resolved_doc_type],
                    context=args.context,
                    project_name=args.name
                )
            else:
                print(f"Unknown document type: {args.doc_type_or_idea}")
                print("Available document types:")
                aliases = docforge_core._get_document_type_aliases()
                for alias, doc_type in aliases.items():
                    print(f"  {alias} -> {doc_type}")
                print("\nOr use: docforge-ai list-docs")
                sys.exit(1)
        else:
            # Legacy syntax: docforge-ai generate "idea" [--docs ...]
            # Parse document types
            doc_types = None
            if args.docs:
                doc_types = [dt.strip() for dt in args.docs.split(',')]
            
            result = await docforge_core.generate_documents(
                idea=args.doc_type_or_idea,  # This is actually the idea in legacy mode
                document_types=doc_types,
                context=args.context,
                project_name=args.name
            )
        
        if not result["success"]:
            print(f"Generation failed: {result['error']}")
            sys.exit(1)
    
    elif args.command == 'list-docs':
        from app.core.simple_config import get_available_document_types
        doc_types = get_available_document_types()
        print("📋 Available Document Types:")
        print("=" * 60)
        
        # Get aliases for each document type
        aliases = docforge_core._get_document_type_aliases()
        
        for i, doc_type in enumerate(doc_types, 1):
            print(f"{i:2d}. {doc_type['name']}")
            print(f"    Type: {doc_type['type']}")
            
            # Find all aliases for this document type
            doc_aliases = [alias for alias, doc_type_name in aliases.items() if doc_type_name == doc_type['type']]
            if doc_aliases:
                aliases_str = ", ".join(sorted(doc_aliases))
                print(f"    Shortcuts: {aliases_str}")
            
            print(f"    Description: {doc_type['description']}")
            print()
        
        print("=" * 60)
        print(f"Total: {len(doc_types)} document types available")
        
        print("\nUsage examples:")
        print("  docforge-ai generate \"My project\" --docs srs,architecture")
        print("  docforge-ai generate \"My project\" --docs PRD,ARCH")
        print("  docforge-ai generate \"My project\"  # Uses default document types")
    
    elif args.command == 'status':
        result = await docforge_core.get_project_status(args.project_slug)
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
        projects = await docforge_core.list_projects()
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
            print("   docforge-ai generate \"Your project idea here\"")
    
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
            print("\n📖 Recommended PRD-First Workflow:")
            print("   # 1. Generate a PRD first (includes user stories)")
            print("   docforge-ai generate \"Your project idea\" --docs srs")
            print()
            print("   # 2. Review the PRD, then optionally revise")
            print("   docforge-ai revise your-project-idea -s \"Additional specifications\"")
            print()
            print("   # 3. Generate additional documents based on validated PRD")
            print("   docforge-ai continue your-project-idea ARCH TEST DEPLOY")
            print()
            print("   Alternative: Generate all documents at once:")
            print("   docforge-ai generate \"Your project idea\"")
            print("   docforge-ai generate \"Your project idea\" --docs project_charter,srs")
        else:
            print("\n📝 Next steps:")
            print("1. Edit .env file and add your OpenAI API key")
            print("2. Get your API key from: https://platform.openai.com/api-keys")
            print("3. Run: docforge-ai generate \"Your project idea\" --docs srs")
    
    elif args.command == 'revise':
        result = await docforge_core.revise_prd(args.project_slug, args.specs)
        if result["success"]:
            print(f"SUCCESS: {result['message']}")
            if result.get('file_path'):
                print(f"Updated file: {result['file_path']}")
            if result.get('tokens_used'):
                print(f"Tokens used: {result['tokens_used']}")
        else:
            print(f"ERROR: Revision failed: {result['error']}")
            sys.exit(1)
    
    elif args.command == 'continue':
        result = await docforge_core.generate_from_prd(args.project_slug, args.document_types)
        if result["success"]:
            print(f"SUCCESS: Generated {result['documents_generated']} documents based on PRD!")
            print(f"Location: {result['project_dir']}")
            print(f"Base PRD: {result['base_prd']}")
            
            if result.get('generated_documents'):
                print("\nGenerated Documents:")
                for doc in result['generated_documents']:
                    print(f"  - {doc['file']} ({doc['type']})")
        else:
            print(f"ERROR: Generation failed: {result['error']}")
            sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
