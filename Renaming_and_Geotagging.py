import os
from exifread import process_file
from piexif.GPS import GPS

def rename_and_geotag_files(folder_path, keyword, company_name, locations):
  # Get list of files in the folder
  files = os.listdir(folder_path)
  start_number = 1  # Adjust if you want a different starting number

  for filename in files:
    # Extract file extension
    extension = os.path.splitext(filename)[1]

    # Open image file for processing Exif data
    with open(os.path.join(folder_path, filename), 'rb') as image_file:
      # Read Exif data using exifread
      exif_data = process_file(image_file)

    # Check if location data available for this image
    if filename in locations:
      image_location = locations[filename]
      latitude = image_location.get('latitude')
      longitude = image_location.get('longitude')

      # Create new GPS tags dictionary (if location data available)
      if latitude is not None and longitude is not None:
        gps_exif = {
          GPS.GPSLatitudeRef: image_location.get('latitude_ref', 'N'),  # Default to North
          GPS.GPSLatitude: ((latitude * 600000, 10**7), (1, 1)),
          GPS.GPSLongitudeRef: image_location.get('longitude_ref', 'E'),  # Default to East
          GPS.GPSLongitude: ((longitude * 600000, 10**7), (1, 1)),
        }
    else:
      gps_exif = None  # No GPS data to write

    # Rename logic (unchanged)
    # Create new filename with sequence number, keyword, company name, and extension
    new_filename = f"{keyword} - {start_number:01d} - {company_name}{extension}"

    # Geotag logic (using piexif)
    if gps_exif:
      from piexif.easy import write_exif_data

      # Write GPS tags using piexif
      write_exif_data(os.path.join(folder_path, new_filename), gps_exif)
      print(f"Geolocated {filename} - Latitude: {latitude:.6f}, Longitude: {longitude:.6f}")
    else:
      print(f"No location data provided for {filename} (using existing Exif data if available).")

    # Rename the file (unchanged)
    os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))
    start_number += 1

# Specify folder path, keyword, company name, and location dictionary
folder_path = "/Users/willstaton/Downloads/WWW4 Images"  # Replace with your actual path
keyword = "Testing123"  # Replace with your desired keyword
company_name = "Test Company"  # Replace with the company name
locations = {
  "image1.jpg": {"latitude": 37.7749, "longitude": -122.4194, "latitude_ref": "S"},  # Replace with actual locations for your images
  # Add entries for other images with their corresponding locations (including optional 'latitude_ref' and 'longitude_ref')
}
rename_and_geotag_files(folder_path, keyword, company_name, locations)

print("Files renamed and geotagged (if data provided).")
