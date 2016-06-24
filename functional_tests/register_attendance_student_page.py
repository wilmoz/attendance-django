from page_objects import MultiPageElement, PageElement, PageObject


class RegisterStudentPage(PageObject):
    checkboxes = MultiPageElement(xpath="//input[@type='checkbox']")
    checked_checkboxes = MultiPageElement(css="input:checked[type='checkbox']")
    submit_button = PageElement(css="input[type='submit']")
    success_message_element = PageElement(css=".info")
    finished_course_message_element = PageElement(css=".finished-course-message")
    not_started_course_message_element = PageElement(css=".not-started-course-message")

    @property
    def not_started_course_message(self):
        return self.not_started_course_message_element.text

    @property
    def finished_course_message(self):
        return self.finished_course_message_element.text

    @property
    def success_message(self):
        return self.success_message_element.text

    @property
    def checked_students(self):
        checked_students = [checked_checkbox.find_element_by_xpath("..").text for checked_checkbox in self.checked_checkboxes]
        return checked_students

    def toggle_check(self, student):
        # this is tied to structure of checkboxes generated by django
        # <label for="id_students_0">
        #   <input id="id_students_0" name="students" value="1" type="checkbox"> john
        # </label>
        student_chekboxes = [checkbox for checkbox in self.checkboxes if checkbox.find_element_by_xpath("..").text == student]
        assert len(student_chekboxes) > 0, "student not found in checkboxes"
        assert len(student_chekboxes) == 1, "many students found in checkboxes"
        student_chekbox = student_chekboxes[0]
        student_chekbox.click()
