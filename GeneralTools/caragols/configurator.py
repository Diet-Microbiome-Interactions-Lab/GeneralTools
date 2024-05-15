from .clix import App


def main():
    print('# Default configuration at: ', App.default_config_path)
    print(App.default_config_path.read_text())


if __name__ == '__main__':
    main()
