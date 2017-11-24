from institute.settings import BASE_DIR
from college.constants import THUMBNAIL_EXTENSION
from college.constants import IMAGE_THUMBNAIL_SIZE,THUMBNAIL_EXTENSION

def thumbnail(file,filename,fl):
    from django.core.files.storage import default_storage as s3_storage
    from PIL import Image
    im = Image.open(s3_storage.open(fl.file.name))
    im.thumbnail(IMAGE_THUMBNAIL_SIZE, Image.ANTIALIAS)
    thumb_loc = BASE_DIR+"/static/images/thumbnails/"+fl.file.name.split("/")[-1]+'.' + str(fl.id) + THUMBNAIL_EXTENSION
    f_thumb = s3_storage.open(thumb_loc, "w")
    im.save(f_thumb, format='JPEG')
    f_thumb.close()
    return thumb_loc

def thumbnail_model(file, filename, fl):
    thumb_loc = BASE_DIR+"/static/images/thumbnails"+fl.file.name+'.' + fl.id + THUMBNAIL_EXTENSION
    return thumb_loc