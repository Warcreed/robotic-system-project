from modules.utils.pose import Pose
from modules.world.block import BlockSlot
from modules.world.obstacle import Obstacle

class Config:

    # main_gui.py

    ## Manipulator
    print_end_effector_ray = False

    ## telemetry
    show_telemetry = False
    print_telemetry_base_joint= True
    print_telemetry_second_joint= False
    print_telemetry_end_eff_joint= False
    seconds_after_show_telemetry = 7

    ## obstacles
    print_block_slots = True
    print_scaled_obstacle = False
    
    ## NF1
    nf1_map_resolution = 30
    print_nf1_map = False
    print_nf1_obstacle = False
    print_nf1_map_values = False
    print_nf1_coord = False
    print_nf1_path = True

    # End Effector pose related to BlockSlot
    end_eff_block_poses = [
        Pose(0.09, 0.0676, 0),
        Pose(0.235, 0.032, -90),
        Pose(0.275, 0.032, -90),
        Pose(0.265, 0.11, 0),
        Pose(0.260, 0.19, 0),
        Pose(0.275, 0.215, 100),
        Pose(0.175, 0.295, 0),
        Pose(0.155, 0.3, 70),
        Pose(0.11, 0.276, 65),
        Pose(0.09, 0.27, 130),            
    ]

    # world.py
    FLOOR_LEVEL = -0.020

    # length factor related to end effector length
    ray_length_factor = 2.2
    
    # obstacle position on world map 
    obstacles = [ 
        Obstacle(x = 220, y = 365, type = 0),
        Obstacle(x = 420, y = 350, type = 1),
        Obstacle(x = 430, y = 210, type = 2),
        Obstacle(x = 309, y = 165, type = 3),
        Obstacle(x = 218, y = 64, type = 4),
        Obstacle(x = 100, y = 110, type = 5)
    ]

    # BlockSlot on wold map
    block_slots = [
        BlockSlot(x = 0.12, y = 0.065, a = 0),       
        BlockSlot(x = 0.22, y = FLOOR_LEVEL, a = 0),
        BlockSlot(x = 0.26, y = FLOOR_LEVEL, a = 0),
        BlockSlot(x = 0.3, y = 0.1, a = 0),       
        BlockSlot(x = 0.285, y = 0.18, a = 90),       
        BlockSlot(x = 0.25, y = 0.25, a = 101),       
        BlockSlot(x = 0.205, y = 0.285, a = 0),       
        BlockSlot(x = 0.152, y = 0.332, a = -110),       
        BlockSlot(x = 0.11, y = 0.305, a = -24),       
        BlockSlot(x = 0.045, y = 0.292, a = -50),       
    ]

    # Trajectory

    use_final_decel_flag = True