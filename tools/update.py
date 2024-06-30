# Supposedly I'm going to try and integrate the beta into the current version... this may be a pipe dream.

import os
import shutil
import click

@click.command()
@click.argument('source_folder')
@click.argument('destination_folder')
def update_folders(source_folder, destination_folder):
    """Deletes all contents of the destination folder and copies contents from the source folder."""
    # Check if source folder exists
    if not os.path.exists(source_folder):
        print(f"Source folder {source_folder} does not exist.")
        return

    # Check if destination folder exists, if not create it
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Delete all contents of the destination folder
    for item in os.listdir(destination_folder):
        item_path = os.path.join(destination_folder, item)
        if os.path.isfile(item_path) or os.path.islink(item_path):
            os.unlink(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)

    # Copy contents from source folder to destination folder
    for item in os.listdir(source_folder):
        src_path = os.path.join(source_folder, item)
        dst_path = os.path.join(destination_folder, item)
        if os.path.isdir(src_path):
            shutil.copytree(src_path, dst_path)
        else:
            shutil.copy2(src_path, dst_path)

    print(f"Copied contents from {source_folder} to {destination_folder}")

if __name__ == "__main__":
    update_folders()