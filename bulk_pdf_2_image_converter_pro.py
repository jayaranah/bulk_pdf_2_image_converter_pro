import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pdf2image import convert_from_path
import threading
import subprocess

class PDFConverterApp:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_variables()
        self.setup_styles()
        self.create_widgets()
        
    def setup_window(self):
        self.root.title("PDF to Image Converter Pro")
        self.root.geometry("550x600")
        self.root.resizable(True, True)
        self.root.configure(bg='#f0f0f0')
        
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (700 // 2)
        y = (self.root.winfo_screenheight() // 2) - (550 // 2)
        self.root.geometry(f"550x600+{x}+{y}")
        
        # Add About Menu
        menubar = tk.Menu(self.root)
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        self.root.config(menu=menubar)
        
    def setup_variables(self):
        self.pdf_paths = []
        self.output_folder_path = tk.StringVar()
        self.dpi_var = tk.StringVar(value="300")
        self.format_var = tk.StringVar(value="JPEG")
        self.selected_files_count = tk.StringVar(value="No files selected")
        
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure styles
        style.configure('Title.TLabel', 
                       font=('Arial', 14, 'bold'),
                       background='#f0f0f0',
                       foreground='#2c3e50')
        
        style.configure('Heading.TLabel',
                       font=('Arial', 10, 'bold'),
                       background='#f0f0f0',
                       foreground='#34495e')
        
        style.configure('Info.TLabel',
                       font=('Arial', 9),
                       background='#f0f0f0',
                       foreground='#7f8c8d')
        
        style.configure('Custom.TButton',
                       font=('Arial', 10),
                       padding=(10, 5))
        
        style.configure('Action.TButton',
                       font=('Arial', 11, 'bold'),
                       padding=(10, 5))
        
        style.map('Action.TButton',
                  background=[('active', '#3498db'),
                             ('!active', '#2980b9')])
        
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill='both', expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="📄 PDF to Image Converter", style='Title.TLabel')
        title_label.pack(pady=(0, 5))
        
        # PDF Files Section
        pdf_frame = ttk.LabelFrame(main_frame, text="📁 Select PDF Files", padding="10")
        pdf_frame.pack(fill='x', pady=(0, 10))
        
        pdf_info_frame = ttk.Frame(pdf_frame)
        pdf_info_frame.pack(fill='x', pady=(0, 8))
        
        ttk.Label(pdf_info_frame, text="Choose one or more PDF files to convert:",
                 style='Info.TLabel').pack(anchor='w')
        
        pdf_count_label = ttk.Label(pdf_info_frame, textvariable=self.selected_files_count,
                                   style='Info.TLabel')
        pdf_count_label.pack(anchor='w')
        
        pdf_button_frame = ttk.Frame(pdf_frame)
        pdf_button_frame.pack(fill='x')
        
        self.pdf_entry = ttk.Entry(pdf_button_frame, textvariable=self.pdf_paths,
                                  font=('Arial', 9), state='readonly')
        self.pdf_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        ttk.Button(pdf_button_frame, text="Browse Files", 
                  command=self.select_pdfs, style='Custom.TButton').pack(side='right')
        
        # Output Folder Section
        output_frame = ttk.LabelFrame(main_frame, text="📂 Output Destination", padding="10")
        output_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(output_frame, text="Choose where to save the converted images:",
                 style='Info.TLabel').pack(anchor='w', pady=(0, 8))
        
        output_button_frame = ttk.Frame(output_frame)
        output_button_frame.pack(fill='x')
        
        self.output_entry = ttk.Entry(output_button_frame, textvariable=self.output_folder_path,
                                     font=('Arial', 9), state='readonly')
        self.output_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        ttk.Button(output_button_frame, text="Browse Folder",
                  command=self.select_output_folder, style='Custom.TButton').pack(side='right')
        
        # Settings Section
        settings_frame = ttk.LabelFrame(main_frame, text="⚙️ Conversion Settings", padding="10")
        settings_frame.pack(fill='x', pady=(0, 10))
        
        settings_grid = ttk.Frame(settings_frame)
        settings_grid.pack(fill='x')
        
        # DPI Setting
        dpi_frame = ttk.Frame(settings_grid)
        dpi_frame.pack(side='left', fill='x', expand=True, padx=(0, 15))
        
        ttk.Label(dpi_frame, text="Image Quality (DPI):", style='Heading.TLabel').pack(anchor='w')
        ttk.Label(dpi_frame, text="Higher values = better quality, larger files",
                 style='Info.TLabel').pack(anchor='w', pady=(0, 3))
        
        dpi_menu = ttk.Combobox(dpi_frame, textvariable=self.dpi_var,
                               values=["150", "200", "300", "600"], width=15, state="readonly")
        dpi_menu.pack(anchor='w')
        
        # Format Setting
        format_frame = ttk.Frame(settings_grid)
        format_frame.pack(side='left', fill='x', expand=True)
        
        ttk.Label(format_frame, text="Image Format:", style='Heading.TLabel').pack(anchor='w')
        ttk.Label(format_frame, text="JPEG = smaller files, PNG = lossless",
                 style='Info.TLabel').pack(anchor='w', pady=(0, 3))
        
        format_menu = ttk.Combobox(format_frame, textvariable=self.format_var,
                                  values=["JPEG", "PNG"], width=15, state="readonly")
        format_menu.pack(anchor='w')
        
        # Progress Section
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill='x', pady=(0, 15))
        
        ttk.Label(progress_frame, text="Conversion Progress:", style='Heading.TLabel').pack(anchor='w')
        
        self.progress_bar = ttk.Progressbar(progress_frame, orient="horizontal",
                                           length=400, mode="determinate")
        self.progress_bar.pack(fill='x', pady=(5, 0))
        
        self.progress_label = ttk.Label(progress_frame, text="Ready to convert",
                                       style='Info.TLabel')
        self.progress_label.pack(anchor='w', pady=(3, 0))
        
        # Action Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=(5, 0))
        
        ttk.Button(button_frame, text="🚀 Start Conversion",
                  command=self.start_bulk_conversion, style='Action.TButton').pack(pady=5)
        
    def select_pdfs(self):
        filepaths = filedialog.askopenfilenames(
            title="Select PDF files",
            filetypes=[("PDF files", "*.pdf")])
        if filepaths:
            self.pdf_paths = list(filepaths)
            count = len(filepaths)
            self.selected_files_count.set(f"{count} file{'s' if count != 1 else ''} selected")
            
            # Show truncated path in entry
            if len(filepaths) == 1:
                display_path = os.path.basename(filepaths[0])
            else:
                display_path = f"{os.path.basename(filepaths[0])} and {count-1} more..."
            
            # Temporarily enable entry to update display
            self.pdf_entry.config(state='normal')
            self.pdf_entry.delete(0, 'end')
            self.pdf_entry.insert(0, display_path)
            self.pdf_entry.config(state='readonly')
    
    def select_output_folder(self):
        # Select and store full path for logic
        folder = filedialog.askdirectory(title="Select output folder")
        if folder:
            self.output_folder_path.set(folder)
            
            # Show full path in entry (no truncation)
            self.output_entry.config(state='normal')
            self.output_entry.delete(0, 'end')
            self.output_entry.insert(0, folder)
            self.output_entry.config(state='readonly')
    
    def start_bulk_conversion(self):
        if not self.pdf_paths:
            messagebox.showwarning("Missing Input", "Please select PDF files.")
            return
        
        pdf_paths = [p for p in self.pdf_paths if os.path.exists(p) and p.lower().endswith('.pdf')]
        output_folder = self.output_folder_path.get()
        dpi = int(self.dpi_var.get())
        image_format = self.format_var.get()

        if not pdf_paths:
            messagebox.showwarning("Missing Input", "No valid PDF files found.")
            return
        if not output_folder or not os.path.isdir(output_folder):
            messagebox.showwarning("Missing Input", "Please select a valid output folder.")
            return

        self.progress_label.config(text="Starting conversion...")
        self.progress_bar["value"] = 0

        threading.Thread(
            target=self.export_multiple_pdfs_to_images,
            args=(pdf_paths, output_folder, dpi, image_format),
            daemon=True
        ).start()

    def export_multiple_pdfs_to_images(self, pdf_paths, output_folder, dpi, image_format):
        try:
            os.makedirs(output_folder, exist_ok=True)
            total_files = len(pdf_paths)
            
            for index, pdf_path in enumerate(pdf_paths, start=1):
                if not pdf_path.lower().endswith(".pdf"):
                    continue

                if not os.path.exists(pdf_path):
                    self.progress_label.config(text=f"Error: File not found - {os.path.basename(pdf_path)}")
                    messagebox.showerror("File Error", f"PDF file not found:\n{pdf_path}")
                    continue

                filename = os.path.basename(pdf_path)
                self.progress_label.config(text=f"Converting {filename} ({index}/{total_files})...")
                self.root.update_idletasks()

                try:
                    base_filename = os.path.splitext(os.path.basename(pdf_path))[0]
                    pdf_output_folder = os.path.join(output_folder, base_filename)
                    os.makedirs(pdf_output_folder, exist_ok=True)

                    pages = convert_from_path(pdf_path, dpi=dpi)

                    if not pages:
                        self.progress_label.config(text=f"Warning: No pages found in {filename}")
                        messagebox.showwarning("PDF Warning", f"No pages could be extracted from:\n{filename}")
                        continue

                    for i, page in enumerate(pages):
                        image_filename = f"{base_filename}_page_{i + 1}.{image_format.lower()}"
                        image_path = os.path.join(pdf_output_folder, image_filename)
                        page.save(image_path, image_format.upper())

                except Exception as pdf_error:
                    error_msg = str(pdf_error)
                    self.progress_label.config(text=f"Error processing {filename}")
                    messagebox.showerror("PDF Conversion Error", 
                                         f"Error processing {filename}:\n{error_msg}\n\nThis file will be skipped.")
                    continue

                # Update progress bar
                progress = int((index / total_files) * 100)
                self.progress_bar["value"] = progress
                self.progress_label.config(text=f"Progress: {progress}% ({index}/{total_files})")
                self.root.update_idletasks()

            self.progress_bar["value"] = 100
            self.progress_label.config(text="Conversion completed successfully!")
            
            messagebox.showinfo("Success", "PDF conversion completed!\n\nNote: Any problematic files were skipped.")
            
            # Ask to open the output folder
            open_folder = messagebox.askyesno("Open Folder", 
                                            "Do you want to open the output folder?")
            if open_folder:
                self.open_output_folder(output_folder)
                
        except Exception as e:
            error_msg = str(e)
            messagebox.showerror("Conversion Error", f"An error occurred during conversion:\n{error_msg}")
            self.progress_bar["value"] = 0
            self.progress_label.config(text="Conversion failed")
    
    def show_about(self):
        messagebox.showinfo("About", "PDF to Image Converter Pro\nDeveloped by: Jay-ar Volante\nDonation: Gcash: 09773200481\n\nhttps://github.com/jayaranah")

    def open_output_folder(self, folder_path):
        try:
            if os.name == "nt":
                os.startfile(folder_path)
            elif os.name == "posix":
                subprocess.call(["xdg-open", folder_path])
            else:
                messagebox.showinfo("Notice", f"Please manually open the folder:\n{folder_path}")
        except Exception as e:
            messagebox.showerror("Failed to open folder", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFConverterApp(root)
    root.mainloop()
