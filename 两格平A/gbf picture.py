import pyautogui
import time
import keyboard

# ====== 图片路径 ======
OK_IMG = r"E:\Code\Project\GBF White Dragon Scale\gbf picture\ok.png"
ATTACK_IMG = r"E:\Code\Project\GBF White Dragon Scale\gbf picture\attack.png"
BACK_IMG = r"E:\Code\Project\GBF White Dragon Scale\gbf picture\back.png"

# ====== 屏幕区域（左1/3）======
screen_width, screen_height = pyautogui.size()
LEFT_REGION = (0, 0, screen_width // 3, screen_height)

# attack计数
attack_count = 0

# ====== 查找图片 ======
def find_image(image_path, confidence=0.65):
    try:
        return pyautogui.locateCenterOnScreen(
            image_path,
            confidence=confidence,
            grayscale=True,
            region=LEFT_REGION
        )
    except:
        return None

# ====== 点击 ======
def click_pos(pos):
    if pos:
        pyautogui.click(pos)

# ====== 主逻辑 ======
def main():
    global attack_count

    print("按 F4 开始运行")
    keyboard.wait("f4")
    print("开始执行")

    while True:
        # ===== ESC退出 =====
        if keyboard.is_pressed("esc"):
            print("退出程序")
            break

        # ===== ① ok 优先 =====
        ok_pos = find_image(OK_IMG)
        if ok_pos:
            print("检测到 ok.png")
            click_pos(ok_pos)
            print("点击 ok.png")
            time.sleep(0.5)
            continue

        # ===== ② attack =====
        attack_pos = find_image(ATTACK_IMG)
        if attack_pos:
            attack_count += 1
            print(f"检测到 attack.png，第 {attack_count} 次")

            # ===== 第1次 =====
            if attack_count == 1:
                click_pos(attack_pos)
                print("点击 attack.png")
                time.sleep(0.5)

                back_pos = find_image(BACK_IMG)
                if back_pos:
                    click_pos(back_pos)
                    print("点击 back.png")

            # ===== 第2次（重点🔥）=====
            elif attack_count == 2:
                click_pos(attack_pos)
                print("点击 attack.png")
                time.sleep(1)

                back_pos = find_image(BACK_IMG)
                if back_pos:
                    click_pos(back_pos)
                    print("点击 back 第1次")
                    time.sleep(1)

                    click_pos(back_pos)
                    print("点击 back 第2次")

            # ===== 重置计数 =====
            if attack_count >= 2:
                attack_count = 0

            time.sleep(1)
            continue

        time.sleep(0.3)

# ====== 运行 ======
if __name__ == "__main__":
    main()
