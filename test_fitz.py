import fitz
path_to_pdf=r'C:\dj-apps-2022-05-25\jd-apps\data_test\test.pdf'
doc = fitz.open(path_to_pdf)  # any supported document type
page = doc[0]  # we want text from this page
page._wrapContents()
"""
-------------------------------------------------------------------------------
Identify the rectangle.
-------------------------------------------------------------------------------
"""
rect = page.first_annot.rect  # this annot has been prepared for us!
# Now we have the rectangle ---------------------------------------------------

print(page.get_textbox(rect))