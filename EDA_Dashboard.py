import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
from mm_adoption_visualization import mm_adoption_visualization

def eda_dashboard(st, df):
    st.title('Mobile Money Adoption in Tanzania')

    # Show image
    mm_adoption_visualization(df)
