model=$1
if [ ! -n "$1" ]
then 
    echo 'pelease input the model para: {deit_base, deit_small}'
    exit 8
fi
if [ $model == 'deit_base' ]
then
    model_type='uda_vit_base_patch16_224_TransReID'
    gpus="('0,1')"
else
    model='deit_small'
    model_type='uda_vit_small_patch16_224_TransReID'
    gpus="('0')"
fi
python train.py --config_file configs/uda.yml MODEL.DEVICE_ID $gpus \
OUTPUT_DIR "../logs/uda/deit_base/shipsear/source2target" \
MODEL.PRETRAIN_PATH "../logs/pretrain/deit_base/shipsear/target/transformer_10.pth" \
DATASETS.ROOT_TRAIN_DIR './data/ShipsEar2DeepShip/source_imgs_list.txt' \
DATASETS.ROOT_TRAIN_DIR2 './data/ShipsEar2DeepShip/target_imgs_list.txt' \
DATASETS.ROOT_TEST_DIR './data/ShipsEar2DeepShip/target_imgs_list.txt' \
DATASETS.NAMES "Shipsear" DATASETS.NAMES2 "Shipsear" \
MODEL.Transformer_TYPE $model_type \
SOLVER.LOG_PERIOD 10 