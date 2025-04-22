from PIL import Image
import streamlit as st
from typing import Optional

def load_logo(path: str = 'logo.png', width: int = 100) -> Optional[Image.Image]:
    """
    Load and display a logo image.
    
    Args:
        path: Path to the logo image file
        width: Display width in pixels
        
    Returns:
        PIL.Image if loaded successfully, None otherwise
    """
    try:
        image = Image.open(path)
        st.image(image, width=width)
        return image
    except FileNotFoundError:
        st.warning(f"Logo image not found at {path}")
        return None
    except Exception as e:
        st.error(f"Error loading logo: {str(e)}")
        return None