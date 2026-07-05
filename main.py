from explorejp.console import configure_console
from explorejp.screens import show_main_menu, show_welcome


def main() -> None:
    configure_console()
    show_welcome()
    show_main_menu()


if __name__ == "__main__":
    main()

