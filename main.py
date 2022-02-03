""" Entry point. """

from controllers.application import Application
from views.base import View


def main():
   view = View()
   app = Application(view)
   app.run()
  
if __name__ == "__main__":
   main()