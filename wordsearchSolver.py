import os
import typing

import tornado.web
import jinja2

from . import solver

j2Environ = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")), autoescape=True)
inputTemplate = j2Environ.get_template("wordsearchSolver/input.html.j2")
displayTemplate = j2Environ.get_template("wordsearchSolver/display.html.j2")

class wordsearchSolver(tornado.web.RequestHandler):
    def displayInput(self, errorClass: solver.badInput = None):
        context: typing.Dict[str, typing.Any] = {"dictionaries": solver.wordLists.values()}
        if errorClass:
            context["error"] = errorClass.reason
        else:
            context["error"] = None
        self.write(inputTemplate.render(context))

    def get(self):
        # Don't care if this is get or post
        self.post()

    def post(self):
        args = {}
        for argName in self.request.arguments:
            args[argName] = self.get_argument(argName)

        # Has the user requested an output, or is this an input?
        if "gridContents" not in args:
            return self.displayInput()

        try:
            print(args)
            arrayIn = args.get("gridContents")
            del args["gridContents"]
            arrayIn = arrayIn.splitlines(keepends=False)

            displayGrid = []
            workGrid = []
            for line in arrayIn:
                displayGrid.append(line.upper())
                workGrid.append(line.lower())
            matches = solver.parseGridSettings(workGrid, args)
            context = {"grid": displayGrid,
                    "wordList": matches}
            self.write(displayTemplate.render(context))
        except solver.badInput as e:
            return self.displayInput(e)

