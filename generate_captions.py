from transformers import pipeline

captioner = pipeline("image-to-text",model="Salesforce/blip-image-captioning-base")
print(captioner("data/mill_fotos_teste/DSC01280.JPG"))
