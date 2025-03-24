#!/usr/bin/env python3
"""
PolyDep: Universal Dependency Resolver for Multiple Programming Languages
"""
import os, sys, json, re, subprocess, argparse, logging
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional, Union, Callable

class LanguageHandler:
    """Base class for language-specific dependency handling"""
    def extract_imports(self, file_path: str) -> Set[str]: pass
    def install_package(self, package: str) -> bool: pass
    def is_installed(self, module: str) -> bool: pass
    def get_package_name(self, module: str) -> str: pass

class PythonHandler(LanguageHandler):
    """Python language dependency handler"""
    def __init__(self, venv_path: str, mapping_file: str):
        self.venv_path = venv_path
        self.mapping_file = mapping_file
        with open(mapping_file) as f:
            self.module_map = json.load(f)
    
    def extract_imports(self, file_path: str) -> Set[str]:
        import_pattern = re.compile(r'^\s*(import|from)\s+([A-Za-z0-9_.]+)')
        modules = set()
        with open(file_path, 'r') as f:
            for line in f:
                match = import_pattern.match(line)
                if match:
                    module = match.group(2).split('.')[0]
                    modules.add(module)
        return modules
    
    def is_installed(self, module: str) -> bool:
        cmd = f"source {self.venv_path}/bin/activate && python -c 'import {module}'"
        return subprocess.call(cmd, shell=True, executable='/bin/bash', stderr=subprocess.DEVNULL) == 0
    
    def get_package_name(self, module: str) -> str:
        return self.module_map.get(module, module)
    
    def install_package(self, package: str) -> bool:
        cmd = f"source {self.venv_path}/bin/activate && pip install {package}"
        return subprocess.call(cmd, shell=True, executable='/bin/bash') == 0

class JavaHandler(LanguageHandler):
    """Java language dependency handler"""
    def __init__(self, maven_path: str, mapping_file: str):
        self.maven_path = maven_path
        with open(mapping_file) as f:
            self.module_map = json.load(f)
    
    def extract_imports(self, file_path: str) -> Set[str]:
        import_pattern = re.compile(r'^\s*import\s+([A-Za-z0-9_.]+)')
        modules = set()
        with open(file_path, 'r') as f:
            for line in f:
                match = import_pattern.match(line)
                if match:
                    module = match.group(1).split('.')[0]
                    modules.add(module)
        return modules
    
    def is_installed(self, module: str) -> bool:
        # Check if the module exists in the Maven repository
        artifact = self.get_package_name(module)
        if ':' not in artifact:
            return True  # Standard library
        cmd = f"mvn dependency:get -Dartifact={artifact} -quiet"
        return subprocess.call(cmd, shell=True, stderr=subprocess.DEVNULL) == 0
    
    def get_package_name(self, module: str) -> str:
        return self.module_map.get(module, module)
    
    def install_package(self, package: str) -> bool:
        if ':' not in package:
            return True  # Standard library, no need to install
        # Add to pom.xml if it exists, otherwise create a new one
        pom_path = Path('pom.xml')
        if pom_path.exists():
            # Add dependency to existing pom.xml
            pass  # Implement XML modification
        else:
            # Create new pom.xml with this dependency
            pass  # Implement pom.xml creation
        return True

class GoHandler(LanguageHandler):
    """Go language dependency handler"""
    def extract_imports(self, file_path: str) -> Set[str]:
        import_pattern = re.compile(r'^\s*import\s+[("](.*)[")]')
        modules = set()
        with open(file_path, 'r') as f:
            for line in f:
                match = import_pattern.match(line)
                if match:
                    module = match.group(1).strip('"').split('/')[0]
                    if not module.startswith("fmt") and not module.startswith("os"):
                        modules.add(module)
        return modules
    
    def is_installed(self, module: str) -> bool:
        cmd = f"go list {module}"
        return subprocess.call(cmd, shell=True, stderr=subprocess.DEVNULL) == 0
    
    def get_package_name(self, module: str) -> str:
        return module  # Go uses the import path as the package name
    
    def install_package(self, package: str) -> bool:
        cmd = f"go get {package}"
        return subprocess.call(cmd, shell=True) == 0

# Language factory
def create_language_handler(file_ext: str, config: dict) -> LanguageHandler:
    """Factory method to create the appropriate language handler"""
    if file_ext in ['.py', '.pyw']:
        return PythonHandler(config['python']['venv_path'], config['python']['mapping_file'])
    elif file_ext in ['.java', '.kt']:
        return JavaHandler(config['java']['maven_path'], config['java']['mapping_file'])
    elif file_ext in ['.go']:
        return GoHandler()
    elif file_ext in ['.js', '.ts']:
        return NodeHandler(config['node']['npm_path'], config['node']['mapping_file'])
    elif file_ext in ['.cpp', '.cc', '.h', '.hpp']:
        return CppHandler(config['cpp']['cmake_path'], config['cpp']['mapping_file'])
    else:
        raise ValueError(f"Unsupported file extension: {file_ext}")

