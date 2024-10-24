import os
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\adriano.silva\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

def process_images():
    folder_path = filedialog.askdirectory(title="Select a folder containing images")
    if not folder_path:
        return
    
    supported_formats = ['.jpg', '.png']

    image_files = [filename for filename in os.listdir(folder_path) if os.path.splitext(filename)[-1].lower() in supported_formats]
    num_images = len(image_files)

    progress_bar['maximum'] = num_images
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    
    transcription_text = ""
    for idx, filename in enumerate(image_files, start=1):
        progress_bar['value'] = idx
        progress_label.config(text=f"Processing image {idx} of {num_images}")
        root.update_idletasks()
        
        image_path = os.path.join(folder_path, filename)
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image, lang='eng')
            transcription_text += f"Text from '{filename}':\n{text.strip()}\n{'-'*50}\n\n"
        except Exception as e:
            print(f"Error processing '{filename}': {e}")
    
    progress_label.config(text="Processing completed.")
    result_text.insert(tk.END, transcription_text)
    result_text.config(state=tk.DISABLED)

def copy_text():
    selected_text = result_text.selection_get()
    root.clipboard_clear()
    root.clipboard_append(selected_text)

root = tk.Tk()
root.title("Image to Text Converter")

main_frame = ttk.Frame(root, padding=(20, 10))
main_frame.grid(row=0, column=0)

browse_button = ttk.Button(main_frame, text="Select Folder", command=process_images)
browse_button.grid(row=0, column=0, padx=5, pady=5)

progress_bar = ttk.Progressbar(main_frame, orient=tk.HORIZONTAL, length=400, mode='determinate')
progress_bar.grid(row=1, column=0, padx=5, pady=5)

progress_label = ttk.Label(main_frame, text="")
progress_label.grid(row=2, column=0, padx=5, pady=5)

result_text = tk.Text(root, wrap=tk.WORD, state=tk.DISABLED)
result_text.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=result_text.yview)
scrollbar.grid(row=1, column=1, sticky='ns')

result_text.config(yscrollcommand=scrollbar.set)
result_text.bind("<Button-3>", lambda e: result_text.tag_add(tk.SEL, "sel.first", "sel.last"))
result_text.bind("<Control-c>", lambda e: copy_text())

root.mainloop()
