import os
import json
import struct

def analyze_glb_file():
    """Analyze GLB file for rig information"""
    try:
        print("=== GLB File Analysis ===")
        
        glb_path = "human_model_sit_possition.glb"
        
        if not os.path.exists(glb_path):
            print("GLB file not found!")
            return False
            
        with open(glb_path, 'rb') as f:
            # Read GLB header
            magic = f.read(4)
            if magic != b'glTF':
                print("Not a valid GLB file")
                return False
                
            version = struct.unpack('<I', f.read(4))[0]
            length = struct.unpack('<I', f.read(4))[0]
            
            print(f"✓ Valid GLB file")
            print(f"Version: {version}")
            print(f"Total size: {length} bytes")
            
            # Read JSON chunk
            chunk_length = struct.unpack('<I', f.read(4))[0]
            chunk_type = f.read(4)
            
            if chunk_type == b'JSON':
                json_data = f.read(chunk_length).decode('utf-8')
                
                try:
                    gltf_data = json.loads(json_data)
                    
                    print(f"\n=== GLTF Structure Analysis ===")
                    
                    # Check for nodes (bones/joints)
                    if 'nodes' in gltf_data:
                        nodes = gltf_data['nodes']
                        print(f"Nodes found: {len(nodes)}")
                        
                        bone_nodes = []
                        for i, node in enumerate(nodes):
                            if 'name' in node:
                                node_name = node['name']
                                # Check if this looks like a bone
                                bone_keywords = ['bone', 'joint', 'spine', 'neck', 'head', 'arm', 'leg', 
                                               'hand', 'foot', 'finger', 'thumb', 'shoulder', 'hip', 
                                               'knee', 'elbow', 'root', 'pelvis', 'chest']
                                
                                if any(keyword.lower() in node_name.lower() for keyword in bone_keywords):
                                    bone_nodes.append((i, node_name))
                                    
                        if bone_nodes:
                            print(f"Found {len(bone_nodes)} bone-like nodes:")
                            for idx, name in bone_nodes:
                                print(f"  Node {idx}: {name}")
                    
                    # Check for skins (rigging data)
                    if 'skins' in gltf_data:
                        skins = gltf_data['skins']
                        print(f"\n✓ Skins found: {len(skins)}")
                        
                        for i, skin in enumerate(skins):
                            print(f"  Skin {i}:")
                            if 'name' in skin:
                                print(f"    Name: {skin['name']}")
                            if 'joints' in skin:
                                print(f"    Joints: {len(skin['joints'])}")
                            if 'inverseBindMatrices' in skin:
                                print(f"    Has inverse bind matrices: Yes")
                    
                    # Check for animations
                    if 'animations' in gltf_data:
                        animations = gltf_data['animations']
                        print(f"\n✓ Animations found: {len(animations)}")
                        
                        for i, anim in enumerate(animations):
                            print(f"  Animation {i}:")
                            if 'name' in anim:
                                print(f"    Name: {anim['name']}")
                            if 'channels' in anim:
                                print(f"    Channels: {len(anim['channels'])}")
                            if 'samplers' in anim:
                                print(f"    Samplers: {len(anim['samplers'])}")
                    
                    # Check for meshes
                    if 'meshes' in gltf_data:
                        meshes = gltf_data['meshes']
                        print(f"\nMeshes found: {len(meshes)}")
                        
                        for i, mesh in enumerate(meshes):
                            if 'name' in mesh:
                                print(f"  Mesh {i}: {mesh['name']}")
                            
                            # Check primitives for skinning attributes
                            if 'primitives' in mesh:
                                for j, primitive in enumerate(mesh['primitives']):
                                    if 'attributes' in primitive:
                                        attrs = primitive['attributes']
                                        has_weights = any('WEIGHTS' in key for key in attrs.keys())
                                        has_joints = any('JOINTS' in key for key in attrs.keys())
                                        
                                        if has_weights or has_joints:
                                            print(f"    Primitive {j}: Has skinning data (WEIGHTS: {has_weights}, JOINTS: {has_joints})")
                    
                    # Summary
                    has_rig = False
                    rig_features = []
                    
                    if 'skins' in gltf_data and len(gltf_data['skins']) > 0:
                        has_rig = True
                        rig_features.append(f"{len(gltf_data['skins'])} skin(s)")
                    
                    if bone_nodes:
                        has_rig = True
                        rig_features.append(f"{len(bone_nodes)} bone node(s)")
                    
                    if 'animations' in gltf_data and len(gltf_data['animations']) > 0:
                        rig_features.append(f"{len(gltf_data['animations'])} animation(s)")
                    
                    print(f"\n=== GLB RIG SUMMARY ===")
                    if has_rig:
                        print(f"✓ RIG DETECTED in GLB file!")
                        print(f"Features: {', '.join(rig_features)}")
                    else:
                        print("✗ No clear rigging data found in GLB")
                    
                    return has_rig
                    
                except json.JSONDecodeError as e:
                    print(f"Failed to parse JSON: {e}")
                    return False
            else:
                print("GLB format not as expected")
                return False
                
    except Exception as e:
        print(f"GLB analysis failed: {e}")
        return False

def main():
    print("GLB Rig Detection Analysis")
    print("=" * 50)
    
    analyze_glb_file()

if __name__ == "__main__":
    main()