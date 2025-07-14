import streamlit as st
import json
import os
import tempfile
import io
import asyncio
from typing import Dict, Any, Optional, List
import pandas as pd
from pathlib import Path
import logging
from datetime import datetime

# Import the analyzer modules
from src.core.company_analyzer import CompanyAnalyzer
from src.ai.company_analyzer_ai import AIEnhancedCompanyAnalyzer
from src.ai.manual_ai_analyzer import ManualAIAnalyzer
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



def validate_config(config: Dict[str, Any], analysis_type: str) -> tuple[bool, str]:
    """Validate configuration file"""
    try:
        required_fields = ["chunk_size", "filter_type", "confidence_threshold"]
        
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


async def run_manual_ai_analysis(analyzer, selected_terms: List[str], config_name: str) -> tuple[bool, str, Optional[Any]]:
    """Run manual AI analysis with the provided terms and configuration"""
    try:
        # Run AI analysis
        results = await analyzer.analyze_manual_selection(selected_terms, config_name)
        
        if results.get('status') == 'success':
            return True, "AI analysis completed successfully", results
        else:
            return False, f"AI analysis failed: {results.get('error', 'Unknown error')}", None
            
    except Exception as e:
        return False, f"Error running AI analysis: {str(e)}", None



def main():
    """Main Streamlit application"""
    st.title("📁 File Folder Analysis Tool")
    st.markdown("Upload configuration files and analyze CSV data for company extraction")
    
    # Sidebar for navigation
    st.sidebar.title("📋 Analysis Options")
    analysis_mode = st.sidebar.selectbox(
        "Choose Analysis Mode",
        ["Local (Offline)", "Manual AI Analysis"],
        help="Select the type of analysis you want to perform"
    )
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📂 Upload Files")
        
        if analysis_mode == "Local (Offline)":
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
        
        elif analysis_mode == "Manual AI Analysis":
            st.subheader("🎯 Manual Term Selection")
            
            # Term input methods
            input_method = st.radio(
                "Choose input method:",
                ["Text Input", "File Upload", "CSV Column Selection"],
                help="Select how you want to provide terms for analysis"
            )
            
            selected_terms = []
            
            if input_method == "Text Input":
                # Text area for manual input
                terms_text = st.text_area(
                    "Enter terms/phrases to analyze (one per line)",
                    height=200,
                    help="Enter each term or phrase on a separate line"
                )
                
                if terms_text:
                    selected_terms = [term.strip() for term in terms_text.split('\n') if term.strip()]
                    st.success(f"✅ {len(selected_terms)} terms entered")
            
            elif input_method == "File Upload":
                # File upload for terms
                terms_file = st.file_uploader(
                    "Upload terms file (txt or csv)",
                    type=['txt', 'csv'],
                    help="Upload a file containing terms to analyze"
                )
                
                if terms_file is not None:
                    try:
                        if terms_file.name.endswith('.txt'):
                            content = terms_file.read().decode('utf-8')
                            selected_terms = [term.strip() for term in content.split('\n') if term.strip()]
                        else:  # CSV
                            df = pd.read_csv(terms_file)
                            # Assume first column contains terms
                            selected_terms = df.iloc[:, 0].dropna().tolist()
                        
                        st.success(f"✅ {len(selected_terms)} terms loaded from file")
                    except Exception as e:
                        st.error(f"Error reading file: {str(e)}")
            
            elif input_method == "CSV Column Selection":
                # CSV file upload for column selection
                csv_file = st.file_uploader(
                    "Upload CSV File",
                    type=['csv'],
                    help="Upload CSV file and select column containing terms"
                )
                
                if csv_file is not None:
                    try:
                        df = pd.read_csv(csv_file)
                        st.subheader("📊 CSV Preview")
                        st.dataframe(df.head(), use_container_width=True)
                        
                        # Column selection
                        column_name = st.selectbox(
                            "Select column containing terms to analyze",
                            df.columns.tolist(),
                            help="Choose the column that contains company names or terms"
                        )
                        
                        if column_name:
                            selected_terms = df[column_name].dropna().astype(str).tolist()
                            st.success(f"✅ {len(selected_terms)} terms selected from column '{column_name}'")
                    except Exception as e:
                        st.error(f"Error reading CSV file: {str(e)}")
            
            # Display selected terms
            if selected_terms:
                st.subheader("📋 Selected Terms")
                terms_df = pd.DataFrame(selected_terms, columns=["Term"])
                st.dataframe(terms_df, use_container_width=True)
                
                # Allow user to edit/remove terms
                st.subheader("✏️ Edit Terms")
                terms_to_remove = st.multiselect(
                    "Select terms to remove:",
                    selected_terms,
                    help="Select terms you want to exclude from analysis"
                )
                
                if terms_to_remove:
                    selected_terms = [term for term in selected_terms if term not in terms_to_remove]
                    st.success(f"✅ {len(selected_terms)} terms remaining after filtering")
    
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
        
        elif analysis_mode == "Manual AI Analysis":
            st.subheader("🤖 Manual AI Analysis Configuration")
            
            # OpenAI API Key
            openai_api_key = st.text_input(
                "OpenAI API Key",
                type="password",
                help="Enter your OpenAI API key for AI analysis"
            )
            
            if not openai_api_key:
                st.warning("⚠️ OpenAI API key is required for Manual AI Analysis")
                return
            
            # Load available AI analysis configurations
            try:
                manual_analyzer = ManualAIAnalyzer(openai_api_key)
                available_configs = manual_analyzer.get_available_configs()
                
                if not available_configs:
                    st.error("❌ No AI analysis configurations found in ai_analysis_configs/")
                    return
                
                # Configuration selection
                config_names = list(available_configs.keys())
                selected_config = st.selectbox(
                    "Select Analysis Configuration",
                    config_names,
                    help="Choose the type of AI analysis to perform"
                )
                
                if selected_config:
                    config_info = available_configs[selected_config]
                    st.info(f"📋 **{config_info.get('name', selected_config)}**")
                    st.write(f"*{config_info.get('description', 'No description available')}*")
                    
                    # Show configuration details
                    with st.expander("📋 Configuration Details", expanded=False):
                        st.json(config_info)
                
            except Exception as e:
                st.error(f"❌ Error loading AI configurations: {str(e)}")
                return
    st.header("🚀 Run Analysis")
    
    # Run analysis button
    if st.button("Start Analysis", type="primary"):
        if analysis_mode == "Local (Offline)":
            if csv_file is None:
                st.error("❌ Please upload a CSV file first")
                return
            
            if config.get("enable_ai_analysis") and not config.get("openai_api_key"):
                st.error("❌ Please provide an OpenAI API key for AI analysis")
                return
            
            # Show progress
            with st.spinner("🔄 Running local analysis..."):
                success, message, results = run_local_analysis(csv_file, config)
        
        elif analysis_mode == "Manual AI Analysis":
            if not selected_terms:
                st.error("❌ Please provide terms to analyze")
                return
            
            if not openai_api_key:
                st.error("❌ Please provide an OpenAI API key")
                return
            
            if not selected_config:
                st.error("❌ Please select an analysis configuration")
                return
            
            # Show progress
            with st.spinner("🔄 Running AI analysis..."):
                try:
                    manual_analyzer = ManualAIAnalyzer(openai_api_key)
                    success, message, results = asyncio.run(run_manual_ai_analysis(
                        manual_analyzer, selected_terms, selected_config
                    ))
                except Exception as e:
                    success = False
                    message = f"AI analysis failed: {str(e)}"
                    results = None
        
        # Display results
        if success:
            display_status(message, "success")
            
            # Show results
            st.header("📊 Analysis Results")
            
            if results:
                if analysis_mode == "Local (Offline)":
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
                
                elif analysis_mode == "Manual AI Analysis":
                    # Create tabs for AI analysis results
                    tab1, tab2, tab3, tab4 = st.tabs(["📈 Summary", "🤖 AI Results", "📋 Details", "📁 Export"])
                    
                    with tab1:
                        st.subheader("📈 AI Analysis Summary")
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("Terms Analyzed", results.get("terms_analyzed", 0))
                        with col2:
                            st.metric("Valid Results", results.get("summary", {}).get("valid_results", 0))
                        with col3:
                            config_name = results.get("config_used", "Unknown")
                            st.metric("Analysis Type", config_name)
                        
                        # Show confidence statistics
                        if results.get("summary", {}).get("confidence_stats"):
                            st.subheader("📊 Confidence Statistics")
                            conf_stats = results["summary"]["confidence_stats"]
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Average Confidence", f"{conf_stats['average']:.2f}")
                            with col2:
                                st.metric("Min Confidence", f"{conf_stats['min']:.2f}")
                            with col3:
                                st.metric("Max Confidence", f"{conf_stats['max']:.2f}")
                    
                    with tab2:
                        st.subheader("🤖 AI Analysis Results")
                        if results.get("analysis_results"):
                            # Display results in a table
                            ai_results = results["analysis_results"]
                            if ai_results:
                                # Convert to DataFrame for better display
                                results_data = []
                                for result in ai_results:
                                    row = {
                                        "Term": result.get("company_name", "Unknown"),
                                        "Is Company": result.get("is_company", False),
                                        "Confidence": f"{result.get('confidence_score', 0):.2f}",
                                        "Industry": result.get("primary_industry", result.get("industry", "Unknown")),
                                        "Type": result.get("company_type", "Unknown"),
                                        "Reasoning": result.get("reasoning", "No reasoning provided")
                                    }
                                    results_data.append(row)
                                
                                results_df = pd.DataFrame(results_data)
                                st.dataframe(results_df, use_container_width=True)
                                
                                # Show industry distribution if available
                                if results.get("summary", {}).get("industry_distribution"):
                                    st.subheader("🏭 Industry Distribution")
                                    industry_data = results["summary"]["industry_distribution"]
                                    industry_df = pd.DataFrame(
                                        list(industry_data.items()),
                                        columns=["Industry", "Count"]
                                    )
                                    st.bar_chart(industry_df.set_index("Industry")["Count"])
                            else:
                                st.info("No analysis results available")
                        else:
                            st.warning("No AI analysis results found")
                    
                    with tab3:
                        st.subheader("📋 Analysis Details")
                        st.json(results)
                    
                    with tab4:
                        st.subheader("📁 Export Results")
                        
                        # Export as JSON
                        results_json = json.dumps(results, indent=2)
                        st.download_button(
                            label="📥 Download JSON Results",
                            data=results_json,
                            file_name=f"ai_analysis_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                            mime="application/json"
                        )
                        
                        # Export as CSV if results are available
                        if results.get("analysis_results"):
                            ai_results = results["analysis_results"]
                            if ai_results:
                                # Create CSV data
                                csv_data = []
                                for result in ai_results:
                                    csv_data.append({
                                        "Term": result.get("company_name", ""),
                                        "Is_Company": result.get("is_company", False),
                                        "Confidence": result.get("confidence_score", 0),
                                        "Industry": result.get("primary_industry", result.get("industry", "")),
                                        "Company_Type": result.get("company_type", ""),
                                        "Reasoning": result.get("reasoning", "")
                                    })
                                
                                csv_df = pd.DataFrame(csv_data)
                                csv_string = csv_df.to_csv(index=False)
                                st.download_button(
                                    label="📥 Download CSV Results",
                                    data=csv_string,
                                    file_name=f"ai_analysis_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                    mime="text/csv"
                                )
        else:
            display_status(message, "error")
    
    # Footer
    st.markdown("---")
    st.markdown("*File Folder Analysis Tool - Upload configurations and analyze CSV data*")

if __name__ == "__main__":
    main() 