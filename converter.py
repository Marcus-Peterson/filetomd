import streamlit as st
from markitdown import MarkItDown
import os
import time

# Skapa en instans av MarkItDown
markitdown = MarkItDown()

def convert_file(uploaded_file):
    # Create a progress bar and status text
    progress = st.progress(0)
    status_text = st.empty()
    
    # Step-by-step progress updates
    progress.step = 0

    # Läs filens innehåll från den uppladdade filen
    temp_path = f"temp_{uploaded_file.name}"
    with open(temp_path, "wb") as temp_file:
        temp_file.write(uploaded_file.read())
    progress.step += 25
    progress.progress(progress.step)
    status_text.text("Uploading file...")

    time.sleep(0.5)  # Simulate processing delay

    dot_index = temp_path.rfind('.')
    try:
        if dot_index != -1:
            new_filename = f"{temp_path[:dot_index]}.md"
        else:
            return "Invalid file name or file type."
    except Exception as e:
        return str(e)

    progress.step += 25
    progress.progress(progress.step)
    status_text.text("Preparing for conversion...")

    time.sleep(0.5)  # Simulate processing delay

    try:
        # Använd MarkItDown för att konvertera filen
        result = markitdown.convert(temp_path)
        progress.step += 25
        progress.progress(progress.step)
        status_text.text("Converting file...")

        time.sleep(0.5)  # Simulate processing delay

        with open(new_filename, "w", encoding="utf-8") as file:
            file.write(result.text_content)

        os.remove(temp_path)  # Rensa upp den temporära filen
        
        # Mark progress as complete and change text color
        progress.progress(100)
        status_text.markdown("**Your file was successfully converted! 🎉**", unsafe_allow_html=True)

        return new_filename
    except Exception as e:
        os.remove(temp_path)  # Rensa upp även vid fel
        progress.progress(0)  # Reset progress on error
        status_text.error("An error occurred during conversion.")
        return str(e)


def main():
    st.title("📝 File to Markdown Converter 📝")
    st.markdown(
        """
        Upload any supported file (e.g., PDF, Word, Excel, PowerPoint), 
        and this app will convert it to Markdown. You can also download the Markdown file afterward.
        """
    )

    uploaded_file = st.file_uploader("Upload your file here: ", type=None)
    if uploaded_file is not None:
        st.write("Converting file...")
        converted_file_path = convert_file(uploaded_file)
        if converted_file_path.endswith(".md"):
            with open(converted_file_path, "r", encoding="utf-8") as md_file:
                markdown_content = md_file.read()
            st.download_button(
                "Download your Markdown file",
                markdown_content,
                file_name="converted_file.md",
                mime="text/markdown",
            )
            os.remove(converted_file_path)  # Rensa upp efter nedladdning
        else:
            st.error(f"Error during conversion: {converted_file_path}")


if __name__ == "__main__":
    main()
