![Smart-Bones for Blender, subtitle: Action Constraints Made Easy](assets/smart-bones-banner.png)

Smart Bones is an add-on for Blender that automates the process of adding action constraints to keyed bones within a selected action.

## Included Files
__Python script / addon :__ [blender-smart-bones.py](/blender-smart-bones.py)
__Character demonstration 01:__ [01-character-blue.blend](/assets/01-character-blue.blend)
__Character demonstration 02:__ [02-character-orange.blend](/assets/02-character-orange.blend)

## Installation
1. Download the SmartBones.py file from the [Github repository](https://github.com/sketchy-squirrel/smart-bones).
2. Open Blender and go to __'Edit > Preferences > Add-ons'__.
3. Click on __'Install...'__ and select the downloaded [blender-smart-bones.py](/blender-smart-bones.py) file.
4. Make sure that the checkmark next to the add-on is enabled.
5. Click on __'Save Preferences'__.

## Usage
1. Select the armature you want to add constraints to.
2. In the __'3D View'__, go to the __'Smart Bones'__ tab.
3. In the __'Smart Bone panel'__, select the __'target armature'__, __'control bone'__, and the __'transform channel'__ for the constraint.
4. Choose the __'transform space'__ from the drop-down list.
5. If you select __'CUSTOM'__ in the space option, specify the name of the object you want to take local space from. And if this object is an armature, then choose the __'custom subtarget'__.
6. Set the __'minimum'__ and __'maximum'__ values for the transform range.
7. Specify the name of the affected action, as well as the start and end frames for the action.
8. Click on the __'Add Smart Bone'__ button to add the action constraint to all bones in the action.

## Properties
* Target: the name of the control armature.
* Control: the name of the control bone.
* Channel: the control axis.
* Space: the transform space, either __'WORLD, CUSTOM,__ or __LOCAL'__.
* Space Object (__'CUSTOM'__ space only): takes local space from another object, to apply to constraint.
* Space Subtarget (Only if __'Space Object'__ is an armature): custom space bone.
* Min Transform Range: the minimum transform value, corresponding to __'Min Frame'__ of the selected action.
* Max Transform Range: the maximum transform value, corresponding to __'Max Frame'__ of the selected action.
* Action: the name of the affected action.
* Min Frame: the start frame of the action.
* Max Frame: the end frame of the action.

## Operators
* __Add Smart Bone__: adds action constraints to all bones in the selected action.
* __Delete Smart Bone__: deletes action constraints with matching action name and control target.

## Compatibility
The add-on is compatible with Blender 2.80 and newer versions.

## Credits
[Sketchy Squirrel](https://sketchysquirrel.com) - Joel Graham
