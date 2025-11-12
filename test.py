from pypdf import PdfReader

reader = PdfReader("docs/FJP Organization Chart_v1.6.pdf")
    
for page in reader.pages:
    # print(page)
    print(page.extract_text())