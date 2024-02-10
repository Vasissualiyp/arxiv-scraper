import re
import sympy as sp
from gtts import gTTS

def text_to_speech(text, output_file):
    tts = gTTS(text)
    tts.save(output_file)

def convert_math_to_text(latex_content):
    # Replace simple symbols
    latex_content = re.sub(r'\$', '', latex_content)  # Remove $ symbols
    latex_content = latex_content.replace('M_\\odot', 'solar masses')

    # Find math expressions
    math_expressions = re.findall(r'\\sim 10\^{(-?\d+)}', latex_content)

    for expr in math_expressions:
        # Convert the expression to text
        sympy_expr = sp.sympify(f"10**{expr}")
        text_expr = sp.pretty(sympy_expr, use_unicode=False)

        # Replace in the original content
        latex_content = latex_content.replace(f'\\sim 10^{{{expr}}}', f'around {text_expr}')

    return latex_content

def extract_document_content(latex_file_path):
    with open(latex_file_path, 'r') as file:
        content = file.read()
    
    print(latex_file_path)
    # Regular expression to find content between \begin{document} and \end{document}
    match = re.search(r'\\begin{document}(.*?)\\end{document}', content, re.DOTALL)

    if match:
        return match.group(1).strip()
    else:
        return "No document content found."

def tts_main(config):
    speech_tex_file = config.SpeechTexFile 
    output_speech_file = config.OutputSpeechFile 

    latex_content = extract_document_content(speech_tex_file)
    print(speech_tex_file)
    print(latex_content)
    text_to_speech(latex_content, output_speech_file)

def tts_with_video_main(config):
    separate_papers_folder = config.SeparatePapersFolder

    # List all files in the separate_papers_folder
    for filename in os.listdir(separate_papers_folder):
        # Filter files that end with '_speech.tex'
        if filename.endswith('_speech.tex'):
            speech_tex_file = os.path.join(separate_papers_folder, filename)
            
            # Construct the output speech file name
            base_name = filename.replace('_speech.tex', '')
            output_speech_file = os.path.join(separate_papers_folder, f"{base_name}.mp3")
            
            # Extract LaTeX content from the file
            latex_content = extract_document_content(speech_tex_file)
            
            # Logging for debugging
            print(f"Processing: {speech_tex_file}")
            print(f"Latex Content: {latex_content[:100]}...")  # Print first 100 characters for preview
            
            # Convert LaTeX content to speech
            text_to_speech(latex_content, output_speech_file)
            
            print(f"Generated speech file: {output_speech_file}")

