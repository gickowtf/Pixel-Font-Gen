import pygame
import numpy as np

characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,!?-:"

num_rows = 10
num_columns = 10
default_rows = 10
default_columns = 10
active_slider = None

github_icon_original = pygame.image.load('github_icon.png')
icon_size = (40, 40)
github_icon = pygame.transform.scale(github_icon_original, icon_size)

cell_size = 40
border_size = 2
character_area_size = (num_columns * cell_size, num_rows * cell_size)

window_width = 800
window_height = 800
window_size = (window_width, window_height)

pygame.init()
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Pixel Font Gen")
rows_slider = pygame.Rect(20, character_area_size[1] + 50, 100, 10)
cols_slider = pygame.Rect(20, character_area_size[1] + 70, 100, 10)
slider_handle_width = 10
rows_slider_value = num_rows
cols_slider_value = num_columns

running = True
character_matrices = {char: {"matrix": np.zeros((num_rows, num_columns), dtype=int),
                             "rows": num_rows, "cols": num_columns} for char in characters}

selected_character = 'A'


def resize_matrix(matrix, rows, cols):
    resized = np.zeros((rows, cols), dtype=int)
    for i in range(min(matrix.shape[0], rows)):
        for j in range(min(matrix.shape[1], cols)):
            resized[i][j] = matrix[i][j]
    return resized


def save_to_file():
    with open("characters_data.txt", "w") as f:
        for char, data in character_matrices.items():
            matrix_data = data["matrix"].flatten()
            matrix_str = ','.join(map(str, matrix_data))
            f.write(f"{char};{matrix_str};{data['rows']};{data['cols']}\n")


def load_from_file():
    try:
        with open("characters_data.txt", "r") as f:
            for line_num, line in enumerate(f, 1):
                parts = line.strip().split(';')
                if len(parts) != 4:
                    print(f"Ungültige Zeile {line_num}: {line.strip()}")
                    continue
                char, matrix_str, rows, cols = parts
                matrix_data = list(map(int, matrix_str.split(',')))
                matrix = np.array(matrix_data).reshape((int(rows), int(cols)))
                character_matrices[char] = {"matrix": matrix, "rows": int(rows), "cols": int(cols)}
    except FileNotFoundError:
        pass


