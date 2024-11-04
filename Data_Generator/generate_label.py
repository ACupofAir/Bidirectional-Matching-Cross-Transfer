import os
from tqdm import tqdm

# ! [FIXME]
folder_path = r"E:\AirFTP\Datasets\DeepShip-Enh\mel-2.5"  # the path contain diff dirs store diff class mel spec
output_path = r"E:\AirFTP\Datasets\DeepShip-Enh\mel-2.5\deepship-enh.txt"  # the output path of the txt file


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
