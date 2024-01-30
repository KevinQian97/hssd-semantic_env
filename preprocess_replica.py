import os
import sys
import json
import time
import numpy as np

sys.path.append(".")
from scannet_util import g_label_names, g_raw2scannet
from lib.pc_util import read_ply_xyzrgbnormal
from lib.utils import get_eta
from lib.config import CONF
import trimesh
NUM_MAX_PTS = 100000

replica_folder = "/datasets01/replica/061819/18_scenes"
preprocess_folder = "./replica_scenes"
if not os.path.exists(preprocess_folder):
    os.makedirs(preprocess_folder)
RGB_LST = CONF.PALETTE
ORG_CLS = CONF.NYUCLASSES
REPLACE  = CONF.REPLICA_MAP 

def map_id_label(ann):
    map = {}
    objects = ann["objects"]
    for object in objects:
        object_id = object["id"]
        class_name = object["class_name"]
        class_id = object["class_id"]
        if class_name in REPLACE:
            class_name = REPLACE[class_name]
        if class_name in ORG_CLS:
            class_id = ORG_CLS.index(class_name)+1
            proj_rgb = RGB_LST[class_id-1]
            map[object_id] = {"class_id":class_id,"RGB":proj_rgb}
        else:
            continue
    return map

scenes = os.listdir(replica_folder)
for scene in scenes:
    mesh_file = os.path.join(replica_folder,scene,"habitat","mesh_semantic.ply")
    ann_file = os.path.join(replica_folder,scene,"habitat","info_semantic.json")
    ann = json.load(open(ann_file))
    map = map_id_label(ann)
    mesh = trimesh.load(mesh_file)
    num_vertices = len(mesh.metadata['_ply_raw']['vertex']['data'])
    num_faces = len(mesh.metadata['_ply_raw']['face']['data'])
    face_objectid_map = {}
    for face_id in range(num_faces):
        face = mesh.metadata['_ply_raw']['face']['data'][face_id]
        vertex_ids = face[0][1]
        for vertex_id in vertex_ids:
            face_objectid_map[vertex_id] = face[1]
    res = []
    for vertex_id in range(num_vertices):
        vertex = list(mesh.metadata['_ply_raw']['vertex']['data'][vertex_id])
        xyz = vertex[:3]
        nxnynz = vertex[3:6]
        obj_id = face_objectid_map[vertex_id]
        if obj_id not in map:
            continue
        rgb = map[obj_id]["RGB"]
        class_id = map[obj_id]["class_id"]
        seq = np.concatenate([xyz,rgb,nxnynz,[obj_id],[class_id]])
        res.append(seq)
    data = np.stack(res,0)
    
    if data.shape[0] > NUM_MAX_PTS:
        choices = np.random.choice(data.shape[0], NUM_MAX_PTS, replace=False)
        data = data[choices]
    out_filename = os.path.join(preprocess_folder,scene+".npy")
    np.save(out_filename, data)
        
    

