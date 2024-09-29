@echo off
set model=%1
if "%1"=="" (
    echo 请提供模型参数: {deit_base, deit_small}
    exit /b 8
)
if "%model%"=="deit_base" (
    set model_type=vit_base_patch16_224_TransReID
    set pretrain_model=deit_base_distilled_patch16_224-df68dfff.pth
) else (
    set model=deit_small
    set model_type=vit_small_patch16_224_TransReID
    set pretrain_model=deit_small_distilled_patch16_224-649709d9.pth
)
python train.py --config_file configs/pretrain.yml MODEL.DEVICE_ID "('0')" DATASETS.NAMES 'Shipsear' ^
OUTPUT_DIR "../logs/pretrain/%model%/shipsear/target" ^
DATASETS.ROOT_TRAIN_DIR "./data/ShipsEar2DeepShip/source_imgs_list.txt" ^
DATASETS.ROOT_TEST_DIR "./data/ShipsEar2DeepShip/target_imgs_list.txt" ^
SOLVER.LOG_PERIOD 10