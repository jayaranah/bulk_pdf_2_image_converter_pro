## 📄 PDF to Image Converter Pro
A user-friendly Python GUI application for converting multiple PDF files into image formats (JPEG or PNG). Built using Tkinter and pdf2image, it supports batch processing with quality and format settings.


## 🚀 Features
✅ Convert multiple PDFs in one go

✅ Output images in JPEG or PNG

✅ Set image quality using DPI (150, 200, 300, 600)

✅ Automatically creates folders for each PDF

✅ Progress bar and status updates

✅ Open output folder after conversion

✅ Clean and modern GUI built with ttk styles

## 📦 Requirements
Python 3.7 or higher

Windows or Linux
## 📚 Install Dependencies
You can install the required dependencies using pip:
```bash
pip install pdf2image
```
🔧 Note: On Windows, pdf2image requires the [Poppler](https://github.com/oschwartz10612/poppler-windows/releases/) library.
After downloading, extract it and add the bin folder to your system PATH.

## 🧠 How It Works
1. Select one or more PDF files using the Browse Files button.

2. Choose the destination folder where the images will be saved.

3. Select the desired image quality (DPI) and format (JPEG/PNG).

4. Click 🚀 Start Conversion to begin.

5. Images will be saved inside folders named after each PDF.


## 📥 Download Poppler (Required for Windows)
Download precompiled Poppler binaries for Windows here:

👉 https://github.com/oschwartz10612/poppler-windows/releases/

Then:

1. Extract it to a folder, e.g., C:\poppler-xx\

2. Add the path C:\poppler-xx\Library\bin to your system PATH.

## 💡 Tip for Developers
If you're improving or modifying the app:

- Modularize the class into separate files (ui.py, converter.py, etc.)

- Add drag-and-drop support for faster file selection

- Implement PDF password handling or image compression options

## 📜 License
This project is open-source and free to use under the MIT License.

## ❤️ Credits
- Built with Tkinter

- Uses pdf2image for conversion

- Styled using ttk and modern layout practices



![2025-07-06_135634](https://github.com/user-attachments/assets/d7557638-1774-485e-8fdf-f8ee8f0fe113)
