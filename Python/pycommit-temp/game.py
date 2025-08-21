# Import modules
import random
import sys
import pygame
from pygame.locals import *
import cv2
import mediapipe as mp
import numpy as np

# MediaPipe setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

# Camera setup
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

# All the Game Variables
window_width = 600
window_height = 499

# set height and width of window
window = pygame.display.set_mode((window_width, window_height))
elevation = window_height * 0.8
game_images = {}
framepersecond = 32
pipeimage = 'images/pipe.png'
background_image = 'images/background.jpg'
birdplayer_image = 'images/bird.png'
sealevel_image = 'images/base.jfif'

# Camera display settings
camera_width = 160
camera_height = 120
camera_x = window_width - camera_width - 10
camera_y = window_height - camera_height - 10


def detect_hand_gesture():
    """
    Detects hand gestures using MediaPipe and returns gesture information.
    Returns:
        dict: Contains 'flap' (bool), 'frame' (processed camera frame), 'landmarks' (hand landmarks)
    """
    ret, frame = cap.read()
    if not ret:
        return {'flap': False, 'frame': None, 'landmarks': None}
    
    # Flip frame horizontally for mirror effect
    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process frame with MediaPipe
    results = hands.process(frame_rgb)
    
    flap_detected = False
    landmarks = None
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            landmarks = hand_landmarks
            
            # Draw hand landmarks
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
            )
            
            # Get landmark positions
            landmark_points = []
            for landmark in hand_landmarks.landmark:
                x = int(landmark.x * frame.shape[1])
                y = int(landmark.y * frame.shape[0])
                landmark_points.append([x, y])
            
            # Gesture detection: Check if index finger is extended upward
            # Compare index finger tip (8) with index finger MCP (5)
            if len(landmark_points) > 8:
                index_tip = landmark_points[20]
                index_mcp = landmark_points[17]
                middle_tip = landmark_points[12]
                middle_mcp = landmark_points[9]
                
                # Check if index finger is pointing up and middle finger is down (pointing gesture)
                index_up = index_tip[1] < index_mcp[1] - 20
                middle_down = middle_tip[1] > middle_mcp[1] + 10
                
                if index_up and middle_down:
                    flap_detected = True
                    cv2.putText(frame, "FLAP!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    # Resize frame for display
    frame_resized = cv2.resize(frame, (camera_width, camera_height))
    
    return {
        'flap': flap_detected,
        'frame': frame_resized,
        'landmarks': landmarks
    }


def pygame_surface_from_cv2(cv_image):
    """Convert OpenCV image to Pygame surface"""
    cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
    cv_image = np.rot90(cv_image)
    cv_image = np.flipud(cv_image)
    return pygame.surfarray.make_surface(cv_image)


def flappygame():
    your_score = 0
    horizontal = int(window_width/5)
    vertical = int(window_width/2)
    ground = 0
    mytempheight = 100

    # Generating two pipes for blitting on window
    first_pipe = createPipe()
    second_pipe = createPipe()

    # List containing lower pipes
    down_pipes = [
        {'x': window_width+300-mytempheight,
         'y': first_pipe[1]['y']},
        {'x': window_width+300-mytempheight+(window_width/2),
         'y': second_pipe[1]['y']},
    ]

    # List Containing upper pipes
    up_pipes = [
        {'x': window_width+300-mytempheight,
         'y': first_pipe[0]['y']},
        {'x': window_width+200-mytempheight+(window_width/2),
         'y': second_pipe[0]['y']},
    ]

    # pipe velocity along x
    pipeVelX = -4

    # bird velocity
    bird_velocity_y = -9
    bird_Max_Vel_Y = 10
    bird_Min_Vel_Y = -8
    birdAccY = 1

    bird_flap_velocity = -8
    bird_flapped = False
    
    while True:
        # Get hand gesture detection
        gesture_data = detect_hand_gesture()
        
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                cap.release()
                cv2.destroyAllWindows()
                sys.exit()
            # Keep keyboard controls as backup
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if vertical > 0:
                    bird_velocity_y = bird_flap_velocity
                    bird_flapped = True

        # Hand gesture control
        if gesture_data['flap'] and vertical > 0:
            bird_velocity_y = bird_flap_velocity
            bird_flapped = True

        # This function will return true
        # if the flappybird is crashed
        game_over = isGameOver(horizontal,
                               vertical,
                               up_pipes,
                               down_pipes)
        if game_over:
            return

        # check for your_score
        playerMidPos = horizontal + game_images['flappybird'].get_width()/2
        for pipe in up_pipes:
            pipeMidPos = pipe['x'] + game_images['pipeimage'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                your_score += 1
                print(f"Your score is {your_score}")

        if bird_velocity_y < bird_Max_Vel_Y and not bird_flapped:
            bird_velocity_y += birdAccY

        if bird_flapped:
            bird_flapped = False
        playerHeight = game_images['flappybird'].get_height()
        vertical = vertical + \
            min(bird_velocity_y, elevation - vertical - playerHeight)

        # move pipes to the left
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Add a new pipe when the first is
        # about to cross the leftmost part of the screen
        if 0 < up_pipes[0]['x'] < 5:
            newpipe = createPipe()
            up_pipes.append(newpipe[0])
            down_pipes.append(newpipe[1])

        # if the pipe is out of the screen, remove it
        if up_pipes[0]['x'] < -game_images['pipeimage'][0].get_width():
            up_pipes.pop(0)
            down_pipes.pop(0)

        # Lets blit our game images now
        window.blit(game_images['background'], (0, 0))
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
            window.blit(game_images['pipeimage'][0],
                        (upperPipe['x'], upperPipe['y']))
            window.blit(game_images['pipeimage'][1],
                        (lowerPipe['x'], lowerPipe['y']))

        window.blit(game_images['sea_level'], (ground, elevation))
        window.blit(game_images['flappybird'], (horizontal, vertical))

        # Display camera feed with hand tracking
        if gesture_data['frame'] is not None:
            camera_surface = pygame_surface_from_cv2(gesture_data['frame'])
            # Draw border around camera feed
            pygame.draw.rect(window, (255, 255, 255), 
                           (camera_x - 2, camera_y - 2, camera_width + 4, camera_height + 4), 2)
            window.blit(camera_surface, (camera_x, camera_y))

        # Fetching the digits of score.
        numbers = [int(x) for x in list(str(your_score))]
        width = 0

        # finding the width of score images from numbers.
        for num in numbers:
            width += game_images['scoreimages'][num].get_width()
        Xoffset = (window_width - width)/1.1

        # Blitting the images on the window.
        for num in numbers:
            window.blit(game_images['scoreimages'][num],
                        (Xoffset, window_width*0.02))
            Xoffset += game_images['scoreimages'][num].get_width()

        # Display gesture instructions
        font = pygame.font.Font(None, 24)
        instruction_text = font.render("Point index finger up to flap!", True, (255, 255, 255))
        window.blit(instruction_text, (10, 10))

        # Refreshing the game window and displaying the score.
        pygame.display.update()
        framepersecond_clock.tick(framepersecond)


def isGameOver(horizontal, vertical, up_pipes, down_pipes):
    if vertical > elevation - 25 or vertical < 0:
        return True

    for pipe in up_pipes:
        pipeHeight = game_images['pipeimage'][0].get_height()
        if(vertical < pipeHeight + pipe['y'] and\
           abs(horizontal - pipe['x']) < game_images['pipeimage'][0].get_width()):
            return True

    for pipe in down_pipes:
        if (vertical + game_images['flappybird'].get_height() > pipe['y']) and\
        abs(horizontal - pipe['x']) < game_images['pipeimage'][0].get_width():
            return True
    return False


def createPipe():
    offset = window_height/3
    pipeHeight = game_images['pipeimage'][0].get_height()
    y2 = offset + \
        random.randrange(
            0, int(window_height - game_images['sea_level'].get_height() - 1.2 * offset))  
    pipeX = window_width + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        # upper Pipe
        {'x': pipeX, 'y': -y1},

        # lower Pipe
        {'x': pipeX, 'y': y2}
    ]
    return pipe


# program where the game starts
if __name__ == "__main__":
    # For initializing modules of pygame library
    pygame.init()
    framepersecond_clock = pygame.time.Clock()

    # Sets the title on top of game window
    pygame.display.set_caption('Flappy Bird Game - Hand Gesture Control')

    # Load all the images which we will use in the game

    # images for displaying score
    game_images['scoreimages'] = (
        pygame.image.load('images/0.png').convert_alpha(),
        pygame.image.load('images/1.png').convert_alpha(),
        pygame.image.load('images/2.png').convert_alpha(),
        pygame.image.load('images/3.png').convert_alpha(),
        pygame.image.load('images/4.png').convert_alpha(),
        pygame.image.load('images/5.png').convert_alpha(),
        pygame.image.load('images/6.png').convert_alpha(),
        pygame.image.load('images/7.png').convert_alpha(),
        pygame.image.load('images/8.png').convert_alpha(),
        pygame.image.load('images/9.png').convert_alpha()
    )
    game_images['flappybird'] = pygame.image.load(
        birdplayer_image).convert_alpha()
    game_images['sea_level'] = pygame.image.load(
        sealevel_image).convert_alpha()
    game_images['background'] = pygame.image.load(
        background_image).convert_alpha()
    game_images['pipeimage'] = (pygame.transform.rotate(pygame.image.load(
        pipeimage).convert_alpha(), 180), pygame.image.load(
      pipeimage).convert_alpha())

    print("WELCOME TO THE FLAPPY BIRD GAME - HAND GESTURE CONTROL")
    print("Point your index finger up to flap!")
    print("Press space/up arrow as backup control")
    print("Press space or enter to start the game")

    # Here starts the main game
    while True:
        # Get hand gesture for menu as well
        gesture_data = detect_hand_gesture()
        
        # sets the coordinates of flappy bird
        horizontal = int(window_width/5)
        vertical = int(
            (window_height - game_images['flappybird'].get_height())/2)
        ground = 0
        
        while True:
            # Get hand gesture detection for menu
            gesture_data = detect_hand_gesture()
            
            for event in pygame.event.get():
                # if user clicks on cross button, close the game
                if event.type == QUIT or (event.type == KEYDOWN and \
                                          event.key == K_ESCAPE):
                    pygame.quit()
                    cap.release()
                    cv2.destroyAllWindows()
                    sys.exit()

                # If the user presses space or up key, start the game for them
                elif event.type == KEYDOWN and (event.key == K_SPACE or\
                                                event.key == K_UP):
                    flappygame()

            # Hand gesture to start game
            if gesture_data['flap']:
                flappygame()

            # Display main menu
            window.blit(game_images['background'], (0, 0))
            window.blit(game_images['flappybird'], (horizontal, vertical))
            window.blit(game_images['sea_level'], (ground, elevation))
            
            # Display camera feed in menu
            if gesture_data['frame'] is not None:
                camera_surface = pygame_surface_from_cv2(gesture_data['frame'])
                pygame.draw.rect(window, (255, 255, 255), 
                               (camera_x - 2, camera_y - 2, camera_width + 4, camera_height + 4), 2)
                window.blit(camera_surface, (camera_x, camera_y))
            
            # Display instructions
            font = pygame.font.Font(None, 36)
            title_text = font.render("Hand Gesture Flappy Bird", True, (255, 255, 255))
            window.blit(title_text, (window_width//2 - title_text.get_width()//2, 50))
            
            font_small = pygame.font.Font(None, 24)
            instruction1 = font_small.render("yOU KNOW THE RULES!", True, (255, 255, 255))
            instruction2 = font_small.render("Or press SPACE/UP arrow", True, (255, 255, 255))
            window.blit(instruction1, (window_width//2 - instruction1.get_width()//2, 100))
            window.blit(instruction2, (window_width//2 - instruction2.get_width()//2, 130))
            
            pygame.display.update()
            framepersecond_clock.tick(framepersecond)