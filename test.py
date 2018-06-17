import os
from theta_shutter import theta_api

save_dir = './saved_dir'

if not os.path.exists(save_dir):
    os.makedirs(save_dir)

theta_api(save_dir)
