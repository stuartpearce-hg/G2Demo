import os
import shutil
import pdfplumber

class PDFToTextConverter:
    def __init__(self, input_dir: str, output_dir: str):
        """
        Initializes the converter with the given input and output directories.
        :param input_dir: Relative path to the directory containing PDF files.
        :param output_dir: Relative path to the directory where TXT files will be saved.
        """
        self.input_dir = os.path.abspath(input_dir)
        self.output_dir = os.path.abspath(output_dir)

        # Ensure input directory exists
        if not os.path.exists(self.input_dir):
            raise FileNotFoundError(f"Input directory '{self.input_dir}' does not exist.")

        # Ensure output directory exists, create if necessary
        os.makedirs(self.output_dir, exist_ok=True)

    def clear_output_directory(self):
        """Removes all files and folders inside the output directory."""
        for filename in os.listdir(self.output_dir):
            file_path = os.path.join(self.output_dir, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

    def convert_pdfs_to_txt(self):
        """Converts all PDF files in the input directory to TXT files in the output directory."""
        self.clear_output_directory()
        
        pdf_files = [f for f in os.listdir(self.input_dir) if f.lower().endswith(".pdf")]

        if not pdf_files:
            print("No PDF files found in the input directory.")
            return

        for filename in pdf_files:
            pdf_path = os.path.join(self.input_dir, filename)
            txt_filename = os.path.splitext(filename)[0] + ".txt"
            txt_path = os.path.join(self.output_dir, txt_filename)

            print(f"Processing: {filename}")

            # Extract text from PDF
            extracted_text = []
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        extracted_text.append(text)
            
            # Write text to file
            with open(txt_path, "w", encoding="utf-8") as txt_file:
                txt_file.write("\n".join(extracted_text))

        print("PDF to TXT conversion completed!")

# Example usage:
if __name__ == "__main__":
    converter = PDFToTextConverter("inputs", "input_txt")
    converter.convert_pdfs_to_txt()
