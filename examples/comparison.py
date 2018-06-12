import os

if __name__ == '__main__':
    for file in os.listdir(os.getcwd()):
        if not file.endswith(".py"):
            test_file = file
            result_script = os.path.splitext(file)[0] + ".py"

            original_size = os.path.getsize(test_file) // 1000
            script_size = os.path.getsize(result_script) // 1000
            ratio = int(((script_size - original_size) / original_size) * 100)
            signe = "+" if ratio > 0 else ""

            print(f"* {test_file} :\t{original_size}kB -> {script_size}kB ({signe}{ratio}%)")

# OUTPUT
# * test_dmg.dmg :	13025kB -> 15919kB (+22%)
# * test_png.png :	24kB -> 29kB (+20%)
# * test_mp4video.mp4 :	676kB -> 860kB (+27%)