load_from_file()
rows_slider_value = character_matrices[selected_character]["rows"]
cols_slider_value = character_matrices[selected_character]["cols"]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if github_icon_rect.collidepoint(mouse_x, mouse_y):
                import webbrowser
                webbrowser.open("https://github.com/gickowtf")
            if 0 <= mouse_x < character_area_size[0] and 0 <= mouse_y < character_area_size[1]:
                col = mouse_x // cell_size
                row = mouse_y // cell_size
                character_matrices[selected_character]["matrix"][row][col] = 1 - character_matrices[selected_character]["matrix"][row][col]
            elif character_area_size[0] + 10 + offset_x <= mouse_x < character_area_size[0] + 10 + columns * spacing_x + offset_x:
                column_clicked = (mouse_x - (character_area_size[0] + 10 + offset_x)) // spacing_x
                row_clicked = (mouse_y - 40) // spacing_y
                index_clicked = column_clicked * chars_per_column + row_clicked
                if 0 <= index_clicked < len(characters):
                    selected_character = characters[index_clicked]
                    rows_slider_value = character_matrices[selected_character]["rows"]
                    cols_slider_value = character_matrices[selected_character]["cols"]
            elif save_button.collidepoint(mouse_x, mouse_y):
                save_to_file()
                print(f"Data for all characters saved to characters_data.txt")
            elif rows_slider.collidepoint(mouse_x, mouse_y):
                active_slider = "rows"
                rows_slider_value = int((mouse_x - rows_slider.x) * default_rows / rows_slider.width)
            elif cols_slider.collidepoint(mouse_x, mouse_y):
                active_slider = "cols"
                cols_slider_value = int((mouse_x - cols_slider.x) * default_columns / cols_slider.width)
                current_matrix = character_matrices[selected_character]["matrix"]
                new_matrix = np.zeros((rows_slider_value, cols_slider_value), dtype=int)
                min_rows = min(rows_slider_value, current_matrix.shape[0])
                min_cols = min(cols_slider_value, current_matrix.shape[1])
                new_matrix[:min_rows, :min_cols] = current_matrix[:min_rows, :min_cols]
                character_matrices[selected_character]["matrix"] = new_matrix
        elif event.type == pygame.MOUSEBUTTONUP:
            if active_slider:
                old_matrix = character_matrices[selected_character]["matrix"]
                new_matrix = resize_matrix(old_matrix, rows_slider_value, cols_slider_value)
                character_matrices[selected_character]["matrix"] = new_matrix
                character_matrices[selected_character]["rows"] = rows_slider_value
                character_matrices[selected_character]["cols"] = cols_slider_value
                active_slider = None
        elif event.type == pygame.MOUSEMOTION and active_slider:
            mouse_x, _ = pygame.mouse.get_pos()
            if active_slider == "rows":
                rows_slider_value = int((mouse_x - rows_slider.x) * default_rows / rows_slider.width)
                rows_slider_value = max(1, min(rows_slider_value,
                                               default_rows))
            elif active_slider == "cols":
                cols_slider_value = int((mouse_x - cols_slider.x) * default_columns / cols_slider.width)
                cols_slider_value = max(1, min(cols_slider_value,
                                               default_columns))


    screen.fill((255, 255, 255))


    offset_x = 0
    offset_y = 0

    current_matrix = character_matrices[selected_character]["matrix"]
    for row in range(current_matrix.shape[0]):
        for col in range(current_matrix.shape[1]):
            rect = pygame.Rect(col * cell_size + offset_x, row * cell_size + offset_y, cell_size, cell_size)
            pygame.draw.rect(screen, (0, 0, 0), rect, border_size)
            if current_matrix[row][col] == 1:
                pygame.draw.rect(screen, (0, 0, 0), rect.inflate(-border_size, -border_size))

    font = pygame.font.Font(None, 30)
    columns = 4
    chars_per_column = len(characters) // columns
    spacing_y = 30
    spacing_x = 60
    offset_x = 100

    for i, char in enumerate(characters):
        column = i // chars_per_column
        row = i % chars_per_column
        if char != selected_character:
            color = (0, 0, 0)
        else:
            color = (255, 0, 0)
        text = font.render(char, True, color)
        x_pos = character_area_size[0] + 10 + column * spacing_x + offset_x
        y_pos = 40 + row * spacing_y
        screen.blit(text, (x_pos, y_pos))

    button_width = 300
    button_height = 40
    button_x = (window_width - button_width) // 2
    button_y = window_height - 100
    slider_width = 300
    rows_slider = pygame.Rect((window_width - slider_width) // 5, button_y - 70, slider_width, 10)
    cols_slider = pygame.Rect((window_width - slider_width) // 5, button_y - 50, slider_width, 10)

    pygame.draw.rect(screen, (150, 150, 150), rows_slider)
    pygame.draw.rect(screen, (0, 0, 255), (
    rows_slider.x + rows_slider_value * rows_slider.width / default_rows - slider_handle_width / 2, rows_slider.y - 5,
    slider_handle_width, 20))

    pygame.draw.rect(screen, (150, 150, 150), cols_slider)
    pygame.draw.rect(screen, (0, 0, 255), (
    cols_slider.x + cols_slider_value * cols_slider.width / default_columns - slider_handle_width / 2,
    cols_slider.y - 5, slider_handle_width, 20))

    save_button = pygame.draw.rect(screen, (0, 255, 0), (button_x, button_y, button_width, button_height))
    save_button_text = font.render(f"Save as character_data.txt", True, (0, 0, 0))
    text_width, text_height = font.size(f"Save as character_data.txt")
    screen.blit(save_button_text,
                (button_x + (button_width - text_width) // 2, button_y + (button_height - text_height) // 2))
    github_icon_y = button_y + button_height + 10
    github_icon_x = (window_width - github_icon.get_width()) // 2
    github_icon_rect = screen.blit(github_icon, (github_icon_x, github_icon_y))

    pygame.display.flip()


pygame.quit()

