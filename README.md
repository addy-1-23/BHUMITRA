# 🌿 BHUMITRA By ADWAITA PATANE

**AI-powered plant disease detection tool using a custom CNN and Gemini Pro API**  
Built with **PyTorch** and **Streamlit**, BHUMITRA enables users to upload leaf images, input crop context, and receive real-time disease predictions, treatment suggestions, and feedback-based model improvement. 
---

## 🚀 Features

- 🖼️ **Image Upload**: Upload via file or URL  
- 🌱 **Context-Aware Predictions**: Inputs for plant species, region, and season  
- 🧠 **CNN-Based Classifier**: High-accuracy model trained on PlantVillage dataset  
- 🤖 **Gemini Pro API Integration**: Enhances interpretation with detailed visual-textual analysis  
- 📈 **Top Disease Predictions**: With confidence scores  
- 💊 **Treatment Suggestions**: Powered by Gemini’s visual reasoning  
- 💬 **User Feedback**: Users can rate prediction accuracy and submit comments  
- 📝 **Feedback Logging**: Stores feedback for future model refinement  
- 🌐 **Streamlit Interface**: Simple, clean, and user-friendly frontend  

---

## 🧰 Tech Stack

- **Model Training:** PyTorch, Torchvision, scikit-learn  
- **Web Interface:** Streamlit  
- **Image Processing:** PIL, NumPy  
- **Inference:** Custom CNN + Gemini Pro API  
- **Deployment:** Google Colab (training), Localhost (interface)  

---

## 🏗️ System Architecture

1. **Data Preprocessing:** Label encoding, image transforms, custom dataset loader  
2. **Model Training:** Custom CNN with dropout, early stopping, and loss optimization  
3. **Inference Pipeline:** CNN predictions + Gemini API for enhanced reasoning  
4. **UI:** Streamlit app with image upload, context inputs, and real-time results  
5. **Feedback Loop:** User ratings and comments saved for model tuning  

---

## 📊 Results & Evaluation

- CNN achieved **>95% accuracy** on the validation set  
- Confusion matrix used to analyze misclassifications  
- Gemini integration validated through qualitative outputs  
- Real-time testing via Streamlit showed low latency and high user satisfaction  

---

## ⚙️ Challenges Faced

| **Challenge**                     | **Solution**                                              |
|----------------------------------|-----------------------------------------------------------|
| Memory bottlenecks with 50k+ images | Batched loading, optimized augmentation                   |
| Class imbalance                  | Oversampling + weighted loss                              |
| Overfitting                      | Dropout, early stopping, data augmentation                |
| Gemini API complexity            | Custom MIME serialization, prompt templating              |
| Streamlit session resets         | File I/O with unique session IDs                          |
| Prompt-context integration       | Dynamic Jinja-style prompt formatting                     |

---

## 📈 Future Scope

- 📱 Mobile & edge deployment  
- 🌐 Multilingual support  
- 👨‍🌾 Collaboration with agri-bodies  
- 🛰️ Offline inference in remote areas  

---

## 📚 References

- [PlantVillage Dataset](https://plantvillage.psu.edu/)  
- [Gemini API](https://ai.google.dev/)  
- [PyTorch Docs](https://pytorch.org/)  
- [Streamlit Docs](https://docs.streamlit.io/)  

---

## 💻 Installation & Setup

### 🔧 Prerequisites

- Python 3.8+  
- `pip` (Python package manager)  
- Google API credentials (for Gemini API access)  

### 📦 Clone the Repository

```bash
git clone https://github.com/yourusername/plant-disease-detector.git
cd plant-disease-detector
pip install torch torchvision scikit-learn streamlit numpy pillow matplotlib tqdm
streamlit run plant_disease_detector.py
