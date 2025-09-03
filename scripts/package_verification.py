#!/usr/bin/env python3
"""
DocForge Package Verification Script

This script verifies that the DocForge package is ready for distribution
and publication. It checks all components, dependencies, and configurations.
"""

import sys
import os
import subprocess
import json
from pathlib import Path
from typing import List, Dict, Tuple, Optional

def run_command(cmd: List[str]) -> Tuple[bool, str, str]:
    """Run a command and return success status, stdout, and stderr"""
    try:
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            cwd=Path(__file__).parent.parent
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_file_exists(filepath: Path, required: bool = True) -> bool:
    """Check if a file exists and report status"""
    exists = filepath.exists()
    status = "✅" if exists else ("❌" if required else "⚠️")
    req_text = "Required" if required else "Optional"
    print(f"{status} {req_text}: {filepath}")
    return exists

def check_python_syntax(filepath: Path) -> bool:
    """Check if a Python file has valid syntax"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
        compile(code, str(filepath), 'exec')
        return True
    except SyntaxError as e:
        print(f"  ❌ Syntax error: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def verify_package_structure() -> bool:
    """Verify that all required files and directories exist"""
    print("🏗️  **Verifying Package Structure**")
    print("=" * 50)
    
    root = Path(__file__).parent.parent
    required_files = [
        "README.md",
        "LICENSE",
        "CONTRIBUTING.md",
        "CHANGELOG.md",
        "requirements.txt",
        "setup.py",
        "pyproject.toml",
        "MANIFEST.in",
        ".gitignore",
        ".env.template",
        "docforge.py"
    ]
    
    optional_files = [
        "docs/INSTALLATION.md",
        "examples/README.md"
    ]
    
    required_dirs = [
        "backend",
        "backend/app",
        "backend/app/core",
        "backend/app/services",
        "prompts",
        ".github",
        ".github/ISSUE_TEMPLATE",
        ".github/workflows"
    ]
    
    all_good = True
    
    # Check required files
    for file_path in required_files:
        if not check_file_exists(root / file_path, required=True):
            all_good = False
    
    # Check optional files
    for file_path in optional_files:
        check_file_exists(root / file_path, required=False)
    
    # Check required directories
    for dir_path in required_dirs:
        if not check_file_exists(root / dir_path, required=True):
            all_good = False
    
    return all_good

def verify_python_files() -> bool:
    """Verify Python files have valid syntax"""
    print("\n🐍 **Verifying Python Files**")
    print("=" * 50)
    
    root = Path(__file__).parent.parent
    python_files = [
        "docforge.py",
        "setup.py",
        "backend/app/__init__.py",
        "backend/app/core/simple_config.py",
        "backend/app/services/local_storage_service.py",
        "backend/app/models.py",
        "tests/test_basic.py"
    ]
    
    all_good = True
    
    for file_path in python_files:
        filepath = root / file_path
        if filepath.exists():
            print(f"Checking {file_path}...")
            if not check_python_syntax(filepath):
                all_good = False
        else:
            print(f"❌ Missing: {file_path}")
            all_good = False
    
    return all_good

def verify_dependencies() -> bool:
    """Verify that all dependencies can be installed"""
    print("\n📦 **Verifying Dependencies**")
    print("=" * 50)
    
    # Check if requirements.txt exists and is readable
    root = Path(__file__).parent.parent
    req_file = root / "requirements.txt"
    
    if not req_file.exists():
        print("❌ requirements.txt not found")
        return False
    
    try:
        with open(req_file, 'r') as f:
            requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        print(f"✅ Found {len(requirements)} dependencies:")
        for req in requirements:
            print(f"   - {req}")
        
        # Try to check if major dependencies are available
        major_deps = ['crewai', 'openai', 'pydantic', 'python-dotenv']
        for dep in major_deps:
            success, stdout, stderr = run_command([sys.executable, "-c", f"import {dep.replace('-', '_')}"])
            if success:
                print(f"✅ {dep} can be imported")
            else:
                print(f"⚠️  {dep} not currently installed (expected for fresh environment)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error reading requirements.txt: {e}")
        return False

def verify_configuration() -> bool:
    """Verify configuration files and templates"""
    print("\n⚙️  **Verifying Configuration**")
    print("=" * 50)
    
    root = Path(__file__).parent.parent
    
    # Check .env template
    env_template = root / ".env.template"
    if env_template.exists():
        try:
            with open(env_template, 'r') as f:
                content = f.read()
            if "OPENAI_API_KEY" in content:
                print("✅ .env.template contains required OPENAI_API_KEY")
            else:
                print("❌ .env.template missing OPENAI_API_KEY")
                return False
        except Exception as e:
            print(f"❌ Error reading .env.template: {e}")
            return False
    else:
        print("❌ .env.template not found")
        return False
    
    # Check if simple_config can be loaded
    try:
        sys.path.insert(0, str(root / "backend"))
        from app.core.simple_config import SimpleSettings
        settings = SimpleSettings()
        print(f"✅ Configuration system works - version: {settings.app_version}")
        return True
    except Exception as e:
        print(f"❌ Configuration system error: {e}")
        return False

def verify_documentation() -> bool:
    """Verify documentation completeness"""
    print("\n📚 **Verifying Documentation**")
    print("=" * 50)
    
    root = Path(__file__).parent.parent
    
    # Check README.md
    readme = root / "README.md"
    if readme.exists():
        try:
            with open(readme, 'r', encoding='utf-8') as f:
                content = f.read()
            
            required_sections = [
                "# 🚀 DocForge",
                "## ✨ Features",
                "## 🚀 Quick Start",
                "## 📖 CLI Commands",
                "## 🤝 Contributing"
            ]
            
            missing_sections = []
            for section in required_sections:
                if section not in content:
                    missing_sections.append(section)
            
            if missing_sections:
                print("❌ README.md missing sections:")
                for section in missing_sections:
                    print(f"   - {section}")
                return False
            else:
                print("✅ README.md has all required sections")
            
            # Check for placeholder URLs
            if "your-username" in content:
                print("⚠️  README.md contains placeholder URLs - update before publishing")
            
        except Exception as e:
            print(f"❌ Error reading README.md: {e}")
            return False
    else:
        print("❌ README.md not found")
        return False
    
    # Check other docs
    docs_to_check = [
        ("CONTRIBUTING.md", ["## 🚀 Quick Start", "## 🎯 Ways to Contribute"]),
        ("CHANGELOG.md", ["## [2.0.0]", "### ✨ **Added**"])
    ]
    
    for doc_file, required_sections in docs_to_check:
        doc_path = root / doc_file
        if doc_path.exists():
            try:
                with open(doc_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                missing = [section for section in required_sections if section not in content]
                if missing:
                    print(f"❌ {doc_file} missing sections: {', '.join(missing)}")
                    return False
                else:
                    print(f"✅ {doc_file} has required sections")
            except Exception as e:
                print(f"❌ Error reading {doc_file}: {e}")
                return False
        else:
            print(f"❌ {doc_file} not found")
            return False
    
    return True

def verify_github_integration() -> bool:
    """Verify GitHub integration files"""
    print("\n🐙 **Verifying GitHub Integration**")
    print("=" * 50)
    
    root = Path(__file__).parent.parent
    
    # Check issue templates
    issue_templates = [
        ".github/ISSUE_TEMPLATE/bug_report.yml",
        ".github/ISSUE_TEMPLATE/feature_request.yml",
        ".github/ISSUE_TEMPLATE/template_request.yml"
    ]
    
    all_good = True
    for template in issue_templates:
        if not check_file_exists(root / template):
            all_good = False
    
    # Check workflows
    workflow_file = root / ".github/workflows/ci.yml"
    if workflow_file.exists():
        try:
            with open(workflow_file, 'r') as f:
                content = f.read()
            if "CI/CD Pipeline" in content and "test:" in content:
                print("✅ CI/CD workflow configured")
            else:
                print("❌ CI/CD workflow incomplete")
                all_good = False
        except Exception as e:
            print(f"❌ Error reading CI workflow: {e}")
            all_good = False
    else:
        print("❌ CI/CD workflow not found")
        all_good = False
    
    return all_good

def verify_examples() -> bool:
    """Verify examples and sample outputs"""
    print("\n📝 **Verifying Examples**")
    print("=" * 50)
    
    root = Path(__file__).parent.parent
    
    examples_dir = root / "examples"
    if not examples_dir.exists():
        print("❌ Examples directory not found")
        return False
    
    # Check examples README
    examples_readme = examples_dir / "README.md"
    if not examples_readme.exists():
        print("❌ Examples README.md not found")
        return False
    else:
        print("✅ Examples README.md found")
    
    # Check for at least one example project
    example_projects = [d for d in examples_dir.iterdir() if d.is_dir() and d.name != "__pycache__"]
    if example_projects:
        print(f"✅ Found {len(example_projects)} example projects:")
        for proj in example_projects:
            print(f"   - {proj.name}")
    else:
        print("⚠️  No example projects found")
    
    return True

def verify_build_system() -> bool:
    """Verify build system configuration"""
    print("\n🔧 **Verifying Build System**")
    print("=" * 50)
    
    root = Path(__file__).parent.parent
    
    # Check setup.py
    setup_py = root / "setup.py"
    if setup_py.exists():
        try:
            success, stdout, stderr = run_command([sys.executable, "setup.py", "check"])
            if success:
                print("✅ setup.py check passed")
            else:
                print(f"❌ setup.py check failed: {stderr}")
                return False
        except Exception as e:
            print(f"❌ Error checking setup.py: {e}")
            return False
    else:
        print("❌ setup.py not found")
        return False
    
    # Check pyproject.toml
    pyproject = root / "pyproject.toml"
    if pyproject.exists():
        try:
            # Try to import tomllib for Python 3.11+, fallback to basic validation
            tomllib = None
            if sys.version_info >= (3, 11):
                try:
                    import tomllib
                except ImportError:
                    tomllib = None
            
            if tomllib:
                with open(pyproject, 'rb') as f:
                    config = tomllib.load(f)
                if "project" in config and "name" in config["project"]:
                    print("✅ pyproject.toml structure valid")
                else:
                    print("❌ pyproject.toml missing required fields")
                    return False
            else:
                # Basic validation for older Python versions
                with open(pyproject, 'r', encoding='utf-8') as f:
                    content = f.read()
                if '[project]' in content and 'name = ' in content:
                    print("✅ pyproject.toml exists and has basic structure")
                else:
                    print("❌ pyproject.toml missing required sections")
                    return False
        except Exception as e:
            print(f"❌ Error reading pyproject.toml: {e}")
            return False
    else:
        print("❌ pyproject.toml not found")
        return False
    
    return True

def generate_package_report() -> Dict:
    """Generate comprehensive package verification report"""
    print("\n📊 **Package Verification Report**")
    print("=" * 50)
    
    checks = [
        ("Package Structure", verify_package_structure),
        ("Python Files", verify_python_files),
        ("Dependencies", verify_dependencies),
        ("Configuration", verify_configuration),
        ("Documentation", verify_documentation),
        ("GitHub Integration", verify_github_integration),
        ("Examples", verify_examples),
        ("Build System", verify_build_system)
    ]
    
    results = {}
    passed = 0
    total = len(checks)
    
    for check_name, check_func in checks:
        print(f"\n🔍 Running: {check_name}")
        try:
            result = check_func()
            results[check_name] = result
            if result:
                passed += 1
        except Exception as e:
            print(f"❌ {check_name} failed with error: {e}")
            results[check_name] = False
    
    # Summary
    print("\n" + "=" * 50)
    print(f"📈 **SUMMARY**: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 **PACKAGE VERIFICATION SUCCESSFUL!**")
        print("   DocForge is ready for publication! 🚀")
    else:
        print("⚠️  **PACKAGE VERIFICATION INCOMPLETE**")
        print("   Please address the issues above before publishing.")
        
        failed_checks = [name for name, result in results.items() if not result]
        print(f"\n❌ Failed checks: {', '.join(failed_checks)}")
    
    return {
        "passed": passed,
        "total": total,
        "success": passed == total,
        "results": results
    }

def main():
    """Main verification routine"""
    print("🔍 DocForge Package Verification")
    print("=" * 60)
    print("Verifying that DocForge is ready for publication...")
    print()
    
    # Generate report
    report = generate_package_report()
    
    # Exit with appropriate code
    sys.exit(0 if report["success"] else 1)

if __name__ == "__main__":
    main()
