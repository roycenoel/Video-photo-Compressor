import os
import subprocess

def compress_media_files(input_folder):
    output_folder = os.path.join(input_folder, 'compressed')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    video_exts = {'.mp4', '.mov', '.avi', '.mkv'}
    image_exts = {'.png', '.jpg', '.jpeg'}

    # List files with creation time, sorted by oldest first
    files_with_ctime = []
    for f in os.listdir(input_folder):
        full_path = os.path.join(input_folder, f)
        if os.path.isfile(full_path):
            ctime = os.path.getctime(full_path)
            files_with_ctime.append((f, ctime))

    files_sorted = sorted(files_with_ctime, key=lambda x: x[1])

    for i, (filename, _) in enumerate(files_sorted, start=1):
        src = os.path.join(input_folder, filename)
        _, ext = os.path.splitext(filename)
        ext = ext.lower()

        compressed_filename = f"{i}{ext}"
        dst = os.path.join(output_folder, compressed_filename)

        if ext in video_exts:
            # Compress video using libx265 codec with CRF 28
            command = [
                "ffmpeg", "-i", src,
                "-vcodec", "libx265", "-crf", "28",
                dst
            ]
        elif ext in image_exts:
            if ext in ['.jpg', '.jpeg']:
                # Compress JPEG with quality setting 23
                command = ["ffmpeg", "-i", src, "-q:v", "23", dst]
            elif ext == ".png":
                # Convert PNG to compressed JPEG for smaller size
                new_dst = os.path.splitext(dst)[0] + ".jpg"
                command = ["ffmpeg", "-i", src, "-q:v", "23", new_dst]
                dst = new_dst
            else:
                print(f"Unsupported image format for compression: {filename}")
                continue
        else:
            print(f"Skipping unsupported file type: {filename}")
            continue

        print(f"Compressing: {filename} → {os.path.basename(dst)}")

        try:
            subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            print(f"Error compressing {filename}: {e}")

    print(f"Compression complete. Files saved in {output_folder}")

# Call the function with your folder path:
input_folder = r"F:\Photo & Video\vids\renamed_files"
compress_media_files(input_folder)
