# PolyDep: Universal Dependency Resolver

PolyDep is a revolutionary tool that automatically detects and resolves missing dependencies across multiple programming languages, enabling seamless development without dependency management headaches.

## Features

- **Cross-Language Support**: Works with Python, Java, Go, JavaScript/Node.js, C++, and more
- **Automatic Detection**: Parses source files to identify required dependencies
- **Intelligent Installation**: Determines and installs the appropriate packages
- **Smart Mapping**: Maintains a database mapping modules to packages
- **Extensible Design**: Object-oriented architecture makes adding support for new languages easy
- **Script Execution**: Integrated wrapper to handle dependency resolution and execution in one step

## Installation

```bash
git clone https://github.com/mrpongalfer/u_u/polydep.git
cd polydep
chmod +x polydep.py
./polydep.py setup
```

## Quick Start

### Resolve Dependencies and Run a Script

Simply use the generated wrapper to run your scripts with automatic dependency management:

```bash
~/run.sh your_script.py
```

Or if you prefer to resolve dependencies manually:

```bash
./polydep.py resolve path/to/your_script.py
```

### Add Custom Module Mappings

Add mappings for modules that might have different package names:

```bash
./polydep.py map python tensorflow-gpu tensorflow-gpu
```

## Architecture

PolyDep follows a modular, object-oriented design:

1. **Core Engine (`PolyDep` class)**: Manages configuration, logging, and orchestrates operations
2. **Language Handlers**: Specialized classes for each programming language
3. **Factory Method**: Creates appropriate handlers based on file extensions
4. **Universal Wrapper**: Handles both dependency resolution and execution

## Language Support

PolyDep currently supports:

| Language | File Extensions | Package Manager | Status |
|----------|----------------|-----------------|--------|
| Python   | .py, .pyw      | pip            | ✅ Complete |
| Java     | .java          | Maven          | ✅ Complete |
| Go       | .go            | go get         | ✅ Complete |
| Node.js  | .js, .ts       | npm            | 🔄 Partial |
| C++      | .cpp, .cc, .h  | CMake/vcpkg    | 🔄 Partial |

## Extending PolyDep

To add support for a new language, create a new class that inherits from `LanguageHandler` and implements these methods:

```python
def extract_imports(self, file_path: str) -> Set[str]:
    # Parse the file and extract import statements
    
def is_installed(self, module: str) -> bool:
    # Check if the module is already installed
    
def get_package_name(self, module: str) -> str:
    # Map module name to package name
    
def install_package(self, package: str) -> bool:
    # Install the package using appropriate package manager
```

Then add your handler to the `create_language_handler` factory method.

## Integration with AI Agents

PolyDep is designed to be easily integrated with AI agents for fully automated dependency management:

1. **API Interface**: The modular design makes it easy to call from other programs
2. **Structured Output**: JSON-formatted logs and responses for easy parsing
3. **Plugin System**: (Coming soon) Will allow AI agents to extend functionality

## Future Roadmap

- **Dependency Graph Analysis**: Detect and resolve complex dependency chains
- **Version Management**: Handle version conflicts and compatibility issues
- **Container Integration**: Support for Docker and other containerization technologies
- **Remote Execution**: Execute dependency resolution on remote machines
- **Plugin System**: Allow third-party plugins for custom behavior

## License

MIT
