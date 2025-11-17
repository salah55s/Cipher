"""
Streamlit Cipher Visualization App
Authors: Salah, Fares, Ziad, Zeiad
Description: Interactive web UI for cipher encryption with rich visualizations.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from ciphers.caesar_cipher_class import CaesarCipher
from aes_modules.aes_low_level import AESLowLevel
import time


# Page configuration
st.set_page_config(
    page_title="Cipher Encryption Tool",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(120deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 1rem;
    }
    .step-box {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        border-left: 5px solid #667eea;
    }
    .matrix-cell {
        display: inline-block;
        width: 50px;
        height: 50px;
        margin: 2px;
        text-align: center;
        line-height: 50px;
        border: 1px solid #ddd;
        border-radius: 5px;
        background-color: #667eea;
        color: white;
        font-family: monospace;
        font-weight: bold;
    }
    .success-box {
        background-color: #d4edda;
        border-color: #c3e6cb;
        color: #155724;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border-color: #bee5eb;
        color: #0c5460;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)


def render_state_matrix(state, title="State Matrix"):
    """Render a 4x4 state matrix as a heatmap."""
    if state is None:
        return
    
    # Convert to DataFrame
    df = pd.DataFrame(state)
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=df.values,
        text=[[f'{val:02x}' for val in row] for row in state],
        texttemplate='%{text}',
        textfont={"size": 14, "color": "white"},
        colorscale='Viridis',
        showscale=True
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Column",
        yaxis_title="Row",
        height=300,
        width=400
    )
    
    return fig


def render_byte_array(data, title="Byte Array"):
    """Render byte array as colored blocks."""
    cols_per_row = 16
    rows = [data[i:i+cols_per_row] for i in range(0, len(data), cols_per_row)]
    
    html = f"<h4>{title}</h4><div>"
    for row in rows:
        html += "<div style='margin: 5px 0;'>"
        for byte in row:
            color = f"hsl({(byte * 360 // 256)}, 70%, 50%)"
            html += f'<span class="matrix-cell" style="background-color: {color};">{byte:02x}</span>'
        html += "</div>"
    html += "</div>"
    
    return html


def visualize_caesar_step(step):
    """Visualize a Caesar cipher step."""
    with st.expander(f"🔍 {step['title']}", expanded=False):
        st.markdown(f"**Description:** {step['description']}")
        st.code(step['details'], language='text')
        
        # Create visualization based on step type
        if 'Encrypt character' in step['title'] or 'Decrypt character' in step['title']:
            # Character transformation visualization
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                st.metric("Input", step['description'].split('→')[0].strip().strip('"'))
            with col2:
                st.markdown("### ➡️")
            with col3:
                st.metric("Output", step['description'].split('→')[1].strip().strip('"'))
            
            # Show position calculation
            if 'Position:' in step['details']:
                st.info(f"📊 {step['details']}")


def visualize_aes_step(step, step_index):
    """Visualize an AES step with detailed information."""
    
    # Determine icon based on operation
    icons = {
        'Key Derivation': '🔑',
        'Key Expansion': '🔄',
        'Encoding and Padding': '📦',
        'Encrypt Block': '🔒',
        'Decrypt Block': '🔓',
        'Base64 Encoding': '📝',
        'Base64 Decoding': '📖',
        'Remove Padding and Decode': '📂'
    }
    
    icon = icons.get(step['title'].split()[0] + (' ' + step['title'].split()[1] if len(step['title'].split()) > 1 else ''), '⚙️')
    
    with st.expander(f"{icon} Step {step['step_number']}: {step['title']}", expanded=(step_index < 3)):
        st.markdown(f"**{step['description']}**")
        st.caption(step['details'])
        
        # Render specific visualizations based on step type
        if 'block_steps' in step.get('data', {}):
            # Show AES round details
            block_steps = step['data']['block_steps']
            
            st.markdown("---")
            st.markdown("### 🔄 AES Round Operations")
            
            # Group steps by round
            rounds_data = {}
            for block_step in block_steps:
                round_num = block_step['round']
                if round_num not in rounds_data:
                    rounds_data[round_num] = []
                rounds_data[round_num].append(block_step)
            
            # Display rounds in tabs
            round_tabs = st.tabs([f"Round {r}" if r != 'initial' else "Initial" 
                                  for r in sorted(rounds_data.keys(), key=lambda x: -1 if x == 'initial' else x)])
            
            for tab_idx, (round_num, operations) in enumerate(sorted(rounds_data.items(), 
                                                                      key=lambda x: -1 if x[0] == 'initial' else x[0])):
                with round_tabs[tab_idx]:
                    for op_idx, op in enumerate(operations):
                        st.markdown(f"**{op['operation']}**")
                        st.caption(op['description'])
                        st.info(f"ℹ️ {op['details']}")
                        
                        # Show state matrices side by side
                        if op.get('state_before') is not None and op.get('state_after') is not None:
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                fig_before = render_state_matrix(op['state_before'], "Before")
                                st.plotly_chart(fig_before, width="stretch", key=f"before_{step_index}_{tab_idx}_{op_idx}")
                            
                            with col2:
                                fig_after = render_state_matrix(op['state_after'], "After")
                                st.plotly_chart(fig_after, width="stretch", key=f"after_{step_index}_{tab_idx}_{op_idx}")
                        
                        # Show round key if present (NO nested expander)
                        if 'round_key' in op:
                            st.markdown("**Round Key:**")
                            fig_key = render_state_matrix(op['round_key'], "Round Key")
                            st.plotly_chart(fig_key, width="stretch", key=f"key_{step_index}_{tab_idx}_{op_idx}")
                        
                        st.markdown("---")
        
        elif 'key_hex' in step.get('data', {}):
            # Visualize key
            st.code(step['data']['key_hex'], language='text')
        
        elif 'output' in step.get('data', {}):
            # Show output
            output = step['data']['output']
            if len(output) > 100:
                st.text_area("Output", output, height=100, key=f"output_{step_index}")
            else:
                st.code(output, language='text')


def main():
    """Main Streamlit application."""
    
    # Header
    st.markdown('<h1 class="main-header">🔐 Cipher Encryption Tool</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666; font-size: 1.2rem;">Interactive Encryption with Visual Step-by-Step Analysis</p>', 
                unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Cipher selection
        cipher_type = st.radio(
            "Select Cipher Algorithm",
            ["Caesar Cipher", "AES-128", "AES-256"],
            help="Choose the encryption algorithm"
        )
        
        st.markdown("---")
        
        # Mode selection
        mode = st.radio(
            "Operation Mode",
            ["🔒 Encrypt", "🔓 Decrypt"]
        )
        
        st.markdown("---")
        
        # Info
        st.info("💡 **Tip:** Expand each step to see detailed visualizations!")
        
        # Authors
        st.markdown("---")
        st.caption("👥 **Authors:**")
        st.caption("Salah, Fares, Ziad, Zeiad")
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📝 Input")
        
        # Input text
        input_text = st.text_area(
            "Enter your text:",
            height=150,
            placeholder="Type or paste your message here..."
        )
        
        # Key input
        if cipher_type == "Caesar Cipher":
            key = st.number_input(
                "Shift Value:",
                min_value=0,
                max_value=25,
                value=3,
                help="Number of positions to shift (0-25)"
            )
        else:
            key = st.text_input(
                "Password:",
                type="password",
                value="SecurePassword123",
                help="Enter a strong password for encryption/decryption"
            )
        
        # Process button
        process_button = st.button(
            "🚀 Process",
            type="primary",
            use_container_width=True
        )
    
    with col2:
        st.subheader("📤 Output")
        output_placeholder = st.empty()
    
    # Processing
    if process_button:
        if not input_text:
            st.error("❌ Please enter some text to process!")
            return
        
        # Initialize cipher
        with st.spinner("Initializing cipher..."):
            if cipher_type == "Caesar Cipher":
                cipher = CaesarCipher()
            elif cipher_type == "AES-128":
                cipher = AESLowLevel(key_size=128)
            else:  # AES-256
                cipher = AESLowLevel(key_size=256)
        
        # Process
        try:
            with st.spinner("Processing..."):
                is_encrypt = mode == "🔒 Encrypt"
                
                if is_encrypt:
                    result, steps = cipher.encrypt(input_text, key)
                else:
                    result, steps = cipher.decrypt(input_text, key)
            
            # Show output
            with output_placeholder.container():
                st.text_area(
                    "Result:",
                    result,
                    height=150
                )
                
                # Copy button
                if st.button("📋 Copy to Clipboard"):
                    st.code(result, language='text')
                    st.success("✅ Result displayed above - you can copy it now!")
            
            # Visualize steps
            st.markdown("---")
            st.header("🔍 Process Visualization")
            
            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for idx, step in enumerate(steps):
                progress = (idx + 1) / len(steps)
                progress_bar.progress(progress)
                status_text.text(f"Showing step {idx + 1} of {len(steps)}")
                
                if cipher_type == "Caesar Cipher":
                    visualize_caesar_step(step)
                else:
                    visualize_aes_step(step, idx)
            
            progress_bar.progress(1.0)
            status_text.text("✅ All steps visualized!")
            
            # Success message
            st.balloons()
            st.markdown('<div class="success-box">✅ <strong>Success!</strong> Operation completed successfully.</div>', 
                       unsafe_allow_html=True)
            
            # Statistics
            st.markdown("---")
            st.subheader("📊 Statistics")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Input Length", len(input_text))
            with col2:
                st.metric("Output Length", len(result))
            with col3:
                st.metric("Total Steps", len(steps))
            with col4:
                st.metric("Cipher", cipher_type)
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.exception(e)


if __name__ == "__main__":
    main()
