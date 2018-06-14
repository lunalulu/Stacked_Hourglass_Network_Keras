import sys
sys.path.insert(0, "../data_gen/")
sys.path.insert(0, "../net/")

import argparse
import os
import tensorflow as tf
from keras import backend as k
from hourglass import HourglassNet

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--gpuID", default=0, type=int, help='gpu id')
    parser.add_argument("--network", help="specify  network arch'")
    parser.add_argument("--batch_size", default=8, type=int, help='batch size for training')
    parser.add_argument("--model_path",  help='path to store trained model')
    parser.add_argument("--num_stack",  default=2, type=int, help='num of stacks')
    parser.add_argument("--epochs", default=20, type=int, help="number of traning epochs")
    parser.add_argument("--resume", default=False, type=bool,  help="resume training or not")
    parser.add_argument("--resumeModel", help="start point to retrain")
    parser.add_argument("--initEpoch", type=int, help="epoch to resume")

    args = parser.parse_args()

    os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
    os.environ["CUDA_VISIBLE_DEVICES"] = str(args.gpuID)


    # TensorFlow wizardry
    config = tf.ConfigProto()

    # Don't pre-allocate memory; allocate as-needed
    config.gpu_options.allow_growth = True

    # Only allow a total of half the GPU memory to be allocated
    config.gpu_options.per_process_gpu_memory_fraction = 1.0

    # Create a session with the above options specified.
    k.tensorflow_backend.set_session(tf.Session(config=config))

    xnet = HourglassNet(num_classes=16, num_stacks=args.num_stack, inres=(256, 256), outres=(64, 64))
    xnet.build_model(show=True)
    xnet.train(epochs=args.epochs, model_path=args.model_path, batch_size=args.batch_size)
