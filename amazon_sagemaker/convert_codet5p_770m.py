import os
import sys
import shutil
import tarfile
import argparse
import boto3
import torch
from transformers import T5ForConditionalGeneration, AutoTokenizer



def compress(tar_dir=None, output_file="model.tar.gz"):
    with tarfile.open(output_file, "w:gz") as tar:
        tar.add(tar_dir, arcname=os.path.sep)

def upload_file_to_s3(bucket_name=None, file_name="model.tar.gz", key_prefix=""):
    s3 = boto3.resource("s3")
    key_prefix_with_file_name = os.path.join(key_prefix, file_name)
    s3.Bucket(bucket_name).upload_file(file_name, key_prefix_with_file_name)
    return f"s3://{bucket_name}/{key_prefix_with_file_name}"

def download_file_from_s3(bucket_name=None, src_loc=None, dest_loc=None):
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(bucket_name)
    for obj in bucket.objects.filter(Prefix=src_loc):
        target = obj.key if dest_loc is None \
            else os.path.join(dest_loc, os.path.relpath(obj.key, src_loc))
        if not os.path.exists(os.path.dirname(target)):
            os.makedirs(os.path.dirname(target))
        if obj.key[-1] == '/':
            continue
        bucket.download_file(obj.key, target)

def convert(bucket_name="hf-sagemaker-inference", checkpoint = "Salesforce/codet5p-770m"):
    key_prefix = "codet5p_770m"
    model_save_dir = f"./tmp_{key_prefix}"
    src_inference_script = "code"
    dst_inference_script = os.path.join(model_save_dir, "code")

    os.makedirs(model_save_dir, exist_ok=True)
    os.makedirs(dst_inference_script, exist_ok=True)

    # load model
    print("Loading model from `Salesforce/codet5p-770m`")
    model = T5ForConditionalGeneration.from_pretrained(checkpoint)

    print("saving model with `torch.save`")
    torch.save(model, os.path.join(model_save_dir, f"model.pt"))

    print("saving tokenizer")
    tokenizer = AutoTokenizer.from_pretrained(checkpoint)
    tokenizer.save_pretrained(model_save_dir)

    # copy inference script
    print("copying inference.py script")
    shutil.copy(src_inference_script, dst_inference_script)

    # create archive
    print("creating `model.tar.gz` archive")
    compress(model_save_dir)

    # upload to s3
    print(
        f"uploading `model.tar.gz` archive to s3://{bucket_name}/{key_prefix}/model.tar.gz"
    )
    model_uri = upload_file_to_s3(bucket_name=bucket_name, key_prefix=key_prefix)
    print(f"Successfully uploaded to {model_uri}")
    
    sys.stdout.write(model_uri)
    return model_uri


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bucket_name", type=str, default=None)
    return parser.parse_args()


if __name__ == "__main__":
    # parse args
    args = parse_args()

    if not args.bucket_name:
        raise ValueError(
            "please provide a valid `bucket_name`, when running `python convert_codet5p_770m.py --bucket_name ...` "
        )

    # read config file
    convert(args.bucket_name)
