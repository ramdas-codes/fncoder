import cv2
import mediapipe
import time
import random


def calculate_game_state(move):
    moves = ["Rock", "Paper", "Scissors"]
    wins = {"Rock": "Scissors", "Paper": "Rock", "Scissors": "Paper"}
    selected = random.randint(0, 2)
    print("Computer played " + moves[selected])

    if moves[selected] == move:
        return 0, moves[selected]

    if wins[move] == moves[selected]:
        return 1, moves[selected]

    return -1, moves[selected]


def get_finger_status(hands_module, hand_landmarks, finger_name):
    finger_id_map = {'INDEX': 8, 'MIDDLE': 12, 'RING': 16, 'PINKY': 20}

    finger_tip_y = hand_landmarks.landmark[finger_id_map[finger_name]].y
    finger_dip_y = hand_landmarks.landmark[finger_id_map[finger_name] - 1].y
    finger_mcp_y = hand_landmarks.landmark[finger_id_map[finger_name] - 2].y

    return finger_tip_y < finger_mcp_y


def get_thumb_status(hands_module, hand_landmarks):
    thumb_tip_x = hand_landmarks.landmark[hands_module.HandLandmark.THUMB_TIP].x
    thumb_mcp_x = hand_landmarks.landmark[hands_module.HandLandmark.THUMB_TIP - 2].x
    thumb_ip_x = hand_landmarks.landmark[hands_module.HandLandmark.THUMB_TIP - 1].x

    return thumb_tip_x > thumb_ip_x > thumb_mcp_x


def start_video():
    drawingModule = mediapipe.solutions.drawing_utils
    hands_module = mediapipe.solutions.hands

    capture = cv2.VideoCapture(0)

    start_time = 0.0
    timer_started = False
    time_left_now = 3
    hold_for_play = False
    draw_timer = 0.0
    game_over_text = ""
    computer_played = ""
    with hands_module.Hands(static_image_mode=False, min_detection_confidence=0.7,
                            min_tracking_confidence=0.4, max_num_hands=2) as hands:
        while True:

            if timer_started:
                now_time = time.time()
                time_elapsed = now_time - start_time
                if time_elapsed >= 1:
                    time_left_now -= 1
                    start_time = now_time
                    if time_left_now <= 0:
                        hold_for_play = True
                        timer_started = False

            ret, frame = capture.read()
            results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            move = "UNKNOWN"
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    if hold_for_play or time.time() - draw_timer <= 2:
                        drawingModule.draw_landmarks(frame, hand_landmarks, hands_module.HAND_CONNECTIONS)

                    current_state = ""
                    thumb_status = get_thumb_status(hands_module, hand_landmarks)
                    current_state += "1" if thumb_status else "0"

                    index_status = get_finger_status(hands_module, hand_landmarks, 'INDEX')
                    current_state += "1" if index_status else "0"

                    middle_status = get_finger_status(hands_module, hand_landmarks, 'MIDDLE')
                    current_state += "1" if middle_status else "0"

                    ring_status = get_finger_status(hands_module, hand_landmarks, 'RING')
                    current_state += "1" if ring_status else "0"

                    pinky_status = get_finger_status(hands_module, hand_landmarks, 'PINKY')
                    current_state += "1" if pinky_status else "0"

                    if current_state == "00000":
                        move = "Rock"
                    elif current_state == "11111":
                        move = "Paper"
                    elif current_state == "01100":
                        move = "Scissors"
                    else:
                        move = "UNKNOWN"

                if hold_for_play and move != "UNKNOWN":
                    hold_for_play = False
                    draw_timer = time.time()
                    print("Player played " + move)
                    won, cmp_move = calculate_game_state(move)
                    computer_played = "You: " + move + " | Computer: " + cmp_move
                    if won == 1:
                        game_over_text = "You've won!"
                    elif won == -1:
                        game_over_text = "You've lost!"
                    else:
                        game_over_text = "It's a draw!"

            font = cv2.FONT_HERSHEY_COMPLEX

            if not hold_for_play and not timer_started:
                cv2.putText(frame,
                            game_over_text + " " + computer_played,
                            (10, 450),
                            font, 0.75,
                            (255, 255, 255),
                            2,
                            cv2.LINE_4)

            label_text = "PRESS SPACE TO START!"
            if hold_for_play:
                label_text = "PLAY NOW!"
            elif timer_started:
                label_text = "PLAY STARTS IN " + str(time_left_now)

            cv2.putText(frame,
                        label_text,
                        (150, 50),
                        font, 1,
                        (0, 255, 255),
                        2,
                        cv2.LINE_4)
            cv2.imshow('Rock Paper Scissors!', frame)

            if cv2.waitKey(1) == 32:
                print("pressed space")
                start_time = time.time()
                timer_started = True
                time_left_now = 3

            if cv2.waitKey(1) == 27:
                break

    cv2.destroyAllWindows()
    capture.release()


if __name__ == "__main__":
    start_video()
