from halo import Halo

TEXT_ANSWER = "[answer]: "
TEXT_COMMAND = "[command]: "
TEXT_CONFIRMATION = "[y/n]: "


class Console:
    # TODO improve colors
    def __init__(self):
        self.spinner = Halo(text="Thinking...\n", spinner="arrow3")
        self.column_width = max(
            [len(t) for t in [TEXT_ANSWER, TEXT_COMMAND, TEXT_CONFIRMATION]]
        )

    def print_answer(self, answer: str):
        print(f"{TEXT_ANSWER:>{self.column_width}}{answer}")

    def print_command(self, command: str):
        print(f"{TEXT_COMMAND:>{self.column_width}}{command}")

    def print_retry(self):
        print("I'm sorry, but I couldn't find an answer. Can you retry please?")

    def print_farewell(self):
        print("Sounds good, anytime.")

    def await_confirmation(self) -> bool:
        return input(f"{TEXT_CONFIRMATION:>{self.column_width}}").lower() == "y"

    def show_spinner(self):
        self.spinner.start()

    def hide_spinner(self):
        self.spinner.stop()
