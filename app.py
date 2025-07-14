import streamlit as st
import json
import os
import tempfile
import io
import asyncio
from typing import Dict, Any, Optional
import pandas as pd
from pathlib import Path
import logging
from datetime import datetime

# Import the analyzer modules
from src.core.company_analyzer import CompanyAnalyzer
from src.ai.company_analyzer_ai import AIEnhancedCompanyAnalyzer
from src.config.config import AnalyzerConfig

# Configure Streamlit page
st.set_page_config(
    page_title="File Folder Analysis Tool",
    page_icon="📁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        padding-top: 1rem;
    }
    .stButton > button {
        width: 100%;
        margin-top: 1rem;
    }
    .status-box {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
    }
    .config-section {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def display_status(message: str, status_type: str = "info"):
    """Display status message with appropriate styling"""
    if status_type == "success":
        st.markdown(f'<div class="status-box success-box">{message}</div>', unsafe_allow_html=True)
    elif status_type == "error":
        st.markdown(f'<div class="status-box error-box">{message}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="status-box info-box">{message}</div>', unsafe_allow_html=True)

def create_default_local_config() -> Dict[str, Any]:
    """Create default configuration for local analysis"""
    return {
        "chunk_size": 5000,
        "filter_type": "all",
        "confidence_threshold": 0.3,
        "enable_enhanced_detection": True,
        "enable_caching": True,
        "log_level": "INFO",
        "output_formats": ["json", "csv", "txt"],
        "max_search_results": 10,
        "max_summary_companies": 50,
        "min_company_name_length": 2,
        "max_company_name_length": 50,
        "spacy_model": "en_core_web_sm",
        "known_companies": [
            "Accent Group",
            "AGL",
            "Microsoft Corporation",
            "Apple Inc"
        ],
        "csv_columns": {
            "name": "Name",
            "path": "Path",
            "modified_by": "Modified By",
            "item_type": "Item Type",
            "file_size": "File Size",
            "modified": "Modified"
        }
    }

def create_default_mcp_config() -> Dict[str, Any]:
    """Create default configuration for MCP analysis"""
    return {
        "chunk_size": 5000,
        "filter_type": "all",
        "confidence_threshold": 0.3,
        "enable_enhanced_detection": True,
        "enable_ai_analysis": True,
        "enable_mcp_server": True,
        "openai_model": "gpt-3.5-turbo",
        "openai_max_tokens": 2000,
        "openai_temperature": 0.3,
        "ai_max_companies_batch": 20,
        "mcp_server_host": "0.0.0.0",
        "mcp_server_port": 8005,
        "mcp_enable_cors": True,
        "log_level": "INFO",
        "output_formats": ["json", "csv", "txt"],
        "max_search_results": 10,
        "max_summary_companies": 50,
        "known_companies": [
            "Accent Group",
            "AGL",
            "Microsoft Corporation",
            "Apple Inc"
        ],
        "csv_columns": {
            "name": "Name",
            "path": "Path",
            "modified_by": "Modified By",
            "item_type": "Item Type",
            "file_size": "File Size",
            "modified": "Modified"
        }
    }

def validate_config(config: Dict[str, Any], analysis_type: str) -> tuple[bool, str]:
    """Validate configuration file"""
    try:
        required_fields = ["chunk_size", "filter_type", "confidence_threshold"]
        
        if analysis_type == "mcp":
            required_fields.extend(["enable_ai_analysis", "openai_model"])
        
        missing_fields = [field for field in required_fields if field not in config]
        if missing_fields:
            return False, f"Missing required fields: {', '.join(missing_fields)}"
        
        # Validate data types
        if not isinstance(config.get("chunk_size"), int) or config["chunk_size"] <= 0:
            return False, "chunk_size must be a positive integer"
        
        if config.get("filter_type") not in ["all", "folders", "files"]:
            return False, "filter_type must be 'all', 'folders', or 'files'"
        
        if not isinstance(config.get("confidence_threshold"), (int, float)) or not (0 <= config["confidence_threshold"] <= 1):
            return False, "confidence_threshold must be a number between 0 and 1"
        
        return True, "Configuration is valid"
        
    except Exception as e:
        return False, f"Error validating configuration: {str(e)}"

def run_local_analysis(csv_file, config: Dict[str, Any]) -> tuple[bool, str, Optional[Any]]:
    """Run local analysis with the provided configuration"""
    try:
        # Create temporary config file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp_file:
            json.dump(config, tmp_file)
            config_file_path = tmp_file.name
        
        # Save uploaded CSV file
        csv_file_path = None
        if csv_file is not None:
            with tempfile.NamedTemporaryFile(mode='wb', suffix='.csv', delete=False) as tmp_csv:
                tmp_csv.write(csv_file.getvalue())
                csv_file_path = tmp_csv.name
        
        # Initialize analyzer with config
        analyzer_config = AnalyzerConfig(config_file=config_file_path)
        analyzer = CompanyAnalyzer(
            csv_file_path=csv_file_path,
            chunk_size=config.get("chunk_size", 5000),
            filter_type=config.get("filter_type", "all")
        )
        
        # Run analysis
        success = analyzer.analyze()
        
        if success:
            # Save results to files (like CLI does)
            output_formats = config.get("output_formats", ["json", "csv", "txt"])
            created_files = analyzer.save_results(output_formats)
            
            # Get results
            results = {
                "companies": dict(analyzer.companies.most_common(50)),
                "total_companies": len(analyzer.companies),
                "total_entries": sum(analyzer.companies.values()),
                "stats": analyzer.stats,
                "using_enhanced_detector": analyzer.using_enhanced_detector,
                "output_files": created_files  # Include created file paths
            }
            
            # Clean up temporary files
            os.unlink(config_file_path)
            if csv_file_path:
                os.unlink(csv_file_path)
            
            return True, "Analysis completed successfully", results
        else:
            return False, "Analysis failed", None
            
    except Exception as e:
        return False, f"Error running analysis: {str(e)}", None

def run_mcp_analysis(csv_file, config: Dict[str, Any]) -> tuple[bool, str, Optional[Any]]:
    """Run MCP analysis with the provided configuration"""
    try:
        # Validate API key is provided
        if not config.get("openai_api_key"):
            return False, "OpenAI API key is required for MCP analysis", None
        
        # Set environment variables for AI
        os.environ["OPENAI_API_KEY"] = config["openai_api_key"]
        os.environ["ANALYZER_ENABLE_AI"] = "true"
        os.environ["ANALYZER_ENABLE_MCP"] = "true"
        
        # Create temporary config file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp_file:
            json.dump(config, tmp_file)
            config_file_path = tmp_file.name
        
        # Save uploaded CSV file
        csv_file_path = None
        if csv_file is not None:
            with tempfile.NamedTemporaryFile(mode='wb', suffix='.csv', delete=False) as tmp_csv:
                tmp_csv.write(csv_file.getvalue())
                csv_file_path = tmp_csv.name
        
        # Initialize AI-enhanced analyzer
        analyzer_config = AnalyzerConfig(config_file=config_file_path)
        analyzer = AIEnhancedCompanyAnalyzer(
            csv_file_path=csv_file_path,
            chunk_size=config.get("chunk_size", 5000),
            filter_type=config.get("filter_type", "all"),
            enable_ai=True
        )
        
        # Run analysis
        success = analyzer.analyze()
        
        if success:
            # Save results to files (like CLI does)
            output_formats = config.get("output_formats", ["json", "csv", "txt"])
            created_files = analyzer.save_results(output_formats)
            
            # Save AI results if available
            ai_files = []
            if hasattr(analyzer, 'save_ai_results'):
                try:
                    ai_files = analyzer.save_ai_results()
                except:
                    pass  # AI results saving is optional
            
            # Get AI-enhanced results
            results = {
                "companies": dict(analyzer.companies.most_common(50)),
                "total_companies": len(analyzer.companies),
                "total_entries": sum(analyzer.companies.values()),
                "stats": analyzer.stats,
                "using_enhanced_detector": analyzer.using_enhanced_detector,
                "ai_enabled": analyzer.enable_ai,
                "ai_results": analyzer.ai_results if hasattr(analyzer, 'ai_results') else None,
                "executive_summary": analyzer.executive_summary if hasattr(analyzer, 'executive_summary') else None,
                "output_files": created_files + ai_files  # Include all created file paths
            }
            
            # Clean up temporary files
            os.unlink(config_file_path)
            if csv_file_path:
                os.unlink(csv_file_path)
            
            return True, "AI-enhanced analysis completed successfully", results
        else:
            return False, "Analysis failed", None
            
    except Exception as e:
        return False, f"Error running MCP analysis: {str(e)}", None

def main():
    """Main Streamlit application"""
    st.title("📁 File Folder Analysis Tool")
    st.markdown("Upload configuration files and analyze CSV data for company extraction")
    
    # Sidebar for navigation
    st.sidebar.title("📋 Analysis Options")
    analysis_mode = st.sidebar.selectbox(
        "Select Analysis Mode",
        ["Local (Offline)", "MCP (Online with AI)"],
        help="Choose between local offline analysis or AI-enhanced online analysis"
    )
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📂 Upload Files")
        
        # CSV file upload
        csv_file = st.file_uploader(
            "Upload CSV File",
            type=['csv'],
            help="Upload the CSV file you want to analyze"
        )
        
        if csv_file is not None:
            st.success(f"✅ CSV file uploaded: {csv_file.name}")
            
            # Show CSV preview
            try:
                df = pd.read_csv(csv_file)
                st.subheader("📊 CSV Preview")
                st.dataframe(df.head(), use_container_width=True)
                st.info(f"CSV contains {len(df)} rows and {len(df.columns)} columns")
            except Exception as e:
                st.error(f"Error reading CSV file: {str(e)}")
    
    with col2:
        st.header("⚙️ Configuration")
        
        if analysis_mode == "Local (Offline)":
            st.subheader("🏠 Local Analysis Configuration")
            
            # Configuration upload
            config_file = st.file_uploader(
                "Upload Local Configuration (JSON)",
                type=['json'],
                help="Upload a JSON configuration file for local analysis"
            )
            
            if config_file is not None:
                try:
                    config = json.load(config_file)
                    st.success("✅ Configuration loaded successfully")
                    
                    # Validate configuration
                    is_valid, validation_message = validate_config(config, "local")
                    if is_valid:
                        display_status(validation_message, "success")
                    else:
                        display_status(validation_message, "error")
                        return
                        
                except Exception as e:
                    st.error(f"Error loading configuration: {str(e)}")
                    return
            else:
                # Use default configuration
                config = create_default_local_config()
                st.info("Using default local configuration")
            
            # Show current configuration
            with st.expander("📋 Current Configuration", expanded=False):
                st.json(config)
            
            # Download default configuration template
            st.subheader("📥 Download Configuration Template")
            default_config = create_default_local_config()
            config_json = json.dumps(default_config, indent=2)
            st.download_button(
                label="Download Local Config Template",
                data=config_json,
                file_name="local_config.json",
                mime="application/json"
            )
        
        else:  # MCP Analysis
            st.subheader("☁️ MCP Analysis Configuration")
            
            # Configuration upload
            config_file = st.file_uploader(
                "Upload MCP Configuration (JSON)",
                type=['json'],
                help="Upload a JSON configuration file for MCP analysis"
            )
            
            if config_file is not None:
                try:
                    config = json.load(config_file)
                    st.success("✅ Configuration loaded successfully")
                    
                    # Validate configuration
                    is_valid, validation_message = validate_config(config, "mcp")
                    if is_valid:
                        display_status(validation_message, "success")
                    else:
                        display_status(validation_message, "error")
                        return
                        
                except Exception as e:
                    st.error(f"Error loading configuration: {str(e)}")
                    return
            else:
                # Use default configuration
                config = create_default_mcp_config()
                st.info("Using default MCP configuration")
            
            # API Key input for MCP
            st.subheader("🔑 API Configuration")
            api_key = st.text_input(
                "OpenAI API Key",
                type="password",
                help="Enter your OpenAI API key for AI-enhanced analysis"
            )
            
            if api_key:
                config["openai_api_key"] = api_key
                st.success("✅ API key configured")
            else:
                st.warning("⚠️ API key is required for MCP analysis")
            
            # Show current configuration
            with st.expander("📋 Current Configuration", expanded=False):
                # Hide API key in display
                display_config = config.copy()
                if "openai_api_key" in display_config:
                    display_config["openai_api_key"] = "***hidden***"
                st.json(display_config)
            
            # Download default configuration template
            st.subheader("📥 Download Configuration Template")
            default_config = create_default_mcp_config()
            config_json = json.dumps(default_config, indent=2)
            st.download_button(
                label="Download MCP Config Template",
                data=config_json,
                file_name="mcp_config.json",
                mime="application/json"
            )
    
    # Analysis section
    st.header("🚀 Run Analysis")
    
    # Run analysis button
    if st.button("Start Analysis", type="primary"):
        if csv_file is None:
            st.error("❌ Please upload a CSV file first")
            return
        
        if analysis_mode == "MCP (Online with AI)" and not config.get("openai_api_key"):
            st.error("❌ Please provide an OpenAI API key for MCP analysis")
            return
        
        # Show progress
        with st.spinner("🔄 Running analysis..."):
            if analysis_mode == "Local (Offline)":
                success, message, results = run_local_analysis(csv_file, config)
            else:
                success, message, results = run_mcp_analysis(csv_file, config)
        
        # Display results
        if success:
            display_status(message, "success")
            
            # Show results
            st.header("📊 Analysis Results")
            
            if results:
                # Create tabs for different result views
                tab1, tab2, tab3, tab4 = st.tabs(["📈 Summary", "🏢 Companies", "📋 Details", "📁 Output Files"])
                
                with tab1:
                    st.subheader("📈 Analysis Summary")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Total Companies", results["total_companies"])
                    with col2:
                        st.metric("Total Entries", results["total_entries"])
                    with col3:
                        detector_type = "Enhanced NLP" if results["using_enhanced_detector"] else "Basic"
                        st.metric("Detector Type", detector_type)
                    
                    # AI results if available
                    if results.get("ai_enabled") and results.get("executive_summary"):
                        st.subheader("🤖 AI Executive Summary")
                        st.write(results["executive_summary"])
                
                with tab2:
                    st.subheader("🏢 Top Companies Found")
                    if results["companies"]:
                        companies_df = pd.DataFrame(
                            list(results["companies"].items()),
                            columns=["Company", "Count"]
                        )
                        companies_df = companies_df.sort_values("Count", ascending=False)
                        st.dataframe(companies_df, use_container_width=True)
                        
                        # Chart
                        st.bar_chart(companies_df.set_index("Company")["Count"])
                    else:
                        st.info("No companies found in the analysis")
                
                with tab3:
                    st.subheader("📋 Technical Details")
                    if results["stats"]:
                        st.json(results["stats"])
                    
                    # AI results if available
                    if results.get("ai_results"):
                        st.subheader("🤖 AI Analysis Details")
                        st.json(results["ai_results"])
                
                with tab4:
                    st.subheader("📁 Generated Output Files")
                    
                    if results.get("output_files"):
                        st.success(f"✅ {len(results['output_files'])} output files created successfully!")
                        
                        for file_path in results["output_files"]:
                            file_name = os.path.basename(file_path)
                            file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
                            
                            col1, col2, col3 = st.columns([3, 1, 1])
                            with col1:
                                st.write(f"📄 **{file_name}**")
                            with col2:
                                st.write(f"{file_size:,} bytes")
                            with col3:
                                # Create download button
                                if os.path.exists(file_path):
                                    with open(file_path, 'rb') as f:
                                        st.download_button(
                                            label="📥 Download",
                                            data=f.read(),
                                            file_name=file_name,
                                            mime="application/octet-stream",
                                            key=f"download_{file_name}"
                                        )
                        
                        st.info("💡 **Tip**: Files are also saved in your project directory for CLI access!")
                        st.code("\n".join([f"• {os.path.basename(f)}" for f in results["output_files"]]))
                        
                    else:
                        st.warning("⚠️ No output files were created")
        else:
            display_status(message, "error")
    
    # Footer
    st.markdown("---")
    st.markdown("*File Folder Analysis Tool - Upload configurations and analyze CSV data*")

if __name__ == "__main__":
    main() 