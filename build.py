import subprocess
import os
import shutil


def check_pyinstaller():
    """
    检查 PyInstaller 是否已安装，如果未安装则尝试安装
    """
    try:
        import PyInstaller
    except ImportError:
        print("PyInstaller is not installed. Attempting to install...")
        install_pyinstaller()


def install_pyinstaller():
    """
    安装 PyInstaller
    """
    try:
        subprocess.run(["pip", "install", "pyinstaller"], check=True)
        print("PyInstaller installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing PyInstaller: {e}")
        raise


def build_with_pyinstaller(script_name, clean=False, onefile=False, debug=False, additional_files=None,
                           additional_options=None, distpath=None, workpath=None, hidden_imports=None):
    '''
    使用 PyInstaller 打包 Python 脚本
    :param script_name: 要打包的 Python 脚本名
    :param clean: 是否清理临时文件
    :param onefile: 是否将所有文件打包到一个文件中
    :param debug: 是否开启调试模式
    :param additional_files: 需要打包的其他文件
    :param additional_options: 其他选项 https://pyinstaller.readthedocs.io/en/stable/usage.html#options
    :param distpath: 指定打包后的输出目录
    :param workpath: 指定临时工作文件的路径
    :param hidden_imports: 需要隐藏导入的模块列表
    '''
    # 检查 PyInstaller 是否已安装，如果未安装则尝试安装
    check_pyinstaller()

    # 构建命令
    build_command = ["pyinstaller"]

    # 添加额外的文件
    if additional_files:
        for source, destination in additional_files:
            build_command.extend(["--add-data", f"{source}:{destination}"])

    # 添加隐藏导入的模块
    if hidden_imports:
        for module in hidden_imports:
            build_command.extend(["--hidden-import", module])

    # 添加其他选项
    if additional_options:
        build_command.extend(additional_options)

    # 开启调试模式
    if debug:
        build_command.append("--debug=imports")

    if clean:
        build_command.append("--clean")

    if onefile:
        build_command.append("--onefile")

    # 添加 --distpath 和 --workpath
    if distpath:
        build_command.extend(["--distpath", distpath])

    if workpath:
        build_command.extend(["--workpath", workpath])

    # 添加脚本名
    build_command.append(script_name)

    # 执行构建命令
    print(f"开始执行打包命令,请稍等：\n{build_command}")
    subprocess.run(build_command)

    # 删除 build 目录和 spec 文件
    build_dir = os.path.join(os.getcwd(), "build")
    spec_file = f"{script_name.split('.')[0]}.spec"

    # 删除 build 目录
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
        print(f"已删除build目录")

    # 删除 spec 文件
    if os.path.exists(spec_file):
        os.remove(spec_file)
        print(f"已删除spec文件: {spec_file}")


if __name__ == '__main__':
    # 如果有配置文件 ，可以添加到 additional_files
    script_name = "wx_api.py"  # 要打包的 Python 脚本名
    # additional_files = [("./costway_health/templates", "costway_health/templates"),
    #                     ("./costway_health/static", "costway_health/static")]  # 需要打包的其他文件
    # # 添加隐藏导入的模块
    # hidden_imports = [
    #     'costway_us.web.forget_password_pc', 'costway_us.web.loginmobile', 'costway_us.web.loginpc',
    #     'costway_us.web.payment_mobile', 'costway_us.web.forget_password_mb', 'costway_us.web.signinpc',
    #     'costway_us.web.signinmobile', 'costway_us.web.payment_pc', 'costway_us.web.buy_plus_pc',
    #     'costway_us.web.buy_plus_mb','costway_ca.loginpc_ca','costway_ca.loginmobile_ca','costway_ca.signinpc_ca',
    #     'costway_ca.signinmobile_ca','costway_ca.forget_password_mb_ca','costway_ca.forget_password_pc_ca',
    #     'costway_ca.payment_mobile_ca','costway_ca.payment_pc_ca','costway_ca.buy_plus_pc_ca',
    #     'costway_ca.buy_plus_mb_ca'
    # ]
    # 设置 distpath 和 workpath
    distpath = "./dist"
    workpath = "./build"
    build_with_pyinstaller(script_name, clean=True, onefile=True, debug=False, distpath=distpath, workpath=workpath)
