# ===== REUSABLE MOVEMENT SYSTEM =====
# Initialize these variables before your game loop
movement_state = "approach_targets"  # or "move_to_goal", "complete"
targets = [(200, 280), (200, 180), (250, 230)]  # List of positions to visit
goal_pos = (690, 100)  # Final destination
current_pos = [WIDTH/2 + 200, HEIGHT/2 - 80]  # Starting position
speed = 2  # Movement speed in pixels/frame
held_items = []  # Items collected along the way
current_target_index = 0

# In your game loop's update section:
if movement_state == "approach_targets":
    if current_target_index < len(targets):
        target = targets[current_target_index]
        
        # Calculate direction vector
        dx = target[0] - current_pos[0]
        dy = target[1] - current_pos[1]
        distance = (dx**2 + dy**2)**0.5
        
        if distance < speed:  # Reached target
            current_pos[0], current_pos[1] = target
            held_items.append(target)  # Collect item
            current_target_index += 1
            
            if current_target_index >= len(targets):
                movement_state = "move_to_goal"  # All targets visited
        else:
            # Move toward target
            current_pos[0] += (dx/distance) * speed
            current_pos[1] += (dy/distance) * speed

elif movement_state == "move_to_goal":
    dx = goal_pos[0] - current_pos[0]
    dy = goal_pos[1] - current_pos[1]
    distance = (dx**2 + dy**2)**0.5
    
    if distance < 30:  # Reached goal
        movement_state = "complete"
        current_pos[0], current_pos[1] = goal_pos
        held_items = []  # Clear collected items
    else:
        # Move toward goal
        current_pos[0] += (dx/distance) * speed
        current_pos[1] += (dy/distance) * speed

# In your drawing section:
# 1. Draw remaining targets
for target in targets:
    if target not in held_items:
        draw_target_item(win, *target)

# 2. Draw moving character
draw_character(win, *current_pos)

# 3. Draw carried items (if applicable)
if movement_state in ["approach_targets", "move_to_goal"]:
    for i, item in enumerate(held_items):
        draw_carried_item(win, current_pos[0] - 30 + i*10, current_pos[1] - 60)

# 4. Draw final goal (if applicable)
draw_goal(win, *goal_pos)