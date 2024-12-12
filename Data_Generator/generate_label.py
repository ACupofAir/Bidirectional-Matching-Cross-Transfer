import os
from tqdm import tqdm

# ! [FIXME]
frame_size = 5
# folder_path = f"C:\\Users\\ASUS\\Desktop\\dataset\\mel-5h36m-frame{frame_size}"
# output_path = f"C:\\Users\\ASUS\\Desktop\\dataset\\mel-5h36m-frame{frame_size}\\deepship-5h36m-frame{frame_size}.txt"
folder_path = rf"C:\Users\ASUS\Dataset\deepship\mel-{frame_size}"
output_path = rf"C:\Users\ASUS\Dataset\deepship\mel-{frame_size}\deepship-{frame_size}.txt"

def generate_folder_file_label(
    folder_path: str, output_path: str, label: str = None
) -> None:
    """Create a txt file contain the folder file and label

    Args:
        folder_path (str): the folder path which need to be labeled
        output_path (str): the txt file path
        label (str): the label name
    """

    if not os.path.isdir(folder_path):
        raise ValueError("Not a valid folder path")
    if label == None:
        label = os.path.basename(folder_path)

    for file_name in tqdm(os.listdir(folder_path)):
        with open(output_path, "a") as output_file:
            file_path = os.path.join(folder_path, file_name)
            print(f"{file_path} {label}", file=output_file)


if __name__ == "__main__":
    print(folder_path)
    cls_folder_list = os.listdir(folder_path)
    for i, cls_folder_basename in enumerate(cls_folder_list):
        abs_folder_path = os.path.join(folder_path, cls_folder_basename)
        print(abs_folder_path)
        generate_folder_file_label(abs_folder_path, output_path, i)
