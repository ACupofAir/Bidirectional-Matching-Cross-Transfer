# TODO: inference audio with pretrain model
import os
import torch
import torchvision.transforms as T
from config import cfg
from model import make_model
from datasets.bases import load_image

if __name__ == "__main__":
    #>>>>>>>>>>>>>>>>>>>>[FIXME]>>>>>>>>>>>>>>>>>>>> 
    # config file and checkpoint file
    input_img_path = "/mnt/e/Datasets/TwoBill/testdata/mel/unknown/a10437.png"

    config_file = "configs/pretrain.yml"
    checkpoint = "../logs/pretrain/deit_base/twoBill/target/transformer_best_model.pth"
    twoBill_transforms = T.Compose(
        [
            T.Resize((256, 256)),
            T.CenterCrop((224, 224)),
            T.ToTensor(),
            T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ]
    )

    num_classes = 10
    device = "cuda"

    cfg.merge_from_file(config_file)
    cfg.freeze()
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    #<<<<<<<<<<<<<<<<<<<<[FIXME]<<<<<<<<<<<<<<<<<<<< 

    model = make_model(cfg, num_class=num_classes, camera_num=1, view_num=1)
    model.load_param_finetune(checkpoint)
    model.to(device)
    model.eval()

    img = load_image(input_img_path, twoBill_transforms).to(device)
    img = img.unsqueeze(0)
    camids = torch.tensor([0]).to(device)
    target_view = torch.tensor([0]).to(device)

    probs = model(img, cam_label=camids, view_label=target_view, return_logits=True)
    _, predict = torch.max(probs, 1)
    input_audio_basename = input_img_path.split('/')[-1].split('.')[0]
    print(f'input audio: {input_audio_basename}')
    print(f'predict value: boat{predict.item()+1}')
    print("===========   end  inference   ===========")
