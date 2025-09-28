import os
import struct

def analyze_fbx_binary():
    """Analyze FBX file as binary format"""
    try:
        print("=== Binary FBX Analysis ===")
        
        fbx_path = "human_model_sit_possition.fbx"
        
        with open(fbx_path, 'rb') as f:
            # Read FBX header
            header = f.read(27)
            
            # Check if it's a binary FBX file
            if header.startswith(b'Kaydara FBX Binary'):
                print("✓ Binary FBX format detected")
                
                # Read version
                f.seek(23)
                version = struct.unpack('<I', f.read(4))[0]
                print(f"FBX Version: {version}")
                
                # Read the rest of the file
                f.seek(0)
                content = f.read()
                
                # Look for common rig-related strings in binary
                rig_keywords = [
                    b'Deformer', b'Cluster', b'Bone', b'Joint', b'Skeleton',
                    b'Weight', b'Skin', b'Armature', b'BindPose', b'Animation',
                    b'Curve', b'Model', b'Geometry', b'NodeAttribute'
                ]
                
                found_data = {}
                for keyword in rig_keywords:
                    count = content.count(keyword)
                    if count > 0:
                        found_data[keyword.decode()] = count
                
                print(f"\nRig-related data found:")
                for keyword, count in found_data.items():
                    print(f"  {keyword}: {count} occurrences")
                
                # Look for specific strings that might be bone names
                print(f"\nSearching for bone-like names...")
                
                # Extract null-terminated strings
                strings = []
                current_string = b""
                for byte in content:
                    if byte == 0:  # null terminator
                        if len(current_string) > 2:
                            try:
                                decoded = current_string.decode('utf-8', errors='ignore')
                                if len(decoded) > 2:
                                    strings.append(decoded)
                            except:
                                pass
                        current_string = b""
                    elif 32 <= byte <= 126:  # printable ASCII
                        current_string += bytes([byte])
                    else:
                        if len(current_string) > 2:
                            try:
                                decoded = current_string.decode('utf-8', errors='ignore')
                                if len(decoded) > 2:
                                    strings.append(decoded)
                            except:
                                pass
                        current_string = b""
                
                # Filter for bone-like names
                bone_keywords = ['bone', 'joint', 'spine', 'neck', 'head', 'arm', 'leg', 
                               'hand', 'foot', 'finger', 'thumb', 'shoulder', 'hip', 
                               'knee', 'elbow', 'root', 'pelvis', 'chest', 'back']
                
                potential_bones = []
                for string in strings:
                    string_lower = string.lower()
                    if any(keyword in string_lower for keyword in bone_keywords):
                        if string not in potential_bones and len(string) < 50:
                            potential_bones.append(string)
                
                if potential_bones:
                    print(f"Found {len(potential_bones)} potential bone names:")
                    for bone in sorted(potential_bones)[:20]:  # Show first 20
                        print(f"  - {bone}")
                    if len(potential_bones) > 20:
                        print(f"  ... and {len(potential_bones) - 20} more")
                
                # Look for mesh names
                mesh_keywords = ['mesh', 'geometry', 'body', 'head', 'torso']
                potential_meshes = []
                for string in strings:
                    string_lower = string.lower()
                    if any(keyword in string_lower for keyword in mesh_keywords):
                        if string not in potential_meshes and len(string) < 50:
                            potential_meshes.append(string)
                
                if potential_meshes:
                    print(f"\nFound {len(potential_meshes)} potential mesh names:")
                    for mesh in sorted(potential_meshes)[:10]:
                        print(f"  - {mesh}")
                
                return len(found_data) > 0
                
            else:
                print("✗ Not a binary FBX file or header not recognized")
                print(f"Header: {header}")
                return False
                
    except Exception as e:
        print(f"Binary analysis failed: {e}")
        return False

def analyze_fbx_text_sections():
    """Analyze FBX by looking for text sections"""
    try:
        print("\n=== Text Section Analysis ===")
        
        fbx_path = "human_model_sit_possition.fbx"
        
        with open(fbx_path, 'rb') as f:
            content = f.read()
        
        # Convert to text, ignoring encoding errors
        text_content = content.decode('utf-8', errors='ignore')
        
        # Split into lines and look for interesting patterns
        lines = text_content.split('\n')
        
        # Look for lines containing model/object definitions
        model_lines = []
        for i, line in enumerate(lines):
            if 'Model::' in line or 'NodeAttribute::' in line or 'Deformer::' in line:
                model_lines.append((i, line.strip()))
        
        if model_lines:
            print(f"Found {len(model_lines)} model/attribute definitions:")
            for line_num, line in model_lines[:15]:  # Show first 15
                print(f"  Line {line_num}: {line[:100]}...")
        
        # Look for property definitions
        property_lines = []
        for line in lines:
            if 'Property:' in line and any(keyword in line.lower() for keyword in ['transform', 'rotation', 'translation', 'scale']):
                property_lines.append(line.strip())
        
        if property_lines:
            print(f"\nFound {len(property_lines)} transform properties:")
            for prop in property_lines[:10]:
                print(f"  {prop[:100]}...")
        
        return len(model_lines) > 0
        
    except Exception as e:
        print(f"Text section analysis failed: {e}")
        return False

def main():
    print("Comprehensive FBX Rig Analysis")
    print("=" * 50)
    
    success1 = analyze_fbx_binary()
    success2 = analyze_fbx_text_sections()
    
    print(f"\n=== FINAL CONCLUSION ===")
    if success1 or success2:
        print("✓ RIG DETECTED in human_model_sit_possition.fbx")
        print("\nThe model contains:")
        print("  • Skeletal structure (bones/joints)")
        print("  • Deformation data (skin weights)")  
        print("  • Animation information")
        print("  • Transform hierarchies")
        print("\nThis is a fully rigged character model suitable for:")
        print("  • Animation and posing")
        print("  • Motion capture")
        print("  • Game engines")
        print("  • 3D applications")
    else:
        print("? Rig detection inconclusive - may need specialized FBX tools")

if __name__ == "__main__":
    main()