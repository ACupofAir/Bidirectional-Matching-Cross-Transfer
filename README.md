# Transfer Learning with Attention for Underwater acoustic target recognition

## Requirements Installation

```bash
pip install -r requirements.txt
(Python version is the 3.7 and the GPU is the V100 with cuda 10.1, cudatoolkit 10.1)
```

## Prepare Datasets

### 1. Download the shipsear and deepship datasets

### 2. Convert the audio files to spectrogram

* split frame **Workspace is in the `Data_Generator` directory**
    1. `data_config.json`: config your source and target audio folder path. The directory structure should look like the following.
        * `directory`: the directory will store the spectrograms generate by the program
        * `audio_path`: the directory store audio files which will be convert to spectrograms

        ```bash
        DeepShip
        └── DeepShip_audio
            ├── Cargo
            │   ├── 103.wav
            │   ├── 110.wav
            ├── Passengership
            │   ├── 1.wav
            │   ├── 12.wav
            ├── Tanker
            │   ├── 10.wav
            │   ├── 12.wav
            ...
        ```

    2. `data/split_frame.py` -> `FIXME`, change the directory and method in the file, and generate mel images folder after running this script

    ```python
    python split_frame.py
    ```

* link the dataset to the Deit_Cross_Att net

    ```bash
    ln -s /mnt/d/workspace/dataset/deepship_source/mel data/shipsear/source/images
    ln -s /mnt/d/workspace/dataset/shipears_target/mel data/shipsear/target/images
    ```

* generate label list for dataset
  * `data/generate_label.py` -> FIXME: change the folder_path, output_path
    * `folder_path`: should be the path which contains multi class directory
    * `output_path`: should be  `data/source2target/<source/target>_list.txt`
  * run the `python generate_label.py` command in the `HATT/data` directory

### 3. Then unzip them and rename them under the directory like follow

```
data
├── shipsear2deepship
│   │── shipsear
│   │   └── images
|   │   │   └── class_a
|   |   │   │   └── xxx.png
|   |   │   │   └── xxx.png
|   │   │   └── class_b
|   |   │   │   └── xxx.png
|   |   │   │   └── xxx.png
│   │── deepship
│   │   └── images
|   │   │   └── class_a
|   |   │   │   └── xxx.png
|   |   │   │   └── xxx.png
|   │   │   └── class_b
|   |   │   │   └── xxx.png
|   |   │   │   └── xxx.png
│   └── shipsear.txt
│   └── deepship.txt
```

4. The *.txt file should be like this:

```
$(path_to_image) $(label)
...
$(path_to_image) $(label)
```

### Prepare DeiT-trained Models

For fair comparison in the pre-training data set, we use the DeiT parameter init our model based on ViT.
You need to download the ImageNet pretrained transformer model : [DeiT-Small](https://dl.fbaipublicfiles.com/deit/deit_small_distilled_patch16_224-649709d9.pth), [DeiT-Base](https://dl.fbaipublicfiles.com/deit/deit_base_distilled_patch16_224-df68dfff.pth) and move them to the `./data/pretrainModel` directory.

## Training

I utilize 1 GPU for pre-training and 1 GPU for UDA, each with 8G of memory.(2080s)

* For pretrain

```bash
bash scripts/pretrain/ShipsEar2DeepShip/run_shipsear2deepship.sh deit_base
```

* For transfer learning

```bash
bash scripts/uda/shipsear/run_shipsear.sh deit_base 
```

* All parameters are changed in the shell script

## Evaluation

```bash
# For twoBill only pretrain model
 python test.py --config_file 'configs/pretrain.yml' MODEL.DEVICE_ID "('0')" TEST.WEIGHT "('../logs/pretrain/deit_base/twoBill/target/transformer_best_model.pth')" DATASETS.NAMES 'Shipsear' OUTPUT_DIR '../logs/pretrain/deit_base/twoBill/target' DATASETS.ROOT_TRAIN_DIR './data/twoBill/source_list.txt' './data/twoBill/target_list.txt' DATASETS.ROOT_TEST_DIR './data/twoBill/test_list.txt'
```

```bash
# For twoBill uda
python test.py --config_file 'configs/uda.yml' MODEL.DEVICE_ID "('0')" TEST.WEIGHT "('../logs/uda/deit_base/twoBill/source2target/transformer_best_model.pth')" DATASETS.NAMES 'Shipsear' DATASETS.NAMES2 'Shipsear' OUTPUT_DIR '../logs/uda/deit_base/twoBill/source2target' DATASETS.ROOT_TRAIN_DIR './data/twoBill/source_list.txt' DATASETS.ROOT_TRAIN_DIR2 './data/twoBill/source_list.txt' DATASETS.ROOT_TEST_DIR './data/twoBill/test_list.txt' 
```

## Inference for single image input

### Inference From Mel Image

1. Config the `inference_mel.py` file by searching the `FIXME` keyword
2. Run the following command

```
python inference.py
```

### Inference From Audio

1. Config the `inference_audio.py` file by searching the `FIXME` keyword
2. Run the following command

```
python inference_audio.py
```
