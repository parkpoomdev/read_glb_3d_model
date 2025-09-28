import os
import sys
import numpy as np

def analyze_fbx_with_trimesh():
    """Try to analyze FBX using trimesh"""
    try:
        import trimesh
        print("=== Analyzing with Trimesh ===")
        
        # Load the FBX file
        fbx_path = "human_model_sit_possition.fbx"
        if not os.path.exists(fbx_path):
            print(f"File {fbx_path} not found!")
            return False
            
        # Load the scene
        scene = trimesh.load(fbx_path)
        
        print(f"Loaded scene type: {type(scene)}")
        
        if hasattr(scene, 'geometry'):
            print(f"Number of geometries: {len(scene.geometry)}")
            for name, geom in scene.geometry.items():
                print(f"  - Geometry '{name}': {type(geom)}")
                if hasattr(geom, 'vertices'):
                    print(f"    Vertices: {len(geom.vertices)}")
                if hasattr(geom, 'faces'):
                    print(f"    Faces: {len(geom.faces)}")
        
        # Check for animations/bones
        if hasattr(scene, 'graph'):
            print(f"Scene graph nodes: {len(scene.graph.nodes)}")
            for node in scene.graph.nodes:
                print(f"  - Node: {node}")
        
        # Check metadata
        if hasattr(scene, 'metadata'):
            print(f"Metadata: {scene.metadata}")
            
        return True
        
    except Exception as e:
        print(f"Trimesh analysis failed: {e}")
        return False

def analyze_fbx_with_open3d():
    """Try to analyze FBX using Open3D"""
    try:
        import open3d as o3d
        print("\n=== Analyzing with Open3D ===")
        
        fbx_path = "human_model_sit_possition.fbx"
        
        # Open3D doesn't directly support FBX, but let's try
        # First convert to a supported format or check if it can read it
        print("Open3D doesn't directly support FBX files.")
        print("Let's try to read the GLB version instead...")
        
        glb_path = "human_model_sit_possition.glb"
        if os.path.exists(glb_path):
            # Try to load as mesh
            mesh = o3d.io.read_triangle_mesh(glb_path)
            if len(mesh.vertices) > 0:
                print(f"GLB mesh loaded successfully:")
                print(f"  Vertices: {len(mesh.vertices)}")
                print(f"  Triangles: {len(mesh.triangles)}")
                print(f"  Has vertex colors: {mesh.has_vertex_colors()}")
                print(f"  Has vertex normals: {mesh.has_vertex_normals()}")
                
                # Check bounding box
                bbox = mesh.get_axis_aligned_bounding_box()
                print(f"  Bounding box: {bbox.get_extent()}")
                
                return True
        
        return False
        
    except Exception as e:
        print(f"Open3D analysis failed: {e}")
        return False

def analyze_fbx_manual():
    """Manual analysis of FBX file structure"""
    try:
        print("\n=== Manual FBX Analysis ===")
        
        fbx_path = "human_model_sit_possition.fbx"
        
        # Read file as binary to look for common rig-related keywords
        with open(fbx_path, 'rb') as f:
            content = f.read()
            
        # Convert to string for text searching (ignore encoding errors)
        try:
            text_content = content.decode('utf-8', errors='ignore')
        except:
            text_content = str(content)
            
        # Common rig/bone related keywords in FBX files
        rig_keywords = [
            'Deformer', 'Cluster', 'Bone', 'Joint', 'Skeleton',
            'Weight', 'Skin', 'Armature', 'BindPose', 'Animation',
            'Curve', 'KeyFrame', 'Transform', 'Matrix'
        ]
        
        found_keywords = []
        for keyword in rig_keywords:
            count = text_content.count(keyword)
            if count > 0:
                found_keywords.append(f"{keyword}: {count}")
        
        print(f"File size: {len(content)} bytes")
        print(f"Rig-related keywords found:")
        for keyword_info in found_keywords:
            print(f"  - {keyword_info}")
            
        # Look for specific FBX sections
        fbx_sections = ['Objects:', 'Connections:', 'Takes:', 'Model:', 'Geometry:']
        for section in fbx_sections:
            if section in text_content:
                print(f"  - Found FBX section: {section}")
        
        return len(found_keywords) > 0
        
    except Exception as e:
        print(f"Manual analysis failed: {e}")
        return False

def main():
    print("FBX Rig Detection Tool")
    print("=" * 50)
    
    # Check if files exist
    fbx_path = "human_model_sit_possition.fbx"
    glb_path = "human_model_sit_possition.glb"
    
    print(f"FBX file exists: {os.path.exists(fbx_path)}")
    print(f"GLB file exists: {os.path.exists(glb_path)}")
    
    if not os.path.exists(fbx_path):
        print("FBX file not found!")
        return
    
    # Try different analysis methods
    methods_tried = 0
    methods_successful = 0
    
    # Method 1: Trimesh
    if analyze_fbx_with_trimesh():
        methods_successful += 1
    methods_tried += 1
    
    # Method 2: Open3D
    if analyze_fbx_with_open3d():
        methods_successful += 1
    methods_tried += 1
    
    # Method 3: Manual analysis
    if analyze_fbx_manual():
        methods_successful += 1
    methods_tried += 1
    
    print(f"\n=== Summary ===")
    print(f"Analysis methods tried: {methods_tried}")
    print(f"Successful analyses: {methods_successful}")
    
    if methods_successful > 0:
        print("\nThe model appears to contain rigging/animation data!")
    else:
        print("\nNo clear rigging data detected with current methods.")

if __name__ == "__main__":
    main()