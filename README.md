# hssd-semantic_env

## Dataset Download
### HSSD Dataset Download
I download the HSSD dataset from [here](https://huggingface.co/datasets/hssd/hssd-hab)
```
git clone https://huggingface.co/datasets/hssd/hssd-hab.git
```

### Replica Dataset Download
You could directly find the Replica Dataset on FAIR Cluster from here: "/datasets01/replica/061819/18_scenes"
Another option is to download from [here](https://github.com/facebookresearch/Replica-Dataset)

## Example Code
### Code to Preprocess 3D Environments for Replica
"./hssd-navmesh" is the example code to generate navmesh for hssd scene.

### Code to Preprocess 3D Environments for Replica
The "./preprocess_replica.py" is the file to preprocess Replica Scenes.
The input files are:
```
# 3D Point Cloud File
# The input record vertex and face infromation in the format of 
# Vertice:[x,y,z,nx,ny,nz,r,g,b]
# Face:[vertice ids, object_id]
/datasets01/replica/061819/18_scenes/frl_apartment_0/habitat/mesh_semantic.ply
# Semantic Annotation
# It contains the object name of each object_id, which enables us to match the semantic information to each # vertice and face in mesh_semantic.ply
/datasets01/replica/061819/18_scenes/frl_apartment_0/habitat/info_semantic.json
```

The example output file is "./frl_apartment_0.npy". The output is a ".npy" file which record semantic information through RGB values of each vertice.

