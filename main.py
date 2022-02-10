""" Entry point. """

from controllers.base import Controller
from views.base import View


def main():
    """ Main entry"""
    view = View()
    app = Controller(view)
    app.run()


if __name__ == "__main__":
    main()
