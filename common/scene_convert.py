def get_child_scene_position(main_scene_position: tuple,
                             child_scene_rect: tuple) -> tuple:
    return (
        main_scene_position[0] - child_scene_rect[0],
        main_scene_position[1] - child_scene_rect[1] 
    )