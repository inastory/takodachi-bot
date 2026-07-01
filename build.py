import os
import sys
import shutil
import subprocess


def main():
    # 1. 決定是否要清除快取全新重編 (--clean)
    clean_build = "--clean" in sys.argv

    print("🚀 開始執行 PyInstaller 打包流程...")

    # 2. 組裝 PyInstaller 指令
    # 我們統一使用你的 takodachi.spec 來維持設定的一致性
    cmd = ["uv", "run", "pyinstaller", "takodachi.spec"]
    if clean_build:
        cmd.append("--clean")
        print("🧹 已啟用 --clean 參數，將清除舊快取...")

    # 3. 執行打包指令
    try:
        subprocess.run(cmd, check=True)
        print("🟢 PyInstaller 打包成功！")
    except subprocess.CalledProcessError as e:
        print(f"❌ PyInstaller 打包失敗，錯誤碼: {e.returncode}")
        sys.exit(e.returncode)

    # 4. 🌟 實作方案 B：自動將 logger.conf 複製到 .exe 旁邊
    # 請根據你實際打包出來的輸出模式（--onefile 或 --onedir）確認目標路徑：
    # 假設你的 spec 配置輸出的單一檔案或資料夾名稱為 takodachi
    src_conf = os.path.join("src", "takodachi_bot", "library", "logger.conf")

    # 這裡我們同時兼容單一檔案 (dist/) 或 資料夾模式 (dist/takodachi/)
    # 自動尋找對應的輸出位置放過去
    dst_possibilities = [
        os.path.join("dist", "takodachi"),  # 狀況 A: 資料夾模式 (目錄)
        "dist",  # 狀況 B: 單一檔案模式 (.exe 直接在 dist 根目錄下)
    ]

    conf_copied = False
    if os.path.exists(src_conf):
        for dst_dir in dst_possibilities:
            if os.path.exists(dst_dir):
                dst_conf = os.path.join(dst_dir, "logger.conf")
                shutil.copy(src_conf, dst_conf)
                print(f"📦 已成功將設定檔複製到外側：{dst_conf}")
                conf_copied = True
                break
        if not conf_copied:
            print(
                "⚠️ 找不到 dist/ 輸出的目標資料夾，請確認 PyInstaller 的輸出檔名是否為 takodachi"
            )
    else:
        print(f"❌ 找不到原始的設定檔：{src_conf}，無法複製！")


if __name__ == "__main__":
    main()
