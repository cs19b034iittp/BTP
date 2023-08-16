# STEP 1
# import libraries
import fitz
import io
from PIL import Image
import os
from predictImage import predict_image
def delete_non_chem_images():
    for filename in os.listdir('./uploads'):
        if filename.endswith('.jpeg') or filename.endswith('.png'):
            if predict_image(f"./uploads/{filename}") == "Non-chem":
                os.remove(f"./uploads/{filename}")
# STEP 2
def extract(file):
    # open the file
    pdf_file = fitz.open("./uploads/" + file)

    # STEP 3
    # iterate over PDF pages
    for page_index in range(len(pdf_file)):

        # get the page itself
        page = pdf_file[page_index]
        image_list = page.get_images()

        # printing number of images found in this page
        if image_list:
            print(
                f"[+] Found a total of {len(image_list)} images in page {page_index}")
        else:
            print("[!] No images found on page", page_index)
        for image_index, img in enumerate(page.get_images(), start=1):

            # get the XREF of the image
            xref = img[0]

            # extract the image bytes
            base_image = pdf_file.extract_image(xref)
            image_bytes = base_image["image"]

            # get the image extension
            image_ext = base_image["ext"]

            image = Image.open(io.BytesIO(image_bytes))
            # save it to local disk
            image.save(open(f"./uploads/image{page_index+1}_{image_index}.{image_ext}", "wb"))

            result=predict_image(f"./uploads/image{page_index+1}_{image_index}.{image_ext}")
            if result == "Chem":
                print("Chemical")
            else:
                print("Non-chemical")
                os.remove(f"./uploads/image{page_index+1}_{image_index}.{image_ext}")
        
