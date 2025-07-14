#!/usr/bin/env python3
"""
MCP Server Startup Script

This script starts the Model Context Protocol server for company analysis
with AI integration. Configure environment variables or use a .env file.
"""

import os
import sys
import logging
from pathlib import Path
import argparse
from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from .mcp_server import MCPCompanyAnalysisServer
from ..config import AnalyzerConfig


def setup_logging(verbose: bool = False):
    """Setup logging for the MCP server"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('mcp_server.log')
        ]
    )


def check_dependencies():
    """Check if required dependencies are installed"""
    missing_deps = []
    
    try:
        import openai
    except ImportError:
        missing_deps.append("openai")
    
    try:
        import fastapi
    except ImportError:
        missing_deps.append("fastapi")
    
    try:
        import uvicorn
    except ImportError:
        missing_deps.append("uvicorn")
    
    if missing_deps:
        print("❌ Missing required dependencies:")
        for dep in missing_deps:
            print(f"   - {dep}")
        print("\nInstall with: pip install -r requirements.txt")
        return False
    
    return True


def validate_configuration():
    """Validate MCP server configuration"""
    config = AnalyzerConfig()
    issues = []
    
    # Check OpenAI configuration for AI features
    if config.enable_ai_analysis and not config.openai_api_key:
        issues.append("AI analysis enabled but OPENAI_API_KEY not set")
    
    # Check MCP server settings
    if config.mcp_server_port < 1024 and os.geteuid() != 0:
        issues.append(f"Port {config.mcp_server_port} requires root privileges")
    
    if issues:
        print("⚠️  Configuration issues:")
        for issue in issues:
            print(f"   - {issue}")
        return False
    
    return True


def print_server_info(config: AnalyzerConfig):
    """Print server startup information"""
    print("🚀 Company Analysis MCP Server")
    print("=" * 50)
    print(f"Host: {config.mcp_server_host}")
    print(f"Port: {config.mcp_server_port}")
    print(f"AI Analysis: {'Enabled' if config.enable_ai_analysis and config.openai_api_key else 'Disabled'}")
    print(f"Enhanced NLP: {'Enabled' if config.enable_enhanced_detection else 'Disabled'}")
    print(f"CORS: {'Enabled' if config.mcp_enable_cors else 'Disabled'}")
    print(f"Log Level: {config.log_level}")
    print()
    print("Available endpoints:")
    print(f"  - Health Check: http://{config.mcp_server_host}:{config.mcp_server_port}/health")
    print(f"  - API Docs: http://{config.mcp_server_host}:{config.mcp_server_port}/docs")
    print(f"  - Analysis: http://{config.mcp_server_host}:{config.mcp_server_port}/analyze")
    print("=" * 50)


def main():
    """Main entry point for MCP server"""
    parser = argparse.ArgumentParser(
        description='Start the Company Analysis MCP Server',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Environment Variables:
  OPENAI_API_KEY          OpenAI API key for AI analysis
  OPENAI_MODEL           OpenAI model to use (default: gpt-3.5-turbo)
  MCP_SERVER_HOST        Server host (default: 0.0.0.0)
  MCP_SERVER_PORT        Server port (default: 8000)
  ANALYZER_LOG_LEVEL     Log level (default: INFO)
  ANALYZER_ENABLE_AI     Enable AI analysis (default: false)
  
Examples:
  python run_mcp_server.py
  python run_mcp_server.py --host localhost --port 8080
  python run_mcp_server.py --config custom_config.yaml --verbose
        """
    )
    
    parser.add_argument(
        '--host',
        type=str,
        help='Server host (overrides config/env)'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        help='Server port (overrides config/env)'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        help='Configuration file path'
    )
    
    parser.add_argument(
        '--env-file',
        type=str,
        default='.env',
        help='Environment file path (default: .env)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    parser.add_argument(
        '--check-deps',
        action='store_true',
        help='Check dependencies and exit'
    )
    
    parser.add_argument(
        '--validate-config',
        action='store_true',
        help='Validate configuration and exit'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    
    # Load environment file if it exists
    env_file = Path(args.env_file)
    if env_file.exists():
        load_dotenv(env_file)
        logger.info(f"Loaded environment from {env_file}")
    
    # Check dependencies
    if not check_dependencies():
        return 1
    
    if args.check_deps:
        print("✅ All dependencies are installed")
        return 0
    
    try:
        # Load configuration
        config = AnalyzerConfig(
            config_file=args.config,
            environment=os.getenv('ANALYZER_ENVIRONMENT', 'default')
        )
        
        # Override with command line arguments
        if args.host:
            config.mcp_server_host = args.host
        if args.port:
            config.mcp_server_port = args.port
        
        # Validate configuration
        if not validate_configuration():
            return 1
        
        if args.validate_config:
            print("✅ Configuration is valid")
            return 0
        
        # Print server information
        print_server_info(config)
        
        # Initialize and start server
        logger.info("Initializing MCP server...")
        server = MCPCompanyAnalysisServer(config)
        
        logger.info(f"Starting server on {config.mcp_server_host}:{config.mcp_server_port}")
        server.run_server(
            host=config.mcp_server_host,
            port=config.mcp_server_port
        )
        
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
        return 0
    except Exception as e:
        logger.error(f"Server startup failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 