"""
Local Storage Service - Replaces Supabase for self-contained DocForge

This service provides all database functionality using local file system,
eliminating the need for external database dependencies.
"""

import json
import uuid
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)

# Use global settings paths so all generated docs live in a single place
try:
    # Import within package context
    from ..core.simple_config import settings
except Exception:  # pragma: no cover
    # Fallback for any alternative import paths
    from backend.app.core.simple_config import settings  # type: ignore

class LocalStorageService:
    """Local file-system based storage service to replace Supabase"""
    
    def __init__(self, base_dir: Optional[Path] = None):
        """Initialize local storage service
        
        Args:
            base_dir: Base directory for storage (default: ./storage)
        """
        self.base_dir = base_dir or Path("storage")
        self.projects_dir = self.base_dir / "projects"
        self.documents_dir = self.base_dir / "documents"
        # Centralize generated markdown output to the global configured path
        self.generated_docs_dir = settings.generated_docs_path
        
        # Create directories
        self.base_dir.mkdir(exist_ok=True)
        self.projects_dir.mkdir(exist_ok=True)
        self.documents_dir.mkdir(exist_ok=True)
        self.generated_docs_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Local storage initialized at: {self.base_dir}")
    
    def _generate_id(self) -> str:
        """Generate a unique ID"""
        return str(uuid.uuid4())
    
    def _get_timestamp(self) -> str:
        """Get current ISO timestamp"""
        return datetime.now().isoformat()
    
    def _slugify(self, text: str) -> str:
        """Convert text to URL-friendly slug"""
        import re
        slug = re.sub(r'[^\w\s-]', '', text.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug.strip('-')
    
    # Project Management Methods
    
    async def create_project(self, 
                           name: str, 
                           initial_idea: str,
                           expanded_concept: Optional[str] = None,
                           additional_context: Optional[str] = None) -> Dict[str, Any]:
        """Create a new project
        
        Args:
            name: Project name
            initial_idea: Initial project idea
            expanded_concept: Expanded project concept (optional)
            additional_context: Additional context (optional)
            
        Returns:
            Dict with project data or error
        """
        try:
            project_id = self._generate_id()
            slug = self._slugify(name)
            timestamp = self._get_timestamp()
            
            project_data = {
                "id": project_id,
                "name": name,
                "slug": slug,
                "initial_idea": initial_idea,
                "expanded_concept": expanded_concept or "",
                "additional_context": additional_context or "",
                "status": "created",
                "created_at": timestamp,
                "updated_at": timestamp,
                "documents_generated": [],
                "generation_config": {
                    "document_types": [],
                    "custom_requirements": [],
                    "ai_model": "gpt-4"
                }
            }
            
            # Save project data
            project_file = self.projects_dir / f"{project_id}.json"
            with open(project_file, 'w', encoding='utf-8') as f:
                json.dump(project_data, f, indent=2)
            
            # Create project directory for documents
            project_doc_dir = self.generated_docs_dir / slug
            project_doc_dir.mkdir(exist_ok=True)
            
            logger.info(f"Created project: {name} ({project_id})")
            
            return {
                "success": True,
                "project": project_data
            }
            
        except Exception as e:
            logger.error(f"Error creating project: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_project(self, project_id: str) -> Dict[str, Any]:
        """Get project by ID
        
        Args:
            project_id: Project ID
            
        Returns:
            Dict with project data or error
        """
        try:
            project_file = self.projects_dir / f"{project_id}.json"
            
            if not project_file.exists():
                return {
                    "success": False,
                    "error": "Project not found"
                }
            
            with open(project_file, 'r', encoding='utf-8') as f:
                project_data = json.load(f)
            
            return {
                "success": True,
                "project": project_data
            }
            
        except Exception as e:
            logger.error(f"Error getting project {project_id}: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def list_projects(self) -> Dict[str, Any]:
        """List all projects
        
        Returns:
            Dict with list of projects or error
        """
        try:
            projects = []
            
            for project_file in self.projects_dir.glob("*.json"):
                try:
                    with open(project_file, 'r', encoding='utf-8') as f:
                        project_data = json.load(f)
                    projects.append(project_data)
                except Exception as e:
                    logger.warning(f"Error reading project file {project_file}: {str(e)}")
                    continue
            
            # Sort by created_at descending
            projects.sort(key=lambda x: x.get("created_at", ""), reverse=True)
            
            return {
                "success": True,
                "projects": projects,
                "count": len(projects)
            }
            
        except Exception as e:
            logger.error(f"Error listing projects: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "projects": [],
                "count": 0
            }
    
    async def update_project(self, project_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update project data
        
        Args:
            project_id: Project ID
            updates: Dictionary of fields to update
            
        Returns:
            Dict with updated project data or error
        """
        try:
            # Get current project data
            result = await self.get_project(project_id)
            if not result["success"]:
                return result
            
            project_data = result["project"]
            
            # Apply updates
            for key, value in updates.items():
                if key != "id":  # Don't allow ID changes
                    project_data[key] = value
            
            # Update timestamp
            project_data["updated_at"] = self._get_timestamp()
            
            # Save updated data
            project_file = self.projects_dir / f"{project_id}.json"
            with open(project_file, 'w', encoding='utf-8') as f:
                json.dump(project_data, f, indent=2)
            
            logger.info(f"Updated project: {project_id}")
            
            return {
                "success": True,
                "project": project_data
            }
            
        except Exception as e:
            logger.error(f"Error updating project {project_id}: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def delete_project(self, project_id: str) -> Dict[str, Any]:
        """Delete a project and all its documents
        
        Args:
            project_id: Project ID
            
        Returns:
            Dict with success status or error
        """
        try:
            # Get project data first
            result = await self.get_project(project_id)
            if not result["success"]:
                return result
            
            project_data = result["project"]
            project_slug = project_data.get("slug", "")
            
            # Delete project file
            project_file = self.projects_dir / f"{project_id}.json"
            if project_file.exists():
                project_file.unlink()
            
            # Delete project documents directory
            if project_slug:
                project_doc_dir = self.generated_docs_dir / project_slug
                if project_doc_dir.exists():
                    shutil.rmtree(project_doc_dir)
            
            # Delete individual document files
            for doc_file in self.documents_dir.glob(f"*{project_id}*.json"):
                doc_file.unlink()
            
            logger.info(f"Deleted project: {project_id}")
            
            return {
                "success": True,
                "message": "Project deleted successfully"
            }
            
        except Exception as e:
            logger.error(f"Error deleting project {project_id}: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    # Document Management Methods
    
    async def create_document(self, 
                            project_id: str,
                            document_type: str,
                            title: str,
                            content: str = "",
                            additional_context: Optional[str] = None) -> Dict[str, Any]:
        """Create a new document
        
        Args:
            project_id: Parent project ID
            document_type: Type of document
            title: Document title
            content: Document content
            additional_context: Additional context (optional)
            
        Returns:
            Dict with document data or error
        """
        try:
            # Verify project exists
            project_result = await self.get_project(project_id)
            if not project_result["success"]:
                return {
                    "success": False,
                    "error": "Project not found"
                }
            
            project_data = project_result["project"]
            document_id = self._generate_id()
            timestamp = self._get_timestamp()
            
            document_data = {
                "id": document_id,
                "project_id": project_id,
                "document_type": document_type,
                "title": title,
                "content": content,
                "additional_context": additional_context or "",
                "status": "generated",
                "version": 1,
                "slug": f"{document_type}-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
                "created_at": timestamp,
                "updated_at": timestamp,
                "tokens_used": 0,
                "agent_used": "unknown"
            }
            
            # Save document data
            document_file = self.documents_dir / f"{document_id}.json"
            with open(document_file, 'w', encoding='utf-8') as f:
                json.dump(document_data, f, indent=2)
            
            # Also save as markdown file in centralized project directory
            project_slug = project_data.get("slug", "unknown")
            project_doc_dir = self.generated_docs_dir / project_slug
            project_doc_dir.mkdir(exist_ok=True)
            
            # Generate filename with sequence number
            existing_docs = list(project_doc_dir.glob("*.md"))
            sequence = len(existing_docs) + 1
            
            markdown_file = project_doc_dir / f"{sequence:02d}_{document_type}.md"
            with open(markdown_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"Created document: {title} ({document_id})")
            
            return {
                "success": True,
                "document": document_data,
                "markdown_file": markdown_file.name,
                "markdown_path": str(markdown_file)
            }
            
        except Exception as e:
            logger.error(f"Error creating document: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_document(self, document_id: str) -> Dict[str, Any]:
        """Get document by ID
        
        Args:
            document_id: Document ID
            
        Returns:
            Dict with document data or error
        """
        try:
            document_file = self.documents_dir / f"{document_id}.json"
            
            if not document_file.exists():
                return {
                    "success": False,
                    "error": "Document not found"
                }
            
            with open(document_file, 'r', encoding='utf-8') as f:
                document_data = json.load(f)
            
            return {
                "success": True,
                "document": document_data
            }
            
        except Exception as e:
            logger.error(f"Error getting document {document_id}: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def list_project_documents(self, project_id: str) -> Dict[str, Any]:
        """List all documents for a project
        
        Args:
            project_id: Project ID
            
        Returns:
            Dict with list of documents or error
        """
        try:
            documents = []
            
            for doc_file in self.documents_dir.glob("*.json"):
                try:
                    with open(doc_file, 'r', encoding='utf-8') as f:
                        doc_data = json.load(f)
                    
                    if doc_data.get("project_id") == project_id:
                        documents.append(doc_data)
                        
                except Exception as e:
                    logger.warning(f"Error reading document file {doc_file}: {str(e)}")
                    continue
            
            # Sort by created_at
            documents.sort(key=lambda x: x.get("created_at", ""))
            
            return {
                "success": True,
                "documents": documents,
                "count": len(documents)
            }
            
        except Exception as e:
            logger.error(f"Error listing documents for project {project_id}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "documents": [],
                "count": 0
            }
    
    async def update_document(self, 
                            document_id: str, 
                            updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update document data
        
        Args:
            document_id: Document ID
            updates: Dictionary of fields to update
            
        Returns:
            Dict with updated document data or error
        """
        try:
            # Get current document data
            result = await self.get_document(document_id)
            if not result["success"]:
                return result
            
            document_data = result["document"]
            
            # Apply updates
            for key, value in updates.items():
                if key not in ["id", "project_id"]:  # Don't allow ID changes
                    document_data[key] = value
            
            # Update timestamp and version
            document_data["updated_at"] = self._get_timestamp()
            if "content" in updates:
                document_data["version"] = document_data.get("version", 1) + 1
            
            # Save updated data
            document_file = self.documents_dir / f"{document_id}.json"
            with open(document_file, 'w', encoding='utf-8') as f:
                json.dump(document_data, f, indent=2)
            
            logger.info(f"Updated document: {document_id}")
            
            return {
                "success": True,
                "document": document_data
            }
            
        except Exception as e:
            logger.error(f"Error updating document {document_id}: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def delete_document(self, document_id: str) -> Dict[str, Any]:
        """Delete a document
        
        Args:
            document_id: Document ID
            
        Returns:
            Dict with success status or error
        """
        try:
            # Get document data first
            result = await self.get_document(document_id)
            if not result["success"]:
                return result
            
            # Delete document file
            document_file = self.documents_dir / f"{document_id}.json"
            if document_file.exists():
                document_file.unlink()
            
            logger.info(f"Deleted document: {document_id}")
            
            return {
                "success": True,
                "message": "Document deleted successfully"
            }
            
        except Exception as e:
            logger.error(f"Error deleting document {document_id}: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    # Utility Methods
    
    def get_storage_info(self) -> Dict[str, Any]:
        """Get storage information and statistics
        
        Returns:
            Dict with storage statistics
        """
        try:
            projects_count = len(list(self.projects_dir.glob("*.json")))
            documents_count = len(list(self.documents_dir.glob("*.json")))
            
            # Calculate storage size
            total_size = 0
            for file_path in self.base_dir.rglob("*"):
                if file_path.is_file():
                    total_size += file_path.stat().st_size
            
            return {
                "base_directory": str(self.base_dir),
                "projects_count": projects_count,
                "documents_count": documents_count,
                "total_size_bytes": total_size,
                "total_size_mb": round(total_size / (1024 * 1024), 2)
            }
            
        except Exception as e:
            logger.error(f"Error getting storage info: {str(e)}")
            return {
                "error": str(e)
            }
    
    def cleanup_storage(self) -> Dict[str, Any]:
        """Clean up orphaned files and optimize storage
        
        Returns:
            Dict with cleanup results
        """
        try:
            orphaned_documents = 0
            
            # Find documents without parent projects
            for doc_file in self.documents_dir.glob("*.json"):
                try:
                    with open(doc_file, 'r', encoding='utf-8') as f:
                        doc_data = json.load(f)
                    
                    project_id = doc_data.get("project_id")
                    if project_id:
                        project_file = self.projects_dir / f"{project_id}.json"
                        if not project_file.exists():
                            # Orphaned document - delete it
                            doc_file.unlink()
                            orphaned_documents += 1
                            logger.info(f"Deleted orphaned document: {doc_file.name}")
                            
                except Exception as e:
                    logger.warning(f"Error processing document {doc_file}: {str(e)}")
                    continue
            
            return {
                "success": True,
                "orphaned_documents_removed": orphaned_documents,
                "message": f"Cleanup completed. Removed {orphaned_documents} orphaned documents."
            }
            
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
