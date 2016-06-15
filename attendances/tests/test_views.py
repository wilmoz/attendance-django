from unittest.mock import Mock, patch, ANY, MagicMock
from attendances.views import register, registered


class UnpackArgsRenderMixin:
    def context(self, call_args):
        args, kwargs = call_args
        request_mock, template, context = args
        return context

    def template(self, call_args):
        args, kwargs = call_args
        request_mock, template, context = args
        return template


class TestRegisterPage(UnpackArgsRenderMixin):
    @patch('attendances.views.get_user')
    @patch('attendances.views.RegisterStudentListForm')
    @patch('attendances.views.render')
    def test_register_sends_form(self, mock_render, mock_StudentListForm, mock_get_user, rf):
        request = rf.get('fake')
        request.user = Mock()
        mock_get_user.return_value = ANY
        mock_student_list_form = mock_StudentListForm.return_value

        register(request, ANY)

        context = self.context(mock_render.call_args)
        assert mock_student_list_form == context['form']

    @patch('attendances.views.get_user')
    @patch('attendances.views.RegisterStudentListForm')
    @patch('attendances.views.render')
    def test_register_page_use_register_template(self, mock_render, mock_StudentListForm, mock_get_user, rf):
        request = rf.get('fake')
        mock_get_user.return_value = ANY
        request.user = Mock()

        register(request, ANY)

        template = self.template(mock_render.call_args)
        assert 'register.html' == template

    @patch('attendances.views.get_user')
    @patch('attendances.views.Attendance')
    @patch('attendances.views.render')
    def test_registered_use_registered_template(self, mock_render, mock_Attendance, mock_get_user, rf):
        request = rf.get('fake')
        mock_get_user.return_value = ANY
        mock_Attendance.objects.filter.return_value = ANY

        registered(request, ANY)

        template = self.template(mock_render.call_args)
        assert 'registered.html' == template

    @patch('attendances.views.get_user')
    @patch('attendances.views.RegisterStudentListForm')
    def test_register_call_save_of_form(self, mock_StudentListForm, mock_get_user, rf):
        request = rf.post('fake')
        request.user = Mock()
        mock_get_user.return_value = ANY
        mock_student_list_form = mock_StudentListForm.return_value
        mock_student_list_form.is_valid.return_value = True

        register(request, ANY)

        assert mock_student_list_form.save.call_count == 1

    @patch('attendances.views.get_user')
    @patch('attendances.views.RegisterStudentListForm')
    def test_register_dont_call_save_of_invalid_form(self, mock_StudentListForm, mock_get_user, rf):
        request = rf.post('fake')
        request.user = Mock()
        mock_get_user.return_value = ANY
        mock_student_list_form = mock_StudentListForm.return_value
        mock_student_list_form.is_valid.return_value = False

        register(request, ANY)

        assert mock_student_list_form.save.call_count == 0

    @patch('attendances.views.get_user')
    @patch('attendances.views.Attendance')
    def test_registered_output_registered_students(self, mock_Attendance, mock_get_user, rf):
        request = rf.get('fake')
        mock_get_user.return_value = ANY
        mock_Attendance.objects.filter.return_value = MagicMock()

        registered(request, ANY)

        assert mock_Attendance.objects.filter.call_count == 1
