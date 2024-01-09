    # def save_to_file(self, email, password, group):
    #     try:
    #         with open('output.txt', 'w') as file:
    #             file.write(f"Email: {email}\nPassword: {password}\nURL: {group}")
    #     except Exception as e:
    #         QMessageBox.critical(None, "Error", f"An error occurred: {str(e)}")

    # def load_previous_text(self):
    #     try:
    #         with open('output.txt', 'r') as file:
    #             lines = file.readlines()
    #             if len(lines) >= 3:
    #                 self.line_edit1.setText(lines[0].strip().split(': ')[1])
    #                 self.line_edit2.setText(lines[1].strip().split(': ')[1])
    #                 self.line_edit3.setText(lines[2].strip().split(': ')[1])
    #     except FileNotFoundError:
    #         pass 