import os

BASE_UPLOAD_PATH = "data/uploads"

def save_file(uploaded_file, category):
    """
    Saves uploaded file into the correct category folder.
    category = notes / syllabus / pyq
    """
    folder_path = os.path.join(BASE_UPLOAD_PATH, category)
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path
