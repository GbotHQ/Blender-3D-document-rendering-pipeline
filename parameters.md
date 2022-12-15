Scene parameters and render settings are written to a conf.json file that is read by a script that runs inside blenders embedded python interpreter.

## Parameters
- ### General
    - resolution: The output resolution
    - render_engine: Which Blender render engine to use
    - cycles_device: Either cpu or gpu
    - cycles_samples: Path tracing samples
    - cycles_denoise: Use cycles denoising
    - output_path: The directory to render to

- ### Ground
    - offset: Texture coordinates offset
    - texture_rotation: Texture rotation
    - displacement_strength: Ground displacement multiplier
    - subdivisions: Mesh resolution
    - texture_path_X: Path to a texture to use (must be absolute)

- ### Paper
    - text_image_path: Path to a document image printed on the paper
    - size: Size of the paper in cm
    - subdivisions: Mesh resolution
    - crumpling_strength: Amount of smaller paper crumpling
    - fold_messiness: Amount of fold imperfection
    - fold_smoothness: Mix between sharp folds and smooth bends
    - texture_rotation: Texture rotation
    - offset: Texture coordinates offset

- ### Folds
    - strength: Folds strength multiplier
    - angle: Angle of the folds in degrees

- ### Camera
    - focal_length: Camera focal length in mm (camera position changes to undo any zoom)
    - relative_camera_distance: Camera distance multiplier
    - depth_of_field: Enable depth of field
    - fstop: Lens f-number, changes depth of field strength (don't use real life values, the scenes scale is dynamic)
    - orbit: Spherical coordinates in degrees
    - look_at_2d: The look-at position on scene XY axes

- ### HDRI
    - hdri_image_path: Path to an HDRI image to use
    - hdri_strength: HDRI multiplier
    - hdri_image_rotation: HDRI image rotation on Z axis

- ### Lights
    - visible: Light visibility
    - distance: Distance in meters from look-at position
    - orbit: Spherical coordinates in degrees
    - look_at_2d: The look-at position on scene XY axes
    - power: Light power (intensity) in watts
    - shadow_softness_radius: Light radius for controlling shadow softness
    - color: Light color
