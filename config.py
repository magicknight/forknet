from easydict import EasyDict as edict

__C = edict()
cfg = __C

#
# Common
#
__C.SUB_CONFIG_FILE = []

__C.CONST = edict()
__C.CONST.N_VOX = [80, 48, 80]
__C.CONST.BATCH_SIZE = 8
__C.SAVER_MAX = 1000
__C.CHECK_FREQ = 1000
__C.RECORD_VOX_NUM = 10
__C.SWITCHING_ITE = 20001

# Network
__C.NET = edict()
__C.NET.DIM_Z = 16
# The last dimension of NET.DIM matters much for GPU consumption for loss function
__C.NET.DIM = [512, 256, 128, 64, 12]
__C.NET.START_VOX = [5, 3, 5]
__C.NET.KERNEL = [[3, 3, 3, 3, 3], [3, 3, 3, 3, 3], [3, 3, 3, 3, 3]]
__C.NET.STRIDE = [1, 2, 2, 2, 1]
__C.NET.DILATIONS = [1, 1, 1, 1, 1]
__C.NET.REFINE_CH = 32
__C.NET.REFINE_KERNEL = 3
__C.NET.REFINER = 'sscnet'

#
# Directories
#
__C.DIR = edict()
# Path where taxonomy.json is stored
# __C.DIR.SCENE_ID_PATH = '../3D-FCR-alphaGAN/Scenevox'
# __C.DIR.VOXEL_PATH = '../3D-FCR-alphaGAN/Scenevox/%s/%s'
__C.DIR.ROOT_PATH = '/media/wangyida/SSD2T/database/SUNCG_Yida/train/voxel_semantic_npy'
__C.DIR.VOXEL_PATH = '/media/wangyida/SSD2T/database/SUNCG_Yida/train/voxel_semantic_npy/%s'
__C.DIR.TSDF_PATH = '/media/wangyida/SSD2T/database/SUNCG_Yida/train/depth_tsdf_npy/%s'
__C.DIR.CHECK_POINT_PATH = '/media/wangyida/SSD2T/models/depvox-gan'
__C.DIR.CHECK_PT_PATH = '/media/wangyida/SSD2T/models/depvox-gan/checkpoint'
__C.DIR.TRAIN_OBJ_PATH = './train_vox'
__C.DIR.EVAL_PATH = './eval'
__C.DIR.LOG_PATH = './log'

#
# Training
#
__C.TRAIN = edict()

__C.TRAIN.DATASET_PORTION = [0, 0.9]
__C.TRAIN.NUM_EPOCH = 500  # maximum number of training epochs

# Learning
__C.LEARNING_RATE_G = 0.0001
__C.LEARNING_RATE_D = 0.0001
__C.LEARNING_RATE_V = [0.0001, 1000, 0.0001]
__C.TRAIN.ADAM_BETA_G = 0.5
__C.TRAIN.ADAM_BETA_D = 0.5
__C.LAMDA_RECONS = 1
__C.LAMDA_GAMMA = 0.97


def cfg_from_file(filename):
    """Load a config file and merge it into the default options."""
    import yaml
    with open(filename, 'r') as f:
        yaml_cfg = edict(yaml.load(f))

    _merge_a_into_b(yaml_cfg, __C)


def cfg_from_list(cfg_list):
    """Set config keys via list (e.g., from command line)."""
    from ast import literal_eval
    assert len(cfg_list) % 2 == 0
    for k, v in zip(cfg_list[0::2], cfg_list[1::2]):
        key_list = k.split('.')
        d = __C
        for subkey in key_list[:-1]:
            assert subkey in d.keys()
            d = d[subkey]
        subkey = key_list[-1]
        assert subkey in d.keys()
        try:
            value = literal_eval(v)
        except:
            # handle the case when v is a string literal
            value = v
        assert type(value) == type(d[subkey]), \
            'type {} does not match original type {}'.format(
            type(value), type(d[subkey]))
        d[subkey] = value
