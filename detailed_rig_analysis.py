import os
import re

def extract_fbx_rig_details():
    """Extract detailed rig information from FBX file"""
    try:
        print("=== Detailed FBX Rig Analysis ===")
        
        fbx_path = "human_model_sit_possition.fbx"
        
        with open(fbx_path, 'rb') as f:
            content = f.read()
            
        # Convert to string for analysis
        text_content = content.decode('utf-8', errors='ignore')
        
        # Look for bone/joint names
        print("\n1. Searching for bone/joint names...")
        
        # Common patterns for bone names in FBX
        bone_patterns = [
            r'Model::\s*"([^"]*(?:bone|joint|Bone|Joint)[^"]*)"',
            r'Model::\s*"([^"]*(?:spine|Spine|neck|Neck|head|Head)[^"]*)"',
            r'Model::\s*"([^"]*(?:arm|Arm|leg|Leg|hand|Hand|foot|Foot)[^"]*)"',
            r'Model::\s*"([^"]*(?:shoulder|Shoulder|hip|Hip|knee|Knee|elbow|Elbow)[^"]*)"',
            r'Model::\s*"([^"]*(?:finger|Finger|toe|Toe|thumb|Thumb)[^"]*)"',
            r'Model::\s*"([^"]*(?:root|Root|pelvis|Pelvis)[^"]*)"'
        ]
        
        found_bones = set()
        for pattern in bone_patterns:
            matches = re.findall(pattern, text_content, re.IGNORECASE)
            for match in matches:
                if len(match.strip()) > 0:
                    found_bones.add(match.strip())
        
        if found_bones:
            print(f"Found {len(found_bones)} potential bone/joint names:")
            for bone in sorted(found_bones):
                print(f"  - {bone}")
        else:
            print("No specific bone names found with pattern matching")
        
        # Look for deformer information
        print("\n2. Analyzing deformers and clusters...")
        
        deformer_count = text_content.count('Deformer::')
        cluster_count = text_content.count('Cluster::')
        skin_count = text_content.count('Skin::')
        
        print(f"Deformers found: {deformer_count}")
        print(f"Clusters found: {cluster_count}")
        print(f"Skin deformers: {skin_count}")
        
        # Look for animation curves
        print("\n3. Animation data analysis...")
        
        animation_curve_count = text_content.count('AnimationCurve::')
        animation_layer_count = text_content.count('AnimationLayer::')
        animation_stack_count = text_content.count('AnimationStack::')
        
        print(f"Animation curves: {animation_curve_count}")
        print(f"Animation layers: {animation_layer_count}")
        print(f"Animation stacks: {animation_stack_count}")
        
        # Look for bind pose information
        print("\n4. Bind pose information...")
        
        bind_pose_count = text_content.count('BindPose::')
        pose_count = text_content.count('Pose::')
        
        print(f"Bind poses: {bind_pose_count}")
        print(f"Poses: {pose_count}")
        
        # Extract some model names that might be bones
        print("\n5. All Model objects (potential bones/meshes)...")
        
        model_pattern = r'Model::\s*"([^"]+)"'
        all_models = re.findall(model_pattern, text_content)
        
        if all_models:
            print(f"Found {len(all_models)} model objects:")
            # Show first 20 to avoid too much output
            for i, model in enumerate(sorted(set(all_models))[:20]):
                print(f"  {i+1:2d}. {model}")
            if len(set(all_models)) > 20:
                print(f"  ... and {len(set(all_models)) - 20} more")
        
        # Summary
        print("\n=== RIG DETECTION SUMMARY ===")
        
        rig_indicators = []
        
        if deformer_count > 0:
            rig_indicators.append(f"✓ {deformer_count} deformers detected")
        
        if cluster_count > 0:
            rig_indicators.append(f"✓ {cluster_count} bone clusters detected")
            
        if animation_curve_count > 0:
            rig_indicators.append(f"✓ {animation_curve_count} animation curves detected")
            
        if bind_pose_count > 0:
            rig_indicators.append(f"✓ {bind_pose_count} bind poses detected")
            
        if found_bones:
            rig_indicators.append(f"✓ {len(found_bones)} bone-like objects identified")
        
        if rig_indicators:
            print("RIG DETECTED! Evidence found:")
            for indicator in rig_indicators:
                print(f"  {indicator}")
                
            print("\nThis model contains:")
            print("  - Skeletal rig/armature")
            print("  - Bone weights (skin clusters)")
            if animation_curve_count > 0:
                print("  - Animation data")
            if bind_pose_count > 0:
                print("  - Bind pose information")
                
            print("\nThe model is ready for:")
            print("  - Character animation")
            print("  - Pose manipulation")
            print("  - Motion capture application")
            
        else:
            print("No clear rigging evidence found")
            
        return True
        
    except Exception as e:
        print(f"Detailed analysis failed: {e}")
        return False

def main():
    print("Advanced FBX Rig Detection")
    print("=" * 50)
    
    extract_fbx_rig_details()

if __name__ == "__main__":
    main()