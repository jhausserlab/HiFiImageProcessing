import numpy as np
from image_processing.czi import get_czis, get_processed_czis
from image_processing.registration import align_images
import time
from datetime import timedelta

# def toType(x):
#   return x.astype(np.uint8)

def get_registration(args, processed_czis):
  if args.disable_registration:
    return processed_czis
  else:
    return align_images(args, processed_czis)


def get_images(args, files):
  # get the czi images with get_czis, then processes the images by background subtraction or normalization
  # Finally gets the aligned images with get_registration.

  #NEW CODE
  #------------------------
  #Process first image
  print('--- Processing first CZI: ', files[0].split())
  processed_czi0 = get_processed_czis(args, get_czis(files[0].split()))
  processed_czi0 = np.array(processed_czi0)
  print('Shape of first image processed is: ', np.shape(processed_czi0))

  #Register the first image as aligned image and use that as reference
  aligned_images = processed_czi0

  #process i images (i=1...R) and align them with the first image
  for file in files[1:]:
    print('--- Processig CZI i:', file.split())
    processed_czi = get_processed_czis(args,get_czis(file.split()))
    processed_czi = np.array(processed_czi)
    print('Shape of processed image i is: ', np.shape(processed_czi))

    #Align image0 and i together, returning an array of [2,C,X,Y]
    aligned_img = get_registration(args, np.concatenate((processed_czi0, processed_czi), axis = 0))
    #To remove the first image as it is already registered in aligned_images before the for
    aligned_img = np.delete(aligned_img, 0, axis = 0)
    aligned_images = np.concatenate((aligned_images, aligned_img), axis = 0)
  #------------------------
  

  return aligned_images



  '''

  #OLD CODE delete all of the above and uncomment below for it to work
  czis = get_czis(files)
  processed_czis = get_processed_czis(args, czis)
  if args.time: aligned_images_time = time.monotonic()
  aligned_images = get_registration(args, processed_czis)
  if args.time: print('info – image registration', timedelta(seconds=time.monotonic() - aligned_images_time))
  
  '''