class PolyDep:
    """Main class for the cross-language dependency resolver"""
    def __init__(self):
        self.home = Path.home()
        self.config_dir = self.home / '.polydep'
        self.config_file = self.config_dir / 'config.json'
        self.log_file = self.config_dir / 'polydep.log'
        self.setup_logging()
        self.load_config()
    
    def setup_logging(self):
        """Configure logging"""
        self.config_dir.mkdir(exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('polydep')
    
    def load_config(self):
        """Load or create configuration"""
        if not self.config_file.exists():
            self.create_default_config()
        
        with open(self.config_file) as f:
            self.config = json.load(f)
    
    def create_default_config(self):
        """Create default configuration files"""
        # Create main config
        config = {
            'python': {
                'venv_path': str(self.home / 'venv'),
                'mapping_file': str(self.config_dir / 'python_mappings.json')
            },
            'java': {
                'maven_path': 'mvn',
                'mapping_file': str(self.config_dir / 'java_mappings.json')
            },
            'go': {
                'mapping_file': str(self.config_dir / 'go_mappings.json')
            },
            'node': {
                'npm_path': 'npm',
                'mapping_file': str(self.config_dir / 'node_mappings.json')
            },
            'cpp': {
                'cmake_path': 'cmake',
                'mapping_file': str(self.config_dir / 'cpp_mappings.json')
            }
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        # Create Python mappings
        python_mappings = {
            "transformers": "transformers", "torch": "torch", "numpy": "numpy",
            "scipy": "scipy", "pandas": "pandas", "sklearn": "scikit-learn",
            "matplotlib": "matplotlib", "tensorflow": "tensorflow"
        }
        with open(config['python']['mapping_file'], 'w') as f:
            json.dump(python_mappings, f, indent=2)
        
        # Create default mappings for other languages
        for lang in ['java', 'node', 'go', 'cpp']:
            with open(config[lang]['mapping_file'], 'w') as f:
                json.dump({}, f, indent=2)
    
    def resolve_dependencies(self, file_path: str) -> bool:
        """Resolve dependencies for a given file"""
        path = Path(file_path)
        if not path.exists():
            self.logger.error(f"File not found: {file_path}")
            return False
        
        try:
            # Get appropriate language handler
            handler = create_language_handler(path.suffix, self.config)
            
            # Extract imports
            self.logger.info(f"Analyzing {file_path}")
            modules = handler.extract_imports(file_path)
            
            if not modules:
                self.logger.info("No imports detected")
                return True
            
            # Check which modules need installation
            missing = []
            for module in modules:
                if not handler.is_installed(module):
                    missing.append(module)
            
            if not missing:
                self.logger.info("All dependencies already installed")
                return True
            
            # Install missing dependencies
            self.logger.info(f"Missing dependencies: {', '.join(missing)}")
            for module in missing:
                package = handler.get_package_name(module)
                self.logger.info(f"Installing {package}")
                if handler.install_package(package):
                    self.logger.info(f"Successfully installed {package}")
                else:
                    self.logger.error(f"Failed to install {package}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error resolving dependencies: {str(e)}")
            return False
    
    def add_mapping(self, language: str, module: str, package: str) -> bool:
        """Add a new module-to-package mapping"""
        try:
            mapping_file = self.config[language]['mapping_file']
            with open(mapping_file, 'r') as f:
                mappings = json.load(f)
            
            mappings[module] = package
            
            with open(mapping_file, 'w') as f:
                json.dump(mappings, f, indent=2)
            
            self.logger.info(f"Added mapping for {language}: {module} → {package}")
            return True
        except Exception as e:
            self.logger.error(f"Error adding mapping: {str(e)}")
            return False
    
    def create_wrapper(self) -> bool:
        """Create a universal wrapper script"""
        wrapper_path = self.home / 'run.sh'
        script_path = sys.argv[0]
        
        content = f"""#!/bin/bash
# PolyDep Universal Script Runner

if [ $# -eq 0 ]; then
  echo "Usage: ./run.sh <script_file> [args]"
  exit 1
fi

SCRIPT="{script_path}"
TARGET="$1"
shift

# Resolve dependencies
python3 "$SCRIPT" "$TARGET"

# Run the script with appropriate interpreter
ext="${{TARGET##*.}}"
case "$ext" in
  py)
    source ~/venv/bin/activate
    python "$TARGET" "$@"
    ;;
  java)
    javac "$TARGET"
    java "${{TARGET%.*}}" "$@"
    ;;
  go)
    go run "$TARGET" "$@"
    ;;
  js)
    node "$TARGET" "$@"
    ;;
  sh)
    bash "$TARGET" "$@"
    ;;
  *)
    echo "Unsupported file type: $ext"
    exit 1
    ;;
esac
"""
        
        with open(wrapper_path, 'w') as f:
            f.write(content)
        
        os.chmod(wrapper_path, 0o755)
        self.logger.info(f"Created wrapper script: {wrapper_path}")
        return True

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="PolyDep: Universal Dependency Resolver")
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Resolve dependencies command
    resolve_parser = subparsers.add_parser('resolve', help='Resolve dependencies for a file')
    resolve_parser.add_argument('file', help='File to analyze')
    
    # Add mapping command
    map_parser = subparsers.add_parser('map', help='Add a module-to-package mapping')
    map_parser.add_argument('language', help='Programming language', choices=['python', 'java', 'go', 'node', 'cpp'])
    map_parser.add_argument('module', help='Module name')
    map_parser.add_argument('package', help='Package name')
    
    # Setup command
    subparsers.add_parser('setup', help='Setup the environment and create wrapper script')
    
    args = parser.parse_args()
    
    polydep = PolyDep()
    
    if args.command == 'resolve':
        polydep.resolve_dependencies(args.file)
    elif args.command == 'map':
        polydep.add_mapping(args.language, args.module, args.package)
    elif args.command == 'setup':
        polydep.create_wrapper()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
