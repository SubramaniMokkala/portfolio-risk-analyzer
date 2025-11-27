import streamlit as st


st.set_page_config(
    page_title="Portfolio Risk Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main application function"""
    
    st.title("📊 Portfolio Risk Analyzer")
    st.markdown("### ML-Powered Investment Analysis Tool")
    
    st.success("✅ Streamlit is successfully installed and running!")
    
    st.markdown("---")
    
    st.info("""
    **Project Status:** Setup Complete  
    **Next Steps:** Add financial data fetching capability
    
    This tool will help you:
    - 📈 Analyze portfolio performance
    - ⚠️ Assess investment risks
    - 🎯 Optimize asset allocation
    - 📊 Visualize financial metrics
    """)
    
    if st.button("🎉 Test Installation"):
        st.balloons()
        st.success("Perfect! Everything is working correctly.")

if __name__ == "__main__":
    main()