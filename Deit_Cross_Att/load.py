import torch
from model import make_model
from datasets import make_dataloader
from config import cfg


# * config model
config_file = 'configs/uda.yml'
cfg.merge_from_file(config_file)
cfg.freeze()
model_path = '/home/june/workspace/logs/uda/deit_base/office/amazon2webcam/transformer_best_model.pth'

# * load model
model = make_model(cfg, num_class=31, camera_num=1, view_num=1)
model.load_state_dict(torch.load(model_path))
