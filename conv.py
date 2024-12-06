
import os
import sys
from PIL import Image
from pillow_heif import register_heif_opener
import piexif

def convert_heic_to_jpg(input_folder, output_folder=None):
    """
    Convert HEIC files to JPG while preserving EXIF metadata including location information.
    
    :param input_folder: Path to the folder containing HEIC files
    :param output_folder: Path to the folder where JPG files will be saved (optional)
    """
    # Normalize Windows file paths
    input_folder = os.path.normpath(input_folder)
    
    # If no output folder specified, use the input folder
    if output_folder is None:
        output_folder = input_folder
    else:
        output_folder = os.path.normpath(output_folder)
    
    # Register HEIF/HEIC opener
    register_heif_opener()
    
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Counter for successful and failed conversions
    success_count = 0
    fail_count = 0
    
    # Iterate through files in the input folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.heic'):
            try:
                # Construct full file paths
                input_path = os.path.join(input_folder, filename)
                output_filename = os.path.splitext(filename)[0] + '.jpg'
                output_path = os.path.join(output_folder, output_filename)
                
                # Open the HEIC image
                with Image.open(input_path) as img:
                    # Extract EXIF data if available
                    exif_dict = None
                    try:
                        # Try to get EXIF data
                        exif = img.info.get('exif')
                        if exif:
                            exif_dict = piexif.load(exif)
                    except Exception as exif_error:
                        print(f"Could not read EXIF data for {filename}: {exif_error}")
                    
                    # Convert image to RGB
                    rgb_img = img.convert('RGB')
                    
                    # Save with EXIF data if available
                    if exif_dict:
                        # Convert EXIF dictionary back to bytes
                        exif_bytes = piexif.dump(exif_dict)
                        rgb_img.save(output_path, 'JPEG', exif=exif_bytes)
                    else:
                        # Save without EXIF if no data found
                        rgb_img.save(output_path, 'JPEG')
                
                print(f"Converted: {filename} -> {output_filename}")
                success_count += 1
            
            except Exception as e:
                print(f"Error converting {filename}: {e}")
                fail_count += 1
    
    # Print summary
    print("\nConversion Summary:")
    print(f"Total HEIC files processed: {success_count + fail_count}")
    print(f"Successful conversions: {success_count}")
    print(f"Failed conversions: {fail_count}")

def main():
    # Check if path is provided as command-line argument
    if len(sys.argv) > 1:
        input_folder = sys.argv[1]
        
        # Check if a second argument for output folder is provided
        if len(sys.argv) > 2:
            output_folder = sys.argv[2]
            convert_heic_to_jpg(input_folder, output_folder)
        else:
            convert_heic_to_jpg(input_folder)
    else:
        # Prompt for input folder if not provided
        input_folder = input("Enter the full path to the folder containing HEIC files: ")
        
        # Ask about output folder
        use_custom_output = input("Do you want to specify a custom output folder? (y/n): ").lower()
        
        if use_custom_output == 'y':
            output_folder = input("Enter the full path to the output folder: ")
            convert_heic_to_jpg(input_folder, output_folder)
        else:
            convert_heic_to_jpg(input_folder)

if __name__ == "__main__":
    main()


