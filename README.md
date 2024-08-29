# SOU-Chat-UI
### Introduction

I’ve chosen a robust tech stack for building a simple chatbot that can map spoken input to video content. This stack combines various tools to handle user interaction, speech-to-text conversion, text comparison, and translation. Here’s a concise overview of each component, including its benefits and potential drawbacks:

### Tech Stack Overview

1. **Streamlit**
   - **Pros**: 
     - Simplifies web app development with minimal code.
     - Supports rapid prototyping with interactive widgets.
     - Easy integration with Python code.
   - **Cons**: 
     - Limited to Python; not ideal if you need advanced frontend customization.
     - May not handle very complex applications or high traffic well.

2. **audio-recorder-streamlit**
   - **Pros**: 
     - Enables users to record and upload audio easily from the Streamlit interface.
     - Streamlined for use within Streamlit apps.
   - **Cons**: 
     - Limited to Streamlit; may not be easily reusable outside this framework.
     - Can be sensitive to browser compatibility issues.

3. **SpeechRecognition**
   - **Pros**: 
     - Converts audio speech to text, making it accessible for text-based processing.
     - Supports various speech recognition engines.
   - **Cons**: 
     - Accuracy can vary with background noise and accents.
     - Might require additional setup for optimal performance.

4. **fuzzywuzzy**
   - **Pros**: 
     - Useful for handling approximate text matching and user input variations.
     - Easy to use with a simple API for string comparison.
   - **Cons**: 
     - Performance can be slow for large datasets.
     - May not handle very complex text matching scenarios well.

5. **python-Levenshtein**
   - **Pros**: 
     - Enhances performance of fuzzy string matching by providing fast computation of string distances.
     - Reduces the computational load compared to pure Python implementations.
 
6. **googletrans==4.0.0-rc1**
   - **Pros**: 
     - Provides easy integration for translation, enabling multi-language support.
     - Simple API for translating text between different languages.
   - **Cons**: 
     - Version stability can be an issue; it’s a release candidate, not a final version.
     - May face limitations or quota restrictions with extensive use.

### Usage
- Create a virtual environment and activate it.
- Install dependencies.
```bash
pip install -r requirements.txt
```
- Make a folder called "videos" and add videos to it.
- Map the videos to questions using mydb dictionary in main.py file.
- Run the main.py file
```
streamlit run main.py
```

### Next steps
 - Make the mapper scalable using a database.
 - Use vector search algorithms instead of FuzzySearch.
 - Remove the Google based dependencies since they have a quota attached to them.
