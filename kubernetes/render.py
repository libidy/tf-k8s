# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 20:18:45 2016

@author: lanlin
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import argparse
import jinja2

HOME = os.environ.get("HOME")

NAMESPACE_JINJA = "namespace.jinja"
NFS_JINJA = "nfs.jinja"
CLUSTER_SPEC_SVC_PS_JINJA = "cluster_spec_svc_ps.jinja"
CLUSTER_SPEC_WORKER_JINJA = "cluster_spec_worker.jinja"
NFS_TENSORBOARD_JINJA = "nfs_tensorboard.jinja"
TENSORBOARD_JINJA = "tensorboard.jinja"
START_CLUSTER_JINJA = "start_cluster.jinja"
STOP_CLUSTER_JINJA = "stop_cluster.jinja"
START_TENSORBOARD_JINJA = "start_tensorboard.jinja"
STOP_TENSORBOARD_JINJA = "stop_tensorboard.jinja"

JINJA_FILE_0 = [NAMESPACE_JINJA, NFS_JINJA, CLUSTER_SPEC_SVC_PS_JINJA,
                NFS_TENSORBOARD_JINJA, TENSORBOARD_JINJA]
JINJA_FILE_1 = [START_CLUSTER_JINJA, STOP_CLUSTER_JINJA,
                START_TENSORBOARD_JINJA, STOP_TENSORBOARD_JINJA]

def main(args):
    properties = dict(args._get_kwargs())
    properties["parameters"] = eval(properties["parameters"])
    dirname = HOME + "/GPU_cluster_storage/{}/{}/k8s_config".format(
        properties["namespace"], properties["name"])
    os.system("mkdir -p {}".format(dirname))
    for jinja_file in JINJA_FILE_0:
        extension = "yaml"
        with open(jinja_file, "r") as f:
            template = jinja2.Template(f.read())
        with open("{}/{}.{}".format(
            dirname, os.path.splitext(jinja_file)[0], extension), "w") as f:
            f.write(template.render(properties=properties))

    for index in range(properties["worker_replicas"]):
        extension = "yaml"
        with open(CLUSTER_SPEC_WORKER_JINJA, "r") as f:
            template = jinja2.Template(f.read())
        with open("{}/{}_{}.{}".format(
            dirname, os.path.splitext(CLUSTER_SPEC_WORKER_JINJA)[0],
            index, extension), "w") as f:
            f.write(template.render(properties=properties, index=index))

    for jinja_file in JINJA_FILE_1:
        extension = "sh"
        with open(jinja_file, "r") as f:
            template = jinja2.Template(f.read())
        with open("{}/{}.{}".format(
            os.path.dirname(dirname),
            os.path.splitext(jinja_file)[0], extension), "w") as f:
            f.write(template.render(properties=properties))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="")
    
    parser.add_argument(
        "--namespace",
        default="llan")
    parser.add_argument(
        "--name",
        default="train")
    parser.add_argument(
        "--tf_image",
        default="tensorflow/tf-cluster-train:1.0",
        required=False)   # TODO: the field "required" should be "True"
    parser.add_argument(
        "--ps_replicas",
        default=1,
        type=int)
    parser.add_argument(
        "--worker_replicas",
        default=2,
        type=int)
    parser.add_argument(
        "--parameters",
        default='[]')
    parser.add_argument(
        "--dist_port",
        default="2222")
    parser.add_argument(
        "--tensorboard_port",
        default="6006")
    parser.add_argument(
        "--nvidia_driver_version",
        default="375.26")
    parser.add_argument(
        "--nfs_image",
        default="gcr.io/google-samples/nfs-server:1.2")
        
    args = parser.parse_args()
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main(args)
