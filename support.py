from os import walk
import pygame 

def import_folder(path):
    
    surface_list = []

    for _folder_path, _subfolders_list, files_list in walk(path):
        # (path, subfolders list, files list)
        # ('graphics/character/left', [], ['2.png', '3.png', '1.png', '0.png'])
        for file in files_list:
            full_path = f"{path}/{file}"
            image_surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surface)


    return surface_list